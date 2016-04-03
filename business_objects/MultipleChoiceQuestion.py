from business_objects.AbstractQuestion import AbstractQuestion


class MultipleChoiceQuestion(AbstractQuestion):

    def __init__(self,
                 question_text=None,
                 answer_1=None,
                 answer_2=None,
                 answer_3=None,
                 answer_4=None,
                 answer_5=None,
                 answer_6=None,
                 topic=None,
                 question_id=None,
                 user_difficulty=1,
                 instructor_difficulty=None,
                 avg_answer_time=None):

        AbstractQuestion.__init__(self,
                                  topic,
                                  question_id,
                                  user_difficulty,
                                  instructor_difficulty,
                                  avg_answer_time)

        self._question_text = question_text
        self._answer_1 = answer_1
        self._answer_2 = answer_2
        self._answer_3 = answer_3
        self._answer_4 = answer_4
        self._answer_5 = answer_5
        self._answer_6 = answer_6
