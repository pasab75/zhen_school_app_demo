from flask import Flask, jsonify, request, abort, json, g
import datetime
import db_access.db_question as questions_table_access_layer
import db_access.db_user as users_table_access_layer
import db_access.db_quest as quest_table_access_layer
import db_access.db_topic_chapter as topic_chapter_table_access_layer
import business_objects.user as user_obj_generator
import requests
import random


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


def authenticate_user(client_request):
    try:
        g.dbconnect_user = users_table_access_layer.UserTableAccess()
        token = client_request.json['user_identifier']
        r = requests.get('https://www.googleapis.com/oauth2/v3/tokeninfo?access_token=' + token)
        user_id = str(r.json()['sub'])
        print(user_id)
        exists = g.dbconnect_user.check_if_user_valid(user_id)
        if exists:
            is_paid = g.dbconnect_user.check_if_user_paid(user_id)
            return {'is_paid': is_paid, 'user_id': user_id}
        else:
            return False
    except Exception as ex:
        print(ex)


@app.route('/')
def index():
    return 'Hello, World!'


@app.route('/api/v1/database/initialize', methods=['POST'])
def database_init():
    try:
        dbconnect = topic_chapter_table_access_layer.TopicChapterTableAccess()
        dbconnect.empty_table('topic_chapter')
        dbconnect.add_dummy_topics(100)
        dbconnect.close_connection()

        dbconnect = quest_table_access_layer.QuestTableAccess()
        dbconnect.empty_table('quests')
        dbconnect.add_dummy_quests(100)
        dbconnect.close_connection()

        dbconnect = questions_table_access_layer.QuestionTableAccess()
        dbconnect.empty_table('questions')
        dbconnect.load_questions_testing(5000)

        dbconnect.close_connection()
        response_text = {'response': 'all good'}
        return jsonify(response_text)

    except Exception as ex:
        print(ex)
        abort(500, "Unable to add questions to DB")


@app.route('/api/v1/get/user', methods=['POST'])
def get_user_state():
    try:
        authentication_response = authenticate_user(request)
        if authentication_response['is_paid']:
            dbconnect = users_table_access_layer.UserTableAccess()

            print(authentication_response['user_id'])

            current_user = dbconnect.get_user_by_user_id(authentication_response['user_id'])
            dbconnect.close_connection()

            current_user.pop('user_id')
            current_user.pop('paid_through')

            print(current_user)

            return json.dumps(current_user)
        else:
            abort(403, "Unable to authenticate user")
    except Exception as ex:
        print(ex)
        print("Unable to retrieve user.")


@app.route('/api/v1/get/quests/daily', methods=['POST'])
def get_quests_daily():
    try:
        authentication_response = authenticate_user(request)
        if authentication_response['is_paid']:
            dbconnect = quest_table_access_layer.QuestTableAccess()

            current_dailies = dbconnect.get_daily_quests_by_chapter(3)

            return json.dumps(current_dailies)
        else:
            abort(403, "Unable to authenticate user")
    except Exception as ex:
        print(ex)
        print("Unable to retrieve user.")


@app.route('/api/v1/get/question/by/quest', methods=['POST'])
def get_question_by_quest():
    try:
        incoming_request = request
        print(incoming_request)

        authentication_response = authenticate_user(request)
        if authentication_response['is_paid']:
            # init variable names
            user_id = authentication_response['user_id']
            # quest_index = (request.json['quest_index'])
            print("User has chosen quest index: " + quest_index)

            # get quest from user table if user is already on quest

            dbconnect = users_table_access_layer.UserTableAccess()
            user = dbconnect.get_user_quest_by_user_id(user_id)
            quest_index = user['quest_index']

            # if user is already on a quest, get it from table according to quest index

            if quest_index:
                dbconnect = quest_table_access_layer.QuestTableAccess()
                quest = dbconnect.get_quest_by_quest_index(quest_index)
                dbconnect.close_connection()

            # check to make sure the quest is a currently daily
            # make sure quest is not expired (from yesterday or something)
            # they can resume only on the same day if it's a daily quest
            # TODO: timestamp the quest when the user gets put on the quest
            # we can save an extra database call this way

            if int(quest['daily']) == 0:
                print('go fuck yourself')
                return False

            if quest['chapter_index']:
                chapter = quest['chapter_index']
            elif quest['topic_index']:
                topic = quest['topic_index']
            else:
                return False

            # set user on quest in user table
            # sets user current progress to 0

            dbconnect = users_table_access_layer.UserTableAccess()
            dbconnect.set_user_quest_by_user_id(user_id, quest_index)
            dbconnect.close_connection()

            # choose a question based on the activity guidelines

            # TODO make a question function to get by quest!
            allowed_types = []

            if int(quest['type_0_allowed']) == 1:
                allowed_types.append(0)
            if int(quest['type_1_allowed']) == 1:
                allowed_types.append(1)
            if int(quest['type_2_allowed']) == 1:
                allowed_types.append(2)

            question_type = random.choice(allowed_types)

            dbconnect = questions_table_access_layer.QuestionTableAccess()
            if chapter:
                result = dbconnect.get_question_random_by_type_and_chapter(question_type, chapter)
            elif topic:
                result = dbconnect.get_question_random_by_type_and_topic(question_type, topic)
            else:
                result = {'error': 'Something bad has occured.'}

            dbconnect.close_connection()

            return jsonify(result)
        else:
            abort(403, "Unable to authenticate user")

    except Exception as ex:
        print(ex)
        abort(500, "Unable to retrieve random question")


