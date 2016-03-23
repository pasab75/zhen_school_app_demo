from db_access.db_general import GeneralDatabaseConnection
import datetime
import business_objects.user as user_generator

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

                    # check database for user

                    # if user exists
                        # check if user is validated (paid for the service)
                            # if user is validated
                                # return true
                            # else
                                # return false

                    # else
                        # create user in database
                        # return false

                    # add the key thing later

                    sql = "SELECT COUNT(*) FROM `users` WHERE `user_id` = %s"
                    cursor.execute(sql, user_id)
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

    def check_if_user_paid(self, user_id):
        try:
            try:
                with self.db_connection.cursor() as cursor:

                    # check database for user

                    # if user exists
                        # check if user is validated (paid for the service)
                            # if user is validated
                                # return true
                            # else
                                # return false

                    # else
                        # create user in database
                        # return false

                    # add the key thing later

                    sql = "SELECT * FROM `users` WHERE `user_id` = %s"
                    cursor.execute(sql, user_id)
                    exists = cursor.fetchone()
                    currentUser = user_generator.user()
                    currentUser.set_dictionary(exists)
                    currentTime = datetime.datetime.now()
                    if currentUser.get_dictionary()['paid_through'] is not None:
                        if currentUser.get_dictionary()['paid_through'] > currentTime:
                            return True
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

    def get_password_by_user_id(self, user_id):
        try:
            user_info = self.get_row_by_key_value('users', 'user_id', user_id)
            return user_info['password']
        except Exception as ex:
            print("Unable to retrieve password: " + str(ex))

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

    def get_user_quest_by_user_id(self, user_id):
        try:
            user_info = self.get_row_by_key_value('users', 'user_id', user_id)
            return user_info['quest_index']
        except Exception as ex:
            print("Unable to retrieve user: " + str(ex))

    def get_user_current_question_id_by_user_id(self, user_id):
        try:
            user_info = self.get_row_by_key_value('users', 'user_id', user_id)
            return user_info['current_question_id']
        except Exception as ex:
            print("Unable to retrieve user: " + str(ex))

    # -------------------------------------------------------------
    # WRITE methods
    # -------------------------------------------------------------

    def update_user_activity(self, user_id, activity_index):
        try:
            try:
                with self.db_connection.cursor() as cursor:
                    sql = "SELECT FROM users WHERE 'user_id' = %s SET 'current_activity_index' = %s"
                    cursor.execute(sql, user_id, activity_index)

                    return True

            except Exception as ex:
                print("Error updating points :" + str(ex))
        except Exception as ex:
            print("Unable to update user: " + str(ex))

    def add_user_new(self, user):
        try:
            self.save_new_row_in_table(user.get_dictionary(), 'users')
        except Exception as ex:
            print("Unable to add new user: " + str(ex))

    def update_user(self, user_info):
        try:
            self.update_row_in_table(user_info, 'users', 'user_id')
        except Exception as ex:
            print("Unable to update user: " + str(ex))

    def set_user_quest_by_user_id(self, user_id, quest_index):
        try:
            user_info = {'user_id': user_id,
                         'quest_index': quest_index,
                         'quest_progress': '0',
                         'date_quest_started': datetime.datetime.now()
                         }
            self.update_row_in_table(user_info, 'users', 'user_id')
        except Exception as ex:
            print("Unable to update user: " + str(ex))

    def update_user_points(self, user_id, points_to_add):
        try:
            try:
                with self.db_connection.cursor() as cursor:
                    sql = "SELECT FROM users WHERE 'user_id' = {} SET points = points + %s".format(user_id)
                    cursor.execute(sql, points_to_add)

                    return True

            except Exception as ex:
                print("Error updating points :" + str(ex))
        except Exception as e:
            print("Error connecting: "+str(e))
            return False
