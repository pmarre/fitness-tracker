import os
from config import *
from flask import Flask, flash, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
import uuid


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

    if 'workout_image' in request.files:
        workout_image = request.files['workout_image']
        new_name = uuid.uuid1().hex
        mongo.save_file(new_name, workout_image)

    workout = {
        'workout_duration_h': h,
        'workout_duration_m': m,
        'workout_duration_s': s,
        'workout_duration': workout_duration,
        'workout_distance': d,
        'workout_distance_metric': unit,
        'workout_type': request.form.get('workout-type'),
        'workout_title': request.form.get('workout-title'),
        'workout_notes': request.form.get('workout-notes'),
        'workout_date': request.form.get('workout-date'),
        'user_id': request.form.get('user_id'),
        'workout_image': new_name}
    mongo.db.workouts.insert_one(workout)
    id = request.form.get("user_id")
    return redirect(url_for('dashboard', user_id=id))


@app.route('/sign-up', methods=['POST', 'GET'])
def sign_up_page():
    email = request.form.get("signup_email")
    f_name = request.form.get('signup_first-name')
    l_name = request.form.get('signup_last-name')
    password_1 = request.form.get('signup_password')
    password_2 = request.form.get('signup_re-password')

    if 'profile_image' in request.files:
        profile_image = request.files['profile_image']
        new_name = uuid.uuid1().hex
        print(new_name, profile_image)
        mongo.save_file(new_name, profile_image)
    else:
        new_name = None

    if password_1 != password_2:
        print("passwords don't match")
        return render_template('sign-up.html')
    elif mongo.db.current_users.find_one({'email': email}) != None:
        print("email already exists")
        return render_template('sign-up.html')
    else:
        mongo.db.current_users.insert_one(
            {'first_name': f_name, 'last_name': l_name, 'email': email, 'password': password_1, 'profile_image': new_name})
        if mongo.db.current_users.find_one({'email': email}) != None:
            user = mongo.db.current_users.find_one({'email': email})
            user_id = user['_id']
            return redirect(url_for('dashboard', user_id=user_id))


@app.route('/file/<filename>')
def file(filename):
    return mongo.send_file(filename)


@app.route('/delete_workout/<workout_id>')
def delete_workout(workout_id):
    workout = mongo.db.workouts.find_one({"_id": ObjectId(workout_id)})
    mongo.db.workouts.remove({'_id': ObjectId(workout_id)})
    return redirect(url_for('dashboard', user_id=workout['user_id']))


@app.route('/edit_workout/<workout_id>')
def edit_workout(workout_id):
    the_workout = mongo.db.workouts.find_one({"_id": ObjectId(workout_id)})
    return render_template('editworkout.html', workout=the_workout)


@app.route('/update_workout/<workout_id>', methods=['GET', 'POST'])
def update_workout(workout_id):
    h = request.form.get('workout-duration-h')
    m = request.form.get('workout-duration-m')
    s = request.form.get('workout-duration-s')
    workout_duration = str(h) + 'h ' + str(m) + 'm ' + str(s) + 's'

    unit = request.form.get('workout-distance-units')
    distance = request.form.get('workout-distance')
    if (distance == None):
        d = '0'
    else:
        d = str(distance)

    workout = mongo.db.workouts.find_one({"_id": ObjectId(workout_id)})
    workout_img = workout["workout_image"]

    if 'workout_image' in request.files:
        print('new image')
    else:
        print('old image')

    mongo.db.workouts.update({"_id": ObjectId(workout_id)}, {
        'workout_duration_h': h,
        'workout_duration_m': m,
        'workout_duration_s': s,
        'workout_duration': workout_duration,
        'workout_distance': d,
        'workout_distance_metric': unit,
        'workout_type': request.form.get('workout-type'),
        'workout_title': request.form.get('workout-title'),
        'workout_notes': request.form.get('workout-notes'),
        'workout_date': request.form.get('workout-date'),
        'user_id': request.form.get('user_id'),
        'workout_image': new_name})
    id = request.form.get("user_id")
    return redirect(url_for('dashboard', user_id=id))


if __name__ == '__main__':
    # for local deployment:
    app.run(debug=True)

    # for deployment to Heroku:
    # app.run(host=os.environ.get('IP'),
    #         port=int(os.environ.get('PORT')), debug=True)
