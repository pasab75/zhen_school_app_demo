import pymysql.cursors
from db_access.db_general import GeneralDatabaseConnection
import business_objects.question as question_obj_generator
from random import randint, shuffle


class ActivityLogTableAccess(GeneralDatabaseConnection):

    # -------------------------------------------------------------
    # class variables
    # -------------------------------------------------------------

    # activity_log table
    activity_log_fields = [None]*7
    activity_log_fields[0] = 'user_id#'
    activity_log_fields[1] = 'time'
    activity_log_fields[2] = 'date'
    activity_log_fields[3] = 'correct'
    activity_log_fields[4] = 'latitude'
    activity_log_fields[5] = 'longitude'
    activity_log_fields[6] = 'activity'

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
