from db_access.db_general import GeneralDatabaseConnection
import business_objects.DefinitionQuestion as questionGenerator
from random import shuffle, randint, choice


# provides interface to the definition question table
# all methods should return a DefinitionQuestion object!

class DefinitionQuestionTableAccess(GeneralDatabaseConnection):

    # -------------------------------------------------------------
    # class constructor
    # -------------------------------------------------------------

    def __init__(self):
        GeneralDatabaseConnection.__init__(self)

    # -------------------------------------------------------------
    # question table methods
    # -------------------------------------------------------------

    # -------------------------------------------------------------
    # debug methods
    # -------------------------------------------------------------

    # loads number of randomly generated function to the questions database for testing purposes only
    # remove this function when we go into production
    def initialize_definition_questions(self, num_questions):
        try:
            for i in range(0, num_questions):
                topic = str(randint(1, 100))
                difficulty = str(randint(1, 10))

                word = str(randint(0, 99999))
                definition_1 = ('I am definition number 1. My difficulty level is '+
                                difficulty +
                                '. My corresponding word is ' +
                                word)
                definition_2 = ('I am definition number 2. My difficulty level is ' +
                                difficulty +
                                ', My corresponding word is ' +
                                word)
                definition_3 = ('I am definition number 3. My difficulty level is ' +
                                difficulty +
                                '. My corresponding word is ' +
                                word)

                question = questionGenerator.DefinitionQuestion(word=word,
                                                                definition_1=definition_1,
                                                                definition_2=definition_2,
                                                                definition_3=definition_3,
                                                                topic=topic,
                                                                instructor_difficulty=difficulty)

                self.save_new_row_in_table(question.get_database_format(), 'definition_questions')

        except Exception as e:
            print("Error loading random shit "+str(e))

    # -------------------------------------------------------------
    # READ methods
    # -------------------------------------------------------------

    # -------------------------------------------------------------
    # WRITE methods
    # -------------------------------------------------------------

    # updates a question already in the database by using the question's question_id field
    def update_question_from_object_with_primary_key(self, question, primary):
        try:
            self.update_row_in_table(question.get_database_format(), 'definition_questions', primary)
        except Exception as e:
            print("Could not update function: " + str(e))
            return False

    # deletes a question from the database using its question_id
    def delete_question_by_question_id(self, question_id):
        try:
            self.delete_row_in_table_with_attribute('definition_questions', 'question_id', question_id)
        except Exception as e:
            print("Could not delete question: " + str(e))

    # saves a new question into the questions database
    # function takes a question object
    # code will null answers that aren't provided
    def save_new_question_from_question_object(self, question):
        try:
            self.save_new_row_in_table(question.get_database_format(), 'definition_questions')

        except Exception as e:
            print("Could not save question: " + str(e))
            return False
