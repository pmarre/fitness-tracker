"""
This is the app.py file that makes FitnessTracker function
"""
import os
import uuid
from flask_bcrypt import Bcrypt
from bson.objectid import ObjectId
from flask_pymongo import PyMongo
from flask import Flask, flash, render_template, redirect, request, url_for, session
from fitness_tracker_config import *

# # For Heroku, comment out for local
MONGO_URI = os.environ.get('MONGO_URI')
SECRET_KEY = os.environ.get('SECRET_KEY')
DB_NAME = os.environ.get('DB_NAME')

app = Flask(__name__)
bcrypt = Bcrypt(app)
app.secret_key = SECRET_KEY
app.config["MONGO-DBNAME"] = DB_NAME
app.config["MONGO_URI"] = MONGO_URI


mongo = PyMongo(app)

## SIGN-UP PAGE ##


@app.route('/')
@app.route('/sign-up', methods=['POST', 'GET'])
def sign_up_page():
    """
    This function validates the signup form
    """
    session.clear()

    if request.method == "POST":
        email = request.form.get("signup_email").lower()
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

        if password_1 is not password_2:
            flash('Passwords do not match')
            return render_template('sign-up.html')
        elif mongo.db.current_users.find_one({'email': email}) is not None:
            flash('Email already exists')
            return render_template('sign-up.html')
        else:
            session.pop('user_id', None)
            pw_hash = bcrypt.generate_password_hash(password_1)
            mongo.db.current_users.insert_one(
                {'first_name': f_name, 'last_name': l_name, 'email': email,
                 'password': pw_hash, 'profile_image': new_name})
            if mongo.db.current_users.find_one({'email': email}) is not None:
                user = mongo.db.current_users.find_one({'email': email})
                user_id = user['_id']
                session['user_id'] = str(user_id)
                return redirect(url_for('dashboard', user_id=user_id))
    return render_template('sign-up.html')

## LOGIN PAGE ##


@app.route('/login')
def login():
    """ Renders Login Template """
    return render_template("login.html", user=mongo.db.current_users.find())

## VALIDATE USER LOGIN ##


@app.route('/validate_login', methods=['POST', 'GET'])
def validate_login():
    """ Validates Login """
    if request.method == "POST":
        email = request.form.get("email").lower()
        password = request.form.get("password")
        user = mongo.db.current_users.find_one({'email': email})
        print(user)
        session.pop('user_id', None)
        if user is not None:
            if bcrypt.check_password_hash(user['password'], password):
                user_id = user['_id']
                session['user_id'] = str(user_id)
                return redirect(url_for('dashboard', user_id=user_id))
            else:
                flash('Login unsuccessful')
                return redirect(url_for('login'))
        else:
            flash('Login unsuccessful')
            return redirect(url_for('login'))
    return redirect(url_for('login'))

## LOGOUT USER ##


@app.route('/logout')
def logout():
    """ Logs user out of site """
    session.pop('user_id', None)
    return render_template('login.html')

## USER DASHBOARD PAGE ##


@app.route('/dashboard/<user_id>')
def dashboard(user_id):
    """ Renders the users dashboard to show all workouts """
    user = mongo.db.current_users.find_one({'_id': ObjectId(user_id)})
    count_workouts = mongo.db.workouts.find(
        {'user_id': user_id}).count()

    if user is None:
        return redirect(url_for("login"))

    if session.get('user_id'):
        if session['user_id'] == str(user['_id']):
            workout_dict = mongo.db.workouts.find(
                {'user_id': user_id}).sort([('workout_date', -1)])
            recent_workout = mongo.db.workouts.find(
                {'user_id': user_id}).sort([('workout_date', -1)]).limit(1)
            if workout_dict.count() == 0:
                workouts = None
            else:
                workouts = workout_dict
            return render_template("dashboard.html", user=mongo.db.current_users.find_one(
                {'_id': ObjectId(user_id)}), workouts=workouts,
                recent=recent_workout, count=count_workouts)
        else:
            return redirect(url_for("login"))
    return redirect(url_for("login"))

## ADD WORKOUT PAGE ##


@app.route('/addworkout/<user_id>')
def addworkout(user_id):
    """ Renders add workout form template so user can add a new workout """
    return render_template("addworkout.html", user_id=user_id,
                           user=mongo.db.current_users.find_one({'_id': ObjectId(user_id)}))

## INSERT WORKOUT TO MONGO ##


@app.route('/insert_workout', methods=['GET', 'POST'])
def insert_workout():
    """ Inserts the newly added workout to Mongo """
    if request.method == "POST":
        hour = request.form.get('workout-duration-h')
        minute = request.form.get('workout-duration-m')
        second = request.form.get('workout-duration-s')
        workout_duration = str(hour) + 'h ' + \
            str(minute) + 'm ' + str(second) + 's'

        unit = request.form.get('workout-distance-units')
        distance = request.form.get('workout-distance')
        if distance is None:
            distance = '0'
        else:
            distance = str(distance)

        uploaded_image = request.files['workout_image']
        if uploaded_image.filename == '':
            print('no file')
            new_name = 'no_img'
        else:
            workout_image = request.files['workout_image']
            new_name = uuid.uuid1().hex
            mongo.save_file(new_name, workout_image)

        workout = {
            'workout_duration_h': hour,
            'workout_duration_m': minute,
            'workout_duration_s': second,
            'workout_duration': workout_duration,
            'workout_distance': distance,
            'workout_distance_metric': unit,
            'workout_type': request.form.get('workout-type'),
            'workout_title': request.form.get('workout-title'),
            'workout_notes': request.form.get('workout-notes'),
            'workout_date': request.form.get('workout-date'),
            'user_id': request.form.get('user_id'),
            'workout_image': new_name}
        mongo.db.workouts.insert_one(workout)
        user_id = request.form.get("user_id")
        return redirect(url_for('dashboard', user_id=user_id))
    return redirect(url_for('addworkout'))

