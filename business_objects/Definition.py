from flask import jsonify
import db_access.db_definitions as db_definition


class Definition:

    _word_index = None
    _definition = None
    _chapter_index = None

    def __init__(self,
                 word_index=None,
                 definition=None,
                 chapter_index=None):

        self._word_index = word_index
        self._definition = definition
        self._chapter_index = chapter_index

    def get_database_format(self):
        return {
            'word_index': self._word_index,
            'definition': self._definition,
            'chapter_index': self._chapter_index
        }

    def set_from_database(self, database_definition):
        self._word_index = database_definition['word_index']
        self._definition = database_definition['definition']
        self._chapter_index = database_definition['chapter_index']

    def get_json(self):
        return {
            'word_index': self._word_index,
            'definition': self._definition,
            'chapter_index': self._chapter_index
        }

    def get_json_min(self):
        return {
            'index': self._word_index,
            'text': self._definition,
        }

    def get_definition_random_by_chapter_index(self, index):
        self.generate_definition_random_from_chapter_index(index)
        return self

    def get_definition_list_random_by_chapter_index(self, index, number_of_questions=6):
        self.generate_definition_list_random_from_chapter_index(index, number_of_questions)
        return self

    def generate_definition_random_from_chapter_index(self, index):
        db_def = db_definition.DefinitionTableAccess()
        self.set_from_database(db_def.get_definition_random_by_chapter_index(index))
        db_def.close_connection()

    def generate_definition_list_random_from_chapter_index(self, index, number_of_questions):
        db_def = db_definition.DefinitionTableAccess()
        self.set_from_database(db_def.get_definition_list_random_by_chapter_index(index, number_of_questions))
        db_def.close_connection()

    def get_definition_random_by_chapter(self, chapter):
        self.generate_definition_random_from_chapter_index(chapter)
        return self

    def generate_random_from_chapter(self, chapter):
        db_def = db_definition.DefinitionTableAccess()
        self.set_from_database(db_def.get_definition_random_by_chapter(chapter))
        db_def.close_connection()

    def get_definition_random_from_word(self, word):
        self.generate_random_from_word(word)
        return self

    def generate_random_from_word(self, word):
        db_def = db_definition.DefinitionTableAccess()
        self.set_from_database(db_def.get_definition_by_word_index(word.get_index()))
        db_def.close_connection()

    def get_definition_random_from_word_index(self, word):
        self.generate_random_from_word_index(word)
        return self

    def generate_random_from_word_index(self, index):
        db_def = db_definition.DefinitionTableAccess()
        self.set_from_database(db_def.get_definition_by_word_index(index))
        db_def.close_connection()

    def get_word_index(self):
        return self._word_index

    def get_definition(self):
        return self._definition

    # only call this if you're sure this doesn't exist in the db already
    def save_new(self):
        try:
            db_def = db_definition.DefinitionTableAccess()
            db_def.save_new_definition_from_object(self.get_database_format())
            db_def.close_connection()
            return True
        except Exception as e:
            print("Could not delete question: " + str(e))
            return False
