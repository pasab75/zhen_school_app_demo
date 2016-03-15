from flask import jsonify

class question():
    def __init__(self, question_text=None, anslist=None, topic=None,
                 question_type=None, answer_num=None, question_id=None):
        self._dictionary = {'question_id': question_id,
                            'question_text': question_text,
                            'answer_a_text': None,
                            "answer_b_text": None,
                            "answer_c_text": None,
                            "answer_d_text": None,
                            "answer_e_text": None,
                            "answer_f_text": None,
                            'answer_num': answer_num,
                            'topic': topic,
                            'question_type': question_type,
                            }

        for i in 'abcdef':
            if anslist:
                self._dictionary['answer_{}_text'.format(i)] = anslist.pop(0)

    def set_dictionary(self, dictionary):
        self._dictionary = dictionary

    def get_dictionary(self):
        return self._dictionary

    def get_jsonified(self):
        return jsonify(
                       question_id=self.get_question_id(),
                       question_text=self.get_question_text(),
                       answer_text=self.get_answer_list(),
                       )

    def get_answer_list(self):
        answer_list = []
        for i in 'abcdef':
            answer_list.append(self._dictionary['answer_{}_text'.format(i)])
        return answer_list

    def get_value(self, key):
        try:
            return self._dictionary[key]
        except Exception as e:
            print("This question does not have that key. " + str(e))

    def get_correct_answer_index(self):
        return self._dictionary['answer_num']

    def get_question_text(self):
        return self._dictionary['question_text']

    def get_question_id(self):
        return self._dictionary['question_id']

    def get_topic(self):
        return self._dictionary['topic']

    def get_type(self):
        return self._dictionary['question_type']

    def set_correct_answer_index(self, index):
        self._dictionary['answer_num'] = index

    def set_question_text(self, text):
        self._dictionary['question_text'] = text

    def set_answers(self, answers):
        self._dictionary['answer_a_text'] = answers

    def set_topic(self, topic):
        self._dictionary['topic'] = topic

    def set_type(self, question_type):
        self._dictionary['question_type'] = question_type


