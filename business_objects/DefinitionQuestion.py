import random

import business_objects.Word as Word
import business_objects.Definition as Definition
import config

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
                 word=None,
                 definition=None,
                 chapter_index=None,
                 question_type=None):
        self._word_index = word_index
        self._word = word
        self._definition = definition
        self._chapter_index = chapter_index
        self._question_type = question_type

    def get_index(self):
        return self._word_index

    def get_json(self):
        random.shuffle(self._words)
        random.shuffle(self._definitions)

        if self._question_type == 1:
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

    def make_from_chapter_index(self, chapter_index, question_type=None, cumulative=False):
        self._question_type = question_type
        self._chapter_index = chapter_index
        self._words = []
        self._definitions = []

        # if no question type is requested, flip a coin to determine the question type
        if question_type not in [0, 1]:
            question_type = random.randint(0, 1)
            self._question_type = question_type

        if cumulative:
            chapter_lower_limit = 1
        else:
            chapter_lower_limit = chapter_index

        db_connection = db_access_words.WordTableAccess()
        raw_list = db_connection.get_row_random_with_limits(
            'words',
            'chapter_index',
            chapter_lower_limit,
            chapter_index,
            config.number_of_multiple_choices
        )
        db_connection.close_connection()

        # question type 1 means that there will be a definition with word choices
        if question_type == 1:
            for word in raw_list:
                word_obj = Word.Word()
                word_obj.set_from_database(word)

                self._words.append(word_obj)

            self._word = self._words[0]
            self._definition = Definition.Definition().get_definition_random_from_word(self._word)

        # question type 2 means that there will be a word with definition choices
        elif question_type == 0:
            for word in raw_list:
                word_obj = Word.Word()
                word_obj.set_from_database(word)

                definition_obj = Definition.Definition()
                definition_obj.generate_random_from_word(word_obj)

                self._definitions.append(definition_obj)

            self._definition = self._definitions[0]
            self._word = Word.Word().get_word_from_definition(self._definition)

        self._word_index = self._word.get_index()
        return self

    def make_from_chapter(self, chapter, num_wanted, type):
        self.make_from_chapter_index(chapter.get_index(), num_wanted, type)

    def get_word_index(self):
        return self._word_index

    def set_word_index(self, index):
        self._word_index = index
