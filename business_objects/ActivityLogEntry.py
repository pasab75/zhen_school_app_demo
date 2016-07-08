from flask import jsonify
import datetime
import db_access.db_activity_log as db_activity_log

class ActivityLogEntry:
    _user_id = None
    _datetime = None
    _correct = False
    _latitude = None
    _longitude = None
    _number_of_questions = None
    _seconds_per_questions = None
    _datetime_quest_started = None
    _datetime_question_started = None
    _current_word_index = None

    def __init__(self, user_id, correct, number_of_questions=10, date_time=datetime.datetime.now(),
                 datetime_quest_started=datetime.datetime.now(), seconds_per_questions=0, latitude=None, longitude=None,
                 datetime_question_started=datetime.datetime.now(), current_word_index=None):
        self._user_id = user_id
        self._datetime = date_time
        self._correct = correct
        self._latitude = latitude
        self._longitude = longitude
        self._number_of_questions = number_of_questions
        self._seconds_per_questions = seconds_per_questions
        self._datetime_quest_started = datetime_quest_started
        self._current_word_index = current_word_index
        self._datetime_question_started = datetime_question_started

    def set_from_database(self, db_quest_log_entry):
        self._user_id = db_quest_log_entry['user_id']
        self._datetime = db_quest_log_entry['datetime']
        self._correct = db_quest_log_entry['correct']
        self._latitude = db_quest_log_entry['latitude']
        self._longitude = db_quest_log_entry['longitude']
        self._number_of_questions = db_quest_log_entry['number_of_questions']
        self._datetime_quest_started = db_quest_log_entry['datetime_quest_started']
        self._current_word_index = db_quest_log_entry['current_word_index']
        self._datetime_question_started = db_quest_log_entry['datetime_question_started']

    def get_jsonified(self):
        return jsonify(
            user_id=self._user_id,
            datetime=self._datetime,
            correct=self._correct,
            latitude=self._latitude,
            longitude=self._longitude,
            number_of_questions=self._number_of_questions,
            datetime_quest_started=self._datetime_quest_started,
            current_word_index=self._current_word_index,
            datetime_question_started=self._datetime_question_started
        )

    def get_database_format(self):
        return {
            "user_id":self._user_id,
            "datetime":self._datetime,
            "correct":self._correct,
            "latitude":self._latitude,
            "longitude":self._longitude,
            "number_of_questions":self._number_of_questions,
            "datetime_quest_started":self._datetime_quest_started,
            "current_word_index":self._current_word_index,
            "datetime_question_started":self._datetime_question_started
        }

    # only call this if you're sure this doesn't exist in the db already
    def save_new(self):
        try:
            db_activity = db_activity_log.ActivityLogTableAccess()
            db_activity.save_new_activity(self.get_database_format())
            db_activity.close_connection()
            return True
        except Exception as e:
            print("Could not delete question: " + str(e))
            raise e

    def get_user_id(self):
        return self._user_id

    def set_datetime(self, date_time):
        self._datetime = date_time

    def get_datetime(self):
        return self._datetime

    def set_correct(self, correct):
        self._correct = correct

    def get_correct(self):
        return self._correct

    def set_lat(self, lat):
        self._latitude = lat

    def get_lat(self):
        return self._latitude

    def set_lon(self, lon):
        self._longitude = lon

    def get_lon(self):
        return self._longitude

    def get_number_of_questions(self):
        return self._number_of_questions

    def set_number_of_questions(self, num):
        self._number_of_questions = num

    def get_seconds_per_questions(self):
        return self._seconds_per_questions

    def set_seconds_per_questions(self, num):
        self._seconds_per_questions = num

    def get_datetime_quest_started(self):
        return self._datetime_quest_started

    def set_datetime_quest_started(self, date_time):
        self._datetime_quest_started = date_time

    def get_datetime_question_started(self):
        return self._datetime_question_started

    def set_datetime_question_started(self, date_time):
        self._datetime_question_started = date_time

    def get_current_word_index(self):
        return self._current_word_index

    def set_current_word_index(self, index):
        self._current_word_index = index

