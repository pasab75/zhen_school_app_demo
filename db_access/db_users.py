from db_access.db_general import GeneralDatabaseConnection
import datetime

table_name = "users"

class UserTableAccess(GeneralDatabaseConnection):

    # -------------------------------------------------------------
    # class constructor
    # -------------------------------------------------------------

    def __init__(self):
        GeneralDatabaseConnection.__init__(self)

    # -------------------------------------------------------------
    # user table methods
    # -------------------------------------------------------------

    # -------------------------------------------------------------
    # READ methods
    # -------------------------------------------------------------

    def check_if_user_valid(self, user_id):
        try:
            try:
                with self.db_connection.cursor() as cursor:
                    sql = "SELECT COUNT(*) FROM `users` WHERE `user_id` = {}}".format(user_id)
                    cursor.execute(sql)
                    exists = cursor.fetchone()['COUNT(*)']
                    if exists == 1:
                        return True
                    else:
                        return False

            except Exception as ex:
                print("Error checking if user exists :" + str(ex))
        except Exception as e:
            print("Error connecting: "+str(e))
            return False

    # gets all users with the requested first name
    # returns a list of dictionaries
    def get_users_by_first_name(self, first_name):
        try:
            self.get_rows_by_key_value('users', 'first_name', first_name)
        except Exception as ex:
            print("Unable to retrieve user: " + str(ex))

    # gets all users with the requested last name
    # returns a list of dictionaries
    def get_users_by_last_name(self, last_name):
        try:
            self.get_rows_by_key_value('users', 'last_name', last_name)
        except Exception as ex:
            print("Unable to retrieve user: " + str(ex))

    # gets one user by unique user id number
    # returns one dictionary
    def get_user_by_user_id(self, user_id):
        try:
            return self.get_row_by_key_value('users', 'user_id', user_id)
        except Exception as ex:
            print("Unable to retrieve user: " + str(ex))

    def get_name_by_user_id(self, user_id):
        try:
            user_info = self.get_row_by_key_value('users', 'user_id', user_id)
            return user_info['first_name']+" " + user_info['last_name']
        except Exception as ex:
            print("Unable to retrieve user: " + str(ex))

    def get_points_by_user_id(self, user_id):
        try:
            user_info = self.get_row_by_key_value('users', 'user_id', user_id)
            return user_info['current_points']
        except Exception as ex:
            print("Unable to retrieve user: " + str(ex))

    def get_lvl_by_user_id(self, user_id):
        try:
            user_info = self.get_row_by_key_value('users', 'user_id', user_id)
            return user_info['current_lvl']
        except Exception as ex:
            print("Unable to retrieve user: " + str(ex))

    def get_role_by_user_id(self, user_id):
        try:
            user_info = self.get_row_by_key_value('users', 'user_id', user_id)
            return user_info['user_role']
        except Exception as ex:
            print("Unable to retrieve user: " + str(ex))

    def get_email_by_user_id(self, user_id):
        try:
            user_info = self.get_row_by_key_value('users', 'user_id', user_id)
            return user_info['e_mail']
        except Exception as ex:
            print("Unable to retrieve user: " + str(ex))

    def get_multiplier_by_user_id(self, user_id):
        try:
            user_info = self.get_row_by_key_value(table_name, 'user_id', user_id)
            return user_info['current_multiplier']
        except Exception as ex:
            print("Unable to retrieve user: " + str(ex))

    def get_chapter_index_by_user_id(self, user_id):
        try:
            user_info = self.get_row_by_key_value(table_name, 'user_id', user_id)
            return user_info['chapter_index']
        except Exception as ex:
            print("Unable to retrieve user: " + str(ex))

    def get_number_of_questions_by_user_id(self, user_id):
        try:
            user_info = self.get_row_by_key_value(table_name, 'user_id', user_id)
            return user_info['number_of_questions']
        except Exception as ex:
            print("Unable to retrieve user: " + str(ex))

    def get_points_per_question_by_user_id(self, user_id):
        try:
            user_info = self.get_row_by_key_value(table_name, 'user_id', user_id)
            return user_info['points_per_question']
        except Exception as ex:
            print("Unable to retrieve user: " + str(ex))

    def get_completion_points_by_user_id(self, user_id):
        try:
            user_info = self.get_row_by_key_value(table_name, 'user_id', user_id)
            return user_info['completion_points']
        except Exception as ex:
            print("Unable to retrieve user: " + str(ex))

    def get_date_quest_started_by_user_id(self, user_id):
        try:
            user_info = self.get_row_by_key_value(table_name, 'user_id', user_id)
            return user_info['date_quest_started']
        except Exception as ex:
            print("Unable to retrieve user: " + str(ex))

    def get_current_word_index_by_user_id(self, user_id):
        try:
            user_info = self.get_row_by_key_value(table_name, 'user_id', user_id)
            return user_info['current_word_index']
        except Exception as ex:
            print("Unable to retrieve user: " + str(ex))

    def get_current_quest_progress_by_user_id(self, user_id):
        try:
            user_info = self.get_row_by_key_value(table_name, 'user_id', user_id)
            return user_info['current_progress']
        except Exception as ex:
            print("Unable to retrieve user: " + str(ex))

    def get_number_correct_by_user_id(self, user_id):
        try:
            user_info = self.get_row_by_key_value(table_name, 'user_id', user_id)
            return user_info['number_correct']
        except Exception as ex:
            print("Unable to retrieve user: " + str(ex))

    def get_point_information_by_user_id(self, user_id):
        try:
            user_info = self.get_row_by_key_value(table_name, 'user_id', user_id)
            user_point_info = {

            }
            return user_point_info
        except Exception as ex:
            print("Unable to retrieve user: " + str(ex))

    def get_quest_information_by_user_id(self, user_id):
        try:
            user_info = self.get_row_by_key_value(table_name, 'user_id', user_id)
            user_quest_info = {

            }
            return user_quest_info
        except Exception as ex:
            print("Unable to retrieve user: " + str(ex))

    # -------------------------------------------------------------
    # WRITE methods
    # -------------------------------------------------------------

    def add_user_new(self, user):
        try:
            self.save_new_row_in_table(user.get_database_format(), 'users')
        except Exception as ex:
            print("Unable to add new user: " + str(ex))

    def update_user(self, user_info):
        try:
            self.update_row_in_table(user_info, 'users', 'user_id')
        except Exception as ex:
            print("Unable to update user: " + str(ex))

    def update_user_current_word(self, user_id, word_index):
        try:
            try:
                with self.db_connection.cursor() as cursor:
                    sql = "UPDATE users SET current_word_index = %s WHERE user_id = %s"
                    args = (word_index, user_id)
                    cursor.execute(sql, args)

                    return True

            except Exception as ex:
                print("Error updating user question :" + str(ex))
        except Exception as e:
            print("Error connecting: "+str(e))
            return False

    def update_user_points(self, user_id, points_to_add):
        try:
            try:
                with self.db_connection.cursor() as cursor:
                    sql = "UPDATE users SET current_points = current_points + %s WHERE user_id = %s"
                    args = (points_to_add, user_id)
                    cursor.execute(sql, args)

                    return True

            except Exception as ex:
                print("Error updating points :" + str(ex))
        except Exception as e:
            print("Error connecting: "+str(e))
            return False

    def update_user_multiplier(self, user_id, multiplier_increase):
        try:
            try:
                with self.db_connection.cursor() as cursor:
                    sql = "UPDATE users SET point_multiplier = point_multiplier + %s WHERE user_id = %s"
                    args = (multiplier_increase, user_id)
                    cursor.execute(sql, args)

                    return True

            except Exception as ex:
                print("Error updating user multiplier :" + str(ex))
        except Exception as e:
            print("Error connecting: "+str(e))
            return False

    def set_user_multiplier(self, user_id, multiplier):
        try:
            try:
                with self.db_connection.cursor() as cursor:
                    sql = "UPDATE users SET point_multiplier = %s WHERE user_id = %s"
                    args = (multiplier, user_id)
                    cursor.execute(sql, args)

                    return True

            except Exception as ex:
                print("Error updating user multiplier :" + str(ex))
        except Exception as e:
            print("Error connecting: "+str(e))
            return False

    def update_user_current_progress(self, user_id):
        try:
            try:
                with self.db_connection.cursor() as cursor:
                    sql = "UPDATE users SET current_progress = current_progress + 1 WHERE user_id = %s"
                    cursor.execute(sql, user_id)

                    return True

            except Exception as ex:
                print("Error updating quest progress :" + str(ex))
        except Exception as e:
            print("Error connecting: "+str(e))
            return False

    def null_user_quest(self, user_id):
        try:
            user_info = {'user_id': user_id,
                         'chapter_index': None,
                         'current_progress': None,
                         'date_quest_started': None,
                         'current_word_index': None,
                         'number_correct': None,
                         'completion_points': None,
                         'seconds_per_question': None,
                         'points_per_question': None,
                         'number_of_questions': None,
                         'cumulative': None
                         }
            self.update_row_in_table(user_info, 'users', 'user_id')
            return True
        except Exception as e:
            print("Error connecting: "+str(e))
            return False

    def update_user_rewards(self):
        try:
            user_info = {'user_id': user_id,
                         'current_lvl': current_lvl,
                         'current_points': current_points,
                         'current_multiplier': current_multiplier,
                         }
            self.update_row_in_table(user_info, 'users', 'user_id')
            return True
        except Exception as e:
            print("Error connecting: " + str(e))
            return False
