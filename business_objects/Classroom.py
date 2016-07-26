from flask import jsonify
import db_access.db_classrooms as db_access


class Classroom:

    _class_code = None
    _current_chapter = None
    _bonus_quests_per_day = None

    def __init__(self,
                 class_code=None,
                 current_chapter=None,
                 bonus_quests_per_day=None):

        self._class_code = class_code
        self._current_chapter = current_chapter
        self._bonus_quests_per_day = bonus_quests_per_day

    def get_database_format(self):
        return {
            'class_code': self._class_code,
            'current_chapter': self._current_chapter,
            'bonus_quests_per_day': self._bonus_quests_per_day
        }

    def save_new(self):
        try:
            db_a = db_access.ClassroomTableAccess()
            db_a.save_new_classroom_from_object(self)
            db_a.close_connection()
        except Exception as e:
            print("Could not save classroom: " + str(e))
            return False
