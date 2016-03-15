from flask import jsonify

class user:
    def __init__(self, user_id=None, o_auth_key=None, user_name=None, password=None, first_name=None, last_name=None, user_role=None, e_mail=None,
                 current_activity_info=None, current_lvl=None, current_points=None, last_active=None):
        self._dictionary = {'o_auth_key': o_auth_key,
                            'user_name': user_name,
                            'user_id': user_id,
                            'password': password,
                            'first_name': first_name,
                            'last_name': last_name,
                            'user_role': user_role,
                            'e_mail': e_mail,
                            'current_activity_info': current_activity_info,
                            'current_lvl': current_lvl,
                            'current_points': current_points,
                            'last_active': last_active
                            }

    def set_dictionary(self, dictionary):
        self._dictionary = dictionary

    def get_dictionary(self):
        return self._dictionary
