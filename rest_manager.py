from flask import Flask, jsonify, request, abort, json, g
import datetime

import business_objects.User as User
import business_objects.quest as Quest
import business_objects.DefinitionQuestion as DefQuestion
import requests
import random

###DEBUG IMPORTS###


###END DEBUG I

local = True
# set this variable to determine whether you are running a test server locally or on the VPS

app = Flask(__name__)


@app.before_request
def before_request():
    print('Request Incoming')


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response


# -------------------------------------------------------------
# Functions
# -------------------------------------------------------------


def check_access_token(client_request):
    try:
        token = client_request.json['user_identifier']
        r = requests.get('https://www.googleapis.com/oauth2/v3/tokeninfo?access_token=' + token)
        if str(r.json()['sub']):
            return r
        else:
            return False

    except Exception as ex:
        print(ex)


def authenticate_user(client_request):
    try:
        r = check_access_token(client_request)
        user_id = str(r.json()['sub'])
        print(user_id)
        user = User.user.generate_from_id(user_id)
        if user and user.is_paid():
            return user
        else:
            return False
    except Exception as ex:
        print(ex)
        raise Exception("Failed to authenticate user")


def drop_user_quest(user):
    user.update_user_quest()
    user.update_current_user()
    return user.jsonify()


def update_user_quest(user, chapter_index=None,
                      seconds_per_question=None, number_of_questions=None,
                      cumulative=False):
    try:
        date_quest_started = datetime.datetime.now()
        number_correct = 0
        current_progress = 0
        # TODO: make method to calculate this
        completion_points = 100

        # TODO: make method to calculate this
        points_per_question = 1

        # TODO: validate number of questions, seconds per question, cumulative as a boolean


        # TODO: GO Get a word/definition question
        new_question = DefQuestion.DefinitionQuestion.make_from_chapter_index(chapter_index)

        user.update_user_quest(chapter_index=chapter_index, current_progress=current_progress,
                               date_quest_started=date_quest_started,
                               current_word_index=new_question.get_word_index(), number_correct=number_correct,
                               completion_points=completion_points,
                               seconds_per_question=seconds_per_question, points_per_question=points_per_question,
                               number_of_questions=number_of_questions,
                               cumulative=cumulative)

        user.update_current_user()
        return new_question.jsonify()

    except Exception as ex:
        # TODO: change prints to logger
        print("Error: " + str(ex))
        raise ex


# -------------------------------------------------------------
# Routes
# -------------------------------------------------------------


@app.route('/')
def index():
    return 'Hello, World!'


@app.route('/api/v1/get/user', methods=['POST'])
def get_user():
    try:
        user = authenticate_user(request)
        if user:
            print(user)
            return user.jsonify()
        else:
            abort(403, "Unable to authenticate user")
    except Exception as ex:
        print(ex)
        print("Unable to retrieve user.")


# starts a quest of the user's selection
# this route requires a json object with the following fields:
# quest_index = index of the quest user is requesting to start
# user_identifier = user's access token
@app.route('/api/v1/quest/start', methods=['POST'])
def start_quest():
    try:
        incoming_request = request
        print(incoming_request)

        # check authentication
        user = authenticate_user(request)
        if user:

            request_chapter_index = request.json['chapter_index']
            request_seconds_per_question = request.json['seconds_per_question']
            request_number_of_questions = request.json['number_of_questions']
            request_cumulative = request.json['cumulative']

            response = user.update_user_quest(user, chapter_index=request_chapter_index,
                                              seconds_per_question=request_seconds_per_question,
                                              number_of_questions=request_number_of_questions,
                                              cumulative=request_cumulative)
            return jsonify({
                    "question": response,
                    "user": user.jsonify()
                })
        else:
            abort(403, "Unable to authenticate user")

    except Exception as ex:
        print(ex)
        abort(500, "Unable to retrieve random question")


# clears current quest data for a user in case they want to start something new
# request requires only
# user_identifier = user's access token
@app.route('/api/v1/quest/drop', methods=['POST'])
def drop_quest():
    try:
        incoming_request = request
        print(incoming_request)
        # check authentication
        user = authenticate_user(request)
        if user:
            # drop the current quest, note that update with no flags does this, check its default args for details
            user = drop_user_quest(user)
            return user.jsonify()

        else:
            abort(403, "Unable to authenticate user")

    except Exception as ex:
        print(ex)
        abort(500, "Unable to retrieve random question")


