from flask import jsonify


class question:
    _question_id = ""
    _question_text = ""
    _answers = []
    _answer_index = 0
    _topic = None
    _type = None

    def __init__(self, id, q_text, ans_a, ans_b, ans_c, ans_d, ans_e, ans_f, answer, topic, type):
        self._answers = []
        self._question_id = id
        self._question_text = q_text
        if ans_a is not None:
            self._answers.append(ans_a)
        if ans_b is not None:
            self._answers.append(ans_b)
        if ans_c is not None and ans_c != "":
            self._answers.append(ans_c)
        if ans_d is not None and ans_d != "":
            self._answers.append(ans_d)
        if ans_e is not None and ans_e != "":
            self._answers.append(ans_e)
        if ans_f is not None and ans_f != "":
            self._answers.append(ans_f)
        self._answer_index = answer
        self._topic = topic
        self._type = type

    def get_correct_answer_index(self):
        return self._answer_index

    def get_question_text(self):
        return self._question_text

    def get_answers(self):
        return self._answers

    def get_answer_text(self, index):
        if index < len(self._answers):
            return self._answers[index]
        else:
            return "index out of bounds"

    def get_question_id(self):
        return self._question_id

    def get_chapter(self):
        return self._chapter

    def get_topic(self):
        return self._topic

    def get_type(self):
        return self._type

    def get_jsonified(self):
        return jsonify(
                       questionID = self.get_question_id(),
                       question_text=self.get_question_text(),
                       answers=self.get_answers(),
                       )

    def set_correct_answer_index(self, index):
        self._answer_index = index

    def set_question_text(self, text):
        self._question_text = text

    def set_answers(self, answers):
        self._answers = answers

    def set_chapter(self, chapter):
        self._chapter = chapter

    def set_topic(self, topic):
        self._topic = topic

    def set_type(self, type):
        self._type = type