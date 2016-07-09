from flask import Flask, jsonify, request, abort
import datetime

import business_objects.User as User
import business_objects.DefinitionQuestion as DefQuestion
import business_objects.QuestLogEntry as QuestLogEntry
import requests

###DEBUG IMPORTS###


###END DEBUG IMPORTS###

# TODO: update DefQuestion.DefinitionQuestion.make_from_chapter_index(user.get_chapter_index())
# TODO: make it whatever SRS library/algorithm zhen comes up with probably will require redo of DB but fuck it

local = False
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

#########################################################################################
# DESCRIPTION
# checks the access token that is passed from the client against google database
# the access token is passed under the "user_identifier" label
# the google database should return information about the user including a user ID number
#
# RETURN CASES
# if the user id is returned, then we return all user information
# if the user is not a valid google user, then we return false
#
# TAKES
# "client_request" JSON that includes "user_identifier" field
#
# RETURNS
# user information json
# False bool
#########################################################################################


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
#########################################################################################
# DESCRIPTION
# sends access token to google server to authenticate
#
# RETURN CASES
# if the user exists in our database, then return the user object
# if the user does not exist in our database, then make a new user object and return it
# returns user object in all foreseeable cases
# if this method returns false, then something bad has happened
#
# TAKES
# "client_request" JSON that includes "user_identifier" field
#
# RETURNS
# User business object
# False bool
#########################################################################################

def authenticate_user(client_request):
    try:
        r = check_access_token(client_request)
        if r:
            user_id = str(r.json()['sub'])
            print(user_id)
            user = User.User().generate_from_id(user_id)
            if user and user.is_paid():
                return user
            else:
                return False
        else:
            return False
    except Exception as ex:
        print(ex)
        raise Exception("Failed to authenticate user")

#########################################################################################
# DESCRIPTION
# clears the current user's quest
#
# RETURN CASES
# always returns User's json object
#
# TAKES
# user object
#
# RETURNS
# json object from user.jsonify
#########################################################################################


def drop_user_quest(user):
    user.update_user_quest()
    user.update_current_user()
    return user.get_json()

#########################################################################################
# DESCRIPTION
# updates the user's quest information when they have chosen a quest to start
#
# RETURN CASES
# should always return a new question json
#
# TAKES
# user object
# chapter index (integer)
# seconds per question (integer) - if this is zero, we should give unlimited time
# number of questions (integer) - this should take specific values
# TODO make this validate to only take specific values
# cumulative (boolean) - whether or not you should include chapters before the given chapter index
# RETURNS
# question json
#########################################################################################


def update_user_quest(user,
                      chapter_index=None,
                      seconds_per_question=None,
                      number_of_questions=None,
                      cumulative=False):
    try:
        datetime_quest_started = datetime.datetime.now()
        number_correct = 0
        current_progress = 0
        points_per_question = 20
        question_multiplier = 5

        completion_points = 50*number_of_questions

        valid_num_questions = [10, 25, 50]
        valid_secs_per_question = [30, 10, 5, 0]
        valid_bool = [True, False]

        # TODO: Make this return something that will display an error on the client side
        if number_of_questions not in valid_num_questions or seconds_per_question not in valid_secs_per_question or cumulative not in valid_bool:
            return False

        if number_of_questions == 25:
            question_multiplier = 15

        if number_of_questions == 50:
            question_multiplier = 40

        if seconds_per_question <= 30:
            points_per_question += 1
            completion_points += 10*question_multiplier

        if seconds_per_question <= 10:
            points_per_question += 2
            completion_points += 10*question_multiplier

        if seconds_per_question <= 5:
            points_per_question += 3
            completion_points += 20*question_multiplier

        if cumulative:
            points_per_question += 1*chapter_index
            completion_points += 10*question_multiplier

        # TODO: GO Get a word/definition question
        new_question = DefQuestion.DefinitionQuestion().make_from_chapter_index(chapter_index, 6)

        user.update_user_quest(chapter_index=chapter_index, current_progress=current_progress,
                               datetime_quest_started=datetime_quest_started,
                               current_word_index=new_question.get_word_index(), number_correct=number_correct,
                               completion_points=completion_points,
                               seconds_per_question=seconds_per_question, points_per_question=points_per_question,
                               number_of_questions=number_of_questions,
                               cumulative=cumulative)

        user.update_current_user()
        return new_question.get_json()

    except Exception as ex:
        # TODO: change prints to logger
        print("Error: " + str(ex))
        raise ex

