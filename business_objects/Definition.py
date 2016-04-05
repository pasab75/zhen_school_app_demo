from business_objects.AbstractQuestion import AbstractQuestion
import db_access.db_definitions as definitions_table_access_layer


class Definition(AbstractQuestion):

    def __init__(self,
                 question_text=None,
                 answer=None,
                 answer_1=None,
                 answer_2=None,
                 answer_3=None,
                 answer_4=None,
                 answer_5=None,
                 answer_6=None,
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

        self._question_text = question_text
        self._answer = answer
        self._answer_1 = answer_1
        self._answer_2 = answer_2
        self._answer_3 = answer_3
        self._answer_4 = answer_4
        self._answer_5 = answer_5
        self._answer_6 = answer_6

    def get_database_format(self):
        return {
            'question_text': self._question_text,
            'answer': self._answer,
            'answer_1': self._answer_1,
            'answer_2': self._answer_2,
            'answer_3': self._answer_3,
            'answer_4': self._answer_4,
            'answer_5': self._answer_5,
            'answer_6': self._answer_6,
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
        self._answer_1 = question['answer_1']
        self._answer_2 = question['answer_2']
        self._answer_3 = question['answer_3']
        self._answer_4 = question['answer_4']
        self._answer_5 = question['answer_5']
        self._answer_6 = question['answer_6']

    # TODO: change db access layer to
    def construct_from_db_id(self, question_id):
        dbconnect = definitions_table_access_layer.QuestionTableAccess()
        result = dbconnect.get_question_by_question_id(question_id)
        self.set_from_database(result)
        dbconnect.close_connection()

    def get_question_text(self):
        return self._question_text

    def set_question_text(self, q_text):
        self._question_text = q_text

    def get_answer(self):
        return self._answer

    def set_answer(self, answer):
        self._answer = answer