# returns the last question the user worked on by looking it up from user table
# request requires only
# user_identifier = user's access token
@app.route('/api/v1/quest/resume', methods=['POST'])
def resume_quest():
    try:
        incoming_request = request
        print(incoming_request)

        # check authentication
        user = authenticate_user(request)
        if user:
            daily_reset = datetime.datetime.today().replace(hour=4, second=0, minute=0, microsecond=0)
            # check if that quest is valid
            if user['date_quest_started'] > daily_reset:
                # TODO: figure out quest logic

                return jsonify(question)
            else:
                print('quest is outdated, please start a new quest')

        else:
            abort(403, "Unable to authenticate user")

    except Exception as ex:
        print(ex)
        abort(500, "Unable to retrieve random question")


# returns the correct answer for the user's current question
# request requires
# user_identifier = user's access token
# user_answer = either the index or the value of the user's answer
@app.route('/api/v1/question/validation', methods=['POST'])
def get_validation():
    try:
        user = authenticate_user(request)
        if user:
            user_answer = (request.json['user_answer'])
            print(request.json)

            # get question with current question index
            dbconnect = questions_table_access_layer.QuestionTableAccess()
            question = dbconnect.get_question_by_question_id(question_id)
            dbconnect.close_connection()

            correct_answer = str(question['correct_answer'])

            # check if this is the last question of the set

            dbconnect = users_table_access_layer.UserTableAccess()
            print(type(user_answer))
            print(type(correct_answer))
            print('user answer is ' + user_answer)
            print('correct answer is ' + correct_answer)

            if user_answer == correct_answer:
                print('user is correct')
                # update points
                dbconnect.update_user_points(user_id, 10 * int(user['point_multiplier']))
                # increase multiplier
                if user['point_multiplier'] < 10:
                    dbconnect.update_user_multiplier(user_id, 1)
            else:
                print('user is incorrect')
                # decrease multiplier
                if user['point_multiplier'] > 1:
                    dbconnect.update_user_multiplier(user_id, -1)

            dbconnect.update_user_quest_progress(user_id)
            user = dbconnect.get_user_by_user_id(user_id)
            dbconnect.close_connection()

            dbconnect = quest_table_access_layer.QuestTableAccess()
            quest = dbconnect.get_quest_by_quest_index(user['quest_index'])
            dbconnect.close_connection()

            dbconnect = questions_table_access_layer.QuestionTableAccess()
            new_question = dbconnect.get_question_by_quest(quest)
            dbconnect.close_connection()

            dbconnect = users_table_access_layer.UserTableAccess()
            dbconnect.update_user_current_question(user_id, new_question['question_id'])
            dbconnect.close_connection()

            validation_package = {'correct_answer': correct_answer,
                                  'multiplier': user['point_multiplier'],
                                  'points': user['current_points'],
                                  'lvl': user['current_lvl']
                                  }

            # get a new question id for the user
            # put it in the user table so the user can get the question when they resume the quest

            return jsonify(validation_package)
        else:
            abort(403, "Unable to authenticate user")

    except Exception as ex:
        print(ex)
        abort(500, "Unable to retrieve random question")


@app.route('/api/v1/create/account', methods=['POST'])
def create_account():
    try:
        incoming_request = request
        print(incoming_request)

        token = request.json['user_identifier']
        r = requests.get('https://www.googleapis.com/oauth2/v3/tokeninfo?access_token=' + token)
        user_id = str(r.json()['sub'])
        user_email = str(r.json()['email'])
        print(user_id)

        user = User.user.generate_from_id(user_id)
        if user:
            return jsonify(user_exists='true', created="false")
        else:
            print('user does not exist')
            user = User.user(user_id=user_id,
                             first_name='derpington',
                             last_name='derpserson',
                             e_mail=user_email,
                             paid_through=datetime.datetime.today() + datetime.timedelta(days=365))
            success = user.save_new()
            if success:
                return jsonify(user_exists='false', created="true")
            else:
                return jsonify(user_exists='false', created="false", error="swallowed, contact an admin, my bad")
    except Exception as ex:
        print(ex)
        print('Invalid token')
        abort(500, "Error: " + str(ex))


@app.route('/api/v1/paidsignin', methods=['POST'])
def paid_sign_in():
    try:
        auth = authenticate_user(request)
        return jsonify(user_paid=auth)

    except Exception as ex:
        print(ex)
        print('Invalid token')
        abort(500, "Unable to retrieve random question")


# -------------------------------------------------------------
# Student client routes
# -------------------------------------------------------------

# -------------------------------------------------------------
# Professor client routes
# -------------------------------------------------------------
# TODO: add professor routes for changing the question database etc

# gets a multiple choice question by question ID
# takes the question ID (qID) as data from the client
# returns JSON that includes question text and answer text

# TODO: check to see if this CORS implementation is safe

if __name__ == '__main__':

    if local:
        app.debug = True
        # be careful with this apparently it's a security hazard
        app.run()
    else:
        app.run(host='0.0.0.0')
        # this allows the API to use the public IP
