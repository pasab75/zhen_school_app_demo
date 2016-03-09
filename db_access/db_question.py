import pymysql.cursors
import business_objects.question as question_obj_generator

class database_access:
    dbconnection = None

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

    def get_by_id(self, question_id):
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
                                            request['chapter'],
                                            request['subject'],
                                            request['answer_num'])
                    return question
            except Exception as e:
                print("Error fetching results: "+str(e))
        except Exception as e:
                print("Error connecting: "+str(e))

    def get_by_question_text(self, text):
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
                                            request['chapter'],
                                            request['subject'],
                                            request['answer_num'])
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

                    sql = "INSERT INTO `questions` (`question_id`,`question_text`, `answer_a_text`, `answer_b_text`, `answer_c_text`, `answer_d_text`, `answer_e_text`, `answer_f_text`, `chapter`, `subject`, `answer_num`)"+\
                          " VALUES ('NULL','"+question.get_question_text()+\
                          "', '"+answers[0]+\
                          "', '"+answers[1]+\
                          "', '"+answers[2]+\
                          "', '"+answers[3]+\
                          "', '"+answers[4]+\
                          "', '"+answers[5]+\
                          "', '"+question.get_chapter()+\
                          "', '"+question.get_subject()+\
                          "', '"+str(question.get_correct_answer_index())+"');"
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
                          '", chapter="'+question.get_chapter()+\
                          '", subject="'+question.get_subject()+\
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
                                            request['chapter'],
                                            request['subject'],
                                            request['answer_num'])
                    return question
            except Exception as e:
                print("Error fetching results: "+str(e))
        except Exception as e:
                print("Error connecting: "+str(e))

    def get_by_subject(self, subject):
        try:
            try:
                with self.dbconnection.cursor() as cursor:
                    question = None
                    sql = 'SELECT * FROM questions WHERE `subject`="'+str(subject)+'";'
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
                                            request['chapter'],
                                            request['subject'],
                                            request['answer_num'])
                    return question
            except Exception as e:
                print("Error fetching results: "+str(e))
        except Exception as e:
                print("Error connecting: "+str(e))

    def close_connection(self):
        self.dbconnection.close()



