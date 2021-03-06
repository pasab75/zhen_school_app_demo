from rest_functions import *
from config import *

from flask import Flask, jsonify, request, abort, send_from_directory, _request_ctx_stack

import jwt
import base64
from functools import wraps
from werkzeug.local import LocalProxy

# TODO: MAKE THESE ROUTES ACTUALLY THROW EXCEPTIONS THAT WORK
# TODO: change from if-then to try-catch we are inconsistent

app = Flask(__name__, static_url_path='/')


# Authentication annotation
current_user = LocalProxy(lambda: _request_ctx_stack.top.current_user)


# Authentication attribute/annotation
def authenticate(error):
    resp = jsonify(error)

    resp.status_code = 401

    return resp


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.headers.get('Authorization', None)
        if not auth:
            return authenticate({'code': 'authorization_header_missing', 'description': 'Authorization header is expected'})

        parts = auth.split()

        if parts[0].lower() != 'bearer':
            return {'code': 'invalid_header', 'description': 'Authorization header must start with Bearer'}
        elif len(parts) == 1:
            return {'code': 'invalid_header', 'description': 'Token not found'}
        elif len(parts) > 2:
            return {'code': 'invalid_header', 'description': 'Authorization header must be Bearer + \s + token'}

        token = parts[1]
        try:
            payload = jwt.decode(
                token,
                base64.b64decode('Ruhcmld2nOTwFL4u_NZgUd8Dzj-LhZVEw5o4deIqcy7O_A6LQ4jJhtvKgy6jauN4'.replace("_","/").replace("-","+")),
                audience='p0YHk3HYjJP7HjleA1zwvNS9xCb5WfIw',
                options={'verify_iat': False}
            )
        except jwt.ExpiredSignature:
            return authenticate({'code': 'token_expired', 'description': 'token is expired'})
        except jwt.InvalidAudienceError:
            return authenticate({'code': 'invalid_audience', 'description': 'incorrect audience, expected: p0YHk3HYjJP7HjleA1zwvNS9xCb5WfIw'})
        except jwt.DecodeError:
            return authenticate({'code': 'token_invalid_signature', 'description': 'token signature is invalid'})

        _request_ctx_stack.top.current_user = payload
        return f(*args, **kwargs)

    return decorated


@app.before_request
def before_request():
    print('Request Incoming')


@app.after_request
def after_request(response):
    # TODO: check to see if this CORS implementation is safe
    # TODO: Mobile may not need CORS here - check to see if it is okay without it
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response

# -------------------------------------------------------------
# Routes
# -------------------------------------------------------------


@app.route('/', methods=['GET'])
def route_hello_world():
    try:
        print(request.json)
        return send_from_directory('', "index.html")
    except Exception as ex:
        print(ex)
        print("Unable to retrieve user.")
        return abort(500, "Unable to retrieve user. Error: " + str(ex))


@app.route('/<path:path>', methods=['GET'])
def route_static_file(path):
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


@app.route('/api/v1/status/get', methods=['POST'])
@requires_auth
def route_get_status():
    try:
        print(request.json)
        user = authenticate_user(request)
        try:
            daily_info = get_daily_info(user)
            rewards = get_rewards(user)
            quest_options = get_quest_options()

            return jsonify({
                "user": user.get_json_min(),
                "daily_status": daily_info,
                'rewards': rewards,
                "quest_options": quest_options
            })
        except Exception as ex:
            print("Unable to get parameters for user's classroom: " + str(ex))
            return abort(500, "Unable to get current server information.")
    except Exception as ex:
        print("Unable to retrieve user:" + str(ex))
        return abort(500, "Unable to authenticate user.")

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
def route_start_quest():
    try:
        incoming_request = request
        print(incoming_request)
        # check authentication
        user = authenticate_user(request)
        if user:
            user_classroom = Classroom.get(Classroom.class_code == user.class_code)
            user.start_new_quest(request, user_classroom)
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
def route_get_quests():
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
def route_drop_quest():
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
def route_resume_quest():
    try:
        incoming_request = request
        print(incoming_request)

        # check authentication
        user = authenticate_user(request)
        if user:
            new_question = user.start_new_question()
            user.save()

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
def route_submit_question():
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

            user_classroom = Classroom.get(Classroom.class_code == user.class_code)

            user_answer = request.json['user_answer']
            correct_answer = user.current_word_index
            correct = (user_answer == correct_answer)

            if correct:
                user.award_question_points(user_classroom)
            else:
                user.multiplier = 1

            make_activity_log_entry(user, correct, request)
            user.update_quest_progress()

            quest_complete = (user.current_progress >= user.number_of_questions)

            if quest_complete:
                user_performance = user.calculate_user_performance()
                make_quest_log_entry(user, request)
                if user.is_on_daily and user.is_eligible_for_daily(user_classroom):
                    user.award_daily_rewards(user_classroom)
                user.drop_user_quest()
                user.save()

                return jsonify({
                    "user": user.get_json_min(),
                    "feedback": {
                        "is_correct": correct,
                        "correct_answer": correct_answer,
                        "user_answer": user_answer
                    },
                    "quest_complete": quest_complete,
                    "user_performance": user_performance
                })

            else:
                new_question = user.start_new_question()
                user.save()

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
        return abort(500, "Unable to get question")

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
def route_create_account():
    try:
        incoming_request = request
        print(incoming_request)

        user_information = get_token_info(request)
        if user_information:
            print(user_information)
            user_id = str(user_information['identities'][0]['user_id'])

            if User.select().where(User.user_id == user_id).count():
                print('aborting')
                return abort(500, "Error: user already exists.")
            class_code = request.json['class_code']
            user_first_name = user_information['given_name']
            user_last_name = user_information['family_name']
            user_email = user_information['email']

            print('Creating new user account')
            new_user = User.create(
                user_id=user_id,
                first_name=user_first_name,
                last_name=user_last_name,
                e_mail=user_email,
                class_code=class_code
            )

            if new_user:
                return jsonify({
                    'user': new_user.get_json_min()
                })

    except Exception as ex:
        print(ex)
        print('Invalid token')
        return abort(500, "Error: " + str(ex))

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
def route_get_daily():
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
def route_get_leaderboard():
    try:
        print(request.json)

        user = authenticate_user(request)
        if user:
            leaderboard = get_leader_board(user)
            return jsonify({
                'leaderboard': leaderboard
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



if __name__ == '__main__':
    if server_local:
        app.run(host='localhost', port=server_port)
        app.debug = True
    else:
        app.run(host=server_host, port=server_port)
        # this allows the API to use the public IP
