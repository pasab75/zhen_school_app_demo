from db_access.db_general import GeneralDatabaseConnection
import business_objects.question as question_obj_generator
from random import shuffle, randint


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
    # question table methods
    # -------------------------------------------------------------

    # -------------------------------------------------------------
    # debug methods
    # -------------------------------------------------------------

    # loads number of randomly generated function to the questions database for testing purposes only
    # remove this function when we go into production
    def load_questions_testing(self, numAdd):
        try:
            for i in range(0, numAdd):
                questionType = str(randint(0, 2))
                topic = str(randint(1, 30))

                answerlist = []

                if questionType == '0':
                    answer = str(randint(0,99999))
                    question_text = ('I am a definition blah blah blah blah blah blah blah my answer is ' + answer)
                    answerlist.append(answer)
                    question = question_obj_generator.question(question_text, answerlist, topic, questionType)

                elif questionType == '1':
                    ranNum = randint(0,5)

                    answerid = str(ranNum)
                    answer = str(ranNum+1)

                    question_text = ('I am a multiple choice question. My answer is ' +
                                  answer + '. My topic is ' + topic + ".")
                    answerlist.append("one")
                    answerlist.append("two")
                    answerlist.append("three")
                    answerlist.append("four")
                    answerlist.append("five")
                    answerlist.append("six")

                    question = question_obj_generator.question(question_text, answerlist, topic, questionType, answerid)

                else:
                    answer = str(randint(0, 100000))
                    question_text = ('I am a calculation type question. My answer is ' +
                                  answer + '. My topic is ' + topic + ".")
                    answerlist.append(answer)

                    question = question_obj_generator.question(question_text, answerlist, topic, questionType)

                self.save_new_row_in_table(question.get_dictionary(), 'questions')

        except Exception as e:
            print("Error loading random shit "+str(e))

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

    # return a random question object given a question type AND a topic
    def get_question_random_by_type_and_topic(self, question_type, topic):
        try:
            try:
                with self.db_connection.cursor() as cursor:
                    sql = "SELECT * FROM questions WHERE question_type = %s AND topic = %s ORDER BY RAND() LIMIT 1;"
                    args = (question_type, topic)
                    print(type(question_type))
                    cursor.execute(sql, args)
                    question = cursor.fetchone()

                    return question

            except Exception as e:
                print("Error fetching results: "+str(e))
        except Exception as e:
                print("Error connecting: "+str(e))

    # returns a random question given a question type AND chapter
    # this uses two previously defined methods to get a random topic given a chapter
    # then pulls a question from that topic
    def get_question_random_by_type_and_chapter(self, question_type, chapter):
        try:
            try:
                topic = self.get_topic_random_by_chapter(chapter)
                return self.get_question_random_by_type_and_topic(question_type, topic)

            except Exception as e:
                print("Error fetching results: "+str(e))
        except Exception as e:
                print("Error connecting: "+str(e))

    # returns a specific question given the unique primary question ID
    def get_question_by_question_id(self, question_id):
        try:
            try:
                with self.db_connection.cursor() as cursor:
                    sql = "SELECT * FROM questions WHERE `question_id`= %s"
                    cursor.execute(sql, question_id)
                    question = question_obj_generator.question()
                    question.set_dictionary(cursor.fetchone())

                    return question
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
                    question = question_obj_generator.question()
                    question.set_dictionary(cursor.fetchone())

                    return question
            except Exception as e:
                print("Error fetching results: "+str(e))
        except Exception as e:
                print("Error connecting: "+str(e))

    # returns all questions that has text in the question text matching the provided string
    # TODO: make this actually work I am guessing we will need to compare regex or something NOT IN A HURRY
    def get_questions_by_question_text(self, text):
        try:
            try:
                with self.db_connection.cursor() as cursor:
                    print("derp I dont do anything yet")
            except Exception as e:
                print("Error fetching results: "+str(e))
        except Exception as e:
                print("Error connecting: "+str(e))

    # this method creates a definition type question by combining 6 different questions from the database
    # it flips a coin to decide whether the answers should be words or definitions
    # it chooses one question to be the "primary question", which means that the word and definition are kept intact
    # it uses the other 5 questions to put in answer distractors
    # it will return a question object and then updates the correct answer field of the primary question using the
    # question_id
    def get_question_def_by_topic(self, topic):
        try:
            try:
                with self.db_connection.cursor() as cursor:
                    sql = ("SELECT * FROM questions "
                           "WHERE topic = %s"
                           " AND "
                           "question_type = 0 "
                           "ORDER BY RAND() "
                           "LIMIT 6;")
                    cursor.execute(sql, topic)
                    questionlist = cursor.fetchall()

                    primary_question = questionlist[0]
                    question_type = questionlist[0]['question_type']

                    print('question type = ' + str(question_type))
                    print('question ID = ' + str(primary_question['question_id']))

                    shuffle(questionlist)
                    correct_index = 0

                    for i in range(len(questionlist)):
                        if questionlist[i] == primary_question:
                            correct_index = i

                    answerlist = []

                    if randint(0, 1) == 1:
                        for i in range(6):
                            answerlist.append(questionlist.pop(0)['answer_a_text'])

                        question = question_obj_generator.question(primary_question['question_text'],
                                                                   answerlist,
                                                                   primary_question['topic_index'],
                                                                   primary_question['question_type'],
                                                                   str(correct_index),
                                                                   primary_question['question_id'])
                    else:
                        for i in range(6):
                            answerlist.append(questionlist.pop(0)['question_text'])

                        question = question_obj_generator.question(primary_question['answer_a_text'],
                                                                   answerlist,
                                                                   primary_question['topic_index'],
                                                                   primary_question['question_type'],
                                                                   str(correct_index),
                                                                   primary_question['question_id'])

                    sql = ("UPDATE `questions` "
                           "SET `correct_answer_index` = %s "
                           "WHERE question_id = %s "
                           ";")

                    args = (question.get_correct_answer_index(), question.get_question_id())
                    cursor.execute(sql, args)

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









