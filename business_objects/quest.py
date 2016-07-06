# make sure to have a function that formats the quest to send to client
from flask import jsonify
import business_objects.CalculationQuestion as Calculation
import business_objects.MultipleChoiceQuestion as MultipleChoice
import business_objects.Definition as Definition
import db_access.db_topic_chapter as topic_chapter_access_layer
from random import randint


class Quest:
    _quest_id = None
    _quest_name = None
    _topic_index = None
    _chapter_index = False
    _number_of_questions = None
    _point_value = None
    _quest_description = None
    _cumulative = None
    _multiple_choice_allowed = None
    _definition_allowed = None
    _daily = False

    def __init__(self,
                 quest_id=None,
                 quest_name=None,
                 topic_index=None,
                 chapter_index=None,
                 number_of_questions=None,
                 point_value=None,
                 quest_description=None,
                 cumulative=False,
                 multiple_choice_allowed=False,
                 definition_allowed=False,
                 daily=False):

        self._quest_id = quest_id
        self._quest_name = quest_name
        self._topic_index = topic_index
        self._chapter_index = chapter_index
        self._number_of_questions = number_of_questions
        self._point_value = point_value
        self._quest_description = quest_description
        self._cumulative = cumulative
        self._multiple_choice_allowed = multiple_choice_allowed
        self._definition_allowed = definition_allowed
        self._daily = daily

    def get_quest_id(self):
        return self._quest_id

    def get_quest_name(self):
        return self._quest_name

    def set_quest_name(self, quest_name):
        self._quest_name = quest_name

    def get_topic_index(self):
        return self._topic_index

    def set_topic_index(self, topic_index):
        self._chapter_index = None
        self._topic_index = topic_index

    def get_chapter_index(self):
        return self._chapter_index

    def set_chapter_index(self, chapter_index):
        self._topic_index = None
        self._chapter_index = chapter_index

    def get_number_of_questions(self):
        return self._number_of_questions

    def set_number_of_questions(self, number_of_questions):
        self._number_of_questions = number_of_questions

    def get_point_value(self, point_value):
        self._point_value = point_value

    def set_point_value(self):
        return self._point_value

    def get_quest_description(self):
        return self._quest_description

    def set_quest_description(self, quest_description):
        self._quest_description = quest_description

    def get_cumulative(self):
        return self._cumulative

    def set_cumulative(self, cumulative):
        self._cumulative = cumulative

    def get_multiple_choice_allowed(self):
        return self._multiple_choice_allowed

    def set_multiple_choice_allowed(self, multiple_choice_allowed):
        self._multiple_choice_allowed = multiple_choice_allowed

    def get_definition_allowed(self):
        return self._definition_allowed

    def set_definition_allowed(self, definition_allowed):
        self._definition_allowed = definition_allowed

    def get_jsonified(self):
        return jsonify(
            quest_id=self._quest_id,
            quest_name=self._quest_name,
            topic_index=self._topic_index,
            chapter_index=self._chapter_index,
            number_of_questions=self._number_of_questions,
            point_value=self._point_value,
            quest_description=self._quest_description,
            cumulative=self._cumulative,
            multiple_choice_allowed=self._multiple_choice_allowed,
            definition_allowed=self._definition_allowed,
            daily=self._daily
            )