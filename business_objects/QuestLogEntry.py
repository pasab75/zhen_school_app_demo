import config
import db_access.db_quest_log as db_access
import datetime


class QuestLogEntry:
    _user_id = None
    _number_correct = None
    _quest_start_datetime = None
    _quest_complete_datetime = None
    _number_of_questions = None
    _lat = None
    _lon = None
    _chapter_index = None
    _cumulative = None
    _is_timed = None
    _ip_address = None
    _device_type = None
    _device_family = None
    _device_model = None
    _is_timed = None

    def __init__(self, user_id=None, number_of_questions=10, number_correct=0, chapter_index=None, latitude=None,
                 longitude=None, cumulative=None, is_timed=None, ip_address=None,
                 device_type=None, device_family=None, device_model=None):
        self._user_id = user_id
        self._number_correct = number_correct
        self._number_of_questions = number_of_questions
        self._lat = latitude
        self._lon = longitude
        self._chapter_index = chapter_index
        self._cumulative = cumulative
        self._is_timed = is_timed
        self._device_family = device_family
        self._device_model = device_model
        self._device_type = device_type
        self._ip_address = ip_address

    def generate_from_user(self, user, ip_address, user_agent, user_current_lat=None, user_current_lon=None):
        self._user_id = user.get_user_id()
        self._number_correct = user.get_number_correct()
        self._quest_start_datetime = user.get_datetime_quest_started()
        self._chapter_index = user.get_chapter_index()
        self._cumulative = user.get_cumulative()
        self._number_of_questions = user.get_number_of_questions()
        self._is_timed = user.get_is_timed()
        self._quest_complete_datetime = datetime.datetime.now()
        self._lat = user_current_lat
        self._lon = user_current_lon
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
            "user_id": self._user_id,
            "number_correct": self._number_correct,
            "quest_start_datetime": self._quest_start_datetime,
            "quest_complete_datetime": self._quest_complete_datetime,
            "number_of_questions": self._number_of_questions,
            "latitude": self._lat,
            "longitude": self._lon,
            "chapter_index": self._chapter_index,
            "cumulative": self._cumulative,
            "is_timed": self._is_timed,
            "device_type": self._device_type,
            "device_family": self._device_family,
            "device_model": self._device_model,
            'ip_address': self._ip_address,
        }

    def set_from_database(self, db_quest_log_entry):
        self._user_id = db_quest_log_entry['user_id']
        self._number_correct = db_quest_log_entry['number_correct']
        self._quest_start_datetime = db_quest_log_entry['quest_start_datetime']
        self._quest_complete_datetime = db_quest_log_entry['quest_complete_datetime']
        self._lat = db_quest_log_entry['latitude']
        self._lon = db_quest_log_entry['longitude']
        self._chapter_index = db_quest_log_entry['chapter_index']
        self._cumulative = db_quest_log_entry['cumulative']
        self._number_of_questions = db_quest_log_entry['number_of_questions']
        self._is_timed = db_quest_log_entry['is_timed']
        self._device_type = db_quest_log_entry['device_type']
        self._device_model = db_quest_log_entry['device_model']
        self._device_family = db_quest_log_entry['device_family']
        self._ip_address = db_quest_log_entry['ip_address']

    def get_database_format(self):
        return {
            "user_id": self._user_id,
            "number_correct": self._number_correct,
            "quest_start_datetime": self._quest_start_datetime,
            "quest_complete_datetime": self._quest_complete_datetime,
            "number_of_questions": self._number_of_questions,
            "latitude": self._lat,
            "longitude": self._lon,
            "chapter_index": self._chapter_index,
            "cumulative": self._cumulative,
            "is_timed": self._is_timed,
            "device_type": self._device_type,
            "device_family": self._device_family,
            "device_model": self._device_model,
            'ip_address': self._ip_address,
        }
        
    # only call this if you're sure this doesn't exist in the db already
    def save_new(self):
        try:
            db_quest = db_access.QuestLogTableAccess()
            db_quest.save_new_quest(self)
            db_quest.close_connection()
            return True
        except Exception as e:
            print("Could not log quest: " + str(e))
            raise e

    def get_user_id(self):
        return self._user_id

    def set_quest_start_datetime(self, datetime):
        self._quest_start_datetime = datetime

    def get_quest_start_datetime(self):
        return self._quest_start_datetime

    def set_quest_complete_datetime(self, datetime):
        self._quest_complete_datetime = datetime

    def get_quest_complete_datetime(self):
        return self._quest_complete_datetime

    def set_number_correct(self, correct):
        self._number_correct = correct

    def get_number_correct(self):
        return self._number_correct

    def set_number_of_questions(self, num):
        self._number_of_questions = num

    def get_number_of_questions(self):
        return self._number_of_questions

    def set_is_timed(self, num):
        self._is_timed = num

    def get_is_timed(self):
        return self._is_timed

    def set_lat(self, lat):
        self._lat = lat

    def get_lat(self):
        return self._lat

    def set_lon(self, lon):
        self._lon = lon

    def get_lon(self):
        return self._lon

    def get_chapter_index(self):
        return self._chapter_index

    def set_chapter_index(self, value):
        self._chapter_index = value

    def get_cumulative(self):
        return self._cumulative

    def set_cumulative(self, value):
        self._cumulative = value

