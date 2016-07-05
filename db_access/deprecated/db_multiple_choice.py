from db_access.db_general import GeneralDatabaseConnection

# provides interface to the multiple choice table


class MultipleChoiceTableAccess(GeneralDatabaseConnection):

    # -------------------------------------------------------------
    # class constructor
    # -------------------------------------------------------------

    def __init__(self):
        GeneralDatabaseConnection.__init__(self)

    # -------------------------------------------------------------
    # question table methods
    # -------------------------------------------------------------al

    # -------------------------------------------------------------
    # READ methods
    # -------------------------------------------------------------

    # returns a specific question given the question index
    # question index is a primary key in the multiple choice table
    def get_question_mc_by_index(self, index):
        try:
            try:
                with self.db_connection.cursor() as cursor:
                    sql = "SELECT * FROM multiple_choice WHERE index = %s"
                    cursor.execute(sql, index)

                    return cursor.fetchone()
            except Exception as e:
                print("Error fetching results: " + str(e))
        except Exception as e:
            print("Error connecting: " + str(e))

    # returns a random question
    def get_question_mc_random(self):
        try:
            try:
                with self.db_connection.cursor() as cursor:
                    sql = "SELECT * FROM multiple_choice ORDER BY RAND() LIMIT 1"
                    cursor.execute(sql)
                    question = cursor.fetchone()

                    return question
            except Exception as e:
                print("Error fetching results: " + str(e))
        except Exception as e:
            print("Error connecting: " + str(e))

    # returns a random question by topic index
    def get_question_mc_random_by_topic(self, topic):
        try:
            try:
                with self.db_connection.cursor() as cursor:
                    sql = "SELECT * FROM multiple_choice WHERE topic = %s ORDER BY RAND() LIMIT 1"
                    cursor.execute(sql, topic)
                    question = cursor.fetchone()

                    return question
            except Exception as e:
                print("Error fetching results: " + str(e))
        except Exception as e:
            print("Error connecting: " + str(e))

    # -------------------------------------------------------------
    # WRITE methods
    # -------------------------------------------------------------

    # updates a question already in the database by using the question's question_id field
    def update_from_object_with_primary_key(self, question, primary):
        try:
            self.update_row_in_table(question.get_database_format(), 'definition_questions', primary)
        except Exception as e:
            print("Could not update function: " + str(e))
            return False

    # deletes a question from the database using its index
    def delete_definition_by_index(self, index):
        try:
            self.delete_row_in_table_with_attribute('definition_questions', 'question_id', index)
        except Exception as e:
            print("Could not delete question: " + str(e))

    # saves a new question into the questions database
    # function takes a question object
    # code will null answers that aren't provided
    def save_new_definition_from_object(self, question):
        try:
            self.save_new_row_in_table(question.get_database_format(), 'definition_questions')

        except Exception as e:
            print("Could not save question: " + str(e))
            return False
