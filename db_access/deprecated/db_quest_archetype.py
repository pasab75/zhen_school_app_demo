from random import randint

from db_access.db_general import GeneralDatabaseConnection

table_name = "quest_archetypes"
table_index = "quest_archetype_index"

class QuestTableAccess(GeneralDatabaseConnection):

    # -------------------------------------------------------------
    # class variables
    # -------------------------------------------------------------

    # -------------------------------------------------------------
    # class constructor
    # -------------------------------------------------------------

    def __init__(self):
        GeneralDatabaseConnection.__init__(self)

    # -------------------------------------------------------------
    # READ methods
    # -------------------------------------------------------------

    def get_quest_archetype_by_index(self, index):
        try:
            try:
                db_obj = self.get_row_by_key_value(table_name, table_index, index)
                return db_obj

            except Exception as e:
                print("Error fetching results: " + str(e))
        except Exception as e:
            print("Error connecting: " + str(e))

    def get_quest_archetype_by_chapter_index(self, index):
        try:
            try:
                db_obj = self.get_row_by_key_value(table_name, "chapter_index", index)
                return db_obj

            except Exception as e:
                print("Error fetching results: " + str(e))
        except Exception as e:
            print("Error connecting: " + str(e))

    def get_quest_archetype_by_number_questions(self, num_questions):
        try:
            try:
                db_obj = self.get_row_by_key_value(table_name, "number_of_questions", num_questions)
                return db_obj

            except Exception as e:
                print("Error fetching results: " + str(e))
        except Exception as e:
            print("Error connecting: " + str(e))

    def get_quest_archetype_by_point_value(self, point_value):
        try:
            try:
                db_obj = self.get_row_by_key_value(table_name, "completion_points", point_value)
                return db_obj

            except Exception as e:
                print("Error fetching results: " + str(e))
        except Exception as e:
            print("Error connecting: " + str(e))

    def get_quest_archetype_by_seconds_per_question(self, seconds):
        try:
            try:
                db_obj = self.get_row_by_key_value(table_name, "seconds_per_question", seconds)
                return db_obj

            except Exception as e:
                print("Error fetching results: " + str(e))
        except Exception as e:
            print("Error connecting: " + str(e))

    def get_quest_archetype_by_attributes(self, point_value):
        try:
            try:
                db_obj = self.get_row_by_key_value(table_name, "completion_points", point_value)
                return db_obj

            except Exception as e:
                print("Error fetching results: " + str(e))
        except Exception as e:
            print("Error connecting: " + str(e))

    # -------------------------------------------------------------
    # WRITE methods
    # -------------------------------------------------------------

