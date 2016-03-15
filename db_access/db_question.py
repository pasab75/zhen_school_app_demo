import pymysql.cursors
from db_access.db_general import GeneralDatabaseConnection
import business_objects.question as question_obj_generator
from random import randint, shuffle


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
    # currently this function supports only definitions questions and multiple choice questions
    # TODO: add support for calculation (free response) questions
    def load_questions_testing(self, numAdd):
        try:
            for i in range(0, numAdd):
                questionType = str(randint(0, 2))
                topic = "topic index " + str(randint(0, 4))

                answerlist = []

                if questionType == '0':
                    answer = str(randint(0,99999))
                    question_text = ('I am a definition blah blah blah blah blah blah blah my answer is ' + answer)
                    answerlist.append(answer)
                    question = question_obj_generator.question(None, question_text, answerlist, None, topic, questionType)

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

                    question = question_obj_generator.question(None, question_text, answerlist, answerid, topic, questionType)

                else:
                    answer = str(randint(0, 100000))
                    question_text = ('I am a calculation type question. My answer is ' +
                                  answer + '. My topic is ' + topic + ".")
                    answerlist.append(answer)

                    question = question_obj_generator.question(None, question_text, answerlist, None, topic, questionType)

                    print(question.get_dictionary())

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

                    return request['topic']

            except Exception as e:
                print("Error fetching results: "+str(e))
        except Exception as e:
                print("Error connecting: "+str(e))

    # returns a random question object given a type of question
    # this question can be from any topic
    def get_question_random_by_type(self, type):
        try:
            try:
                with self.db_connection.cursor() as cursor:
                    question = None

                    sql = "SELECT * FROM questions WHERE question_type = %s ORDER BY RAND() LIMIT 1"
                    cursor.execute(sql, type)
                    request = cursor.fetchone()

                    answerlist = []
                    answerlist.append(request['answer_a_text'])
                    answerlist.append(request['answer_b_text'])
                    answerlist.append(request['answer_c_text'])
                    answerlist.append(request['answer_d_text'])
                    answerlist.append(request['answer_e_text'])
                    answerlist.append(request['answer_f_text'])
                    question = question_obj_generator.question(request['question_id'],
                                                               request['question_text'],
                                                               answerlist,
                                                               request['answer_num'],
                                                               request['topic'],
                                                               request['question_type'])
                    return question
            except Exception as e:
                print("Error fetching results: "+str(e))
        except Exception as e:
                print("Error connecting: "+str(e))

    # return a random question object given a question type AND a topic
    def get_question_random_by_type_topic(self, type, topic):
        try:
            try:
                with self.db_connection.cursor() as cursor:
                    question = None
                    sql = "SELECT * FROM questions WHERE question_type = %s AND topic = %s ORDER BY RAND() LIMIT 1;"
                    args = (type, topic)
                    cursor.execute(sql, args)
                    request = cursor.fetchone()

                    answerlist = []
                    answerlist.append(request['answer_a_text'])
                    answerlist.append(request['answer_b_text'])
                    answerlist.append(request['answer_c_text'])
                    answerlist.append(request['answer_d_text'])
                    answerlist.append(request['answer_e_text'])
                    answerlist.append(request['answer_f_text'])
                    question = question_obj_generator.question(request['question_id'],
                                                               request['question_text'],
                                                               answerlist,
                                                               request['answer_num'],
                                                               request['topic'],
                                                               request['question_type'])
                    return question

            except Exception as e:
                print("Error fetching results: "+str(e))
        except Exception as e:
                print("Error connecting: "+str(e))

    # returns a random question given a question type AND chapter
    # this uses two previously defined methods to get a random topic given a chapter
    # then pulls a question from that topic
    def get_question_random_by_type_chapter(self, type, chapter):
        try:
            try:
                topic = self.get_topic_random_by_chapter(chapter)
                self.get_question_random_by_type_topic(type, topic)

            except Exception as e:
                print("Error fetching results: "+str(e))
        except Exception as e:
                print("Error connecting: "+str(e))

    # returns a specific question given the unique primary question ID
    def get_question_by_id(self, question_id):
        try:
            try:
                with self.db_connection.cursor() as cursor:
                    question = None
                    sql = "SELECT * FROM questions WHERE `question_id`= %s"
                    cursor.execute(sql, question_id)
                    request = cursor.fetchone()

                    answerlist = []
                    answerlist.append(request['answer_a_text'])
                    answerlist.append(request['answer_b_text'])
                    answerlist.append(request['answer_c_text'])
                    answerlist.append(request['answer_d_text'])
                    answerlist.append(request['answer_e_text'])
                    answerlist.append(request['answer_f_text'])
                    question = question_obj_generator.question(request['question_id'],
                                                               request['question_text'],
                                                               answerlist,
                                                               request['answer_num'],
                                                               request['topic'],
                                                               request['question_type'])
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
                    question = None
                    sql = "SELECT * FROM questions ORDER BY RAND() LIMIT 1;"
                    cursor.execute(sql)
                    request = cursor.fetchone()
                    answerlist = []
                    answerlist.append(request['answer_a_text'])
                    answerlist.append(request['answer_b_text'])
                    answerlist.append(request['answer_c_text'])
                    answerlist.append(request['answer_d_text'])
                    answerlist.append(request['answer_e_text'])
                    answerlist.append(request['answer_f_text'])
                    question = question_obj_generator.question(request['question_id'],
                                                               request['question_text'],
                                                               answerlist,
                                                               request['answer_num'],
                                                               request['topic'],
                                                               request['question_type'])
                    return question
            except Exception as e:
                print("Error fetching results: "+str(e))
        except Exception as e:
                print("Error connecting: "+str(e))

    # returns all questions that has text in the question text matching the provided string
    # TODO: make this actually work I am guessing we will need to compare regex or something NOT IN A HURRY
    def get_questionlist_by_questiontext(self, text):
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
                    questions = cursor.fetchall()
                    primary_question = questions[0]
                    question_type = questions[0]['question_type']

                    print('question type = ' + str(question_type))
                    print('question ID = ' + str(primary_question['question_id']))

                    shuffle(questions)
                    correct_index = 0

                    for i in range(len(questions)):
                        if questions[i] == primary_question:
                            correct_index = i

                    answerlist = []



                    if randint(0, 1) == 1:
                        for i in range(6):
                            answerlist.append(questions.pop(0)['answer_a_text'])

                        question = question_obj_generator.question(primary_question['question_id'],
                                                                   primary_question['question_text'],
                                                                   answerlist,
                                                                   str(correct_index),
                                                                   primary_question['topic'],
                                                                   primary_question['question_type'])
                    else:
                        for i in range(6):
                            answerlist.append(questions.pop(0)['question_text'])

                        question = question_obj_generator.question(primary_question['question_id'],
                                                                   primary_question['answer_a_text'],
                                                                   answerlist,
                                                                   str(correct_index),
                                                                   primary_question['topic'],
                                                                   primary_question['question_type'])

                    sql = ("UPDATE `questions` "
                           "SET `answer_num` = %s "
                           "WHERE question_id = %s "
                           ";")

                    args = (correct_index, primary_question['question_id'])
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
    def update_question_from_object(self, question):
        try:
            try:
                with self.db_connection.cursor() as cursor:
                    answers = question.get_answers()
                    for x in range (len(answers), 5):
                        answers.append(None)
                    #example query
                    #UPDATE `rest_school_db`.`questions` SET `answer_d_text`='Why are you asking me this?', `answer_e_text`='you\'re a jerk!!!' WHERE `question_id`='4';
                    sql = 'UPDATE `questions` SET question_text="'+question.get_question_text()+\
                          '" , answer_a_text="'+answers[0]+\
                          '", answer_b_text="'+answers[1]+\
                          '", answer_c_text="'+answers[2]+\
                          '", answer_d_text="'+answers[3]+\
                          '", answer_e_text="'+answers[4]+\
                          '", answer_f_text="'+answers[5]+\
                          '", topic="'+question.get_topic()+\
                          '", question_type="'+question.get_type()+\
                          '", answer_num='+str(question.get_correct_answer_index())+\
                          " WHERE question_id="+str(question.get_question_id())+";"
                    cursor.execute(sql)
                    return True
            except Exception as e:
                print("Error fetching results: "+str(e))
                return False
        except Exception as e:
            print("Error connecting: "+str(e))
            return False

    # deletes a question from the database using its question_id
    def delete_question(self, question_id):
        try:
            self.delete_row_in_table_with_attribute('questions', 'question_id', question_id)
        except Exception as e:
            print("Could not delete question " + str(e))

    # updates one or more columns of a question by question_id
    def update_question_attribute_by_id(self, question_id, keylist, valuelist):
        try:
            self.update_row_in_table(keylist, valuelist, 'questions', question_id)

        except Exception as e:
                print("Error updating question: "+str(e))

    # saves a new question into the questions database
    # function takes a question object
    # code will null answers that aren't provided
    def save_new_question_from_question_object(self, question):
        try:
            self.save_new_row_in_table(question.get_dictionary(), 'questions')

        except Exception as e:
            print("Error connecting: "+str(e))
            return False

    # saves a new question into the questions database
    # function takes a question object
    # code will null answers that aren't provided
    def save_new_question_from_dictionary(self, question):
        try:
            self.save_new_row_in_table(question.get_dictionary(), 'questions')

        except Exception as e:
            print("Error connecting: "+str(e))
            return False









