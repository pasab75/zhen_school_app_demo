from flask import Flask, jsonify, request, abort
import json
import datetime
import db_access.db_question as db_access_layer

local = True
# set this variable to determine whether you are running a test server locally or on the VPS

app = Flask(__name__)

@app.route('/')
def index():
    return "Hello, World!"

# student client routes

@app.route('/get/random/FR', methods=['POST'])

@app.route('/get/random/DEF', methods=['POST'])

@app.route('/get/WORD', methods=['POST'])

@app.route('/get/DEF', methods=['POST'])

@app.route('/get/FR', methods=['POST'])

#TODO:make these routes available


# gets a multiple chocie question by question ID
# takes the question ID (qID) as data from the client
# returns JSON that includes question text and answer text
@app.route('/get/MC', methods=['POST'])
def get_question():
    try:
        incoming_request = request
        print(incoming_request)
        task_id = (request.json['id'])
        result = None
        dbconnect = db_access_layer.database_access()
        result = dbconnect.get_by_id(task_id)

        dbconnect.close_connection()
        return result.get_jsonified()
    except Exception as ex:
        print(ex)
        abort(500, "Unable to find id or no id given")


# gets a random multiple choice question
@app.route('/get/MC/random', methods=['POST'])
def get_random_mc():
    try:
        incoming_request = request
        print(incoming_request)
        result = None
        dbconnect = db_access_layer.database_access()
        result = dbconnect.get_randomALL()

        dbconnect.close_connection()
        return result.get_jsonified()

    except Exception as ex:
        print(ex)
        abort(500, "Unable to retrieve random question")


# adds some random questions to the database so we can test it better
@app.route('/add/dummy/questions', methods=['POST'])
def add_random():
    try:
        incoming_request = request
        dbconnect = db_access_layer.database_access()
        dbconnect.load_randomShit(10)

        dbconnect.close_connection()
        return "false"

    except Exception as ex:
        print(ex)
        abort(500, "Unable to add questions to DB")


#checks if a multiple choice question is correct
@app.route('/validate/MC', methods=['POST'])
def get_validation():
    try:
        incoming_request = request
        print(incoming_request)
        questionID = (request.json['qID'])
        answerID = int((request.json['aID']))
        print(questionID)
        print(answerID)

        result = None

        dbconnect = db_access_layer.database_access()

        #TODO: create user table and record point gain
        #TODO: create log table to record question statistics

        #TODO: how do we make sure students can't just game the system by writing some front end code that accesses the API to get free points? for example, a student has a frontend html file that requests the same question over and over again...
        #TODO: add table that records sessions for users this should include what was the last question served to the user. we can use this for server side validation to make sure students aren't juking the system

        #TODO: look at zhen's code and make sure it's not ass backwards

        query = result = dbconnect.get_by_id(questionID)
        correctID = result.get_correct_answer_index()

        dbconnect.get_numEntries('questions')

        if answerID == correctID:
            return jsonify(validation = 'true')
        else:
            return jsonify(validation = 'false')

        dbconnect.close_connection()



    except Exception as ex:
        print(ex)
        abort(500, "Unable to validate question")

#professor client routes

#TODO: add professor routes for changing the question database etc

#TODO: check to see if this CORS implementation is safe

@app.after_request
def after_request(response):
  response.headers.add('Access-Control-Allow-Origin', '*')
  response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
  response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
  return response

if __name__ == '__main__':

        if local == True:
            app.debug = True
            #be careful with this apparently it's a security hazard
            app.run()
        else:
            app.run(host='0.0.0.0')
            #this allows the API to use the public IP
