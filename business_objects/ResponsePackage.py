from flask import jsonify

# figure out how this should work >.<


class ResponsePackage:
    def __init__(self, response_type, question=None, activity=None):
        self._question = question
        self._activity = activity
        self._response_type = response_type

    def make_json(self):
        return jsonify(response_type=self._response_type,
                       question_id=self._question.get_question_id(),
                       question_text=self._question.get_question_text(),
                       answer_text=self._question.get_answer_list(),
                       activity_text='',
                       activity_description='',
                       point_value='',
                       number_of_questions='',
                       current_question='',
                       )

