from flask import Flask, jsonify
import re
import pandas as pd
import db
import clean

from flask import request
from flasgger import Swagger, LazyString, LazyJSONEncoder
from flasgger import swag_from

#### flask
app = Flask(__name__)\

###swager
app.json_encoder = LazyJSONEncoder
swagger_template = {
    "info": {
        "title":  "API Documentation for Data Preprocessing",
        "version": "1.0.0",
        "description": "Dokumentasi API"
    },
    "host": "127.0.0.1:5000"
}
swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": 'docs',
            "route": '/docs.json',
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/docs/"
}
swagger = Swagger(app, template=swagger_template,
                  config=swagger_config)

@swag_from("docs/text_processing.yml", methods=['POST'])
@app.route('/clean_teks', methods=['POST'])
def input_teks():
    data = request.form.get('text')
    hs = int(request.args.get('hs'))
    abusive = int(request.args.get('abusive'))
    target = request.args.get('target')
    topic = request.args.get('topic')
    level = request.args.get('level')

    dict = {
        'Tweet':'', 
        'HS':0, 
        'Abusive':0,
        'HS_Individual':0, 
        'HS_Group':0, 
        'HS_Religion':0, 
        'HS_Race':0, 
        'HS_Physical':0, 
        'HS_Gender':0, 
        'HS_Other':0,
        'HS_Weak':0, 
        'HS_Moderate':0, 
        'HS_Strong':0,
        'Tweet_Cleaned':''
    }
    dict['Tweet'] = data
    
    data = re.sub(r'\\n', ' ', data) #hapus \\n
    data = re.sub(r'\bRT\b|\brt\b',' ', data) #hapus rt
    data_cleaned = clean.clean_data(data) #clean data input

    dict['HS'] = hs
    dict['Abusive'] = abusive

    if target != 'None':
        dict[target] = 1
    if topic != 'None':
        dict[topic] = 1
    if level != 'None':
        dict[level] = 1

    dict['Tweet_Cleaned'] = data_cleaned
    db.create_text_db(dict)
    json_response = dict
    
    return jsonify(json_response)

@swag_from("docs/text_processing_file.yml", methods=['POST'])
@app.route('/text-processing-file', methods=['POST'])
def text_processing_file():

    # Upladed file
    file = request.files.getlist('file')[0]

    # Import file csv ke Pandas
    df_file = pd.read_csv(file, encoding='latin-1')

    df_clean_rt_n = df_file.copy()
    df_clean_rt_n['Tweet'] = df_clean_rt_n['Tweet'].replace(r'\\n',' ', regex=True)
    df_clean_rt_n['Tweet'] = df_clean_rt_n['Tweet'].replace(r'\bRT\b|\brt\b',' ', regex=True)
    
    df_file['Tweet_Cleaned'] = df_clean_rt_n['Tweet'].apply(clean.clean_data)
    
    db.create_db(df_file)

    # df_tweet = df_file['Tweet'].to_json()
    json_response = {
        'status_code': 200,
        'description': "Teks yang sudah diproses",
        # 'Tweet' : df_tweet,
        'Tweet_Cleaned': df_file['Tweet_Cleaned'].values.tolist(),
    }

    response_data = jsonify(json_response)

    return response_data


##running api
if __name__ == '__main__':
    app.run()