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

    # -------------------------------------------------------------
    # WRITE methods
    # -------------------------------------------------------------

    def update_question_from_object_with_primarykey(self, question, primary):
        try:
            self.update_row_in_table(question.get_dictionary(), 'questions', primary)
        except Exception as e:
            print("Could not update function: "+str(e))
            return False
