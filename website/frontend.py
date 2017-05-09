#!/usr/bin/python
from flask import Flask
from flask import render_template, redirect, url_for
from flask_pymongo import PyMongo
from flask import json
from flask import jsonify
from bson import Binary, Code
from jinja2 import Template
from bson.json_util import dumps
from json2table import convert
import html

app = Flask(__name__)
#app.config['MONGO_URI'] = 'mongodb://localhost'
app.config['MONGO_DBNAME'] = 'sacbusinesses'
mongo = PyMongo(app)

@app.route('/')
def index():
    test = mongo.db.clustered.find({"Cluster Label":"AUTO"}, {'_id':0, 'Account Number':0, 'Good Cluster': 0, 'Cluster':0, 'Representation':0, 'Cluster Description':0, 'Location City':0}) #mongo returns bson

    test2 = dumps(test) #converst bson tojson
    data = json.loads(test2)
    build_direction = "TOP_TO_BOTTOM"
    html = ""
    table_attributes = {"style" : "width:100%", "class" : "table table-striped"}
    for obj in range(len(data)):
        json_object = data[obj]
    html = html+convert(json_object, build_direction=build_direction, table_attributes=table_attributes)
    return render_template('index.html', html=html)#passes json to index.html

app.run(debug = True, host = '0.0.0.0', port = 5000) #running on localhost:5000
