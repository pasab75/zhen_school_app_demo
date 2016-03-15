import pymysql.cursors
from db_access.db_general import GeneralDatabaseConnection

#TODO: create methods to get information from user database
#TODO: user name
#TODO: user password
#TODO: user class ID(s)
#TODO: user level
#TODO: user points
#TODO: user activities completed


class UserTableAccess(GeneralDatabaseConnection):

    # users table
    users_fields = [None]*12
    users_fields[0] = 'o_auth_key'
    users_fields[1] = 'user_name'
    users_fields[2] = 'user_id'
    users_fields[3] = 'password'
    users_fields[4] = 'last_active'
    users_fields[5] = 'first_name'
    users_fields[6] = 'last_name'
    users_fields[7] = 'user_role'
    users_fields[8] = 'e_mail'
    users_fields[9] = 'current_activity_info'
    users_fields[10] = 'current_lvl'
    users_fields[11] = 'current_points'

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

    # -------------------------------------------------------------
    # WRITE methods
    # -------------------------------------------------------------

    # TODO: Make the following methods:

    def add_user_new(self, oauthkey, username, password, first_name, last_name, user_role, e_mail):
        try:
            keylist = self.users_fields
            print(keylist)

            keylist.remove('user_id')
            keylist.remove('last_active')
            keylist.remove('current_activity_info')
            keylist.remove('current_lvl')
            keylist.remove('current_points')

            valuelist = []
            valuelist.append(oauthkey)
            valuelist.append(username)
            valuelist.append(password)
            valuelist.append(first_name)
            valuelist.append(last_name)
            valuelist.append(user_role)
            valuelist.append(e_mail)

            self.save_new_row_in_table(keylist, valuelist, 'users')
        except Exception as ex:
            print("Unable to add new user: " + str(ex))


    # get id number from name
    # get id number from email
    # get all other attributes by id number