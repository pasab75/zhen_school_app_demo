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

# -------------------------------------------------------------
# Functions
# -------------------------------------------------------------


def check_access_token(client_request):
    try:
        g.dbconnect_user = users_table_access_layer.UserTableAccess()
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

# -------------------------------------------------------------
# Routes
# -------------------------------------------------------------


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
            dbconnect.close_connection()

            return json.dumps(current_dailies)
        else:
            abort(403, "Unable to authenticate user")
    except Exception as ex:
        print(ex)
        print("Unable to retrieve user.")


@app.route('/api/v1/start/quest', methods=['POST'])
def start_quest():
    try:
        incoming_request = request
        print(incoming_request)

        # check authentication
        authentication_response = authenticate_user(request)
        if authentication_response['is_paid']:
            user_id = authentication_response['user_id']

            # get rid of whatever they have already just in case they have a quest
            dbconnect = users_table_access_layer.UserTableAccess()
            dbconnect.null_user_quest(user_id)
            # get current user from table
            user = dbconnect.get_user_by_user_id(user_id)
            dbconnect.close_connection()

            user_input_quest = request.json['quest_index']
            dbconnect = users_table_access_layer.UserTableAccess()
            dbconnect.set_user_quest_by_user_id(user_id, user_input_quest)
            dbconnect.close_connection()

            dbconnect = quest_table_access_layer.QuestTableAccess()
            quest = dbconnect.get_quest_by_quest_index(user_input_quest)
            dbconnect.close_connection()


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
            if quest['chapter_index']:
                question = dbconnect.get_question_random_by_type_and_chapter(question_type, quest['chapter_index'])
            elif quest['topic_index']:
                question = dbconnect.get_question_random_by_type_and_topic(question_type, quest['topic_index'])
            else:
                question = {'error': 'Something bad has occurred.'}

            dbconnect.close_connection()

            dbconnect = users_table_access_layer.UserTableAccess()
            dbconnect.update_user_current_question(user_id, question['question_id'])
            dbconnect.close_connection()

            return jsonify(question)

        else:
            abort(403, "Unable to authenticate user")

    except Exception as ex:
        print(ex)
        abort(500, "Unable to retrieve random question")


@app.route('/api/v1/stop/quest', methods=['POST'])
def stop_quest():
    try:
        incoming_request = request
        print(incoming_request)

        # check authentication
        authentication_response = authenticate_user(request)
        if authentication_response['is_paid']:
            user_id = authentication_response['user_id']

            # initiate connection to user table
            dbconnect = users_table_access_layer.UserTableAccess()
            dbconnect.null_user_quest(user_id)
            dbconnect.close_connection()

            dbconnect = quest_table_access_layer.QuestTableAccess()
            current_dailies = dbconnect.get_daily_quests_by_chapter(3)
            dbconnect.close_connection()

            return json.dumps(current_dailies)

        else:
            abort(403, "Unable to authenticate user")

    except Exception as ex:
        print(ex)
        abort(500, "Unable to retrieve random question")


@app.route('/api/v1/resume/quest', methods=['POST'])
def resume_quest():
    try:
        incoming_request = request
        print(incoming_request)

        # check authentication
        authentication_response = authenticate_user(request)
        if authentication_response['is_paid']:
            user_id = authentication_response['user_id']
            print(type(user_id))

            # initiate connection to user table
            dbconnect = users_table_access_layer.UserTableAccess()

            # get current user from table
            user = dbconnect.get_user_by_user_id(user_id)
            dbconnect.close_connection()

            daily_reset = datetime.datetime.today().replace(hour=4, second=0, minute=0, microsecond=0)
            # check if that quest is valid
            if user['date_quest_started'] > daily_reset:
                dbconnect = questions_table_access_layer.QuestionTableAccess()
                question = dbconnect.get_question_by_question_id(user['current_question_id'])
                dbconnect.close_connection()

                return jsonify(question)
            else:
                print('quest is outdated, please start a new quest')

        else:
            user_input_quest = request.json['quest_index']
            dbconnect = users_table_access_layer.UserTableAccess()
            dbconnect.set_user_quest_by_user_id(user_id, user_input_quest)
            dbconnect.close_connection()

            dbconnect = quest_table_access_layer.QuestTableAccess()
            quest = dbconnect.get_quest_by_quest_index(user_input_quest)
            dbconnect.close_connection()


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
            if quest['chapter_index']:
                result = dbconnect.get_question_random_by_type_and_chapter(question_type, quest['chapter_index'])
            elif quest['topic_index']:
                result = dbconnect.get_question_random_by_type_and_topic(question_type, quest['topic_index'])
            else:
                result = {'error': 'Something bad has occurred.'}

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

        dbconnect = users_table_access_layer.UserTableAccess()
        exists = dbconnect.check_if_user_valid(str(user_id))

        if exists:
            dbconnect.close_connection()
            print('user already exists')
            return jsonify(user_exists='true')
        else:
            print('user does not exist')
            new_user = user_obj_generator.user(user_id=user_id,
                                               first_name='derpington',
                                               last_name='derpserson',
                                               e_mail=user_email,
                                               paid_through=datetime.datetime.today() + datetime.timedelta(days=365)
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

# -------------------------------------------------------------
# Professor client routes
# -------------------------------------------------------------
# TODO: add professor routes for changing the question database etc

# gets a multiple choice question by question ID
# takes the question ID (qID) as data from the client
# returns JSON that includes question text and answer text


@app.route('/api/v1/get/question/<question>', methods=['POST'])
def get_question_by_question_id():
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
