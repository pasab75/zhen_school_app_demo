from business_objects.AbstractQuestion import AbstractQuestion
import db_access.db_multiple_choice as multiple_choice_table_access_layer
import db_access.db_definitions as definitions_table_access_layer
from random import randint, shuffle


class MultipleChoiceQuestion(AbstractQuestion):

    # -------------------------------------------------------------
    # class constructor
    # -------------------------------------------------------------

    def __init__(self,
                 question_text=None,
                 answer=None,
                 answer_0=None,
                 answer_1=None,
                 answer_2=None,
                 answer_3=None,
                 answer_4=None,
                 answer_5=None,
                 topic=None,
                 question_id=None,
                 calculated_difficulty=1,
                 instructor_difficulty=None,
                 avg_answer_time=None,
                 image_path=None
                 ):

        AbstractQuestion.__init__(self,
                                  topic,
                                  question_id,
                                  calculated_difficulty,
                                  instructor_difficulty,
                                  avg_answer_time)

    # -------------------------------------------------------------
    # set variables
    # -------------------------------------------------------------

        self._question_text = question_text
        self._answer = answer
        self._image_path = image_path
        self._answer[0] = answer_0
        self._answer[1] = answer_1
        self._answer[2] = answer_2
        self._answer[3] = answer_3
        self._answer[4] = answer_4
        self._answer[5] = answer_5

    # -------------------------------------------------------------
    # database connectors
    # -------------------------------------------------------------

    def get_database_format(self):
        return {
            'question_text': self._question_text,
            'answer': self._answer,
            'answer_0': self._answer[0],
            'answer_1': self._answer[1],
            'answer_2': self._answer[2],
            'answer_3': self._answer[3],
            'answer_4': self._answer[4],
            'answer_5': self._answer[5],
            'question_id': self._question_id,
            'topic': self._topic,
            'user_difficulty': self._calculated_difficulty,
            'instructor_difficulty': self._instructor_difficulty,
            'avg_answer_time': self._avg_answer_time
        }

    def set_from_database(self, question):
        self._topic = question['topic']
        self._question_id = question['question_id']
        self._calculated_difficulty = question['user_difficulty']
        self._instructor_difficulty = question['instructor_difficulty']
        self._avg_answer_time = question['avg_answer_time']
        self._question_text = question['question_text']
        self._answer = question['answer']
        self._answer[0] = question['answer_0']
        self._answer[1] = question['answer_1']
        self._answer[2] = question['answer_2']
        self._answer[3] = question['answer_3']
        self._answer[4] = question['answer_4']
        self._answer[5] = question['answer_5']

    def make_question_from_multiple_choice(self, topic):
        db_connect = multiple_choice_table_access_layer.MultipleChoiceTableAccess()
        result = db_connect.get_question_mc_random_by_topic(topic)
        self.set_from_database(result)
        db_connect.close_connection()
        return True

    def make_question_from_definitions(self, topic):
        db_connect = definitions_table_access_layer.DefinitionTableAccess()
        definition_list = db_connect.get_definition_random_by_topic_multiple(topic)
        coinflip = randint(0, 1)
        definition_index = randint(1, 3)
        primary_question = definition_list[0]
        index_list = [0, 1, 2, 3, 4, 5]
        shuffle(index_list)

        self._topic = primary_question['topic']
        self._question_id = primary_question['question_id']
        self._calculated_difficulty = primary_question['user_difficulty']
        self._instructor_difficulty = primary_question['instructor_difficulty']
        self._avg_answer_time = primary_question['avg_answer_time']

        if coinflip:
            self._question_text = primary_question['word']
            self._answer = primary_question['definition_{}'.format(definition_index)]
            for i in index_list:
                self._answer.append(definition_list[i]['definition_{}'.format(definition_index)])
        else:
            self._question_text = primary_question['definition_{}'.format(definition_index)]
            for i in index_list:
                self._answer.append(definition_list[i]['word'])

        return True

    # -------------------------------------------------------------
    # generic setters and getters
    # -------------------------------------------------------------

    def get_question_text(self):
        return self._question_text

    def set_question_text(self, q_text):
        self._question_text = q_text

    def get_answer(self):
        return self._answer

    def set_answer(self, answer):
        self._answer = answer

    def get_answer_0(self):
        return self._answer[0]

    def set_answer_0(self, answer):
        self._answer[0] = answer

    def get_answer_1(self):
        return self._answer[1]

    def set_answer_1(self, answer):
        self._answer[1] = answer

    def get_answer_2(self):
        return self._answer[2]

    def set_answer_2(self, answer):
        self._answer[2] = answer

    def get_answer_3(self):
        return self._answer[3]

    def set_answer_3(self, answer):
        self._answer[3] = answer

    def get_answer_4(self):
        return self._answer[4]

    def set_answer_4(self, answer):
        self._answer[4] = answer

    def get_answer_5(self):
        return self._answer[5]

    def set_answer_5(self, answer):
        self._answer[5] = answer
