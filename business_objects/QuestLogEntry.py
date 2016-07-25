import db_access.db_quest_log as db_quest_log
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
    _seconds_per_question = None

    def __init__(self, user_id=None, number_of_questions=10, number_correct=0, chapter_index=None, latitude=None,
                 longitude=None, cumulative=None, seconds_per_question=0):
        self._user_id = user_id
        self._number_correct = number_correct
        self._number_of_questions = number_of_questions
        self._lat = latitude
        self._lon = longitude
        self._chapter_index = chapter_index
        self._cumulative = cumulative
        self._seconds_per_question = seconds_per_question

    def generate_from_user(self, user, quest_end_time=datetime.datetime.now(), user_current_lat=None, user_current_lon=None):
        self._user_id = user.get_user_id()
        self._number_correct = user.get_number_correct()
        self._quest_start_datetime = user.get_datetime_quest_started()
        self._chapter_index = user.get_chapter_index()
        self._cumulative = user.get_cumulative()
        self._number_of_questions = user.get_number_of_questions()
        self._seconds_per_question = user.get_seconds_per_question()
        self._quest_complete_datetime = quest_end_time
        self._lat = user_current_lat
        self._lon = user_current_lon
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
            "seconds_per_question": self._seconds_per_question
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
        self._seconds_per_question = db_quest_log_entry['seconds_per_question']

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
            "seconds_per_question": self._seconds_per_question
        }
        
    # only call this if you're sure this doesn't exist in the db already
    def save_new(self):
        try:
            db_quest = db_quest_log.QuestLogTableAccess()
            db_quest.save_new_quest(self.get_database_format())
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

    def set_seconds_per_question(self, num):
        self._seconds_per_question = num

    def get_seconds_per_question(self):
        return self._seconds_per_question

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

