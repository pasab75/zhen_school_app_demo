# make sure to have a function that formats the quest to send to client
from flask import jsonify
import db_access.db_chapters as db_chapters


class Chapter:
    _chapter_index = None
    _chapter_name = None

    def __init__(self,
                 chapter_index=None,
                 chapter_name=None
                 ):

        self._index = chapter_index
        self._chapter_name = chapter_name

    def get_database_format(self):
        return {
            'chapter_index': self._index,
            'chapter_name': self._chapter_name,
        }

    def get_chapter_name(self):
        return self._chapter_name

    def get_index(self):
        return self._chapter_index

    def set_chapter_name(self, name):
        self._chapter_name = name

    def set_index(self, index):
        self._chapter_index = index

    def get_json(self):
        return {
            'chapter_name': self._chapter_name
        }

    def save_new(self):
        try:
            db_c = db_chapters.ChapterTableAccess()
            db_c.save_new_chapter_from_object(self.get_database_format())
            db_c.close_connection()
            return True
        except Exception as e:
            print("Could not delete question: " + str(e))
            return False