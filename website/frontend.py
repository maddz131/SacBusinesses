#!/usr/bin/python
from flask import Flask
from flask import render_template, redirect, url_for
from flask_pymongo import PyMongo
from flask import json
from flask import jsonify
from bson import Binary, Code
from bson.json_util import dumps

app = Flask(__name__)
#app.config['MONGO_URI'] = 'mongodb://localhost'
app.config['MONGO_DBNAME'] = 'sacbusinesses'
mongo = PyMongo(app)

@app.route('/')
def index():
    test = mongo.db.test4.find({"Business Description":"DRIVER"}) #mongo returns bson
    test2 = dumps(test) #converst bson to json
    return render_template('index.html', test2=test2)#passes json to index.html

app.run(debug = True, host = '0.0.0.0', port = 5000) #running on localhost:5000
