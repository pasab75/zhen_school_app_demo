import datetime
from logging import exception
from config import *

from business_objects.Models import *
from business_objects.DefinitionQuestion import DefinitionQuestion


class User(BaseModel):
    chapter_index = IntegerField(null=True)
    class_code = ForeignKeyField(db_column='class_code', null=True, rel_model=Classroom, to_field='class_code')
    completion_points = IntegerField(null=True)
    cumulative = IntegerField(null=True)
    current_progress = IntegerField(null=True)
    current_word_index = IntegerField(null=True)
    datetime_quest_started = DateTimeField(null=True)
    datetime_question_started = DateTimeField(null=True)
    e_mail = CharField()
    first_name = CharField(null=True)
    is_on_daily = IntegerField(null=True)
    is_timed = IntegerField(null=True)
    last_name = CharField(null=True)
    multiplier = IntegerField(null=True)
    number_correct = IntegerField(null=True)
    number_of_questions = IntegerField(null=True)
    points_earned_current_quest = IntegerField(null=True)
    points_per_question = IntegerField(null=True)
    question_type = IntegerField(null=True)
    reward_level = IntegerField()
    total_points = IntegerField(null=True)
    user_id = CharField(db_column='user_id', primary_key=True)
    user_role = IntegerField()

    def get_json_min(self):
        data = self._data

        key_list = (
            'class_code',
            'current_word_index',
            'datetime_quest_started',
            'datetime_question_started',
            'e_mail',
            'user_role'
        )

        for key in key_list:
            data.pop(key, None)

        return data

    class Meta:
        db_table = 'users'

    #########################################################################################
    # Convenience Methods
    #########################################################################################

    def start_new_quest(self, request):
        client_choices = request.json
        requested_chapter_index = client_choices['chapter_index']
        requested_is_timed = client_choices['is_timed']
        requested_number_of_questions = client_choices['number_of_questions']
        requested_cumulative = client_choices['cumulative']
        requested_question_type = client_choices['question_type']
        requested_is_daily = client_choices['is_daily']

        updated_user = update_user_quest(
            self,
            chapter_index=requested_chapter_index,
            is_timed=requested_is_timed,
            number_of_questions=requested_number_of_questions,
            cumulative=requested_cumulative,
            question_type=requested_question_type,
            is_daily=requested_is_daily
        )

        make_quest_log_entry(self, request)

        return updated_user

    def update_user_quest(
            user,
            chapter_index=None,
            is_timed=None,
            number_of_questions=None,
            cumulative=False,
            question_type=None,
            is_daily=None
    ):
        try:
            class_code = user.class_code
            number_correct = 0
            current_progress = 0
            points_per_question = 10

            valid_num_questions = number_of_question_options
            valid_bool = [True, False]

            if is_daily:
                current_class = Classroom.get(Classroom.class_code == class_code)
                chapter_index = current_class.chapter_index

                is_timed = True
                number_of_questions = 50
                cumulative = True
                question_type = 3

            if number_of_questions not in valid_num_questions or is_timed not in valid_bool or cumulative not in valid_bool:
                raise exception(500, "You have chosen invalid quest options.")

            if is_timed:
                points_per_question += 3

            if cumulative:
                points_per_question += 1 * (chapter_index - 1)

            completion_points = 20 * number_of_questions

            user.chapter_index = chapter_index
            user.current_progress = current_progress
            user.number_correct = number_correct
            user.completion_points = completion_points
            user.is_timed = is_timed
            user.points_per_question = points_per_question
            user.number_of_questions = number_of_questions
            user.cumulative = cumulative
            user.question_type = question_type
            user.is_on_daily = is_daily

            user.save()

            return user

        except Exception as ex:
            # TODO: change prints to logger
            print("Error: " + str(ex))
            raise ex

    def drop_user_quest(self):
        self.chapter_index = None
        self.completion_points = None
        self.cumulative = None
        self.current_progress = 0
        self.current_word_index = None
        self.datetime_question_started = None
        self.datetime_quest_started = None
        self.is_on_daily = None
        self.is_timed = None
        self.multiplier = 1
        self.number_correct = 0
        self.number_of_questions = None
        self.points_earned_current_quest = 0
        self.points_per_question = None
        self.question_type = None

        self.save()

        return self

    def start_new_question(self, new_question):
        self.current_word_index = new_question.word_index
        self.datetime_question_started = datetime.datetime.now()

        self.save()

        return self