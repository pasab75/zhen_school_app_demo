class AbstractQuestion:
    _topic = None
    _question_id = None
    _calculated_difficulty = 1
    _instructor_difficulty = 1
    _avg_answer_time = None

    def __init__(self,
                 topic=None,
                 question_id=None,
                 user_difficulty=1,
                 instructor_difficulty=None,
                 avg_answer_time=None):

        self._topic = topic
        self._question_id = question_id
        self._calculated_difficulty = user_difficulty
        self._instructor_difficulty = instructor_difficulty
        self._avg_answer_time = avg_answer_time

    def get_topic(self):
        return self._topic

    def set_topic(self, topic):
        self._topic = topic

    def get_question_id(self):
        return self._question_id

    def get_user_difficulty(self):
        return self._calculated_difficulty

    def set_user_difficulty(self, difficulty):
        self._calculated_difficulty = difficulty

    def get_instructor_difficulty(self):
        return self._instructor_difficulty

    def set_instructor_difficulty(self, difficulty):
        self._instructor_difficulty = difficulty

    def get_avg_answer_time(self):
        return self._avg_answer_time

    def set_avg_answer_time(self, time):
        self._avg_answer_time = time

