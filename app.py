from flask import Flask, session, redirect, url_for, escape, request, render_template

# TEMP
import json
import requests

# LOCAL IMPORTS
import config_util
import index_util

app = Flask("solrdocs")
app.config['SECRET_KEY'] = "A0Zr98j/3yX R~XHH!jmN]LWX/,?RT"

# Define configuration at startup
'''config_util.set_configuration(section ='file_location'
                            , option ='path'
                            , value = '/home/rodrigo/Documents/Projetos/SolrDocs/assets,/opt/solr/example/exampledocs')'''

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        session['keyword'] = request.form['keyword']
        return redirect(url_for('busca'))
    session.pop('keyword', None) # Apaga os dados de login lá da session
    return render_template('index.html', title=u'Home')

@app.route('/busca')
def busca():
    if 'keyword' in session:
        payload = {
                    'q': session['keyword']
                    #, 'defType': 'edismax'
                    , 'rows': '500'
                    , 'wt': 'json' 
                    }
        search_url = 'http://localhost:8983/solr/SolrDoc_Core/select'

        connection = requests.get(search_url, params=payload)
        response = json.loads(connection.text)
        result_dic = response['response']['docs']
        return render_template("search_result.html"
                                , search_keyword = escape(session['keyword'])
                                , result_size = response['response']['numFound']
                                , results = result_dic)
    return u"""
            <h1>Nao há termo de busca definido</h1>
            <a href="%s"> Voltar ao inicio </a>
        """ % (url_for('home'))

@app.route('/configure', methods=['GET', 'POST'])
def configure():
    # Gather configuration form file
    file_path_value = config_util.get_configuration(section='file_location', option='path')
    supported_files = config_util.get_configuration(section='index_util', option='supported_formats')
    file_path_value_lenght = len(file_path_value)+50

    if request.method == 'POST':
        session['filepath'] = request.form['filepath']
        session['supportedFiles'] = request.form['supportedFiles']

        config_util.set_configuration(section='file_location', option='path', value=session['filepath'])
        config_util.set_configuration(section='index_util', option='supported_formats', value=session['supportedFiles'])

        print('session filepath: ' + file_path_value)
        print('session supportedFiles: ' + supported_files)

        return u"""
            <h1>Configuracao salva com sucesso!</h1>
            <a href="%s"> Voltar ao inicio </a>
        """ % (url_for('home'))
    
    session.pop('filepath', None) # Apaga os dados da session
    session.pop('supportedFiles', None) # Apaga os dados da session

    return render_template('configure.html', title=u'Configuração', file_path_value=file_path_value, supported_files=supported_files, input_size=file_path_value_lenght)

@app.route('/index_all', methods=['GET', 'POST'])
def index_all():
    index_util.index_all_documents()
    return u"""
            <h1>Documentos reindaxos com sucesso!</h1>
            <a href="%s"> Voltar ao inicio </a>
        """ % (url_for('home'))


app.run(debug=True, use_reloader=True)