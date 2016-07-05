from flask import jsonify
import db_access.db_words as db_words
import business_objects.Word as Word
import business_objects.definition as Definition
import db_access.db_definitions as db_definition
from enum import Enum

class DefinitionQuestion():
    _word_index = None
    _definition = None
    _topic_index = None
    _words = []
    _definitions = []
    _type = 0

    def __init__(self,
                 word_index=None,
                 definition=None,
                 topic_index=None,
                 type=None):
        self._word_index = word_index
        self._definition = definition
        self._topic_index = topic_index
        self._type = type

    def get_database_format(self):
        return {
            'word_index': self._word_index,
            'definition': self._definition,
            'topic_index': self._topic_index
        }

    def get_jsonified(self):
        return jsonify(
            word_index=self._word_index,
            definition=self._definition,
            topic_index=self._topic_index
        )

    # word is the business object not the db_obj version of it
    # 0 would be a words presented question, 1 is a definitions presented question
    def make_from_word(self, word, num_wanted, type):
        db_word = db_words.WordTableAccess()
        db_def = db_definition.DefinitionTableAccess()
        definition = db_def.get_definition_by_wordindex(self._word_index)
        word = Word(word)
        self._type = type

        if type == 0:
            self._word_index = word.get_index()
            self._definition = definition.get_definition()
            self._topic_index = word.get_topic_index()
            self._words.append(word.get_word())
            for x in range(0, num_wanted):
                filler_word = Word()
                filler_word = filler_word.set_from_database(db_word.get_word_random_by_topic_index(self._topic_index))
                self._words.append(filler_word.get_word())

        if type == 1:
            self._word_index = word.get_index()
            self._definition = definition.get_definition()
            self._topic_index = word.get_topic_index()
            self._definitions.append(self._definition)
            for x in range(0, num_wanted):
                filler_def = Definition()
                filler_def = filler_def.set_from_database(db_def.get_definition_random_by_topic_index(self._topic_index))
                self._definitions.append(filler_word.get_definition())

    def get_index(self):
        return self._index

    def set_index(self, index):
        self._index = index

class DefQuestionType(Enum):
    word = 0
    definition = 1
