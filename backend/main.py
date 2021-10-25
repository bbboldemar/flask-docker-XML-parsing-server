import os
import re

from flask import Flask, request, Response, send_from_directory
import xmltodict

path_abuse = r""

app = Flask(__name__)

@app.route('/')
def hello():
    r = Response(
        response = 'Working...',
        status = 200, 
        mimetype = "str"
    )
    r.headers["Content-Type"] = "str; charset=utf-8"
    return r


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(
        os.path.join(path_abuse, app.root_path, 'static'),
        'favicon.ico', 
        mimetype = 'image/vnd.microsoft.icon'
    )


@app.route('/thru_parser', methods = ['POST'])
def thru_parser():
    '''
    Get and decode body thru xmltodict and add status, 
    return xml
    '''
    parsed = xmltodict.parse(request.get_data())
    parsed['soapenv:Envelope']['soapenv:Body']['ns1:MatchPersonInBlackList']['PersonInBlackList']['BlackList'] = 'true'
    unparsed = xmltodict.unparse(parsed, pretty=True)
    
    r = Response(
        response = unparsed, 
        status=200, 
        mimetype="application/xml"
    )
    r.headers["Content-Type"] = "text/xml; charset=utf-8"
    return r


@app.route('/thru_file', methods = ['POST'])
def thru_file():
    '''
    Get and decode body into str(), return xml file
    '''
    path_to_directory = os.path.join(app.root_path, 'request')
    path_to_file = os.path.join(path_to_directory, 'data.xml')
    string_data = request.get_data().decode('utf-8')
    
    def write_file(string_data):
        '''
        Get and write decoded to utf-8 body into xml file
        '''
        with open(path_to_file, 'w') as f:
            f.write(string_data)  

    def change_file():
        '''
        Add status to file
        '''
        with open(path_to_file, 'r') as f:
            get_all = f.readlines()
        with open(path_to_file, 'w') as f:
            working_line = 0
            for i, line in enumerate(get_all, 1):
                if i > working_line:
                    f.writelines(line)
                if re.match(r'^.*(<PersonInBlackList>)$', line):
                    # better write line with re.sub(pattern, (<BlackList>true</BlackList>), line)
                    f.writelines(
                        '				<BlackList>true</BlackList>\n'
                    )
                if i < working_line:
                    f.writelines(line)

                working_line += 1
    write_file(string_data)
    change_file()
    
    return send_from_directory(
        path_to_directory, 
        'data.xml',
        as_attachment = True
    )

if __name__ == '__main__':
   app.run(host='0.0.0.0')
