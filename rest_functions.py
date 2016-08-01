from oauth2client import client, crypt
from user_agents import parse

import business_objects.User as User
import business_objects.DefinitionQuestion as DefQuestion
import business_objects.Chapter as Chapter
import business_objects.ActivityLogEntry as ActivityLogEntry
import business_objects.QuestLogEntry as QuestLogEntry

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
            user = User.User().generate_from_id(user_id)
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
    request_seconds_per_question = client_choices['seconds_per_question']
    request_number_of_questions = client_choices['number_of_questions']
    request_cumulative = client_choices['cumulative']

    new_question = update_user_quest(
        user,
        chapter_index=request_chapter_index,
        seconds_per_question=request_seconds_per_question,
        number_of_questions=request_number_of_questions,
        cumulative=request_cumulative
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
        number_correct = 0
        current_progress = 0
        points_per_question = 20
        question_multiplier = 5

        completion_points = 50*number_of_questions

        valid_num_questions = config.number_of_question_options
        valid_secs_per_question = config.seconds_per_question_options
        valid_secs_per_question.append(0)
        valid_bool = [True, False]

        if number_of_questions not in valid_num_questions or seconds_per_question not in valid_secs_per_question or cumulative not in valid_bool:
            return False

        valid_secs_per_question.pop()

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
        new_question = DefQuestion.DefinitionQuestion().make_from_chapter_index(chapter_index, cumulative=cumulative)

        user.update_user_quest(chapter_index=chapter_index, current_progress=current_progress,
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
    total_chapters = Chapter.Chapter().get_number_chapters()
    for index in range(1, total_chapters + 1):
        new_chapter = Chapter.Chapter()
        new_chapter.get_chapter_by_index(index)
        chapter_list.append(new_chapter.get_json())
    return {
        'user': user.get_json(),
        'quest_options': {
            'chapter_options': chapter_list,
            'number_of_questions_options': config.number_of_question_options,
            'seconds_per_question_options': config.seconds_per_question_options
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
    chapter_index = user.get_chapter_index()

    new_question = DefQuestion.DefinitionQuestion().make_from_chapter_index(
        chapter_index,
        cumulative=user.get_cumulative()
    )

    question_json = new_question.get_json()
    user.start_new_question(new_question.get_word_index())
    user.update_current_user()
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


def make_activity_log_entry(user, correct, request):
    try:
        ip_address = request.remote_addr
        user_agent = parse(request.user_agent.string)
        new_activity = ActivityLogEntry.ActivityLogEntry().generate_from_user(user, correct, ip_address, user_agent)
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


def make_quest_log_entry(user, request):
    try:
        ip_address = request.remote_addr
        user_agent = parse(request.user_agent.string)
        # TODO: add Lat and Lon
        new_quest_entry = QuestLogEntry.QuestLogEntry().generate_from_user(user, ip_address, user_agent)
        new_quest_entry.save_new()
    except Exception as ex:
        print(ex)
        print("failed too make quest log entry, not the end of the world, but no log entry made")
