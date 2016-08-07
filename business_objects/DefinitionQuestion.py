import random

from peewee import fn, JOIN

import config

from business_objects.Models import Definition as Definition
from business_objects.Models import Word as Word


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
                "prompt": self._definition.definition,
                "chapter_index": self._chapter_index,
                "answers": words,
                "question_type": 1
            }
        else:
            definitions = []
            for definition in self._definitions:
                temp_word = definition.get_json_min()
                definitions.append(temp_word)
            return {
                "prompt": self._word.word,
                "chapter_index": self._chapter_index,
                "answers": definitions,
                "question_type": 0
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

        # TODO: This query is currently borked. fix it tomorrow

        if cumulative:
            self._words = (Word
                           .select(Word, Definition)
                           .join(Definition, JOIN.LEFT_OUTER)
                           .where(Word.chapter_index <= chapter_index)
                           .order_by(fn.Rand())
                           .limit(config.number_of_multiple_choices)
                           )
        else:
            self._words = (Word
                           .select(Word, Definition)
                           .join(Definition, JOIN.LEFT_OUTER)
                           .where(Word.chapter_index == chapter_index)
                           .order_by(fn.Rand())
                           .limit(config.number_of_multiple_choices)
                           )

        # question type 1 means that there will be a definition with word choices
        if question_type == 1:
            self._word = self._words[0]
            self._definition = random.choice(self._word.definitions)

        # question type 2 means that there will be a word with definition choices
        elif question_type == 0:
            for word in self._words:
                random_definition = random.choice(word.definitions)
                self._definitions.append(random_definition)

            self._definition = self._definitions[0]
            self._word = self._words[0]

        self._word_index = self._word.word_index
        return self

    def get_word_index(self):
        return self._word_index
