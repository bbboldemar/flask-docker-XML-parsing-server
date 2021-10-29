import os
import re

from flask import Flask, Response, request, send_from_directory
import xmltodict

app = Flask(__name__)

path_to_directory = os.path.join(app.root_path, 'request')
path_to_file = os.path.join(path_to_directory, 'data.xml')


def write_file(string_data):
    '''
    Get and write decoded to utf-8 body into xml file.
    '''
    with open(path_to_file, 'w') as f:
        f.write(string_data)


def change_file():
    '''
    Add status to file thru RegEx
    '''
    with open(path_to_file, 'r') as f:
        get_all = f.readlines()
    with open(path_to_file, 'w') as f:
        for line in get_all:
            if re.match(r'^.*(</DULSeries>)$', line):
                f.writelines(re.sub(
                    r'[<]{1}(.*)>(.*)</(.*)>',
                    r'<BlackList>true</BlackList>',
                    line))
            f.writelines(line)


def return_updated_file():
    with open(path_to_file, 'r') as f:
        return f.readlines()


@app.route('/')
def hello():
    r = Response(
        response='Working...',
        status=200,
        mimetype="str"
    )
    r.headers["Content-Type"] = "str; charset=utf-8"
    return r


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(
        os.path.join(app.root_path, 'static'),
        'favicon.ico',
        mimetype='image/vnd.microsoft.icon'
    )


@app.route('/thru_parser', methods=['POST'])
def thru_parser():
    '''
    Gets and parse body thru xmltodict and change it, 
    return xml.
    '''
    parsed = xmltodict.parse(request.get_data())
    parsed['soapenv:Envelope']['soapenv:Body']['ns1:MatchPersonInBlackList']['PersonInBlackList']['BlackList'] = 'true'
    unparsed = xmltodict.unparse(parsed, pretty=True)

    r = Response(
        response=unparsed,
        status=200,
        mimetype="application/xml"
    )
    r.headers["Content-Type"] = "text/xml; charset=utf-8"
    return r


@app.route('/thru_file', methods=['POST'])
def thru_file():
    '''
    Gets and decode body into str(), save it to file and
    change it, return xml.
    '''

    write_file(request.get_data().decode('utf-8'))
    change_file()

    r = Response(
        response=return_updated_file(),
        status=200,
        mimetype="application/xml"
    )
    r.headers["Content-Type"] = "text/xml; charset=utf-8"
    return r


if __name__ == '__main__':
    app.run(host='0.0.0.0')
