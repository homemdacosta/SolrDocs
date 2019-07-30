from configparser import SafeConfigParser
import requests
import os
#import json
import datetime

# Local import
import config_util

def striplist(l):
    return([x.strip() for x in l])

# Load configuration
solr_url = config_util.get_configuration(section='solr', option='url')
file_path = config_util.get_configuration(section='file_location', option='path')
supported_formats = striplist(config_util.get_configuration(section='index_util', option = 'supported_formats').split(','))

# Solr configuration
solr_host = config_util.get_configuration('solr', 'url')
core = config_util.get_configuration('solr', 'core')
update = config_util.get_configuration('solr', 'update')
update_extract = config_util.get_configuration('solr', 'update_extract')
commit_flag = config_util.get_configuration('solr', 'commit_flag')

def get_list_all_files(file_path, supported_formats):
    file_path = config_util.get_configuration(section='file_location', option='path')
    supported_formats = striplist(config_util.get_configuration(section='index_util', option = 'supported_formats').split(','))
    files = []
    for single_path in file_path.split(','): # Remove any starting ending space
        single_path = single_path.strip()
        for r, d, f in os.walk(single_path): # Navigate on the file path
            for file in f: # Iterate over the list of all files found on the directory
                file_extension = os.path.splitext(file)[1] # Split filename and retrieve the file extensions
                for sp in supported_formats: # Iterate over the list of all supported files
                    #print('file: ' + str(file) + ' - File_Extension: ' + str(file_extension) + ' - SP for comparision: ' + str(sp) + '#')
                    if sp == file_extension: # Check if file is terminated by one of the valids extensions
                        files.append(os.path.join(r, file))
                        break
    return files

def delete_all_indexed ():
    print('Trying to delete all indexed documents')
    #Referencia: curl "http://localhost:8983/solr/techproducts/update/?commit=true" -H "Content-Type: text/xml" --data-binary '<delete><query>*:*</query></delete>'
    data = '<delete><query>*:*</query></delete>'
    url_submit = solr_host + core + update + commit_flag
    #print (url_submit)
    response = requests.post(url_submit, headers={'Content-Type': 'text/xml'}, data = data)
    if response.status_code == 200:
        print('All indexed documents deleted successfully!')
        return True
    else:
        print('An error was thrown while trying to delete the indexed documents')
        return False
                
def index_all_documents ():
    print('Full index started')
    if delete_all_indexed(): # Remove todos os documentos indexados
        config_util.set_configuration('index_util', 'last_index', '0') # Reset index values
        for file in get_list_all_files(file_path, supported_formats):
            new_id = int(config_util.get_configuration('index_util', 'last_index')) + 1
            
            payload = {'literal.id':  new_id
                        , 'literal.resourcename': file
                        , 'commit': 'true'
                        }
            
            file_opened = open(file, 'rb') # Open binary file

            url_submit = solr_host + core + update_extract # Construct URL

            response = requests.post(url_submit
                , data = payload
                , files = {'file': file_opened}) # Send POST request to SOLR

            if response.status_code == 200:
                print(file + ' - sucessfully indexed with ID: ' + str(new_id))
                config_util.set_configuration('index_util', 'last_index', str(new_id))
            else:
                print('Error while trying to index the file: ' + file)
            
            file_opened.close()
        return True
    
    return False

#for i,f in enumerate(get_list_all_files(file_path, supported_formats)):
#   print(str(i) + ' - ' + f)
#delete_all_indexed()


#index_all_documents()