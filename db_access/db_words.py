from db_access.db_general import GeneralDatabaseConnection
import random

table_name = "words"


class WordTableAccess(GeneralDatabaseConnection):

    # -------------------------------------------------------------
    # class constructor
    # -------------------------------------------------------------

    def __init__(self):
        GeneralDatabaseConnection.__init__(self)

    def get_word_by_index(self, index):
        try:
            try:
                db_obj = self.get_row_by_key_value(table_name,"index",index)
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

    def get_word_random_by_chapter(self, chapter, number_wanted=1):
        try:
            try:
                db_obj = self.get_row_random_by_key(table_name, "chapter", chapter.get_chapter_name(), number=number_wanted)
                return db_obj

            except Exception as e:
                print("Error fetching results: " + str(e))
        except Exception as e:
            print("Error connecting: " + str(e))

    def get_word_random_by_chapter_index(self, chapter_index, number_wanted=1):
        try:
            try:
                db_obj = self.get_row_random_by_key(table_name, "chapter_index", chapter_index, number=number_wanted)
                return db_obj

            except Exception as e:
                print("Error fetching results: " + str(e))
        except Exception as e:
            print("Error connecting: " + str(e))
    # -------------------------------------------------------------
    # WRITE methods
    # -------------------------------------------------------------

    # updates a word already in the database by using the word question_id field
    def update_word_by_index(self, word, index):
        try:
            self.update_row_in_table(word.get_database_format(), table_name, index)
        except Exception as e:
            print("Could not update word: " + str(e))
            return False

    # deletes a word from the database using its index
    def delete_word_by_index(self, index):
        try:
            self.delete_row_in_table_with_attribute(table_name, 'index', index)
        except Exception as e:
            print("Could not delete word: " + str(e))

    # saves a new question into the questions database
    # function takes a question object
    # code will null answers that aren't provided
    def save_new_word_from_object(self, word):
        try:
            self.save_new_row_in_table(word.get_database_format(), table_name)

        except Exception as e:
            print("Could not save question: " + str(e))
            return False