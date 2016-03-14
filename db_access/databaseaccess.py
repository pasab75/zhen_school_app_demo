import pymysql.cursors
from random import randint


class GeneralDatabaseConnection:

    # -------------------------------------------------------------
    # class variables
    # -------------------------------------------------------------

    dbconnection = None

    # -------------------------------------------------------------
    # class constructor
    # -------------------------------------------------------------

    def __init__(self):
        print("connected")
        self.dbconnection = pymysql.connect(host='localhost',
                                            user='appuser',
                                            password='carhorsebatterysuccess',
                                            db='testdb',
                                            charset='utf8mb4',
                                            cursorclass=pymysql.cursors.DictCursor,
                                            autocommit=True
                                            )

    # As a rule of thumb, all values that can be thought of as text input from the API should never
    # be concatenated into a SQL query directly. Instead, they should be passed as arguments to the execution
    # method. I've rewritten most, if not all, methods to reflect this

    # -------------------------------------------------------------
    # general methods
    # -------------------------------------------------------------

    # this is a general method to insert one row into a table
    # the keylist is an ordered list of field names for the sql database
    # the valuelist is an ordered list of values that correspond to the field names
    # table is the name of the table that you are putting the row in
    def save_new_row_in_table(self, keylist, valuelist, table):
        try:
            try:
                with self.dbconnection.cursor() as cursor:
                    keystring = ",".join(map(str, keylist))

                    nulllist = []

                    for i in range(len(keylist)):
                        nulllist.append("%s")

                    nullstring = ','.join(nulllist)
                    add_string = ("INSERT INTO " + table + " ( " + keystring + ") VALUES (" + nullstring + ")")

                    # print(cursor.mogrify(add_string, valuelist))
                    cursor.execute(add_string, valuelist)
                    return True

            except Exception as e:
                print("Error saving new row: "+str(e))
                return False
        except Exception as e:
            print("Error connecting: "+str(e))
            return False

    # this is a general method to update a row in a table
    # the keylist is an ordered list of field names for the sql database
    # the valuelist is an ordered list of values that correspond to the field names
    # table is the name of the table that you are searching in
    # primary should be an index of the primary key that you are search with
    # THE PRIMARY KEY WILL NOT BE UPDATED
    def update_row_in_table(self, keylist, valuelist, table, primary):
        try:
            try:
                with self.dbconnection.cursor() as cursor:

                    # formats each field to have =%s behind it
                    for i in range(len(keylist)):
                        keylist[i] += "=%s"

                    # removes the primiary search key and value from respective lists
                    searchkey = keylist.pop(primary)
                    valuekey = valuelist.pop(primary)

                    # puts the value back as the last element of the list
                    valuelist.append(valuekey)

                    # comma delimits the list of fields
                    keystring = ",".join(map(str, keylist))

                    # adds prefix to the string telling it we want to update
                    prefix_command = "UPDATE " + str(table) + " SET "

                    # puts together the sql execution string and adds the field to be search by at the end
                    add_string = (prefix_command + keystring + " WHERE " + str(searchkey))

                    # executes the sql code with list of values to update as a parameter
                    cursor.execute(add_string, valuelist)

                    return True
            except Exception as e:
                print("Error updating row: "+str(e))
                return False
        except Exception as e:
            print("Error connecting: "+str(e))
            return False

    def delete_row_in_table_with_attribute(self, table, field, value):
        try:
            try:
                with self.dbconnection.cursor() as cursor:
                    sql = "DELETE FROM %s WHERE %s = %s"
                    args = (table, field, value)
                    cursor.execute(sql, args)

                    return True
            except Exception as e:
                print("Error fetching results: "+str(e))
                return False
        except Exception as e:
            print("Error connecting: "+str(e))
            return False

    def close_connection(self):
        self.dbconnection.close()

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

                fields = []
                values = []

                if questionType == '0':
                    answer = str(randint(0,99999))

                    fields.append('question_text')
                    fields.append('answer_a_text')
                    fields.append('topic')
                    fields.append('question_type')

                    values.append('I am a definition blah blah blah '
                                  'blah blah blah blah blah blah my answer is ' + answer)
                    values.append(answer)
                    values.append(topic)
                    values.append(questionType)

                elif questionType == '1':
                    ranNum = randint(0,5)

                    answerid = str(ranNum)
                    answer = str(ranNum+1)

                    fields.append('question_text')
                    fields.append('answer_a_text')
                    fields.append('answer_b_text')
                    fields.append('answer_c_text')
                    fields.append('answer_d_text')
                    fields.append('answer_e_text')
                    fields.append('answer_f_text')
                    fields.append('answer_num')
                    fields.append('topic')
                    fields.append('question_type')

                    values.append('I am a multiple choice question. My answer is ' +
                                  answer + '. My topic is ' + topic + ".")
                    values.append("one")
                    values.append("two")
                    values.append("three")
                    values.append("four")
                    values.append("five")
                    values.append("six")
                    values.append(answerid)
                    values.append(topic)
                    values.append(questionType)

                else:
                    answer = str(randint(0, 100000))
                    fields.append('question_text')
                    fields.append('answer_a_text')
                    fields.append('topic')
                    fields.append('question_type')

                    values.append('I am a calculation type question. My answer is ' +
                                  answer + '. My topic is ' + topic + ".")
                    values.append(answer)
                    values.append(topic)
                    values.append(questionType)

                self.save_new_row_in_table(fields, values, 'questions')

        except Exception as e:
            print("Error loading random shit "+str(e))

    # empties all rows from the questions table
    # currently the front end requests that the questions table gets emptied every time and is replaced by new
    # randomly generated questions
    def empty_table(self):
        try:
            try:
                with self.dbconnection.cursor() as cursor:
                    sql = "DELETE FROM questions"
                    cursor.execute(sql)

            except Exception as e:
                print("Error emptying table "+str(e))
        except Exception as e:
            print("Error while connecting "+str(e))

    # returns the number of rows in any table
    def get_numrows(self, table):
        try:
            try:
                with self.dbconnection.cursor() as cursor:
                    question = None
                    sql = "SELECT COUNT(*) FROM %s"
                    cursor.execute(sql, table)
                    request = cursor.fetchone()
                    print(request)

            except Exception as e:
                print("Error counting rows "+str(e))
        except Exception as e:
            print("Error while connecting "+str(e))
