import pymysql.cursors
import business_objects.question as question_obj_generator
from random import randint, shuffle


class DatabaseAccess:
    dbconnection = None

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

# -------------------------------------------------------------
# question table methods
# -------------------------------------------------------------

    # returns which chapter a certain topic corresponds to
    def get_chapter_by_topic(self, topic):
        try:
            try:
                with self.dbconnection.cursor() as cursor:
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
                with self.dbconnection.cursor() as cursor:
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
                with self.dbconnection.cursor() as cursor:
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
                with self.dbconnection.cursor() as cursor:
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
                with self.dbconnection.cursor() as cursor:
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
                with self.dbconnection.cursor() as cursor:
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
                with self.dbconnection.cursor() as cursor:
                    print("derp I dont do anything yet")
            except Exception as e:
                print("Error fetching results: "+str(e))
        except Exception as e:
                print("Error connecting: "+str(e))

    # saves a new question into the questions database
    # function takes a question object
    # code will null answers that aren't provided
    def save_new_question(self, question):
        try:
            try:
                with self.dbconnection.cursor() as cursor:
                    answers = question.get_answers()
                    for x in range (len(answers), 5):
                        answers.append(None)

                    sql = ("INSERT INTO `questions` "
                           "(`question_id`,"
                           "`question_text`, "
                           "`answer_a_text`, "
                           "`answer_b_text`, "
                           "`answer_c_text`, "
                           "`answer_d_text`, "
                           "`answer_e_text`, "
                           "`answer_f_text`, "
                           "`topic`, "
                           "`answer_num`, "
                           "`question_type`)"
                           " VALUES "
                           "('NULL','" +
                           question.get_question_text() +
                           "', '" + answers[0] +
                           "', '" + answers[1] +
                           "', '" + answers[2] +
                           "', '" + answers[3] +
                           "', '" + answers[4] +
                           "', '" + answers[5] +
                           "', '" + question.get_topic() +
                           "', '" + str(question.get_correct_answer_index()) +
                           "', '" + question.get_type() +
                           "');")

                    cursor.execute(sql)
                    return True
            except Exception as e:
                print("Error fetching results: "+str(e))
                return False
        except Exception as e:
            print("Error connecting: "+str(e))
            return False

    # updates a question already in the database by using the question's question_id field
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

    # deletes a question from the database using its question_id
    def delete_question(self, question_id):
        try:
            self.delete_row_in_table_with_attribute('questions', 'question_id', question_id)
        except Exception as e:
            print("Could not delete question " + str(e))

    # updates a specific column of a question from the questions database
    # may want to make this into something that takes a dictionary instead of just one key-value pair
    # TODO: make this able to take more than one key-value pair
    def update_question_attribute_by_questionid(self, question_id, attribute, value):
        try:
            try:
                with self.dbconnection.cursor() as cursor:
                    sql = "UPDATE `questions` SET `%s` = %s WHERE question_id = %s"
                    args = (attribute, value, question_id)
                    cursor.execute(sql, args)

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
                with self.dbconnection.cursor() as cursor:
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
# user table methods
# -------------------------------------------------------------

    # define user table methods below

    # TODO: Make the following methods:
    # get id number from name
    # get id number from email
    # get all other attributes by id number





