from db_access.db_general import GeneralDatabaseConnection
from random import randint, shuffle
import math


class TopicChapterTableAccess(GeneralDatabaseConnection):

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

    def add_dummy_topics(self, number_of_topics):
        try:
            topics_per_chapter = math.floor(number_of_topics/10)
            chapter = 0
            for i in range(1, number_of_topics+1):
                if i % topics_per_chapter == 1:
                    chapter += 1
                topic = {'chapter': chapter,
                         'chapter_name': 'Chapter ' + str(chapter),
                         'topic_index': str(i),
                         'topic_name': 'Topic ' + str(i)
                         }

                self.add_topic(topic)

        except Exception as e:
                print("Error connecting: "+str(e))

    # -------------------------------------------------------------
    # READ methods
    # -------------------------------------------------------------

    # returns the chapter index number for a specific topic
    # topics can only have one chapter associated with them
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

    # returns ALL rows that have a certain chapter
    def get_topic_all_by_chapter(self, chapter):
        try:
            try:
                with self.db_connection.cursor() as cursor:
                    sql = "SELECT * FROM topic_chapter WHERE chapter = %s"
                    cursor.execute(sql, chapter)
                    request = cursor.fetchall()

                    return request

            except Exception as e:
                print("Error fetching results: "+str(e))
        except Exception as e:
                print("Error connecting: "+str(e))

    # gets a random topic from a specific chapter
    # returns just the topic index
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

    # -------------------------------------------------------------
    # WRITE methods
    # -------------------------------------------------------------

    def add_topic(self, topic):
        try:
            self.save_new_row_in_table(topic, 'topic_chapter')
        except Exception as e:
            print("Could save new topic: "+str(e))
            return False

    def update_question_from_object_with_primarykey(self, question, primary):
        try:
            self.update_row_in_table(question.get_dictionary(), 'questions', primary)
        except Exception as e:
            print("Could not update function: "+str(e))
            return False
