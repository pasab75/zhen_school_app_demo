from flask import jsonify


class Definition():

    _word_index = None
    _definition = None
    _topic_index = None

    def __init__(self,
                 word_index=None,
                 definition=None,
                 topic_index=None):

        self._word_index = word_index
        self._definition = definition
        self._topic_index = topic_index

    def get_database_format(self):
        return {
            'word_index': self._word_index,
            'definition': self._definition,
            'topic_index': self._topic_index
        }

    def set_from_database(self, question):
        self._word_index = question['word_index']
        self._definition = question['definition']
        self._topic_index = question['topic_index']

    def get_jsonified(self):
        return jsonify(
            word_index=self._word_index,
            definition=self._definition,
            topic_index=self._topic_index
        )
