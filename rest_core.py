from flask import Flask, jsonify, request, abort, send_from_directory

import datetime

import config as config
import rest_functions as functions

import business_objects.User as User

# TODO: update DefQuestion.DefinitionQuestion.make_from_chapter_index(user.get_chapter_index())
# TODO: make it whatever SRS library/algorithm zhen comes up with probably will require redo of DB but fuck it

app = Flask(__name__, static_url_path='/')


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
# Routes
# -------------------------------------------------------------


@app.route('/', methods=['GET'])
def hello_world():
    try:
        print(request.json)
        return send_from_directory('', "index.html")
    except Exception as ex:
        print(ex)
        print("Unable to retrieve user.")
        return abort(500, "Unable to retrieve user. Error: " + str(ex))


@app.route('/<path:path>', methods=['GET'])
def static_file(path):
    return send_from_directory('', path)

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
        user = functions.authenticate_user(request)
        if user:
            print(user)
            return jsonify({
                "user": user.get_json()
            })
        else:
            return abort(403, "Unable to authenticate user")
    except Exception as ex:
        print("Unable to retrieve user:" + str(ex))
        return abort(500, "Unable to retrieve user. Error: "+str(ex))

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
        # check authentication
        user = functions.authenticate_user(request)
        if user:
            new_question = functions.update_quest_with_client_choices(user, request)
            return jsonify({
                "question": new_question,
                "user": user.get_json()
            })
        else:
            return abort(403, "Unable to authenticate user")

    except Exception as ex:
        print(ex)
        return abort(500, "Unable to retrieve random question, error: "+str(ex))


#########################################################################################
# DESCRIPTION
# When the user requests, returns a valid set of quest options
# to populate the quest selection screen
#
# RETURN CASES
# Error: if the user does not authenticate
# Error: if the user causes an internal server error
# On Success: Returns the user object and a new set of question parameters
#
# TAKES
# user authentication token string
#
# RETURNS
# json including user and valid quest parameters
#
#########################################################################################


@app.route('/api/v1/quests/get', methods=['POST'])
def get_quests():
    try:
        incoming_request = request
        print(incoming_request)
        # check authentication
        user = functions.authenticate_user(request)
        if user:
            response = functions.get_quest_options(user)
            return jsonify(response)
        else:
            return abort(403, "Unable to authenticate user")

    except Exception as ex:
        print(ex)
        return abort(500, "Unable to retrieve random question, error: " + str(ex))

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


# @app.route('/api/v1/quest/drop', methods=['POST'])
# def drop_quest():
#     try:
#         incoming_request = request
#         print(incoming_request)
#         # check authentication
#         user = authenticate_user(request)
#         if user:
#             # drop the current quest, note that update with no flags does this, check its default args for details
#             user = drop_user_quest(user)
#             user.update_current_user()
#             return jsonify(user.get_json())
#
#         else:
#             return abort(403, "Unable to authenticate user")
#
#     except Exception as ex:
#         print(ex)
#         return abort(500, "Unable to retrieve random question")


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
        user = functions.authenticate_user(request)
        if user:
            question_json = functions.start_next_question(user)
            return jsonify({
                'user': user.get_json(),
                'question': question_json
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

        user = functions.authenticate_user(request)
        if user:
            quest_complete = user.is_quest_complete()

            if quest_complete:
                return jsonify({
                    "user": user.get_json(),
                    "quest_complete": quest_complete
                })

            user_answer = (request.json['user_answer'])
            correct_answer = user.get_current_word_index()
            correct = user.check_answer(user_answer)

            functions.make_activity_log_entry(user, correct, request)
            user.update_quest_progress()
            user.handle_question_rewards(correct)
            quest_complete = user.is_quest_complete()

            if quest_complete:
                functions.make_quest_log_entry(user, request)
                user.handle_quest_rewards()
                question_json = None
                user.set_current_multiplier(1)
                user.update_current_user()

            else:
                question_json = functions.start_next_question(user)

            return jsonify({
                "user": user.get_json(),
                "correct": correct,
                "correct_answer": correct_answer,
                "user_answer": user_answer,
                "question": question_json,
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

        user_information = functions.check_access_token(request)
        if user_information:
            print(user_information)
            user_id = str(user_information['sub'])

            user = User.User().generate_from_id(user_id)
            if user:
                print('aborting')
                return abort(500, "Error: user already exists.")
            class_code = request.json['class_code']
            user_first_name = user_information['given_name']
            user_last_name = user_information['family_name']
            user_email = user_information['email']

            print('Creating new user account')
            user = User.User(user_id=user_id,
                             first_name=user_first_name,
                             last_name=user_last_name,
                             e_mail=user_email,
                             paid_through=datetime.datetime.today() + datetime.timedelta(days=365),
                             class_code=class_code
                             )
            new_user = user.save_new()

            if new_user:
                return jsonify({
                    'user': new_user.get_json(),
                    'user_exists': False,
                    'user_created': True
                })
            else:
                return jsonify({
                    'user_exists': False,
                    'user_created': False
                })
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
    if config.local:
        app.run(host='localhost', port=config.port)
        app.debug = True
    else:
        app.run(host=config.host, port=config.port)
        # this allows the API to use the public IP
