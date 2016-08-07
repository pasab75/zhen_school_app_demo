import datetime
from oauth2client import client, crypt
from user_agents import parse
from flask import abort

from business_objects.DefinitionQuestion import DefinitionQuestion
from business_objects.Models import *
from business_objects.User import User

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
                raise Exception("Failed to authenticate user")
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


def get_quest_options():
    chapter_list = []
    for chapter in Chapter.select():
        chapter_list.append(chapter.get_json_min())
    return {
        'chapter_options': chapter_list,
        'number_of_questions_options': config.number_of_question_options
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


def make_activity_log_entry(user, correct, request):
    try:
        ip_address = request.remote_addr
        user_agent = parse(request.user_agent.string)
        if user_agent.is_mobile:
            device_type = 0
        elif user_agent.is_tablet:
            device_type = 1
        elif user_agent.is_pc:
            device_type = 2
        else:
            device_type = -1

        new_activity_log_entry = ActivityLogEntry(
            correct=correct,
            current_word_index=user.current_word_index,
            datetime=datetime.datetime.now(),
            datetime_quest_started=user.datetime_quest_started,
            datetime_question_started=user.datetime_question_started,
            device_family=user_agent.device.family,
            device_model=user_agent.device.model,
            device_type=device_type,
            ip_address=ip_address,
            is_daily=user.is_on_daily,
            is_timed=user.is_timed,
            # latitude = ,
            # longitude =,
            number_of_questions=user.number_of_questions,
            user_id=user.user_id
        )
        new_activity_log_entry.save()
    except Exception as ex:
        print(ex)
        print("failed too make activity log entry.")

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
        if user_agent.is_mobile:
            device_type = 0
        elif user_agent.is_tablet:
            device_type = 1
        elif user_agent.is_pc:
            device_type = 2
        else:
            device_type = -1

        new_quest_log_entry = QuestLogEntry(
            chapter_index=user.chapter_index,
            cumulative=user.cumulative,
            datetime_quest_completed=datetime.datetime.now,
            datetime_quest_started=user.datetime_quest_started,
            device_family=user_agent.device.family,
            device_model=user_agent.device.model,
            device_type=device_type,
            ip_address=ip_address,
            is_daily=user.is_on_daily,
            is_timed=user.is_timed,
            # latitude = ,
            # longitude =,
            number_of_questions=user.number_of_questions,
            user_id=user.user_id
        )
        new_quest_log_entry.save()
    except Exception as ex:
        print(ex)
        print("Failed to make quest log entry.")

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

