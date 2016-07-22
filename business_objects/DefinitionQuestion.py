from flask import jsonify
import random
from enum import Enum

import business_objects.Word as Word
import business_objects.Definition as Definition




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
                temp_word = word.get_json()
                temp_word['text'] = word['word']
                words.append(temp_word)
            return {
                "prompt":self._definition.get_json(),
                "chapter_index":self._chapter_index,
                "answers":words,
                "question_type":0
            }
        else:
            defins = []
            for defin in self._definitions:
                defins.append(defin.get_json())
            return {
                "prompt":self._word.get_json(),
                "chapter_index":self._chapter_index,
                "answers":defins,
                "question_type":1
            }

    def make_from_chapter_index(self, chapter_index, num_wanted=5, question_type=None):
        word = Word.Word().get_word_random_by_chapter_index(chapter_index)
        definition = Definition.Definition().get_definition_random_by_from_word(word)
        self._word = word
        self._question_type = question_type
        self._word_index = word.get_index()
        self._definition = definition
        self._chapter_index = word.get_chapter_index()

        #TODO remove duplication aka multiquery
        if not question_type:
            question_type = random.randint(0, 1)
            self._question_type = question_type
        if question_type == 0:
            self._words.append(word)
            for x in range(num_wanted):
                new_word = Word.Word().get_word_random_by_chapter_index(chapter_index)
                self._words.append(new_word)

        if question_type == 1:
            self._definitions.append(definition)
            for x in range(num_wanted):
                filler_def = Definition.Definition().get_definition_random_by_chapter_index(word.get_chapter_index())
                self._definitions.append(filler_def)

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
