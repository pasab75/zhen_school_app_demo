from flask import jsonify


class question:
    _question_id = ""
    _question_text = ""
    _answers = []
    _answer_index = 0
    _topic = None
    _type = None

    def __init__(self, id, q_text, anslist, answer, topic, question_type):
        self._answers = []

        for i in range(len(anslist)):
            if anslist[i] is not None and not "":
                self._answers.append(anslist[i])

        self._question_id = id
        self._question_text = q_text

        self._answer_index = answer
        self._topic = topic
        self._type = question_type

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

    def set_topic(self, topic):
        self._topic = topic

    def set_type(self, question_type):
        self._type = question_type
