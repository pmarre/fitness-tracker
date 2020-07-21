import os
from config import *
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

app = Flask(__name__)

app.config["MONGO-DBNAME"] = "fitnessDB"
app.config["MONGO_URI"] = MONGO_URI


mongo = PyMongo(app)


@app.route('/')
@app.route('/login')
def login(login_success=True):
    print(login_success)
    if login_success:
        return render_template("login.html", user=mongo.db.current_users.find(), login_error=False)
    else:
        return render_template("login.html", user=mongo.db.current_users.find(), login_error=True)


@app.route('/validate_login', methods=['POST', 'GET'])
def validate_login():
    email = request.form.get("email")
    password = request.form.get("password")
    if mongo.db.current_users.find_one({'email': email, 'password': password}) != None:
        return redirect(url_for('login', login_success=True))
    else:
        return redirect(url_for('login', login_success=False))


@app.route('/sign-up', methods=['POST', 'GET'])
def sign_up_page():
    email = request.form.get("signup_email")
    f_name = request.form.get('signup_first-name')
    l_name = request.form.get('signup_last-name')
    password_1 = request.form.get('signup_password')
    password_2 = request.form.get('signup_re-password')
    if password_1 != password_2:
        print("passwords don't match")
    elif mongo.db.current_users.find_one({'email': email}) != None:
        print("email already exists")
    else:
        mongo.db.current_users.insert_one(
            {'first_name': f_name, 'last_name': l_name, 'email': email, 'password': password_1})
    return render_template('sign-up.html')


if __name__ == '__main__':
    # for local deployment:
    app.run(debug=True)

    # for deployment to Heroku:
    # app.run(host=os.environ.get('IP'),
    #         port=int(os.environ.get('PORT')), debug=True)
