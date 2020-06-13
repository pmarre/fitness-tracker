import os
from config import *
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

app = Flask(__name__)

app.config["MONGO-DBNAME"] = "task_manager"
app.config["MONGO_URI"] = MONGO_URI


mongo = PyMongo(app)


@app.route('/')
@app.route('/login')
def login():
    return render_template("login.html")


if __name__ == '__main__':
    # for local deployment:
    app.run(debug=True)

    # for deployment to Heroku:
    # app.run(host=os.environ.get('IP'),
    #         port=int(os.environ.get('PORT')), debug=True)
