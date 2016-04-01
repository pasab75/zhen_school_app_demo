class abstract_question():
    _question_text = None
    _topic = None
    _question_id = None
    _user_difficulty = 1
    _instructor_difficulty = 1
    _avg_answer_time = None

    def __init__(self, question_text=None, topic=None, question_id=None,
                 user_difficulty=1, instructor_difficulty=None, avg_answer_time=None):
        self._question_text = question_text
        self._topic = topic
        self._question_id = question_id
        self._user_difficulty = user_difficulty
        self._instructor_difficulty = instructor_difficulty
        self._avg_answer_time = avg_answer_time