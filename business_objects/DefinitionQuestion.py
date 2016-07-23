from flask import jsonify
import random
from enum import Enum

import business_objects.Word as Word
import business_objects.Definition as Definition
import db_access.db_definitions as db_access_definitions
import db_access.db_words as db_access_words




class DefinitionQuestion:
    _word_index = None
    _word = None
    _definition = None
    _chapter_index = None
    _words = []
    _definitions = []
    _question_type = 0

    def __init__(self,
                 word_index=None,
                 definition=None,
                 chapter_index=None,
                 type=None):
        self._word_index = word_index
        self._definition = definition
        self._chapter_index = chapter_index
        self._question_type = type

    def get_json(self):
        random.shuffle(self._words)
        random.shuffle(self._definitions)

        if self._question_type == 0:
            words = []
            for word in self._words:
                temp_word = word.get_json_min()
                words.append(temp_word)
            return {
                "prompt": self._definition.get_definition(),
                "chapter_index": self._chapter_index,
                "answers": words,
                "question_type": 0
            }
        else:
            defins = []
            for defin in self._definitions:
                temp_word = defin.get_json_min()
                defins.append(temp_word)
            return {
                "prompt": self._word.get_word(),
                "chapter_index": self._chapter_index,
                "answers": defins,
                "question_type": 1
            }

    def make_from_chapter_index(self, chapter_index, num_wanted=6, question_type=None):
        self._question_type = question_type
        self._chapter_index = chapter_index
        self._words = []
        self._definitions = []

        print(type(chapter_index))

        if not question_type:
            question_type = random.randint(0, 1)
            self._question_type = question_type

        if question_type == 0:
            db_word = db_access_words.WordTableAccess()
            raw_list = db_word.get_word_list_random_by_chapter_index(chapter_index)
            for database_word in raw_list:
                new_word = Word.Word()
                new_word.set_from_database(database_word)
                self._words.append(new_word)
            self._word = self._words[0]
            self._definition = Definition.Definition().get_definition_random_from_word(self._word)

        elif question_type == 1:
            db_def = db_access_definitions.DefinitionTableAccess()
            raw_list = db_def.get_definition_list_random_by_chapter_index(chapter_index)
            for database_definition in raw_list:
                new_definition = Definition.Definition()
                new_definition.set_from_database(database_definition)
                self._definitions.append(new_definition)
            self._definition = self._definitions[0]
            self._word = Word.Word().get_word_from_definition(self._definition)

        return self

    def make_from_chapter(self, chapter, num_wanted, type):
        self.make_from_chapter_index(chapter.get_index(), num_wanted, type)

    def get_word_index(self):
        return self._word_index

    def set_word_index(self, index):
        self._word_index = index

class DefQuestionType(Enum):
    word = 0
    definition = 1

def main():
    defQuestion = DefinitionQuestion().make_from_chapter_index(1, 2, 0)

if __name__ == "__main__":
    print("Starting run")
    main()
    print("Ending run")
