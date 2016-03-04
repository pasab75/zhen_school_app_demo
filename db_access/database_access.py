import pymysql.cursors

class database_access:
    dbconnection = None
    def __init__(self):
        print("connected")
        self.dbconnection = pymysql.connect(host='localhost',
                             user='app_user',
                             password='derp123',
                             db='rest_school_db',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

    def get_question(self, question_id):
        try:
            try:
                with self.dbconnection.cursor() as cursor:
                    sql = "SELECT * FROM questions WHERE `question_id`="+str(question_id)
                    cursor.execute(sql)
                    request = cursor.fetchone()
                    self.dbconnection.close()
                    return request
            except Exception as e:
                print("Error fetching results: "+str(e))
        except Exception as e:
                print("Error connecting: "+str(e))

    def close_connection(self):
        self.dbconnection.close()