# -------------------------------------------------------------
# Routes
# -------------------------------------------------------------

# -------------------------------------------------------------
# Student client routes
# -------------------------------------------------------------

#########################################################################################
# DESCRIPTION
# returns the user's information to the client after authenticating
#
# RETURN CASES
# should always return user json
#
# TAKES
# user authentication token
#
# RETURNS
# user json
#
#########################################################################################



@app.route('/api/v1/user/get', methods=['POST'])
def get_user():
    try:
        print(request.json)
        user = authenticate_user(request)
        if user:
            print(user)
            return jsonify(user.get_json())
        else:
            return abort(403, "Unable to authenticate user")
    except Exception as ex:
        print(ex)
        print("Unable to retrieve user.")
        return abort(500, "Unable to retrieve user. Error: "+str(ex))

@app.route('/', methods=['GET'])
def helloworld():
    try:
        print(request)
        return jsonify("Hello World")
    except Exception as ex:
        print(ex)
        print("Unable to retrieve user.")
        return abort(500, "Unable to retrieve user. Error: " + str(ex))
#########################################################################################
# DESCRIPTION
# When the user requests, authenticate them and then serves up a new question
# for the start of the quest
#
# RETURN CASES
# Error: if the user does not authenticate
# Error: if the user causes an internal server error
# On Success: Returns the user object and a new question in json format
#
# TAKES
# user authentication token string, chapter_index int, number_of_questions int,
# seconds_per_question int, cumulative boolean
#
# RETURNS
# updated user object, new question, and 200 code
#
#########################################################################################


@app.route('/api/v1/quest/start', methods=['POST'])
def start_quest():
    try:
        incoming_request = request
        print(incoming_request)
        json_obj = request.json
        # check authentication
        user = authenticate_user(request)
        if user:
            request_chapter_index = json_obj['chapter_index']
            request_seconds_per_question = json_obj['seconds_per_question']
            request_number_of_questions = json_obj['number_of_questions']
            request_cumulative = json_obj['cumulative']

            response = update_user_quest(user, chapter_index=request_chapter_index,
                                         seconds_per_question=request_seconds_per_question,
                                         number_of_questions=request_number_of_questions,
                                         cumulative=request_cumulative)

            user.update_current_user()
            return jsonify({
                "question": response,
                "user": user.get_json()
            })

        else:
            return abort(403, "Unable to authenticate user")

    except Exception as ex:
        print(ex)
        return abort(500, "Unable to retrieve random question, error: "+str(ex))


#########################################################################################
# DESCRIPTION
# Drops the users current quest, presumably used before start new quest if user is frustrated
#
# RETURN CASES
# Error: if the user does not authenticate
# Error: if the user causes an internal server error
# On Success: Returns the user object and a new question in json format
#
# TAKES
# user authentication token string
#
# RETURNS
# updated user object, and 200 code
#
#########################################################################################


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
            user.update_current_user()
            return jsonify(user.get_json())

        else:
            return abort(403, "Unable to authenticate user")

    except Exception as ex:
        print(ex)
        return abort(500, "Unable to retrieve random question")
#

#########################################################################################
# DESCRIPTION
# Assumed use: on user phone reboot or other session clear, the user will request a new
# question.  This could be used to avoid particularly hard questions, watch logs for abuse
#
# RETURN CASES
# Error: if the user does not authenticate
# Error: if the user causes an internal server error
# On Success: Returns the user object and a new question in json format
#
# TAKES
# user authentication token string
#
# RETURNS
# updated user object, new question, and 200 code
#
#########################################################################################


