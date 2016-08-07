from rest_functions import *

from flask import Flask, jsonify, request, abort, send_from_directory

# TODO: update DefQuestion.DefinitionQuestion.make_from_chapter_index(user.get_chapter_index())
# TODO: make it whatever SRS library/algorithm zhen comes up with probably will require redo of DB but fuck it


# TODO: MAKE THESE ROUTES ACTUALLY THROW EXCEPTIONS THAT WORK
# TODO: make route that provides leaderboard with anonymous ids

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
        user = authenticate_user(request)
        if user:
            print(user)
            return jsonify({
                "user": user.get_json_min()
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
# is_timed boolean, cumulative boolean
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
        user = authenticate_user(request)
        if user:
            user.start_new_quest(request)
            new_question = user.start_new_question()
            user.save()

            return jsonify({
                "question": new_question.get_json_min(),
                "user": user.get_json_min()
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
        user = authenticate_user(request)
        if user:
            quest_options = get_quest_options()
            return jsonify({
                "user": user.get_json_min(),
                "quest_options": quest_options
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


@app.route('/api/v1/quest/drop', methods=['POST'])
def drop_quest():
    try:
        incoming_request = request
        print(incoming_request)
        # check authentication
        user = authenticate_user(request)
        if user:
            user.drop_user_quest()
            user.save()

            return jsonify({
                "user": user.get_json_min()
            })

        else:
            return abort(403, "Unable to authenticate user")

    except Exception as ex:
        print(ex)
        return abort(500, "Unable to drop quest.")


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
            new_question = user.start_new_question

            return jsonify({
                'user': user.get_json_min(),
                'question': new_question.get_json_min()
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
            quest_complete = (user.current_progress >= user.number_of_questions)

            if quest_complete:
                return jsonify({
                    "user": user.get_json_min(),
                    "quest_complete": True
                })

            user_answer = request.json['user_answer']
            correct_answer = user.current_word_index
            correct = (user_answer == correct_answer)

            if correct:
                user.award_question_points()

            make_activity_log_entry(user, correct, request)
            user.update_quest_progress()

            quest_complete = (user.current_progress >= user.number_of_questions)

            if quest_complete:
                quest_stats = {}
                make_quest_log_entry(user, request)
                user.award_daily_rewards()
                user.drop_user_quest()

                return jsonify({
                    "user": user.get_json_min(),
                    "feedback": {
                        "is_correct": correct,
                        "correct_answer": correct_answer,
                        "user_answer": user_answer
                    },
                    "quest_complete": quest_complete,
                    "quest_stats": quest_stats
                })

            else:
                new_question = user.start_new_question()

                return jsonify({
                    "user": user.get_json_min(),
                    "feedback": {
                        "is_correct": correct,
                        "correct_answer": correct_answer,
                        "user_answer": user_answer
                    },
                    "question": new_question.get_json_min(),
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


# @app.route('/api/v1/account/create', methods=['POST'])
# def create_account():
#     try:
#         incoming_request = request
#         print(incoming_request)
#
#         user_information = check_access_token(request)
#         if user_information:
#             print(user_information)
#             user_id = str(user_information['sub'])
#
#             user = User.User().generate_from_id(user_id)
#             if user:
#                 print('aborting')
#                 return abort(500, "Error: user already exists.")
#             class_code = request.json['class_code']
#             user_first_name = user_information['given_name']
#             user_last_name = user_information['family_name']
#             user_email = user_information['email']
#
#             print('Creating new user account')
#             user = User.create(user_id=user_id,
#                                first_name=user_first_name,
#                                last_name=user_last_name,
#                                e_mail=user_email,
#                                paid_through=datetime.datetime.today() + datetime.timedelta(days=365),
#                                class_code=class_code
#                                )
#             try:
#                 new_user = user.save_new()
#             except Exception as ex:
#                 return abort(500, "Error creating user.")
#
#             if new_user:
#                 return jsonify({
#                     'user': new_user.get_json(),
#                     'user_exists': False,
#                     'user_created': True
#                 })
#
#     except Exception as ex:
#         print(ex)
#         print('Invalid token')
#         return abort(500, "Error: " + str(ex))

#########################################################################################
# DESCRIPTION
#
#
# RETURN CASES
#
#
#
#
# TAKES
#
#
# RETURNS
#
#########################################################################################


@app.route('/api/v1/rewards/get', methods=['POST'])
def get_rewards():
    try:
        print(request.json)

        user = authenticate_user(request)
        if user:
            rewards = get_rewards(user)
            return jsonify({
                'rewards': rewards
            })
        else:
            return abort(403, "Unable to authenticate user")

    except Exception as exception:
        print(exception)
        print('Invalid token')
        return abort(500, "Error: " + str(exception))

#########################################################################################
# DESCRIPTION
#
#
# RETURN CASES
#
#
#
#
# TAKES
#
#
# RETURNS
#
#########################################################################################


@app.route('/api/v1/daily/get', methods=['POST'])
def get_daily():
    try:
        print(request.json)

        user = authenticate_user(request)
        if user:
            daily_info = get_daily_info(user)

            return jsonify({
                'daily_status': daily_info
            })
        else:
            return abort(403, "Unable to authenticate user")

    except Exception as exception:
        print(exception)
        print('Invalid token')
        return abort(500, "Error: " + str(exception))

#########################################################################################
# DESCRIPTION
#
#
# RETURN CASES
#
#
#
#
# TAKES
#
#
# RETURNS
#
#########################################################################################


@app.route('/api/v1/leaderboard/get', methods=['POST'])
def get_leaderboard():
    try:
        print(request.json)

        user = authenticate_user(request)
        if user:

            return jsonify({
                'leaderboard': 'this is supposed to be a leaderboard'
            })
        else:
            return abort(403, "Unable to authenticate user")

    except Exception as exception:
        print(exception)
        print('Invalid token')
        return abort(500, "Error: " + str(exception))

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
