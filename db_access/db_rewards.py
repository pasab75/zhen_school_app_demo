from db_access.db_general import GeneralDatabaseConnection

table_name = 'rewards'


class RewardsTableAccess(GeneralDatabaseConnection):

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

    def get_rewards_by_class_code(self, class_code):
        try:
            try:
                db_obj = self.get_all_by_key_value(table_name, 'class_code', class_code)
                return db_obj

            except Exception as e:
                print("Error fetching results: " + str(e))
        except Exception as e:
            print("Error connecting: " + str(e))

    # -------------------------------------------------------------
    # WRITE methods
    # -------------------------------------------------------------

    def save_new_reward(self, reward):
        try:
            try:
                self.save_new_row_in_table(reward.get_database_format(), table_name)

            except Exception as e:
                print("Error fetching results: " + str(e))
        except Exception as e:
            print("Error connecting: " + str(e))