import os
import json
from flask import Flask, request, Response, send_from_directory
import xml.etree.ElementTree as ET
import xmltodict

path_abuse = r""
DULNumberBL = ['123456']
DULSeriesBL = ['QWE123']

app = Flask(__name__)

@app.route('/')
def hello():
    r = Response(response='Working...', status=202, mimetype="str")
    r.headers["Content-Type"] = "str; charset=utf-8"
    return r

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(path_abuse, app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

# парсит XML на ключ-значение и отправляет заготовленный XML (true/false)
@app.route('/test', methods = ['POST'])
def test():
    content = xmltodict.parse(request.get_data())
    output_dict = json.loads(json.dumps(content))
    DULSeries = output_dict['soapenv:Envelope']['soapenv:Body']['ns1:MatchPersonInBlackList']['PersonInBlackList']['DULSeries']
    DULNumber = output_dict['soapenv:Envelope']['soapenv:Body']['ns1:MatchPersonInBlackList']['PersonInBlackList']['DULNumber']
    if DULSeries in DULSeriesBL and DULNumber in DULNumberBL:
        file = 'true.xml'
    else:
        file = 'false.xml'
    return send_from_directory(os.path.join(app.root_path, 'response'), file, as_attachment=True)


# # Парсит элементы XML-файла на НЕ вхождение в стоп-лист. Потенциально сожно допилить изменение этого файла до нудного вида
# def not_in_stoplist_check():
#     script_dir, rel_path = os.path.dirname(__file__), r"request\req1_ex.xml"
#     abs_file_path = os.path.join(script_dir, rel_path)
#     for event, elem in ET.iterparse(abs_file_path):
#         if (elem.tag == 'DULNumber' and elem.text in DULNumberBL) or (elem.tag == 'DULSeries' and elem.text in DULSeriesBL):
#             return False
#     return True


# # Парсит XML в папке request
# @app.route('/stoplist', methods=['GET', 'POST'])
# def stoplist():
#     if request.method == 'POST':
#         if not_in_stoplist_check():
#             file = 'true.xml'
#         else:
#             file = 'false.xml'
#         return send_from_directory(os.path.join(app.root_path, 'response'), file, as_attachment=True)
#     else:
#         r = Response(response='POST expected!', status=400, mimetype="str")
#         r.headers["Content-Type"] = "str; charset=utf-8"
#         return r


# # Сохраняет body в строку и пишет в txt файл
# @app.route('/write_XML_Body_data_to_txt', methods = ['POST'])
# def write_XML_Body_data_to_txt():
#     data = str(request.get_data())
#     print (data)
#     with open(os.path.join(app.root_path, 'request\TEST.txt'), 'w') as f:
#         f.write(data)
#     r = Response(response=data, status=200, mimetype="str")
#     r.headers["Content-Type"] = "str; charset=utf-8"
#     return r

if __name__ == '__main__':
   app.run(host='0.0.0.0')
