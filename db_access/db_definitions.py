from db_access.db_general import GeneralDatabaseConnection

table_name = "definitions"


class DefinitionTableAccess(GeneralDatabaseConnection):

    # -------------------------------------------------------------
    # class constructor
    # -------------------------------------------------------------

    def __init__(self):
        GeneralDatabaseConnection.__init__(self)

    # -------------------------------------------------------------
    # fetch db_obj methods
    # -------------------------------------------------------------

    def get_definition_by_word_index(self, index):
        try:
            try:
                db_obj = self.get_row_random_by_key(table_name, "word_index", index)
                return db_obj

            except Exception as e:
                print("Error fetching results: " + str(e))
        except Exception as e:
            print("Error connecting: " + str(e))

    def get_word_random(self):
        try:
            try:
                db_obj = self.get_row_random(table_name)
                return db_obj
            except Exception as e:
                print("Error fetching results: " + str(e))
        except Exception as e:
            print("Error connecting: " + str(e))

    def get_definition_random_by_chapter(self, chapter):
        try:
            try:
                db_obj = self.get_row_random_by_key(table_name,
                                                    "chapter",
                                                    chapter.get_chapter_name())
                return db_obj

            except Exception as e:
                print("Error fetching results: " + str(e))
        except Exception as e:
            print("Error connecting: " + str(e))

    def get_definition_random_by_chapter_index(self, chapter_index):
        try:
            try:
                db_obj = self.get_row_random_by_key(table_name, "chapter_index", chapter_index)
                return db_obj

            except Exception as e:
                print("Error fetching results: " + str(e))
        except Exception as e:
            print("Error connecting: " + str(e))

    # -------------------------------------------------------------
    # WRITE methods
    # -------------------------------------------------------------

    # updates a question already in the database by using the question's question_id field
    def update_from_object_with_primary_key(self, definition, primary):
        try:
            self.update_row_in_table(definition.get_database_format(), table_name, primary)
        except Exception as e:
            print("Could not update function: " + str(e))
            return False

    # deletes a question from the database using its question_id
    def delete_definition_by_id(self, index):
        try:
            self.delete_row_in_table_with_attribute(table_name, 'definition', index)
        except Exception as e:
            print("Could not delete question: " + str(e))

    # saves a new question into the questions database
    # function takes a question object
    # code will null answers that aren't provided
    def save_new_definition_from_object(self, definition):
        try:
            self.save_new_row_in_table(definition.get_database_format(), table_name)

        except Exception as e:
            print("Could not save question: " + str(e))
            return False
