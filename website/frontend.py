#!/usr/bin/python
from flask import Flask
from flask import render_template, redirect, url_for
from flask_pymongo import PyMongo
from flask import json
from flask import jsonify
from bson import Binary, Code
from jinja2 import Template
from bson.json_util import dumps
from json2html import *
import HTML

app = Flask(__name__)
#app.config['MONGO_URI'] = 'mongodb://localhost'
app.config['MONGO_DBNAME'] = 'sacbusinesses'
mongo = PyMongo(app)

@app.route('/')
def index():
    test = mongo.db.test4.find({"Business Description":"DRIVER"}) #mongo returns bson
    test2 = dumps(test) #converst bson tojson
    #json_object = [test2]
    #build_direction = "LEFT_TO_RIGHT"
    #table_attributes = {"style" : "width:100%"}
    #html = convert(json_object, build_direction=build_direction, table_attributes=table_attributes)
    data = json.loads(test2)
    return render_template('index.html', data=data)#passes json to index.html

app.run(debug = True, host = '0.0.0.0', port = 5000) #running on localhost:5000
