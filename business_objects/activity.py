from flask import jsonify

class activity:
    _user_id = None;
    _time = None;
    _date = None;
    _correct = False;
    _latitude = None;
    _longitude = None;
    _quest_progess = None;
    _activity = None;
    _question_id = None;

    def __init__(self, user_id, question_id, time, date, correct, latitude=None,
                 longitude=None, quest_progress=None, activity=None):
        self._user_id = user_id
        self._time = time
        self._date = date
        self._correct = correct
        self._latitude = latitude
        self._longitude = longitude
        self._quest_progess = quest_progress
        self._activity = activity
        self._question_id = question_id

    def get_user_id(self):
        return self._user_id

    def set_time(self, time):
        self._time = time

    def get_time(self):
        return self._time

    def set_date(self, date):
        self._date = date

    def get_date(self):
        return self._date

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

    def set_quest_progress(self, qp):
        self._quest_progess = qp

    def get_quest_progress(self):
        return self._quest_progess

    def set_activity(self, activity):
        self._activity = activity

    def get_activity(self):
        return self._activity

    def get_question_id(self):
        return self._question_id

    def get_jsonified(self):
        return jsonify(
                    user_id = self._user_id,
                    time = self._time,
                    date = self._date,
                    correct = self._correct,
                    latitude = self._latitude,
                    longitude = self._longitude,
                    quest_progress = self._quest_progess,
                    activity = self._activity,
                    question_id = self._question_id
                )