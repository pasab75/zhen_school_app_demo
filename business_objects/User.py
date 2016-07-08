import db_access.db_users as User_db
import flask.jsonify as jsonify
import datetime


class User:
    _user_id = None
    _first_name = None
    _last_name = None
    _e_mail = None
    _user_role = None
    _current_lvl = None
    _current_points = None
    _current_multiplier = None
    _chapter_index = None
    _cumulative = None
    _number_of_questions = None
    _points_per_question = None
    _seconds_per_question = None
    _completion_points = None
    _date_quest_started = None
    _datetime_question_started = None
    _current_word_index = None
    _current_progress = None
    _number_correct = 0
    _last_active = None
    _paid_through = None

    def __init__(self, user_id=None,
                 first_name=None,
                 last_name=None,
                 e_mail=None,
                 user_role='0',
                 current_lvl='1',
                 current_points=0,
                 current_multiplier=0,
                 chapter_index=1,
                 cumulative=False,
                 number_of_questions=None,
                 points_per_question=None,
                 seconds_per_question=None,
                 completion_points=None,
                 date_quest_started=None,
                 datetime_question_started=None,
                 current_word_index=None,
                 current_progress=None,
                 number_correct=0,
                 last_active=None,
                 paid_through=None):

        self._user_id = user_id
        self._first_name = first_name
        self._last_name = last_name
        self._e_mail = e_mail
        self._user_role = user_role
        self._current_lvl = current_lvl
        self._current_points = current_points
        self._current_multiplier = current_multiplier
        self._chapter_index = chapter_index
        self._cumulative = cumulative
        self._number_of_questions = number_of_questions
        self._points_per_question = points_per_question
        self._seconds_per_question = seconds_per_question
        self._completion_points = completion_points
        self._date_quest_started = date_quest_started
        self._datetime_question_started = datetime_question_started
        self._current_word_index = current_word_index
        self._current_progress = current_progress
        self._number_correct = number_correct
        self._last_active = last_active
        self._paid_through = paid_through

    def check_answer(self, answer):
        if self.get_current_word_index() == answer:
            self.add_current_points(self.get_points_per_question()*self.get_current_multiplier())
            self.set_current_multiplier(self.get_current_multiplier()+1)
            self.update_quest_progress()
            return True
        else:
            self.set_current_multiplier(1)
            return False

    def update_quest_progress(self):
        self.set_current_progress(self.get_current_progress()+1)

    def is_quest_complete(self):
        if self.get_current_progress() == self.get_number_of_questions():
            return True
        else:
            return False

    def get_database_format(self):
        return {
            "user_id": self._user_id,
            "first_name": self._first_name,
            "last_name": self._last_name,
            "e_mail": self._e_mail,
            "user_role": self._user_role,
            "current_lvl": self._current_lvl,
            "current_points": self._current_points,
            "current_multiplier": self._current_multiplier ,
            "chapter_index": self._chapter_index,
            "cumulative": self._cumulative,
            "number_of_questions": self._number_of_questions,
            "points_per_question": self._points_per_question,
            "seconds_per_question": self._seconds_per_question,
            "completion_points": self._completion_points,
            "date_quest_started": self._date_quest_started,
            "current_word_index": self._current_word_index,
            "current_progress": self._current_progress,
            "number_correct": self._number_correct,
            "last_active": self._last_active,
            "paid_through": self._paid_through
        }

    def jsonify(self):
        return jsonify(
            user_id=self._user_id,
            first_name=self._first_name,
            last_name=self._last_name,
            e_mail=self._e_mail,
            user_role=self._user_role,
            current_lvl=self._current_lvl,
            current_points=self._current_points,
            current_multiplier=self._current_multiplier,
            chapter_index=self._chapter_index,
            cumulative=self._cumulative,
            number_of_questions=self._number_of_questions,
            points_per_question=self._points_per_question,
            seconds_per_question=self._seconds_per_question,
            completion_points=self._completion_points,
            date_quest_started=self._date_quest_started,
            current_word_index=self._current_word_index,
            current_progress=self._current_progress,
            number_correct=self._number_correct,
            last_active=self._last_active,
            paid_through=self._paid_through
        )

    def set_from_database(self, user):
        self._user_id = user['user_id']
        self._first_name = user['first_name']
        self._last_name = user['last_name']
        self._e_mail = user['e_mail']
        self._user_role = user['user_role']
        self._current_lvl = user['current_lvl']
        self._current_points = user['current_points']
        self._current_multiplier = user['current_multiplier']
        self._chapter_index = user['chapter_index']
        self._cumulative = user['cumulative']
        self._number_of_questions = user['number_of_questions']
        self._points_per_question = user['points_per_question']
        self._seconds_per_question = user['seconds_per_question']
        self._completion_points = user['completion_points']
        self._date_quest_started = user['date_quest_started']
        self._datetime_question_started = user['datetime_question_started']
        self._current_word_index = user['current_word_index']
        self._current_progress = user['current_progress']
        self._number_correct = user['number_correct']
        self._last_active = user['last_active']
        self._paid_through = user['paid_through']

    def update_user_quest(self, chapter_index=None, current_progress=None, date_quest_started=None,
                          current_word_index=None, number_correct=None, completion_points=None,
                          seconds_per_question=None, points_per_question=None, number_of_questions=None,
                          cumulative=None, datetime_question_started=None):
        self._chapter_index = chapter_index
        self._cumulative = cumulative
        self._number_of_questions = number_of_questions
        self._points_per_question = points_per_question
        self._seconds_per_question = seconds_per_question
        self._completion_points = completion_points
        self._date_quest_started = date_quest_started
        self._datetime_question_started = datetime_question_started
        self._current_word_index = current_word_index
        self._current_progress = current_progress
        self._number_correct = number_correct

    def generate_from_id(self, identification):
        db = User_db.UserTableAccess()
        current_user = db.get_user_by_user_id(identification)
        self.set_from_database(current_user)
        db.close_connection()

    def isPaid(self):
        current_time = datetime.datetime.now()
        if self._paid_through is not None:
            if self._paid_through > current_time:
                return True
        return False

    # only call this if you're sure this doesn't exist in the db already
    def save_new(self):
        try:
            db_user = User_db.UserTableAccess()
            db_user.save_user_new(self.get_database_format())
            db_user.close_connection()
            return True
        except Exception as e:
            print("Could not delete question: " + str(e))
            raise e

    def get_user_id(self):
        return self._user_id

    def get_first_name(self):
        return self._first_name

    def set_first_name(self, first_name):
        self._first_name = first_name

    def get_last_name(self):
        return self._last_name

    def set_last_name(self, last_name):
        self._last_name = last_name

    def get_email_address(self):
        return self._e_mail

    def set_email_address(self, email_addr):
        self._e_mail = email_addr

    def set_datetime_question_started(self):
        self._datetime_question_started = datetime.datetime.now

    def get_datetime_question_started(self):
        return self._datetime_question_started

    def get_user_role(self):
        return self._user_role

    def set_user_role(self, role):
        self._user_role = role

    def get_current_points(self):
        return self._current_points

    def set_current_points(self, points):
        self._current_points = points

    def add_current_points(self, points):
        self._current_points += points

    def get_last_activity_date(self):
        return self._last_active

    def set_last_activity_date(self, last_active):
        self._last_active = last_active

    def mark_activity_now(self):
        self._last_active = datetime.datetime.now()

    def get_paid_time(self):
        return self._paid_through

    def set_paid_time(self, paid_through):
        self._paid_through = paid_through

    def get_current_multiplier(self):
        return self._current_multiplier

    def set_current_multiplier(self, value):
        self._current_multiplier = value

    def get_chapter_index(self):
        return self._chapter_index

    def set_chapter_index(self, value):
        self._chapter_index = value

    def get_cumulative(self):
        return self._cumulative

    def set_cumulative(self, value):
        self._cumulative = value

    def get_number_of_questions(self):
        return self._number_of_questions

    def set_number_of_questions(self, value):
        self._number_of_questions = value

    def get_points_per_question(self):
        return self._points_per_question

    def set_points_per_question(self, value):
        self._points_per_question = value

    def get_seconds_per_question(self):
        return self._seconds_per_question

    def set_seconds_per_question(self, value):
        self._seconds_per_question = value

    def get_completion_points(self):
        return self._completion_points

    def set_completion_points(self, value):
        self._completion_points = value

    def get_date_quest_started(self):
        return self._date_quest_started

    def set_date_quest_started(self, value):
        self._date_quest_started = value

    def get_current_word_index(self):
        return self._current_word_index

    def set_current_word_index(self, value):
        self._current_word_index = value

    def get_current_progress(self):
        return self._current_progress

    def set_current_progress(self, value):
        self._current_progress = value

    def get_number_correct(self):
        return self._number_correct

    def set_number_correct(self, value):
        self._number_correct = value

    def update_current_user(self):
        user_db = User_db.UserTableAccess()
        user_db.update_user(self.get_database_format())
        user_db.close_connection()