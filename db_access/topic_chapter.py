import pymysql.cursors
from db_access.databaseaccess import GeneralDatabaseConnection
import business_objects.question as question_obj_generator
from random import randint, shuffle


class TopicChapterTableAccess(GeneralDatabaseConnection):

    # -------------------------------------------------------------
    # class variables
    # -------------------------------------------------------------

    # topic_chapter table
    topic_chapter_fields = [None]*3
    topic_chapter_fields[0] = 'chapter'
    topic_chapter_fields[1] = 'topic'
    topic_chapter_fields[2] = 'topic_index'

    # -------------------------------------------------------------
    # class constructor
    # -------------------------------------------------------------

    def __init__(self):
        GeneralDatabaseConnection.__init__(self)

    # -------------------------------------------------------------
    # READ methods
    # -------------------------------------------------------------

    # -------------------------------------------------------------
    # WRITE methods
    # -------------------------------------------------------------
