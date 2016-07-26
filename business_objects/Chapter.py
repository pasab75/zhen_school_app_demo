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

        self._chapter_index = chapter_index
        self._chapter_name = chapter_name

    def get_database_format(self):
        return {
            'chapter_index': self._chapter_index,
            'chapter_name': self._chapter_name
        }

    def get_json(self):
        return {
            'chapter_index': self._chapter_index,
            'chapter_name': self._chapter_name
        }

    def get_chapter_name(self):
        return self._chapter_name

    def get_index(self):
        return self._chapter_index

    def set_chapter_name(self, name):
        self._chapter_name = name

    def set_index(self, index):
        self._chapter_index = index

    def get_number_chapters(self):
        try:
            db_c = db_chapters.ChapterTableAccess()
            result = db_c.get_chapters_total()
            db_c.close_connection()
            return result
        except Exception as e:
            print("could not retrieve number of chapters: " + str(e))
            return False

    def get_chapter_by_index(self, index):
        try:
            db_c = db_chapters.ChapterTableAccess()
            chapter_object = db_c.get_chapter_by_index(index)
            db_c.close_connection()
            self.set_from_database(chapter_object)

        except Exception as e:
            print("Could not get chapter object: " + str(e))
            return False

    def set_from_database(self, chapter):
        self._chapter_index = chapter['chapter_index']
        self._chapter_name = chapter['chapter_name']

    def save_new(self):
        try:
            db_c = db_chapters.ChapterTableAccess()
            db_c.save_new_chapter_from_object(self.get_database_format())
            db_c.close_connection()
            return True
        except Exception as e:
            print("Could not save new chapter: " + str(e))