#!/usr/bin/python3
# testing code
from flask import Flask, render_template
from flask_restx import Api, Resource

import json

with open('configs.json', 'r') as f:    # config file loading
    configs = json.load(f)

app = Flask (__name__)
api = Api(app)

@app.route('/demo')
def hello_world():
    return 'Hello World!'

@app.route('/index')
def index():
    return render_template(
        'index.html',
        title = 'AWSome Demo Day!',
        app_version = configs['INFO']['VERSION'],
        region = configs['INFO']['REGION']
    )
    

@api.route('/hello')
class InfoReturn(Resource):
    def get(self):
        return {"hello": "HelloWorld!", "version": "Blue", "region": "localhost"}
        
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8080)