@app.route('/api/v1/quest/resume', methods=['POST'])
def resume_quest():
    try:
        incoming_request = request
        print(incoming_request)

        # check authentication
        user = authenticate_user(request)
        if user:
            new_question = DefQuestion.DefinitionQuestion.make_from_chapter_index(user.get_chapter_index())
            response = new_question.get_json()
            user.set_datetime_question_started(datetime.datetime.now())
            user.update_current_user()
            return jsonify({
                "question": response,
                "user": user.get_json()
            })
        else:
            return abort(403, "Unable to authenticate user")

    except Exception as ex:
        print(ex)
        return abort(500, "Unable to retrieve random question")


#########################################################################################
# DESCRIPTION
# User is submitting answer for a question they were presented
#
# RETURN CASES
# Error: if the user does not authenticate
# Error: if the user causes an internal server error
# On Success: returns updated user object, if they got the answer correct (boolean), the index of the correct answer,
# quest_complete boolean flag, and a new question for them to answer if they are still in an active quest
#
# TAKES
# user authentication token string, user_answer
# TODO: geo location data
# RETURNS
# user object, answer_index (int), correct (boolean), question object, quest_complete (boolean)
#########################################################################################


@app.route('/api/v1/question/submit', methods=['POST'])
def submit_question():
    try:
        print(request.json)

        user = authenticate_user(request)
        if user:
            user_answer = (request.json['user_answer'])
            correct = user.check_answer(user_answer)
            answer_index = user.get_current_word_index()
            quest_complete = user.is_quest_complete()
            if not quest_complete:
                question = DefQuestion.DefinitionQuestion().make_from_chapter_index(user.get_chapter_index(), 6).get_json()
            else:
                question = None
                try:
                    #TODO: add Lat and Lon
                    QuestLogEntry.QuestLogEntry().generate_from_user(user)
                except:
                    print("failed too make log entry, not the end of the world, but no log entry made")
            user.update_current_user()
            return jsonify({
                "user": user.get_json(),
                "correct": correct,
                "answer_index": answer_index,
                "question": question,
                "quest_complete": quest_complete
            })
        else:
            return abort(403, "Unable to authenticate user")

    except Exception as ex:
        print(ex)
        return abort(500, "Unable to retrieve random question")

#########################################################################################
# DESCRIPTION
# new user is submitting for an account
#
# RETURN CASES
# Error: if the user does not authenticate
# Error: if the user causes an internal server error
# On Success:
#
# TAKES
# user_identifier, sub, email, first name, last name
#
# RETURNS
# user_exists (boolean), created (boolean), error flag if we think an error occured but couldnt find it
#########################################################################################


@app.route('/api/v1/account/create', methods=['POST'])
def create_account():
    try:
        incoming_request = request
        print(incoming_request)
        json = request.json
        token = json['user_identifier']
        r = requests.get('https://www.googleapis.com/oauth2/v3/tokeninfo?access_token=' + token)
        user_id = str(r.json()['sub'])
        user_email = str(r.json()['email'])
        print(user_id)

        user = User.User().generate_from_id(user_id)

        if user:
            return jsonify(user_exists='true', created="false")
        else:
            print('user does not exist')
            user = User.User(user_id=user_id,
                             first_name=json['first_name'],
                             last_name=json['last_name'],
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
        return abort(500, "Error: " + str(ex))

# -------------------------------------------------------------
# Professor client routes
# -------------------------------------------------------------
# TODO: add professor routes for changing the question database etc

# TODO: check to see if this CORS implementation is safe

if __name__ == '__main__':

    if local:
        app.run(host='0.0.0.0', port=5000)
        app.debug = True

    else:
        app.run(host='0.0.0.0', port=5000)
        # this allows the API to use the public IP
