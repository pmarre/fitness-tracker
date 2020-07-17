import os
from config import *
from flask import Flask, flash, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

app = Flask(__name__)
app.secret_key = SECRET_KEY
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
        user = mongo.db.current_users.find_one({'email': email})
        user_id = user['_id']
        return redirect(url_for('dashboard', user_id=user_id))
    else:
        flash('Login unsuccessful')
        return redirect(url_for('login'))


@app.route('/dashboard/<user_id>', methods=['POST', 'GET'])
def dashboard(user_id):
    workout_dict = mongo.db.workouts.find(
        {'user_id': user_id}).sort([('workout_date', -1)])

    return render_template("dashboard.html", user=mongo.db.current_users.find_one({'_id': ObjectId(user_id)}), workouts=workout_dict)


@app.route('/addworkout/<user_id>', methods=['POST', 'GET'])
def addworkout(user_id):
    return render_template("addworkout.html", user_id=user_id)


@app.route('/insert_workout', methods=['GET', 'POST'])
def insert_workout():
    h = request.form.get('workout-duration-h')
    m = request.form.get('workout-duration-m')
    s = request.form.get('workout-duration-s')
    print(h)
    workout_duration = str(h) + 'h ' + str(m) + 'm ' + str(s) + 's'

    unit = request.form.get('workout-distance-units')
    distance = request.form.get('workout-distance')
    if (distance == None):
        d = '0'
    else:
        d = str(distance)

    print(d + str(unit))
    workout = {
        'workout_duration': workout_duration,
        'workout_distance': d + ' ' + unit,
        'workout_type': request.form.get('workout-type'),
        'workout_title': request.form.get('workout-title'),
        'workout_notes': request.form.get('workout-notes'),
        'workout_date': request.form.get('workout-date'),
        'user_id': request.form.get('user_id')}
    mongo.db.workouts.insert_one(workout)
    id = request.form.get("user_id")
    return redirect(url_for('dashboard', user_id=id))


if __name__ == '__main__':
    # for local deployment:
    app.run(debug=True)

    # for deployment to Heroku:
    # app.run(host=os.environ.get('IP'),
    #         port=int(os.environ.get('PORT')), debug=True)
