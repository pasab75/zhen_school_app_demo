# make sure to have a function that formats the quest to send to client
from flask import jsonify


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

    def get_chapter_name(self):
        return self._chapter_name

    def get_index(self):
        return self._index

    def set_chapter_name(self, name):
        self._chapter_name = name

    def set_index(self, index):
        self._index = index

    def get_jsonified(self):
        return jsonify(
            index=self._index,
            chapter_name=self._chapter_name
        )
