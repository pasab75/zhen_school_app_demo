from flask import Flask, jsonify, request, abort
import datetime

import business_objects.User as User
import business_objects.DefinitionQuestion as DefQuestion
import requests

###DEBUG IMPORTS###


###END DEBUG IMPORTS###

#TODO: update DefQuestion.DefinitionQuestion.make_from_chapter_index(user.get_chapter_index())
#TODO: make it whatever SRS library/algorithm zhen comes up with probably will require redo of DB but fuck it

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
            user.update_current_user()
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
            user.update_current_user()
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
            new_question = DefQuestion.DefinitionQuestion.make_from_chapter_index(user.get_chapter_index())
            response = new_question.jsonify()
            user.set_datetime_question_started(datetime.datetime.now())
            user.update_current_user()
            return jsonify({
                "question": response,
                "user": user.jsonify()
            })
        else:
            abort(403, "Unable to authenticate user")

    except Exception as ex:
        print(ex)
        abort(500, "Unable to retrieve random question")


# returns the correct answer for the user's current question
# request requires
# user_identifier = user's access token
# user_answer = either the index or the value of the user's answer
@app.route('/api/v1/question/submit', methods=['POST'])
def submit_question():
    try:
        # TODO:  the user has the word indexs of all possibilities, just return the
        # TODO CONTINUED: a new question for them and update the user object
        print(request.json)

        user = authenticate_user(request)
        if user:
            user_answer = (request.json['user_answer'])
            correct = user.check_answer(user_answer)
            answer_index = user.get_current_word_index()
            quest_complete = user.is_quest_complete()
            if not quest_complete:
                question = DefQuestion.DefinitionQuestion.make_from_chapter_index(user.get_chapter_index()).jsonify()
            else:
                question = None
            user.update_current_user()
            return jsonify({
                "user": user.jsonify(),
                "correct": correct,
                "answer_index": answer_index,
                "question": question,
                "quest_complete": quest_complete
            })
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
