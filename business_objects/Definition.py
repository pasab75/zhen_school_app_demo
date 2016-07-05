from flask import jsonify
import db_access.db_definitions as db_definition

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

    def get_word_index(self):
        return self._word_index

    def get_definition(self):
        return self._definition

    # only call this if you're sure this doesn't exist in the db already
    def save_new(self):
        try:
            db_def = db_definition.DefinitionTableAccess()
            db_def.save_new_definition_from_object(self.get_database_format())
            return True
        except Exception as e:
            print("Could not delete question: " + str(e))
            return False
