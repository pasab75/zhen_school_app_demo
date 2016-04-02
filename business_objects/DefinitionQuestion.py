from business_objects.AbstractQuestion import AbstractQuestion
from random import randint
from flask import jsonify


class DefinitionQuestion(AbstractQuestion):
    _word = None
    _definition_1 = None
    _definition_2 = None
    _definition_3 = None
    _question_list = None

    def __init__(self,
                 word=None,
                 definition_1=None,
                 definition_2=None,
                 definition_3=None,
                 topic=None,
                 question_id=None,
                 calculated_difficulty=1,
                 instructor_difficulty=None,
                 avg_answer_time=None):

        AbstractQuestion.__init__(self,
                                  topic,
                                  question_id,
                                  calculated_difficulty,
                                  instructor_difficulty,
                                  avg_answer_time)

        self._word = word
        self._definition_1 = definition_1
        self._definition_2 = definition_2
        self._definition_3 = definition_3
        self._question_list = []

    def get_database_format(self):
        return {
            'word': self._word,
            'definition_1': self._definition_1,
            'definition_2': self._definition_2,
            'definition_3': self._definition_3,
            'question_id': self._question_id,
            'topic': self._topic,
            'avg_answer_time': self._avg_answer_time,
            'instructor_difficulty': self._instructor_difficulty,
            'calculated_difficulty': self._calculated_difficulty
        }

    def set_question_from_database(self, question):
        self._topic = question['topic']
        self._question_id = question['question_id']
        self._calculated_difficulty = question['calculated_difficulty']
        self._instructor_difficulty = question['instructor_difficulty']
        self._avg_answer_time = question['avg_answer_time']
        self._word = question['word']
        self._definition_1 = question['definition_1']
        self._definition_2 = question['definition_2']
        self._definition_3 = question['definition_3']

    def make_multiple_choice(self):
        coin_flip = randint(0, 1)

        primary_question = self._question_list[0]
        answer_list = []

        if coin_flip == 0:

            for question in self._question_list:
                definition_number = randint(0, 2)

                if definition_number == 1 and question.get_definition_2():
                    answer = {'text': question.get_definition_2(), 'id': question.get_question_id()}
                elif definition_number == 2 and question.get_definition_3():
                    answer = {'text': question.get_definition_3(), 'id': question.get_question_id()}
                else:
                    answer = {'text': question.get_definition_1(), 'id': question.get_question_id()}

                answer_list.append(answer)

            return jsonify(
                question_text=primary_question.get_word(),
                answer=answer_list
            )

        else:
            for question in self._question_list:

                answer = {'text': question.get_word(), 'id': question.get_question_id()}

                answer_list.append(answer)

            definition_number = randint(0, 2)

            if definition_number == 1 and primary_question.get_definition_2():
                question_text = primary_question.get_definition_2()
            elif definition_number == 2 and primary_question.get_definition_3():
                question_text = primary_question.get_definition_3()
            else:
                question_text = primary_question.get_definition_1()

            return jsonify(
                question_text=question_text,
                answer=answer_list
            )

    def get_word(self):
        return self._word

    def set_word(self, word):
        self._word = word

    def get_definition_1(self):
        return self._definition_1

    def set_definition_1(self, definition):
        self._definition_1 = definition

    def get_definition_2(self):
        if self._definition_2 is not None:
            return self._definition_2
        else:
            return False

    def set_definition_2(self, definition):
        self._definition_2 = definition

    def get_definition_3(self):
        if self._definition_3 is not None:
            return self._definition_3
        else:
            return False

    def set_definition_3(self, definition):
        self._definition_3 = definition

    def get_definition_random(self):
        definition_list = [self._definition_1, self._definition_2, self._definition_3]
        return definition_list[randint(2)]
