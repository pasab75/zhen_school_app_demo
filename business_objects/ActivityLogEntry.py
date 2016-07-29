import datetime
import db_access.db_activity_log as db_access

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
    _ip_address = None
    _device_type = None
    _device_family = None
    _device_model = None

    def __init__(self, user_id=None, correct=None, number_of_questions=None, date_time=datetime.datetime.now(),
                 datetime_quest_started=datetime.datetime.now(), seconds_per_questions=None, latitude=None, longitude=None,
                 datetime_question_started=datetime.datetime.now(), current_word_index=None, ip_address=None,
                 device_type=None, device_family=None, device_model=None):
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
        self._ip_address = ip_address
        self._device_family = device_family
        self._device_model = device_model
        self._device_type = device_type

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
        self._ip_address = db_quest_log_entry['ip_address']
        self._device_type = db_quest_log_entry['device_type']
        self._device_model = db_quest_log_entry['device_model']
        self._device_family = db_quest_log_entry['device_family']

    def generate_from_user(
            self,
            user,
            correct,
            ip_address,
            user_agent,
            user_current_lat=None,
            user_current_lon=None,
    ):
        self._user_id = user.get_user_id()
        self._datetime = datetime.datetime.now()
        self._correct = correct
        self._latitude = user_current_lat
        self._longitude = user_current_lon
        self._number_of_questions = user.get_number_of_questions()
        self._datetime_quest_started = user.get_datetime_quest_started()
        self._current_word_index = user.get_current_word_index()
        self._datetime_question_started = user.get_datetime_question_started()
        self._ip_address = ip_address
        if user_agent.is_mobile:
            self._device_type = 0
        elif user_agent.is_tablet:
            self._device_type = 1
        elif user_agent.is_pc:
            self._device_type = 2
        self._device_family = user_agent.device.family
        self._device_model = user_agent.device.model
        return self

    def get_json(self):
        return {
            'user_id': self._user_id,
            'datetime': self._datetime,
            'correct': self._correct,
            'latitude': self._latitude,
            'longitude': self._longitude,
            'number_of_questions': self._number_of_questions,
            'datetime_quest_started': self._datetime_quest_started,
            'current_word_index': self._current_word_index,
            'datetime_question_started': self._datetime_question_started,
            'ip_address': self._ip_address,
            "device_type": self._device_type,
            "device_family": self._device_family,
            "device_model": self._device_model
        }

    def get_database_format(self):
        return {
            "user_id": self._user_id,
            "datetime": self._datetime,
            "correct": self._correct,
            "latitude": self._latitude,
            "longitude": self._longitude,
            "number_of_questions": self._number_of_questions,
            "datetime_quest_started": self._datetime_quest_started,
            "current_word_index": self._current_word_index,
            "datetime_question_started": self._datetime_question_started,
            "ip_address": self._ip_address,
            "device_type": self._device_type,
            "device_family": self._device_family,
            "device_model": self._device_model
        }

    def save_new(self):
        try:
            db_activity = db_access.ActivityLogTableAccess()
            db_activity.save_new_activity_from_obj(self)
            db_activity.close_connection()
            return True
        except Exception as e:
            print("Could not log activity " + str(e))
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


