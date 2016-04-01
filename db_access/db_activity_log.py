import pymysql.cursors
from db_access.db_general import GeneralDatabaseConnection
import business_objects.Question as question_obj_generator
from random import randint, shuffle


class ActivityLogTableAccess(GeneralDatabaseConnection):

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

    # -------------------------------------------------------------
    # WRITE methods
    # -------------------------------------------------------------
