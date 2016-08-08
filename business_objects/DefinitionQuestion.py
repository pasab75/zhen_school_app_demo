from random import shuffle, randint
from peewee import fn

from config import *
from business_objects.Models import Definition as Definition
from business_objects.Models import Word as Word


class DefinitionQuestion:
    word_index = None
    question_text = None
    answer_choices = None
    chapter_index = None
    question_type = None

    def make_definition_question(
            self,
            chapter_index,
            question_type=None,
            cumulative=False,
            ):
        # if no question type is requested, flip a coin to determine the question type
        self.chapter_index = chapter_index
        if question_type not in [0, 1]:
            self.question_type = randint(0, 1)

        if cumulative:
            query = (Definition
                     .select(Word, Definition)
                     .join(Word)
                     .where(Word.chapter_index <= chapter_index)
                     .order_by(fn.Rand())
                     .limit(number_of_multiple_choices)
                     )
        else:
            query = (Definition
                     .select(Word, Definition)
                     .join(Word)
                     .where(Word.chapter_index == chapter_index)
                     .order_by(fn.Rand())
                     .limit(number_of_multiple_choices)
                     )

        if self.question_type == 1:
            definition_list = []
            for element in query:
                definition = {
                    "text": element.definition,
                    "index": element.word_index.word_index
                }
                definition_list.append(definition)
            self.answer_choices = definition_list
            self.question_text = query[0].word_index.word

        elif self.question_type == 0:
            word_list = []
            for element in query:
                word = {
                    "text": element.word_index.word,
                    "index": element.word_index_id
                }
                word_list.append(word)

            self.answer_choices = word_list
            self.question_text = query[0].definition

        self.word_index = query[0].word_index.word_index
        shuffle(self.answer_choices)

        return self

    def get_json_min(self):
        return {
            "prompt": self.question_text,
            "answers": self.answer_choices,
            "chapter_index": self.chapter_index,
            "question_type": self.question_type
        }
