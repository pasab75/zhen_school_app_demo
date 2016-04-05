from db_access.db_general import GeneralDatabaseConnection

class QuestionTableAccess(GeneralDatabaseConnection):

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

    # returns which chapter a certain topic corresponds to
    def get_chapter_by_topic(self, topic):
        try:
            try:
                with self.db_connection.cursor() as cursor:
                    sql = "SELECT * FROM topic_chapter WHERE topic = %s"
                    cursor.execute(sql, topic)
                    request = cursor.fetchone()

                    return request['chapter']

            except Exception as e:
                print("Error fetching results: "+str(e))
        except Exception as e:
                print("Error connecting: "+str(e))

    # returns a random topic from a specific chapter
    def get_topic_random_by_chapter(self, chapter):
        try:
            try:
                with self.db_connection.cursor() as cursor:
                    sql = "SELECT * FROM topic_chapter WHERE chapter = %s ORDER BY RAND() LIMIT 1"
                    cursor.execute(sql, chapter)
                    request = cursor.fetchone()

                    return request['topic_index']

            except Exception as e:
                print("Error fetching results: "+str(e))
        except Exception as e:
                print("Error connecting: "+str(e))

    # returns a random question object given a type of question
    # this question can be from any topic
    def get_question_random_by_type(self, question_type):
        try:
            try:
                with self.db_connection.cursor() as cursor:
                    sql = "SELECT * FROM questions WHERE question_type = %s ORDER BY RAND() LIMIT 1"

                    cursor.execute(sql, question_type)
                    question = question_obj_generator.question()
                    question.set_dictionary(cursor.fetchone())

                    return question

            except Exception as e:
                print("Error fetching results: "+str(e))
        except Exception as e:
                print("Error connecting: "+str(e))

    # returns a specific question given the unique primary question ID
    def get_question_by_question_id(self, question_id):
        try:
            try:
                with self.db_connection.cursor() as cursor:
                    sql = "SELECT * FROM questions WHERE question_id = %s"
                    cursor.execute(sql, question_id)

                    return cursor.fetchone()
            except Exception as e:
                print("Error fetching results: "+str(e))
        except Exception as e:
                print("Error connecting: "+str(e))

    # returns a random question from the entire questions database
    def get_question_random(self):
        try:
            try:
                with self.db_connection.cursor() as cursor:
                    sql = "SELECT * FROM questions ORDER BY RAND() LIMIT 1;"
                    cursor.execute(sql)
                    question = cursor.fetchone()

                    return question
            except Exception as e:
                print("Error fetching results: "+str(e))
        except Exception as e:
                print("Error connecting: "+str(e))

    # -------------------------------------------------------------
    # WRITE methods
    # -------------------------------------------------------------

    # updates a question already in the database by using the question's question_id field
    def update_question_from_object_with_primarykey(self, question, primary):
        try:
            self.update_row_in_table(question.get_dictionary(), 'questions', primary)
        except Exception as e:
            print("Could not update function: "+str(e))
            return False

    # deletes a question from the database using its question_id
    def delete_question_by_questionid(self, question_id):
        try:
            self.delete_row_in_table_with_attribute('questions', 'question_id', question_id)
        except Exception as e:
            print("Could not delete question: " + str(e))

    # saves a new question into the questions database
    # function takes a question object
    # code will null answers that aren't provided
    def save_new_question_from_question_object(self, question):
        try:
            self.save_new_row_in_table(question.get_dictionary(), 'questions')

        except Exception as e:
            print("Could not save question: "+str(e))
            return False









