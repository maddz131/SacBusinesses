#!/usr/bin/python
from flask import Flask
from flask import render_template, redirect, url_for
from flask_pymongo import PyMongo
from flask import request
from flask import json
from flask import jsonify
from bson import Binary, Code
from jinja2 import Template
from bson.json_util import dumps
from json2table import convert
import HTML

app = Flask(__name__)
#app.config['MONGO_URI'] = 'mongodb://localhost'
app.config['MONGO_DBNAME'] = 'sacbusinesses'
mongo = PyMongo(app)

statuses = {'License Cancelled','License Expired','License Issued','License Renewed'}
selection = "AUTO"

def setSelection(data):
   selection = "JANITOR"
   return selection

def query(selection):
    return mongo.db.clustered.find({"Cluster Label": selection}) #mongo returns bson


@app.route('/')
def index():
    return render_template('index2.html')#passes json to index.html

@app.route('/datamart')
def datamart():
    test1 = mongo.db.clustered.find({"Cluster Label":"AUTO"}, {'_id':0, 'Account Number':0, 'Good Cluster': 0, 'Cluster':0, 'Representation':0, 'Cluster Description':0, 'Location City':0}) #mongo returns bson
    test2 = dumps(test1) #converst bson tojson
    data = json.loads(test2)
    build_direction = "TOP_TO_BOTTOM"
    html = ""
    table_attributes = {"style" : "width:100%", "class" : "table table-striped"}
    for obj in range(len(data)):
        json_object = data[obj]
        html = html+convert(json_object, build_direction=build_direction, table_attributes=table_attributes)
    return render_template('index.html', statuses=statuses, html=html)


@app.route('/datamart/update',methods = ['POST'])
def update():
    selection = setSelection("JANITOR")
    return redirect(url_for('datamart')), selection

@app.route('/heatmap')
def heatmap():
    return render_template('heatmap.html')

app.run(debug = True, host = '0.0.0.0', port = 5000) #running on localhost:5000
