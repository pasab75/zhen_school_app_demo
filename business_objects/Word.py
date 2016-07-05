# make sure to have a function that formats the quest to send to client
from flask import jsonify


class Word():
    _index = None
    _word = None
    _topic_index = None
    _instructor_difficulty = False
    _calculated_difficulty = None
    _avg_answer_time = None

    def __init__(self,
                 index=None,
                 word=None,
                 topic_index=None,
                 instructor_difficulty=None,
                 calculate_difficulty=None,
                 avg_answer_time=None):

        self._index = index
        self._word = word
        self._topic_index = topic_index
        self._instructor_difficulty = instructor_difficulty
        self._calculated_difficulty = calculate_difficulty
        self._avg_answer_time = avg_answer_time

    def get_jsonified(self):
        return jsonify(
            index = self._index,
            word = self._word,
            topic_index = self._topic_index,
            instructor_difficulty = self._instructor_difficulty,
            calculated_difficulty = self._calculated_difficulty,
            avg_answer_time = self._avg_answer_time
            )

    def get_database_format(self):
        return {
            'index': self._index,
            'word': self._word,
            'topic_index': self._topic_index,
            'instructor_difficulty': self._instructor_difficulty,
            'calculated_difficulty': self._calculated_difficulty,
            'avg_answer_time': self._avg_answer_time
        }


    def set_from_database(self, word):
        self._index = word['index']
        self._word = word['word']
        self._topic_index = word['topic_index']
        self._instructor_difficulty = word['instructor_difficulty']
        self._calculated_difficulty = word['calculated_difficulty']
        self._avg_answer_time = word['avg_answer_time']

    def get_word(self):
        return self._word

    def get_index(self):
        return self._index

    def set_index(self, index):
        self._index = index

    def get_topic_index(self):
        return self._topic_index

    def set_topic_index(self, index):
        self._topic_index = index