## UPLOAD IMAGE TO MONGO ##


@app.route('/file/<filename>')
def file(filename):
    """ Sends file to Mongo """
    return mongo.send_file(filename)

## DELETE WORKOUT FROM MONGO ##


@app.route('/delete_workout/<workout_id>')
def delete_workout(workout_id):
    """ Deletes workout from Mongo """
    workout = mongo.db.workouts.find_one({"_id": ObjectId(workout_id)})
    mongo.db.workouts.remove({'_id': ObjectId(workout_id)})
    return redirect(url_for('dashboard', user_id=workout['user_id']))

## EDIT WORKOUT PAGE ##


@app.route('/edit_workout/<workout_id>')
def edit_workout(workout_id):
    """ Edits workout in Mongo """
    the_workout = mongo.db.workouts.find_one({"_id": ObjectId(workout_id)})
    return render_template('editworkout.html',
                           workout=the_workout,
                           user=mongo.db.current_users.find_one(
                               {'_id': ObjectId(the_workout['user_id'])}))

## UPDATE WORKOUT IN MONGO ##


@app.route('/update_workout/<workout_id>', methods=['GET', 'POST'])
def update_workout(workout_id):
    """ Updates workout in Mongo """
    if request.method == "POST":
        hour = request.form.get('workout-duration-h')
        minute = request.form.get('workout-duration-m')
        second = request.form.get('workout-duration-s')
        workout_duration = str(hour) + 'h ' + \
            str(minute) + 'm ' + str(second) + 's'

        unit = request.form.get('workout-distance-units')
        distance = request.form.get('workout-distance')
        if distance is None:
            distance = '0'
        else:
            distance = str(distance)

        workout = mongo.db.workouts.find_one({"_id": ObjectId(workout_id)})

        if request.files['workout_image_update'].filename == '':
            img = workout['workout_image']
        else:
            updated_img = request.files['workout_image_update']
            img = uuid.uuid1().hex
            mongo.save_file(img, updated_img)

        mongo.db.workouts.update({"_id": ObjectId(workout_id)}, {
            'workout_duration_h': hour,
            'workout_duration_m': minute,
            'workout_duration_s': second,
            'workout_duration': workout_duration,
            'workout_distance': distance,
            'workout_distance_metric': unit,
            'workout_type': request.form.get('workout-type'),
            'workout_title': request.form.get('workout-title'),
            'workout_notes': request.form.get('workout-notes'),
            'workout_date': request.form.get('workout-date'),
            'user_id': request.form.get('user_id'),
            'workout_image': img})
        user_id = request.form.get("user_id")
        return redirect(url_for('dashboard', user_id=user_id))
    return redirect(url_for('update_workout', workout_id=workout_id))

## EDIT PROFILE PAGE ##


@app.route('/edit_profile/<user_id>')
def edit_profile(user_id):
    """ Edit profile information """
    user = mongo.db.current_users.find_one({"_id": ObjectId(user_id)})
    return render_template('editprofile.html', user=user)

## UPDATE PROFILE IN MONGO ##


@app.route('/update_profile/<user_id>', methods=['GET', 'POST'])
def update_profile(user_id):
    """ Update profile in Mongo """
    if request.method == "POST":
        user = mongo.db.current_users.find_one({"_id": ObjectId(user_id)})
        if request.files['profile_image_update'].filename == '':
            img = user['profile_image']
        else:
            updated_img = request.files['profile_image_update']
            img = uuid.uuid1().hex
            mongo.save_file(img, updated_img)

        mongo.db.current_users.update(
            {"_id": ObjectId(user_id)},
            {"$set":
                {
                    'first_name': request.form.get('first_name'),
                    'last_name': request.form.get('last_name'),
                    'email': request.form.get('email'),
                    'profile_image': img}
             })

        return redirect(url_for('dashboard', user_id=user_id))
    return redirect(url_for('update_profile', user_id=user_id))

## DELETE PROFILE FROM MONGO ##


@app.route('/delete_profile/<user_id>')
def delete_profile(user_id):
    """ Delete profile from Mongo """
    mongo.db.current_users.remove({'_id': ObjectId(user_id)})
    return redirect(url_for('sign_up_page'))

## ABOUT PAGE ##


@app.route('/about')
def about():
    """ Check if user is logged in on about page to render proper nav """
    if session.get('user_id'):
        print('logged in')
        user_id = session['user_id']
        return render_template('about.html', user_id=user_id, loggedin=True)
    else:
        print('logged out')
        return render_template('about.html', loggedin=False)


if __name__ == '__main__':
    # for local deployment:
    # app.run(debug=True)

    # for deployment to Heroku:
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')), debug=False)
