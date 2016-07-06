from flask import jsonify

import business_objects.Word as Word
import business_objects.Definition as Definition
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

    def make_from_chapter_index(self, chapter_index, num_wanted, type):
        word = Word.word.generate_word_randomly_chapter_index(chapter_index)
        definition = Definition.Definition.generate_random_from_word(word)
        self._word = word
        self._type = type
        self._word_index = word.get_index()
        self._definition = definition.get_definition()
        self._topic_index = word.get_topic_index()

        if type == 0:
            self._words.append(word)
            for x in range(num_wanted):
                new_word = Word.word.generate_word_randomly_chapter_index(chapter_index)
                self._words.append(new_word[0])

        if type == 1:
            self._definitions.append(definition)
            for x in range(num_wanted):
                filler_def = Definition.Definition.generate_random_from_chapter_index(word)
                self._definitions.append(filler_def[0])

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
    defQuestion = DefinitionQuestion().make_from_topic_index(1,2,0)

if __name__ == "__main__":
    print("Starting run")
    main()
    print("Ending run")
