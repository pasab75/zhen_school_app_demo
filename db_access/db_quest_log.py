from db_access.db_general import GeneralDatabaseConnection
import datetime

table_name = 'quest_log'

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

    def get_quests_by_user_id(self, user_id):
        try:
            try:
                db_obj = self.get_all_by_key_value(table_name, 'user_id', user_id)
                return db_obj

            except Exception as e:
                print("Error fetching results: " + str(e))
        except Exception as e:
            print("Error connecting: " + str(e))

    def get_quests_completed_between_dates_by_user_id(self, user_id, date1, date2):
        try:
            try:
                # TODO: make this only get the quests completed between certain dates
                db_obj = self.get_all_by_key_value()
                return db_obj

            except Exception as e:
                print("Error fetching results: " + str(e))
        except Exception as e:
            print("Error connecting: " + str(e))

    def get_quests_completed_today_by_user_id(self, user_id):
        try:
            try:
                db_obj = self.get_quests_completed_between_dates_by_user_id(user_id, datetime.datetime.today()-datetime.timedelta(1))
                return db_obj

            except Exception as e:
                print("Error fetching results: " + str(e))
        except Exception as e:
            print("Error connecting: " + str(e))

    # -------------------------------------------------------------
    # WRITE methods
    # -------------------------------------------------------------

    def save_new_quest(self, quest):
        try:
            try:
                db_obj = self.save_new_row_in_table(quest.get_database_format(), table_name)
                return db_obj

            except Exception as e:
                print("Error fetching results: " + str(e))
        except Exception as e:
            print("Error connecting: " + str(e))

