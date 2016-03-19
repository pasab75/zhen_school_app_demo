from flask import Flask, jsonify, request, abort, json, g
import datetime
import db_access.db_question as questions_table_access_layer
import db_access.db_user as users_table_access_layer
import business_objects.user as user_obj_generator
from oauth2client import client


local = True
# set this variable to determine whether you are running a test server locally or on the VPS

app = Flask(__name__)

#


@app.before_request
def before_request():
    print('Request Incoming')

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response


@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

# -------------------------------------------------------------
# Routes
# -------------------------------------------------------------


def authenticate_user(request):
    g.dbconnect_user = users_table_access_layer.UserTableAccess()
    token = request.json['user_identifier']
    client_id = '334346238965-oliggj0124b9r4nhbdf4nuboiiha7ov3.apps.googleusercontent.com'
    idinfo = client.verify_id_token(str(token), client_id)
    exists = g.dbconnect_user.check_if_user_valid(str(idinfo['sub']))
    if exists:
        is_paid = g.dbconnect_user.check_if_user_paid(str(idinfo['sub']))
        return is_paid
    else:
        return False


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
        token = request.json['user_identifier']
        print(token)

        client_id = '334346238965-oliggj0124b9r4nhbdf4nuboiiha7ov3.apps.googleusercontent.com'
        idinfo = client.verify_id_token(str(token), client_id)

        dbconnect = users_table_access_layer.UserTableAccess()

        exists = dbconnect.check_if_user_valid(str(idinfo['sub']))

        if exists:
            dbconnect.close_connection()
            print('user exists')
            return jsonify(user_exists='true')
        else:
            print('user does not exist')
            new_user = user_obj_generator.user(idinfo['sub'],
                                               idinfo['given_name'],
                                               idinfo['family_name'],
                                               idinfo['email'],
                                               '0'
                                               '0'
                                               )

            dbconnect.add_user_new(new_user)
            dbconnect.close_connection()
            return jsonify(user_exists='false')


    except Exception as ex:
        print(ex)
        print('Invalid token')


@app.route('/api/v1/paidsignin', methods=['POST'])
def paid_sign_in():
    try:
        auth = authenticate_user(request)
        return jsonify(user_paid=auth)

    except Exception as ex:
        print(ex)
        print('Invalid token')
        abort(500, "Unable to retrieve random question")

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


@app.route('/api/v1/get/daily/activities', methods=['POST'])
def get_activities():
    try:
        exists = authenticate_user(request)
        if exists:
            return jsonify(response_type='activity_list',
                           activity_text_1='Random Activity 1',
                           activity_description_1='This is a random activity',
                           number_of_questions_1='30',
                           point_value_1='300',
                           activity_text_2='Random Activity 2',
                           activity_description_2='This is a random activity',
                           number_of_questions_2='25',
                           point_value_2='300',
                           activity_text_3='Random Activity 3',
                           activity_description_3='This is a random activity',
                           number_of_questions_3='20',
                           point_value_3='300',
                           activity_text_4='Random Activity 4',
                           activity_description_4='This is a random activity',
                           number_of_questions_4='50',
                           point_value_4='300',
                           activity_text_5='Random Activity 5',
                           activity_description_5='This is a random activity',
                           number_of_questions_5='15',
                           point_value_5='300'
                           )
        else:
            abort(403, "Unable to authenticate user")
    except Exception as ex:
        print(ex)
        print("Unable to retrieve activity list.")


@app.route('/api/v1/get/activity/list', methods=['POST'])
def get_activity_list():
    try:
        exists = authenticate_user(request)
        if exists:
        # grab current activity list

        # return list text to user
            return True
        else:
            abort(403, "Unable to authenticate user")
    except Exception as ex:
        print(ex)
        print("Unable to retrieve activity list.")


@app.route('/api/v1/set/activity/by/user', methods=['POST'])
def set_activity_by_user():
    try:
        exists = authenticate_user(request)
        if exists:
        # save activity index in (user)? database?
            return True
        else:
            abort(403, "Unable to authenticate user")
    except Exception as ex:
        print(ex)
        print("Unable to save activity.")


@app.route('/api/v1/get/question/next/by/activity', methods=['POST'])
def get_question_next_by_activity():
    try:
        exists = authenticate_user(request)
        if exists:
        # determine user identity

        # get current activity for user

        # update activity progress

        # generate valid question parameters for given activity
        # get a question from database that matches question parameters
        # return question to client

            return True
        else:
            abort(403, "Unable to authenticate user")
    except Exception as ex:
        print(ex)
        abort(500, "Unable to retrieve next question.")


@app.route('/api/v1/validate/question', methods=['POST'])
def validate_question():
    try:
        exists = authenticate_user(request)
        if exists:
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

            question_id = (request.json['question_id'])
            user_answer = int((request.json['user_answer']))
            print("question ID = " + str(question_id))
            print("given answer index = " + str(user_answer))

            dbconnect = questions_table_access_layer.QuestionTableAccess()

            result = dbconnect.get_question_by_question_id(question_id)
            correct_answer = result.get_correct_answer_index()

            print("correct answer index = " + str(correct_answer))
            print("question type index = " + str(result.get_type()))
            print("question topic index = " + str(result.get_topic()))

            dbconnect.close_connection()

            if user_answer == correct_answer:
                return jsonify(validation='true', answer_index=str(correct_answer))
            else:
                return jsonify(validation='false', answer_index=str(correct_answer), given_answer=str(user_answer))
        else:
            abort(403, "Unable to authenticate user")
    except Exception as ex:
        print(ex)
        abort(500, "Unable to validate question")


@app.route('/api/v1/get/question/definition/by/topic', methods=['POST'])
def get_question_definition_by_topic():
    try:
        exists = authenticate_user(request)
        if exists:

            incoming_request = request
            print(incoming_request)
            topic_index = (request.json['topic'])
            print(topic_index)

            dbconnect = questions_table_access_layer.QuestionTableAccess()
            result = dbconnect.get_question_def_by_topic(topic_index)

            dbconnect.close_connection()
            return result.get_jsonified()
        else:
            abort(403, "Unable to authenticate user")

    except Exception as ex:
        print(ex)
        abort(500, "Unable to retrieve random question")


@app.route('/api/v1/get/question/random', methods=['POST'])
def get_question_random():
    try:
        exists = authenticate_user(request)
        if exists:
            incoming_request = request
            print(incoming_request)
            qType = (request.json['question_type'])
            print(qType)

            dbconnect = questions_table_access_layer.QuestionTableAccess()
            result = dbconnect.get_question_random_by_type(qType)

            dbconnect.close_connection()
            return result.get_jsonified()
        else:
            abort(403, "Unable to authenticate user")
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

if __name__ == '__main__':

    if local:
        app.debug = True
        # be careful with this apparently it's a security hazard
        app.run()
    else:
        app.run(host='0.0.0.0')
        # this allows the API to use the public IP
