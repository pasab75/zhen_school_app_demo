from flask import Flask, jsonify, request, abort
import json
import datetime
import db_access.db_question as questions_table_access_layer
import db_access.db_user as users_table_access_layer

local = True
# set this variable to determine whether you are running a test server locally or on the VPS

app = Flask(__name__)


@app.route('/')
def index():

    dict = {'Name': 'Zara', 'Age': 7, 'Class': 'First'}

    print( '=%s, '.join(dict.keys()) + "=%s" )

    return "hihi"

# adds some random test questions to the database


@app.route('/add/dummy/questions', methods=['POST'])
def add_random():
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

# student client routes


@app.route('/get/defquestion/topic', methods=['POST'])
def get_defquestion_topic():
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


@app.route('/get/question/random', methods=['POST'])
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

# checks if a multiple choice question is correct


@app.route('/validate/question', methods=['POST'])
def validate_question():
    try:
        incoming_request = request
        print(incoming_request)
        questionID = (request.json['qID'])
        answerID = int((request.json['aID']))
        print("question ID = " + str(questionID))
        print("given answer index = " + str(answerID))

        dbconnect = questions_table_access_layer.QuestionTableAccess()

        # TODO: create user table and record point gain
        # TODO: create log table to record question statistics

        # TODO: how do we make sure students can't just game the system by writing some front end code that accesses the API to get free points? for example, a student has a frontend html file that requests the same question over and over again...
        # TODO: add table that records sessions for users this should include what was the last question served to the user. we can use this for server side validation to make sure students aren't juking the system

        # TODO: look at zhen's code and make sure it's not ass backwards

        result = dbconnect.get_question_by_id(questionID)
        correctID = result.get_correct_answer_index()

        print("correct answer index = " + str(correctID))
        print("question type index = " + str(result.get_type()))
        print("question topic index = " + str(result.get_topic()))

        dbconnect.close_connection()

        if answerID == correctID:
            return jsonify(validation = 'true')
        else:
            return jsonify(validation = 'false')



    except Exception as ex:
        print(ex)
        abort(500, "Unable to validate question")


# professor client routes

# TODO: add professor routes for changing the question database etc

# gets a multiple choice question by question ID
# takes the question ID (qID) as data from the client
# returns JSON that includes question text and answer text


@app.route('/get/question/byid', methods=['POST'])
def get_question_byid():
    try:
        incoming_request = request
        print(incoming_request)
        task_id = (request.json['id'])
        result = None
        dbconnect = questions_table_access_layer.DatabaseAccess()
        result = dbconnect.get_question_by_id(task_id)

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
