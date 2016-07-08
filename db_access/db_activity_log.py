from db_access.db_general import GeneralDatabaseConnection

table_name = 'activity_log'


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

    def get_activity_by_user_id(self, user_id):
        try:
            try:
                db_obj = self.get_all_by_key_value(table_name, 'user_id', user_id)
                return db_obj

            except Exception as e:
                print("Error fetching results: " + str(e))
        except Exception as e:
            print("Error connecting: " + str(e))

    def get_activities_today_by_user_id(self, user_id):
        try:
            try:
                db_obj = self.get_all_by_key_value()
                return db_obj

            except Exception as e:
                print("Error fetching results: " + str(e))
        except Exception as e:
            print("Error connecting: " + str(e))

    def get_activities_between_dates_by_user_id(self, user_id):
        try:
            try:
                db_obj = self.get_all_by_key_value()
                return db_obj

            except Exception as e:
                print("Error fetching results: " + str(e))
        except Exception as e:
            print("Error connecting: " + str(e))
    # -------------------------------------------------------------
    # WRITE methods
    # -------------------------------------------------------------

    def save_new_activity(self, activity):
        try:
            try:
                db_obj = self.save_new_row_in_table(activity.get_database_format(), table_name)
                return db_obj

            except Exception as e:
                print("Error fetching results: " + str(e))
        except Exception as e:
            print("Error connecting: " + str(e))
