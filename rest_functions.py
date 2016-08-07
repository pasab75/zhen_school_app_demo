from oauth2client import client, crypt
from user_agents import parse
from flask import abort

from business_objects.DefinitionQuestion import DefinitionQuestion as DefinitionQuestion
from business_objects.Models import Classroom as Classroom
from business_objects.Models import User as User
from business_objects.Models import Chapter as Chapter
from business_objects.Models import Reward as Reward
from business_objects.Models import QuestLogEntry as QuestLogEntry
from business_objects.Models import ActivityLogEntry as ActivityLogEntry

import config as config

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
        idinfo = client.verify_id_token(token, config.WEB_CLIENT_ID)
        # If multiple clients access the backend server:
        if idinfo['aud'] not in [config.ANDROID_CLIENT_ID, config.IOS_CLIENT_ID, config.WEB_CLIENT_ID]:
            raise crypt.AppIdentityError("Unrecognized client.")
        if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
            raise crypt.AppIdentityError("Wrong issuer.")
        return idinfo

    except crypt.AppIdentityError as ex:
        print(ex)


def authenticate_user(client_request):
    try:
        user_information = check_access_token(client_request)
        if user_information:
            # print(user_information)
            user_id = str(user_information['sub'])
            user = User.get(User.user_id == user_id)
            if user:
                return user
            else:
                print('Failed to authenticate user')
                return False
    except Exception as ex:
        print(ex)
        raise Exception("Failed to authenticate user")

#########################################################################################
# DESCRIPTION
#
#
# RETURN CASES
#
#
# TAKES
#
#
# RETURNS
#
#########################################################################################


def update_quest_with_client_choices(user, request):
    client_choices = request.json
    request_chapter_index = client_choices['chapter_index']
    request_is_timed = client_choices['is_timed']
    request_number_of_questions = client_choices['number_of_questions']
    request_cumulative = client_choices['cumulative']
    request_question_type = client_choices['question_type']
    request_is_daily = client_choices['is_daily']

    new_question = update_user_quest(
        user,
        chapter_index=request_chapter_index,
        is_timed=request_is_timed,
        number_of_questions=request_number_of_questions,
        cumulative=request_cumulative,
        question_type=request_question_type,
        is_daily=request_is_daily
    )

    make_quest_log_entry(user, request)

    return new_question

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
# cumulative (boolean) - whether or not you should include chapters before the given chapter index
# RETURNS
# question json
#########################################################################################


def update_user_quest(
        user,
        chapter_index=None,
        is_timed=None,
        number_of_questions=None,
        cumulative=False,
        question_type=None,
        is_daily=None
):
    try:
        class_code = user.class_code
        number_correct = 0
        current_progress = 0
        points_per_question = 10

        valid_num_questions = config.number_of_question_options
        valid_bool = [True, False]

        if is_daily:
            current_class = Classroom.get(Classroom.class_code == class_code)
            chapter_index = current_class.chapter_index

            is_timed = True
            number_of_questions = 50
            cumulative = True
            question_type = 3

        if number_of_questions not in valid_num_questions or is_timed not in valid_bool or cumulative not in valid_bool:
            return abort(500, "You have chosen invalid quest options.")

        if is_timed:
            points_per_question += 3

        if cumulative:
            points_per_question += 1*(chapter_index-1)

        completion_points = 20 * number_of_questions

        new_question = DefinitionQuestion()
        new_question.make_from_chapter_index(
            chapter_index=chapter_index,
            cumulative=cumulative,
            question_type=question_type
        )

        user.chapter_index = chapter_index
        user.current_progress = current_progress
        user.current_word_index = new_question.get_word_index()
        user.number_correct = number_correct
        user.completion_points = completion_points
        user.is_timed = is_timed
        user.points_per_question = points_per_question
        user.number_of_questions = number_of_questions
        user.cumulative = cumulative
        user.question_type = question_type
        user.is_on_daily = is_daily

        user.save()

        return new_question.get_json()

    except Exception as ex:
        # TODO: change prints to logger
        print("Error: " + str(ex))
        raise ex

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

#########################################################################################
# DESCRIPTION
#
#
# RETURN CASES
#
#
# TAKES
#
#
# RETURNS
#
#########################################################################################


def get_quest_options(user):
    chapter_list = []
    for chapter in Chapter.select():
        chapter_list.append(chapter.get_json_min())
    return {
        'user': user.get_json_min(),
        'quest_options': {
            'chapter_options': chapter_list,
            'number_of_questions_options': config.number_of_question_options
        }
    }

#########################################################################################
# DESCRIPTION
#
#
# RETURN CASES
#
#
# TAKES
#
#
# RETURNS
#
#########################################################################################


def start_next_question(user):
    new_question = DefinitionQuestion()
    new_question.make_from_chapter_index(
        chapter_index=user.chapter_index,
        cumulative=user.cumulative,
        question_type=user.question_type
    )

    question_json = new_question.get_json()
    # TODO: These no longer do anything, make them do something
    # user.start_new_question(new_question.get_word_index())
    # user.update_current_user()
    return question_json

#########################################################################################
# DESCRIPTION
#
#
# RETURN CASES
#
#
# TAKES
#
#
# RETURNS
#
#########################################################################################

# TODO: add activity log method in activity log object
def make_activity_log_entry(user, correct, request):
    try:
        ip_address = request.remote_addr
        user_agent = parse(request.user_agent.string)
        new_activity = ActivityLogEntry.generate_from_user(user, correct, ip_address, user_agent)
        new_activity.save_new()
    except Exception as ex:
        print(ex)
        print("failed too make activity log entry, not the end of the world, but no log entry made")

#########################################################################################
# DESCRIPTION
#
#
# RETURN CASES
#
#
# TAKES
#
#
# RETURNS
#
#########################################################################################

# TODO: add quest log method in quest log object
def make_quest_log_entry(user, request):
    try:
        ip_address = request.remote_addr
        user_agent = parse(request.user_agent.string)
        # TODO: add Lat and Lon
        new_quest_entry = QuestLogEntry.generate_from_user(user, ip_address, user_agent)
        new_quest_entry.save_new()
    except Exception as ex:
        print(ex)
        print("failed too make quest log entry, not the end of the world, but no log entry made")

#########################################################################################
# DESCRIPTION
#
#
# RETURN CASES
#
#
# TAKES
#
#
# RETURNS
#
#########################################################################################


def get_rewards(user):
    class_code = user.class_code
    raw_rewards = Reward.select().where(Reward.class_code == class_code)
    reward_list = []
    for reward in raw_rewards:
        reward_list.append(reward.get_json_min())

    return reward_list

#########################################################################################
# DESCRIPTION
#
#
# RETURN CASES
#
#
# TAKES
#
#
# RETURNS
#
#########################################################################################


def get_daily_info(user):
    class_code = user.class_code
    classroom = Classroom.get(Classroom.class_code == class_code)
    dailies_complete = QuestLogEntry.select().where(QuestLogEntry.is_daily == True).count()
    dailies_allowed = classroom.number_dailies_allowed
    current_chapter = classroom.current_chapter.chapter_index
    return {
        'dailies_complete': dailies_complete,
        'dailies_allowed': dailies_allowed,
        'daily_chapter': current_chapter
    }