@app.route('/api/v1/get/validation', methods=['POST'])
def get_validation():
    try:
        authentication_response = authenticate_user(request)
        if authentication_response['is_paid']:
            user_id = authentication_response['user_id']
            incoming_request = request
            print(incoming_request)
            user_answer = (request.json['user_answer'])
            print("User has chosen quest index: " + quest_index)

            # get question index of current question
            dbconnect = users_table_access_layer.UserTableAccess()
            question_id = dbconnect.get_user_current_question_id_by_user_id(user_id)
            dbconnect.close_connection()

            # get question with current question index

            dbconnect = questions_table_access_layer.QuestionTableAccess()
            question = dbconnect.get_question_by_question_id(question_id)
            correct_answer = question.get_correct_answer_index()
            dbconnect.close_connection()

            # check if this is the last question of the set

            if user_answer == correct_answer:
                print('do the things')
                # update points
                # increase multiplier
            else:
                print('do the other things')
                # decrease multiplier

            validation_package = {}

            return validation_package
        else:
            abort(403, "Unable to authenticate user")

    except Exception as ex:
        print(ex)
        abort(500, "Unable to retrieve random question")


@app.route('/api/v1/tokensignin', methods=['POST'])
def sign_in():
    try:
        token = request.json['user_identifier']
        r = requests.get('https://www.googleapis.com/oauth2/v3/tokeninfo?access_token=' + token)
        dbconnect = users_table_access_layer.UserTableAccess()
        exists = dbconnect.check_if_user_valid(str(r.json()['sub']))

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


@app.route('/api/v1/get/next/prompt/by/student', methods=['POST'])
def get_next_prompt_by_student():
    try:
        exists = authenticate_user(request)
        if exists:
            user_id = (request.json['user_id'])
            print("user id = " + str(user_id))
            return jsonify(response_type='derpderp')
        else:
            abort(403, "Unable to authenticate user")
    except Exception as ex:
        print(ex)
        print("Unable to retrieve activity list.")


@app.route('/api/v1/paidsignin', methods=['POST'])
def paid_sign_in():
    try:
        auth = authenticate_user(request)
        return jsonify(user_paid=auth)

    except Exception as ex:
        print(ex)
        print('Invalid token')
        abort(500, "Unable to retrieve random question")


@app.route('/api/v1/add/dummy/questions', methods=['POST'])
def add_random():
    try:
        incoming_request = request
        print(incoming_request)
        dbconnect = questions_table_access_layer.QuestionTableAccess()
        dbconnect.empty_table('questions')
        dbconnect.load_questions_testing(10000)

        dbconnect.close_connection()
        return "false"

    except Exception as ex:
        print(ex)
        abort(500, "Unable to add questions to DB")


# -------------------------------------------------------------
# Student client routes
# -------------------------------------------------------------


@app.route('/api/v1/get/activity/daily', methods=['POST'])
def get_activity_daily():
    try:
        exists = authenticate_user(request)
        if exists:
            dbconnect = quest_table_access_layer.QuestTableAccess()
            current_chapter = 3 # change this to get the current chapter OR topic

            dailies = dbconnect.get_daily_quests_by_chapter(current_chapter)
            dbconnect.close_connection()
            print(type(dailies))
            return json.dumps(dailies)
        else:
            abort(403, "Unable to authenticate user")
    except Exception as ex:
        print(ex)
        print("Unable to retrieve activity list.")


@app.route('/api/v1/set/activity', methods=['POST'])
def set_activity():
    try:
        authentication_response = authenticate_user(request)
        if authentication_response['is_paid']:
            dbconnect = users_table_access_layer.UserTableAccess()

            dbconnect.update_user_activity(authentication_response['user_id'], request['activity_index'])
            dbconnect.close_connection()

            dbconnect = questions_table_access_layer.QuestionTableAccess()

            return json.dumps(dailies)
        else:
            abort(403, "Unable to authenticate user")
    except Exception as ex:
        print(ex)
        print("Unable to retrieve activity list.")


@app.route('/api/v1/get/activity/list', methods=['POST'])
def get_activity_list():
    try:
        authentication_response = authenticate_user(request)
        if authentication_response['is_paid']:
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
        authentication_response = authenticate_user(request)
        if authentication_response['is_paid']:
        # save activity index in (user)? database?
            return True
        else:
            abort(403, "Unable to authenticate user")
    except Exception as ex:
        print(ex)
        print("Unable to save activity.")


@app.route('/api/vi/set/activity/<chapter>/<topic>/<question_type>', methods=['POST'])
def set_activity_by_options():
    return True


@app.route('/api/v1/get/question/next/by/activity', methods=['POST'])
def get_question_next_by_activity():
    try:
        authentication_response = authenticate_user(request)
        if authentication_response['is_paid']:
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
        authentication_response = authenticate_user(request)
        if authentication_response['is_paid']:
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
        authentication_response = authenticate_user(request)
        if authentication_response['is_paid']:
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
        authentication_response = authenticate_user(request)
        if authentication_response['is_paid']:
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
