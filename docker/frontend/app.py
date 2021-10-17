#!/usr/bin/python3
# testing code
from flask import Flask, render_template, redirect, url_for, Response, request
from flask_restx import Api, Resource

import json, datetime, requests

with open('configs.json', 'r') as f:    # config file loading
    configs = json.load(f)

app = Flask (__name__)
api = Api(app)
SITE_NAME = 'http://service.mydomain.int/'
#SITE_NAME = 'http://localhost:8080/'   # for local test

# @app.route('/demo')
# def hello_world():
#    return 'Hello World!'

@app.route('/', defaults={'path': '/index'})

@app.route('/index')
def index():
    d = datetime.datetime.now()
    return render_template(
        'index.html',
        title = 'AWSome Demo Day!',
        time_now = d.strftime("%Y. %m. %d %A, %p %I:%m:%S"),
        region = configs['INFO']['REGION']
    )

# @app.route('/service')
# def service():
#    return redirect("http://service.mydomain.int/service") # backend serviced의 endpoint, 실습에서는 hardcording으로 수행

@app.route('/<path:path>',methods=['GET'])
def proxy(path):
    global SITE_NAME
    if request.method=='GET':
        resp = requests.get(f'{SITE_NAME}{path}')
        response = Response(resp.text, resp.status_code)
    return response


if __name__ == "__main__":
    app.run(debug=False, host='0.0.0.0', port=80)
