import pymysql.cursors
import business_objects.question as question_obj_generator
from random import randint

class database_access:
    dbconnection = None

#TODO:differentiate between different questions types (multiple choice, word-definition pairs, and free response calculations) each of these will most likely need a separate set of methods

    def __init__(self):
        print("connected")
        self.dbconnection = pymysql.connect(host='localhost',
                             user='appuser',
                             password='carhorsebatterysuccess',
                             db='testDB',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor,
                             autocommit=True
                            )



    def load_questions_testing(self, numAdd):
        try:
            try:
                with self.dbconnection.cursor() as cursor:
                    for i in range(0,numAdd):
                        answerID = str(randint(0,5))
                        questionType = str(randint(0,3))
                        topic = "this is topic " + str(randint(0,30))
                        sql = "INSERT INTO `testDB`.`questions` (`question_text`, `answer_a_text`, `answer_b_text`, `answer_c_text`, `answer_d_text`, `answer_e_text`, `answer_f_text`, `answer_num`, `topic`, `question_type`) VALUES ('I am a question. My answer index is " + answerID + ". My topic is  " + topic + ". My question type is " + questionType + "', 'one', 'two', 'three', 'four', 'five', 'six', '" + answerID + "','" + topic + "' , '" + questionType + "');"
                        cursor.execute(sql)
                    print("added " + str(numAdd) + " records to table")

            except Exception as e:
                print("Error loading random shit "+str(e))
        except Exception as e:
            print("Error while connecting "+str(e))


    def empty_table(self):
        try:
            try:
                with self.dbconnection.cursor() as cursor:
                    sql = "DELETE FROM questions"
                    cursor.execute(sql)


            except Exception as e:
                print("Error loading random shit "+str(e))
        except Exception as e:
            print("Error while connecting "+str(e))


    def get_numEntries(self, table):
        try:
            try:
                with self.dbconnection.cursor() as cursor:
                    question = None
                    sql = "SELECT COUNT(*) AS NumberofQuestions FROM " + str(table) + ";"
                    cursor.execute(sql)
                    request = cursor.fetchone()
                    print(request)

            except Exception as e:
                print("Error counting rows "+str(e))
        except Exception as e:
            print("Error while connecting "+str(e))


    def get_id_by_chapter(self, chapter):
        try:
            try:
                with self.dbconnection.cursor() as cursor:
                    return "derp"
                #TODO: make this a thing
            except Exception as e:
                print("Error fetching results: "+str(e))
        except Exception as e:
                print("Error connecting: "+str(e))


    def get_id_by_topic(self, topic):
        try:
            try:
                with self.dbconnection.cursor() as cursor:
                    return "derp"
                #TODO: make this a thing
            except Exception as e:
                print("Error fetching results: "+str(e))
        except Exception as e:
                print("Error connecting: "+str(e))

    def get_question_by_questiontype(self, type): #TODO: check to make sure this is legit
        try:
            try:
                with self.dbconnection.cursor() as cursor:
                    question = None
                    sql = "SELECT * FROM questions WHERE question_type = " + str(type) + " ORDER BY RAND() LIMIT 1;"
                    cursor.execute(sql)
                    request = cursor.fetchone()
                    question = question_obj_generator.question(request['question_id'],
                                            request['question_text'],
                                            request['answer_a_text'],
                                            request['answer_b_text'],
                                            request['answer_c_text'],
                                            request['answer_d_text'],
                                            request['answer_e_text'],
                                            request['answer_f_text'],
                                            request['answer_num'],
                                            request['topic'],
                                            request['question_type'])
                    return question
            except Exception as e:
                print("Error fetching results: "+str(e))
        except Exception as e:
                print("Error connecting: "+str(e))

    def get_question_by_questiontype_topic(self, type, topic): #TODO: check to make sure this is legit
        try:
            try:
                with self.dbconnection.cursor() as cursor:
                    question = None
                    sql = "SELECT * FROM questions WHERE question_type = " + str(type) + " AND topic = " + str(topic) + " ORDER BY RAND() LIMIT 1;"
                    cursor.execute(sql)
                    request = cursor.fetchone()
                    question = question_obj_generator.question(request['question_id'],
                                            request['question_text'],
                                            request['answer_a_text'],
                                            request['answer_b_text'],
                                            request['answer_c_text'],
                                            request['answer_d_text'],
                                            request['answer_e_text'],
                                            request['answer_f_text'],
                                            request['answer_num'],
                                            request['topic'],
                                            request['question_type'])
                    return question
            except Exception as e:
                print("Error fetching results: "+str(e))
        except Exception as e:
                print("Error connecting: "+str(e))

    def get_question_by_type_chapter(self, type, chapter): #TODO: Make this work. it doesn't work right now because chapter column doesn't exist there should be eventually a table that relates topics to chapters
        try:
            try:
                with self.dbconnection.cursor() as cursor:
                    question = None
                    sql = "SELECT * FROM questions WHERE question_type = " + str(type) + " AND chapter = " + str(chapter) + " ORDER BY RAND() LIMIT 1;"
                    cursor.execute(sql)
                    request = cursor.fetchone()
                    question = question_obj_generator.question(request['question_id'],
                                            request['question_text'],
                                            request['answer_a_text'],
                                            request['answer_b_text'],
                                            request['answer_c_text'],
                                            request['answer_d_text'],
                                            request['answer_e_text'],
                                            request['answer_f_text'],
                                            request['answer_num'],
                                            request['topic'],
                                            request['question_type'])
                    return question
                #TODO: make this a thing
            except Exception as e:
                print("Error fetching results: "+str(e))
        except Exception as e:
                print("Error connecting: "+str(e))

    def get_question_by_id(self, question_id):
        try:
            try:
                with self.dbconnection.cursor() as cursor:
                    question = None
                    sql = "SELECT * FROM questions WHERE `question_id`="+str(question_id)+";"
                    cursor.execute(sql)
                    request = cursor.fetchone()
                    question = question_obj_generator.question(request['question_id'],
                                            request['question_text'],
                                            request['answer_a_text'],
                                            request['answer_b_text'],
                                            request['answer_c_text'],
                                            request['answer_d_text'],
                                            request['answer_e_text'],
                                            request['answer_f_text'],
                                            request['answer_num'],
                                            request['topic'],
                                            request['question_type'])
                    return question
            except Exception as e:
                print("Error fetching results: "+str(e))
        except Exception as e:
                print("Error connecting: "+str(e))

    def get_question_random(self):
        try:
            try:
                with self.dbconnection.cursor() as cursor:
                    question = None
                    sql = "SELECT * FROM questions ORDER BY RAND() LIMIT 1;"
                    cursor.execute(sql)
                    request = cursor.fetchone()
                    question = question_obj_generator.question(request['question_id'],
                                            request['question_text'],
                                            request['answer_a_text'],
                                            request['answer_b_text'],
                                            request['answer_c_text'],
                                            request['answer_d_text'],
                                            request['answer_e_text'],
                                            request['answer_f_text'],
                                            request['answer_num'],
                                            request['topic'],
                                            request['question_type'])
                    return question
            except Exception as e:
                print("Error fetching results: "+str(e))
        except Exception as e:
                print("Error connecting: "+str(e))

    def get_question_by_questiontext(self, text):
        try:
            try:
                with self.dbconnection.cursor() as cursor:
                    question = None
                    sql = 'SELECT * FROM questions WHERE `question_text`="'+str(text)+'";'
                    cursor.execute(sql)
                    request = cursor.fetchone()
                    question = question_obj_generator.question(request['question_id'],
                                            request['question_text'],
                                            request['answer_a_text'],
                                            request['answer_b_text'],
                                            request['answer_c_text'],
                                            request['answer_d_text'],
                                            request['answer_e_text'],
                                            request['answer_f_text'],
                                            request['answer_num'],
                                            request['topic'],
                                            request['question_type'])
                    return question
            except Exception as e:
                print("Error fetching results: "+str(e))
        except Exception as e:
                print("Error connecting: "+str(e))

    def save_new_question(self, question):
        try:
            try:
                with self.dbconnection.cursor() as cursor:
                    answers = question.get_answers()
                    for x in range (len(answers), 5):
                        answers.append(None)

                    sql = "INSERT INTO `questions` (`question_id`,`question_text`, `answer_a_text`, `answer_b_text`, `answer_c_text`, `answer_d_text`, `answer_e_text`, `answer_f_text`, `topic`, `answer_num`, `question_type`)"+\
                          " VALUES ('NULL','"+question.get_question_text()+\
                          "', '"+answers[0]+\
                          "', '"+answers[1]+\
                          "', '"+answers[2]+\
                          "', '"+answers[3]+\
                          "', '"+answers[4]+\
                          "', '"+answers[5]+\
                          "', '"+question.get_topic()+\
                          "', '"+str(question.get_correct_answer_index())+\
                          "', '"+question.get_type()+"');"
                    cursor.execute(sql)
                    return True
            except Exception as e:
                print("Error fetching results: "+str(e))
                return False
        except Exception as e:
            print("Error connecting: "+str(e))
            return False

    def update_question(self, question):
        try:
            try:
                with self.dbconnection.cursor() as cursor:
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

    def delete_question(self, question_id):
        try:
            try:
                with self.dbconnection.cursor() as cursor:
                    #UPDATE `rest_school_db`.`questions` SET `answer_d_text`='Why are you asking me this?', `answer_e_text`='you\'re a jerk!!!' WHERE `question_id`='4';
                    sql = "DELETE FROM `questions` WHERE question_id = "+str(question_id)+";"
                    cursor.execute(sql)
                    return True
            except Exception as e:
                print("Error fetching results: "+str(e))
                return False
        except Exception as e:
            print("Error connecting: "+str(e))
            return False

    def get_by_chapter(self, chapter):
        try:
            try:
                with self.dbconnection.cursor() as cursor:
                    question = None
                    sql = 'SELECT * FROM questions WHERE `chapter`="'+str(chapter)+'";'
                    cursor.execute(sql)
                    request = cursor.fetchone()
                    question = question_obj_generator.question(request['question_id'],
                                            request['question_text'],
                                            request['answer_a_text'],
                                            request['answer_b_text'],
                                            request['answer_c_text'],
                                            request['answer_d_text'],
                                            request['answer_e_text'],
                                            request['answer_f_text'],
                                            request['answer_num'],
                                            request['topic'],
                                            request['question_type'])
                    return question
            except Exception as e:
                print("Error fetching results: "+str(e))
        except Exception as e:
                print("Error connecting: "+str(e))

    def get_by_topic(self, topic):
        try:
            try:
                with self.dbconnection.cursor() as cursor:
                    question = None
                    sql = 'SELECT * FROM questions WHERE `topic`="'+str(topic)+'";'
                    cursor.execute(sql)
                    request = cursor.fetchone()
                    question = question_obj_generator.question(request['question_id'],
                                            request['question_text'],
                                            request['answer_a_text'],
                                            request['answer_b_text'],
                                            request['answer_c_text'],
                                            request['answer_d_text'],
                                            request['answer_e_text'],
                                            request['answer_f_text'],
                                            request['answer_num'],
                                            request['topic'],
                                            request['question_type'])
                    return question
            except Exception as e:
                print("Error fetching results: "+str(e))
        except Exception as e:
                print("Error connecting: "+str(e))

    def close_connection(self):
        self.dbconnection.close()



