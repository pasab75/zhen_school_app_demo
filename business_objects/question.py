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

    # def get_fieldlist(self):
    #     qtype = self.get_type()
    #     fieldlist = []
    #
    #     fieldlist.append('question_text')
    #     fieldlist.append('answer_a_text')
    #
    #     if qtype == 1:
    #         fieldlist.append('answer_b_text')
    #         fieldlist.append('answer_c_text')
    #         fieldlist.append('answer_d_text')
    #         fieldlist.append('answer_e_text')
    #         fieldlist.append('answer_f_text')
    #         fieldlist.append('answer_num')
    #
    #     fieldlist.append('topic')
    #     fieldlist.append('question_type')
    #
    #     return fieldlist
    #
    # def get_valuelist(self):
    #         qtype = self.get_type()
    #         valuelist = []
    #
    #         valuelist.append(self.get_question_text())
    #         answers = self.get_answers()
    #
    #         for i in range(len(answers)):
    #             valuelist.append(answers[i])
    #
    #         if qtype == 1:
    #             valuelist.append(question.get_correct_answer_index)
    #
    #         valuelist.append(self.get_topic())
    #         valuelist.append(str(qtype))
    #
    #         return valuelist


class Definition(question):

    def __init__(self, id, definition, word, topic):
        self._answers = []

        self._answers.append(word)

        self._question_id = id
        self._question_text = definition

        self._answer_index = 0
        self._topic = topic
        self._type = 0


class MultipleChoice(question):

    def __init__(self, id, q_text, anslist, answer, topic):
        self._answers = []

        for i in range(len(anslist)):
            if anslist[i] is not None and not "":
                self._answers.append(anslist[i])

        self._question_id = id
        self._question_text = q_text

        self._answer_index = answer
        self._topic = topic
        self._type = 1


class FreeResponse(question):

    def __init__(self, id, q_text, answer, topic):
        self._answers = []

        self._answers.append(answer)

        self._question_id = id
        self._question_text = q_text

        self._answer_index = 0
        self._topic = topic
        self._type = 2

