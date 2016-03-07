from flask import jsonify

class question:
    _question_id = ""
    _question_text = ""
    _answers = []
    _answer_index = 0

    def __init__(self, id, q_text, ans_a, ans_b, ans_c, ans_d, ans_e, answer):
        self._question_id = id
        self._question_text = q_text
        if ans_a is not None:
            self._answers.append(ans_a)
        if ans_b is not None:
            self._answers.append(ans_b)
        if ans_c is not None:
            self._answers.append(ans_c)
        if ans_d is not None:
            self._answers.append(ans_d)
        if ans_e is not None:
            self._answers.append(ans_e)
        self._answer_index = answer

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

    def get_jsonified(self):
        return jsonify(question_id=self.get_question_id(),
                       question_text=self.get_question_text(),
                       answers = self.get_answers(),
                       answer_index = self.get_correct_answer_index()
        )