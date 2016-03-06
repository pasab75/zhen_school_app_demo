import pymysql.cursors
import business_objects.question as question_obj_generator

class database_access:
    dbconnection = None

    def __init__(self):
        print("connected")
        self.dbconnection = pymysql.connect(host='localhost',
                             user='app_user',
                             password='derp123',
                             db='rest_school_db',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor,
                             autocommit=True
                            )

    def get_question(self, question_id):
        try:
            try:
                with self.dbconnection.cursor() as cursor:
                    sql = "SELECT * FROM questions WHERE `question_id`="+str(question_id)
                    cursor.execute(sql)
                    request = cursor.fetchone()
                    question = question_obj_generator.question(request['question_id'],
                                            request['question_text'],
                                            request['answer_a_text'],
                                            request['answer_b_text'],
                                            request['answer_c_text'],
                                            request['answer_d_text'],
                                            request['answer_e_text'],
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

                    sql = "INSERT INTO `questions` (`question_id`,`question_text`, `answer_a_text`, `answer_b_text`, `answer_c_text`, `answer_d_text`, `answer_e_text`, `answer_num`)"+\
                          " VALUES ('NULL','"+question.get_question_text()+\
                          "', '"+answers[0]+\
                          "', '"+answers[1]+\
                          "', '"+answers[2]+\
                          "', '"+answers[3]+\
                          "', '"+answers[4]+\
                          "', '"+\
                          str(question.get_correct_answer_index())+"');"
                    cursor.execute(sql)
                    return True
            except Exception as e:
                print("Error fetching results: "+str(e))
                return False
        except Exception as e:
            print("Error connecting: "+str(e))
            return False

    def update_question(self, question_id):
        #TODO do this!
        print("Not yet implemented")

    def close_connection(self):
        self.dbconnection.close()



