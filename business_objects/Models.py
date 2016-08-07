from peewee import *

database = MySQLDatabase('testdb', **{'password': 'carhorsebatterysuccess', 'user': 'appuser'})


class UnknownField(object):
    pass


class BaseModel(Model):
    class Meta:
        database = database


class ActivityLogEntry(BaseModel):
    correct = IntegerField()
    current_word_index = IntegerField()
    datetime = DateTimeField()
    datetime_quest_started = DateTimeField()
    datetime_question_started = DateTimeField(null=True)
    device_family = CharField(null=True)
    device_model = CharField(null=True)
    device_type = IntegerField(null=True)
    ip_address = CharField(null=True)
    is_daily = IntegerField()
    is_timed = IntegerField(null=True)
    latitude = FloatField(null=True)
    longitude = FloatField(null=True)
    number_of_questions = IntegerField()
    user_id = CharField(db_column='user_id')

    class Meta:
        db_table = 'activity_log'


class Chapter(BaseModel):
    chapter_index = PrimaryKeyField()
    chapter_name = CharField(null=True)

    class Meta:
        db_table = 'chapters'

    def get_json_min(self):
        data = self._data

        key_list = ()

        for key in key_list:
            data.pop(key, None)

        return data


class Classroom(BaseModel):
    class_code = CharField(primary_key=True)
    current_chapter = ForeignKeyField(db_column='current_chapter', rel_model=Chapter, to_field='chapter_index')
    daily_exp_base = IntegerField()
    max_multiplier = IntegerField()
    number_dailies_allowed = IntegerField()
    daily_point_value = IntegerField()

    class Meta:
        db_table = 'classrooms'


class Word(BaseModel):
    avg_answer_time = IntegerField(null=True)
    calculated_difficulty = IntegerField(null=True)
    chapter_index = ForeignKeyField(db_column='chapter_index', rel_model=Chapter, to_field='chapter_index')
    instructor_difficulty = IntegerField(null=True)
    word = CharField()
    word_index = PrimaryKeyField()

    class Meta:
        db_table = 'words'

    def get_json_min(self):
        data = {
            'text': self._data.word,
            'index': self._data.word_index
        }

        return data


class Definition(BaseModel):
    chapter_index = ForeignKeyField(db_column='chapter_index', rel_model=Chapter, to_field='chapter_index')
    definition = CharField(primary_key=True)
    word_index = ForeignKeyField(db_column='word_index', rel_model=Word, to_field='word_index')

    class Meta:
        db_table = 'definitions'

    def get_json_min(self):
        data = {
            'text': self._data.definition,
            'index': self._data.word_index
        }

        return data


class QuestLogEntry(BaseModel):
    chapter_index = IntegerField(null=True)
    cumulative = IntegerField()
    datetime_quest_completed = DateTimeField()
    datetime_quest_started = DateTimeField()
    device_family = CharField(null=True)
    device_model = CharField(null=True)
    device_type = IntegerField(null=True)
    ip_address = CharField(null=True)
    is_daily = IntegerField()
    is_timed = IntegerField(null=True)
    latitude = FloatField(null=True)
    longitude = FloatField(null=True)
    number_correct = IntegerField()
    number_of_questions = IntegerField()
    user_id = CharField(db_column='user_id')

    class Meta:
        db_table = 'quest_log'

    def get_json_min(self):
        data = self._data

        key_list = (
            'class_code'
        )

        for key in key_list:
            data.pop(key, None)

        return data


class Reward(BaseModel):
    class_code = ForeignKeyField(db_column='class_code', rel_model=Classroom, to_field='class_code')
    required_points = IntegerField()
    reward_description = CharField()
    reward_name = CharField()

    class Meta:
        db_table = 'rewards'

    def get_json_min(self):
        data = self._data

        key_list = (
            'class_code'
        )

        for key in key_list:
            data.pop(key, None)

        return data

