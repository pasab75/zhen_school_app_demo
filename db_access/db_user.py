import pymysql.cursors
from db_access.db_general import GeneralDatabaseConnection


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
            self.get_row_by_key_value('users', 'user_id', user_id)
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

    def get_activity_by_user_id(self, user_id):
        try:
            user_info = self.get_row_by_key_value('users', 'user_id', user_id)
            return user_info['current_activity_info']
        except Exception as ex:
            print("Unable to retrieve user: " + str(ex))

    # -------------------------------------------------------------
    # WRITE methods
    # -------------------------------------------------------------

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
