# make sure to have a function that formats the quest to send to client
from flask import jsonify
import db_access.db_chapters as database


class Chapter:
    _index = None
    _chapter_name = None

    def __init__(self,
                 index=None,
                 chapter_name=None
                 ):

        self._index = index
        self._chapter_name = chapter_name

    def get_database_format(self):
        return {
            'index': self._index,
            'chapter_index': self._chapter_name,
        }
