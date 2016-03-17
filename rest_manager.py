from flask import Flask, jsonify, request, abort
import json
import datetime
import db_access.db_question as questions_table_access_layer
import db_access.db_user as users_table_access_layer
import requests
from oauth2client import client, crypt


local = True
# set this variable to determine whether you are running a test server locally or on the VPS

app = Flask(__name__)


# -------------------------------------------------------------
# Routes
# -------------------------------------------------------------


@app.route('/')
def index():
    try:
        incoming_request = request
        print(incoming_request)
        dbconnect = questions_table_access_layer.QuestionTableAccess()
        dbconnect.empty_table('questions')
        dbconnect.load_questions_testing(1000)

        dbconnect.close_connection()
        return "false"

    except Exception as ex:
        print(ex)
        abort(500, "Unable to add questions to DB")


@app.route('/api/v1/tokensignin', methods=['POST'])
def sign_in():
    try:
        token = request.form.get('idtoken')

        client_id = '334346238965-oliggj0124b9r4nhbdf4nuboiiha7ov3.apps.googleusercontent.com'
        idinfo = client.verify_id_token(str(token), client_id)
        userid = idinfo['sub']

        print(userid)

        return "false"
    except Exception as ex:
        print(ex)
        print('Invalid token')


# @app.route('/api/v1/add/dummy/questions', methods=['POST'])
# def add_random():
#     try:
#         incoming_request = request
#         print(incoming_request)
#         dbconnect = questions_table_access_layer.QuestionTableAccess()
#         dbconnect.empty_table('questions')
#         dbconnect.load_questions_testing(1000)
#
#         dbconnect.close_connection()
#         return "false"
#
#     except Exception as ex:
#         print(ex)
#         abort(500, "Unable to add questions to DB")

# -------------------------------------------------------------
# Student client routes
# -------------------------------------------------------------


@app.route('/api/v1/get/activities', methods=['POST'])
def get_activities():
    return True


@app.route('/api/v1/get/activity/list', methods=['POST'])
def get_activity_list():
    try:
        # grab current activity list

        # return list text to user
        return True

    except Exception as ex:
        print(ex)
        print("Unable to retrieve activity list.")


@app.route('/api/v1/set/activity/by/user', methods=['POST'])
def set_activity_by_user():
    try:
        # save activity index in (user)? database?
        return True

    except Exception as ex:
        print(ex)
        print("Unable to save activity.")


@app.route('/api/v1/get/question/next/by/activity', methods=['POST'])
def get_question_next_by_activity():
    try:
        # determine user identity

        # get current activity for user

        # update activity progress

        # generate valid question parameters for given activity
        # get a question from database that matches question parameters
        # return question to client

        return True

    except Exception as ex:
        print(ex)
        abort(500, "Unable to retrieve next question.")


@app.route('/api/v1/validate/question', methods=['POST'])
def validate_question():
    try:
        incoming_request = request
        print(incoming_request)

        # TODO: implement the following psuedocode instead of what is here already
        # identify user

        # grab the last question that the user was served

        # get the answer to the question

        # compare the answer to the user's answer

        # if answer is correct
            # record point gain for user
            # update the user's multiplier
            # update user's activity progress
            # return true

        # if answer is incorrect
            # update the user's multiplier
            # update user's activity progress
            # return false

        questionID = (request.json['question_id'])
        answerID = int((request.json['answer_id']))
        print("question ID = " + str(questionID))
        print("given answer index = " + str(answerID))

        dbconnect = questions_table_access_layer.QuestionTableAccess()

        result = dbconnect.get_question_by_question_id(questionID)
        correctID = result.get_correct_answer_index()

        print("correct answer index = " + str(correctID))
        print("question type index = " + str(result.get_type()))
        print("question topic index = " + str(result.get_topic()))

        dbconnect.close_connection()

        if answerID == correctID:
            return jsonify(validation='true', answer_index=str(correctID),)
        else:
            return jsonify(validation='false', answer_index=str(correctID), given_answer=str(answerID))

    except Exception as ex:
        print(ex)
        abort(500, "Unable to validate question")


@app.route('/api/v1/get/question/definition/by/topic', methods=['POST'])
def get_question_definition_by_topic():
    try:
        incoming_request = request
        print(incoming_request)
        topic_index = (request.json['topic'])
        print(topic_index)

        dbconnect = questions_table_access_layer.QuestionTableAccess()
        result = dbconnect.get_question_def_by_topic(topic_index)

        dbconnect.close_connection()
        return result.get_jsonified()

    except Exception as ex:
        print(ex)
        abort(500, "Unable to retrieve random question")


@app.route('/api/v1/get/question/random', methods=['POST'])
def get_question_random():
    try:
        incoming_request = request
        print(incoming_request)
        qType = (request.json['question_type'])
        print(qType)

        dbconnect = questions_table_access_layer.QuestionTableAccess()
        result = dbconnect.get_question_random_by_type(qType)

        dbconnect.close_connection()
        return result.get_jsonified()

    except Exception as ex:
        print(ex)
        abort(500, "Unable to retrieve random question")


# -------------------------------------------------------------
# Professor client routes
# -------------------------------------------------------------
# TODO: add professor routes for changing the question database etc

# gets a multiple choice question by question ID
# takes the question ID (qID) as data from the client
# returns JSON that includes question text and answer text


@app.route('/api/v1/get/question/by_id', methods=['POST'])
def get_question_byid():
    try:
        incoming_request = request
        print(incoming_request)
        task_id = (request.json['id'])
        result = None
        dbconnect = questions_table_access_layer.QuestionTableAccess()
        result = dbconnect.get_question_by_question_id(task_id)

        dbconnect.close_connection()
        return result.get_jsonified()
    except Exception as ex:
        print(ex)
        abort(500, "Unable to find id or no id given")

# TODO: check to see if this CORS implementation is safe


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response

if __name__ == '__main__':

    if local:
        app.debug = True
        # be careful with this apparently it's a security hazard
        app.run()
    else:
        app.run(host='0.0.0.0')
        # this allows the API to use the public IP
