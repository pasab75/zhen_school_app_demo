from flask import Flask, jsonify, request, abort, send_from_directory
import datetime
import requests

import config as config
import rest_functions as functions

import business_objects.ActivityLogEntry as ActivityLogEntry
import business_objects.Chapter as Chapter
import business_objects.DefinitionQuestion as DefQuestion
import business_objects.QuestLogEntry as QuestLogEntry
import business_objects.User as User

# TODO: update DefQuestion.DefinitionQuestion.make_from_chapter_index(user.get_chapter_index())
# TODO: make it whatever SRS library/algorithm zhen comes up with probably will require redo of DB but fuck it

app = Flask(__name__, static_url_path='/')
STATIC_FOLDER = "angular-frontend"

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
        print(ex)
        print("Unable to retrieve user.")
        return abort(500, "Unable to retrieve user. Error: "+str(ex))


@app.route('/', methods=['GET'])
def helloworld():
    try:
        print(request)
        return send_from_directory(STATIC_FOLDER, "index.html")

    except Exception as ex:
        print(ex)
        print("Unable to retrieve user.")
        return abort(500, "Unable to retrieve user. Error: " + str(ex))


@app.route('/<path:path>', methods=['GET'])
def static_file(path):
    return send_from_directory(STATIC_FOLDER, path)
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
        user = functions.authenticate_user(request)
        if user:
            request_chapter_index = json_obj['chapter_index']
            request_seconds_per_question = json_obj['seconds_per_question']
            request_number_of_questions = json_obj['number_of_questions']
            request_cumulative = json_obj['cumulative']

            response = functions.update_user_quest(
                user,
                chapter_index=request_chapter_index,
                seconds_per_question=request_seconds_per_question,
                number_of_questions=request_number_of_questions,
                cumulative=request_cumulative
            )

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
def get_chapters():
    try:
        incoming_request = request
        print(incoming_request)
        # check authentication
        user = functions.authenticate_user(request)
        chapter_list = []
        if user:
            total_chapters = Chapter.Chapter().get_number_chapters()
            for index in range(1, total_chapters+1):
                new_chapter = Chapter.Chapter()
                new_chapter.get_chapter_by_index(index)
                chapter_list.append(new_chapter.get_json())
            return jsonify({
                'user': user.get_json(),
                'chapters': chapter_list,
                'time_limits': [0, 5, 10, 30],
                'number_of_questions': config.number_of_question_choices
            })
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

        user = functions.authenticate_user(request)
        if user:
            quest_complete = user.is_quest_complete()

            if quest_complete:
                return jsonify({
                    "user": user.get_json(),
                    "quest_complete": quest_complete
                })

            user_answer = (request.json['user_answer'])
            answer_index = user.get_current_word_index()

            correct = user.check_answer(user_answer)

            new_activity = ActivityLogEntry.ActivityLogEntry().generate_from_user(user, correct)
            new_activity.save_new()

            user.update_quest_progress()
            user.update_multiplier(correct)

            if correct:
                user.give_question_rewards()

            quest_complete = user.is_quest_complete()

            if quest_complete:
                user.give_quest_rewards()
                question_json = None
                user.set_current_multiplier(1)
                try:
                    # TODO: add Lat and Lon
                    new_quest_entry = QuestLogEntry.QuestLogEntry().generate_from_user(user)
                    new_quest_entry.save_new()
                except Exception as ex:
                    print(ex)
                    print("failed too make log entry, not the end of the world, but no log entry made")
            else:
                current_chapter = user.get_chapter_index()
                question = DefQuestion.DefinitionQuestion().make_from_chapter_index(current_chapter)
                user.start_new_question(question.get_index())
                question_json = question.get_json()
            user.update_current_user()
            return jsonify({
                "user": user.get_json(),
                "correct": correct,
                "correct_answer": answer_index,
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
    if config.local:
        app.run(host='0.0.0.0', port=5000)
        app.debug = True
    else:
        app.run(host='0.0.0.0', port=5000)
        # this allows the API to use the public IP