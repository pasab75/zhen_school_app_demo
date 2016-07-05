from flask import jsonify

import business_objects.Word as Word
import business_objects.Definition as Definition
import db_access.db_definitions as db_definition
import db_access.db_words as db_wordzors
import random
from enum import Enum


class DefinitionQuestion():
    _word_index = None
    _word = None
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

    def get_jsonified(self):
        random.shuffle(self._words)
        random.shuffle(self._definitions)

        if type == 0:
            return jsonify(
                question=self._definition,
                topic_index=self._topic_index,
                answers=self._words,
                type=0
            )
        else:
            return jsonify(
                question=self._word,
                topic_index=self._topic_index,
                answers=self._definitions,
                type=1
            )

    # word is the business object not the db_obj version of it
    # 0 would be a words presented question, 1 is a definitions presented question
    def make_from_topic_index(self, topic_index, num_wanted, type):
        db_def = db_definition.DefinitionTableAccess()
        db_word = db_wordzors.WordTableAccess()
        word = Word.word.set_from_database(db_word.get_word_random_by_topic_index(topic_index))
        definition = db_def.get_definition_by_wordindex(word.get_index())
        self._word = word
        self._type = type
        self._word_index = word.get_index()
        self._definition = definition.get_definition()
        self._topic_index = word.get_topic_index()

        if type == 0:
            self._words.append(word)
            db_words = db_word.get_word_random_by_topic_index(self._topic_index, num_wanted)
            for word_obj in db_words:
                filler_word = Word.word.set_from_database(word_obj)
                self._words.append(filler_word.get_word())

        if type == 1:
            self._definitions.append(definition)
            db_defs = db_def.get_definition_random_by_topic_index(self._topic_index, num_wanted)
            for def_obj in db_defs:
                filler_def = Definition.Definition.set_from_database(db_def.get_definition_random_by_topic_index(self._topic_index))
                self._definitions.append(filler_word.get_definition())

        db_word.close_connection()
        db_def.close_connection()

    # word is the business object not the db_obj version of it
    # 0 would be a words presented question, 1 is a definitions presented question
    def make_from_topic(self, topic, num_wanted, type):
        db_def = db_definition.DefinitionTableAccess()
        db_word = db_wordzors.WordTableAccess()
        word = Word.word.set_from_database(db_word.get_word_random_by_topic(topic))
        definition = db_def.get_definition_by_wordindex(word.get_index())
        self._word = word
        self._type = type
        self._word_index = word.get_index()
        self._definition = definition.get_definition()
        self._topic_index = word.get_topic_index()

        if type == 0:
            self._words.append(word)
            db_words = db_word.get_word_random_by_topic_index(self._topic_index, num_wanted)
            for word_obj in db_words:
                filler_word = Word.word.set_from_database(word_obj)
                self._words.append(filler_word.get_word())

        if type == 1:
            self._definitions.append(definition)
            db_defs = db_def.get_definition_random_by_topic_index(self._topic_index, num_wanted)
            for def_obj in db_defs:
                filler_def = Definition.Definition.set_from_database(
                    db_def.get_definition_random_by_topic_index(self._topic_index))
                self._definitions.append(filler_word.get_definition())

        db_word.close_connection()
        db_def.close_connection()
    def get_word_index(self):
        return self._word_index

    def set_word_index(self, index):
        self._word_index = index

class DefQuestionType(Enum):
    word = 0
    definition = 1

def main():
    defQuestion = DefinitionQuestion().make_from_topic_index(1,2,0)

if __name__ == "__main__":
    print("Starting run")
    main()
    print("Ending run")
