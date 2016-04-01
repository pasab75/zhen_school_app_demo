from db_access.db_general import GeneralDatabaseConnection
from db_access.db_topic_chapter import TopicChapterTableAccess
from random import randint, shuffle


class QuestTableAccess(GeneralDatabaseConnection):

    # -------------------------------------------------------------
    # class variables
    # -------------------------------------------------------------

    # -------------------------------------------------------------
    # class constructor
    # -------------------------------------------------------------

    def __init__(self):
        GeneralDatabaseConnection.__init__(self)

    # -------------------------------------------------------------
    # DEBUG methods
    # -------------------------------------------------------------

    def add_dummy_quests(self, number_of_quests):
        try:
            for i in range(number_of_quests):
                coinflip = 0
                type_0_allowed = 1
                daily = 1
                number_of_questions = randint(10, 50)
                point_value = number_of_questions*10

                quest_name = 'I am a quest. I contain ' + str(number_of_questions) + ' questions.'

                quest = {'quest_name': quest_name,
                         'type_0_allowed': type_0_allowed,
                         'daily': daily,
                         'number_of_questions': number_of_questions,
                         'point_value': point_value
                         }

                if coinflip == 0:
                    quest['chapter_index'] = randint(1, 10)
                    quest['cumulative'] = randint(0, 1)
                else:
                    quest['topic_index'] = randint(1, 100)

                self.add_quest(quest)
        except Exception as e:
                print("Error connecting: "+str(e))

    # -------------------------------------------------------------
    # READ methods
    # -------------------------------------------------------------

    def get_quest_by_quest_index(self, quest_index):
        try:
            try:
                with self.db_connection.cursor() as cursor:
                    sql = "SELECT * FROM quests WHERE quest_index = %s"
                    cursor.execute(sql, quest_index)
                    request = cursor.fetchone()

                    return request

            except Exception as e:
                print("Error fetching results: "+str(e))
        except Exception as e:
                print("Error connecting: "+str(e))

    def get_quest_is_daily(self, quest_index):
        try:
            try:
                with self.db_connection.cursor() as cursor:
                    sql = "SELECT COUNT(*) FROM quests WHERE quest_index = %s AND daily = 1"
                    cursor.execute(sql, quest_index)
                    request = cursor.fetchone()

                    return request

            except Exception as e:
                print("Error fetching results: "+str(e))
        except Exception as e:
                print("Error connecting: "+str(e))

    def get_quest_random_by_chapter_index(self, chapter):
        try:
            try:
                with self.db_connection.cursor() as cursor:
                    sql = "SELECT * FROM quests WHERE chapter_index = %s ORDER BY RAND() LIMIT 1"
                    cursor.execute(sql, chapter)
                    request = cursor.fetchone()

                    return request

            except Exception as e:
                print("Error fetching results: "+str(e))
        except Exception as e:
                print("Error connecting: "+str(e))

    def get_quest_random_by_topic_index(self, topic):
        try:
            try:
                with self.db_connection.cursor() as cursor:
                    sql = "SELECT * FROM quests WHERE topic_index = %s ORDER BY RAND() LIMIT 1"
                    cursor.execute(sql, topic)
                    request = cursor.fetchone()

                    return request

            except Exception as e:
                print("Error fetching results: "+str(e))
        except Exception as e:
                print("Error connecting: "+str(e))

    def get_quest_random_by_topic_random_in_chapter(self, chapter):
        try:
            try:
                with self.db_connection.cursor() as cursor:
                    dbconnect = TopicChapterTableAccess()
                    topic_index = dbconnect.get_topic_random_by_chapter(chapter)
                    sql = "SELECT * FROM quests WHERE topic_index = %s ORDER BY RAND() LIMIT 1"
                    cursor.execute(sql, topic_index)
                    request = cursor.fetchone()

                    return request

            except Exception as e:
                print("Error fetching results: "+str(e))
        except Exception as e:
                print("Error connecting: "+str(e))

    def get_daily_quests_by_chapter(self, chapter):
        try:
            try:
                with self.db_connection.cursor() as cursor:
                    sql = "SELECT * FROM quests WHERE chapter_index = %s AND daily = '1' ORDER BY RAND() LIMIT 5"
                    cursor.execute(sql, chapter)
                    request = cursor.fetchall()

                    return request

            except Exception as e:
                print("Error fetching results: "+str(e))
        except Exception as e:
                print("Error connecting: "+str(e))

    def get_quests_daily(self, number_of_quests):
        try:
            try:
                with self.db_connection.cursor() as cursor:
                    sql = "SELECT * FROM quests WHERE daily = '1' ORDER BY RAND() LIMIT {}".format(number_of_quests)
                    cursor.execute(sql)
                    request = cursor.fetchall()

                    return request

            except Exception as e:
                print("Error fetching results: " + str(e))
        except Exception as e:
            print("Error connecting: " + str(e))

    # -------------------------------------------------------------
    # WRITE methods
    # -------------------------------------------------------------

    def add_quest(self, quest):
        try:
            self.save_new_row_in_table(quest, 'quests')
        except Exception as e:
            print("Could not update function: "+str(e))
            return False

    def update_quest_from_object_with_primarykey(self, quest, primary):
        try:
            self.update_row_in_table(question.get_dictionary(), 'questions', primary)
        except Exception as e:
            print("Could not update function: "+str(e))
            return False
