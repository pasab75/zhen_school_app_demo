from flask import jsonify

class user:
    _dictionary = {'o_auth_key': None,
                   'user_name': None,
                   'user_id': None,
                   "password": None,
                   "last_active": None,
                   "first_name": None,
                   "last_name": None,
                   "user_role": None,
                   'e_mail': None,
                   'current_activity_info': None,
                   'current_lvl': None,
                   'current_points': None,
                   }

    def __init__(self, user_id=None, o_auth_key=None, user_name=None, password=None, first_name=None, last_name=None, user_role=None, e_mail=None,
                 current_activity_info=None, current_lvl=None, current_points=None, last_active=None):
        self._dictionary['o_auth_key'] = o_auth_key
        self._dictionary['user_name'] = user_name
        self._dictionary['user_id'] = user_id
        self._dictionary['password'] = password
        self._dictionary['first_name'] = first_name
        self._dictionary['last_name'] = last_name
        self._dictionary['user_role'] = user_role
        self._dictionary['e_mail'] = e_mail
        self._dictionary['current_activity_info'] = current_activity_info
        self._dictionary['current_lvl'] = current_lvl
        self._dictionary['current_points'] = current_points
        self._dictionary['last_active'] = last_active

    def set_dictionary(self, dictionary):
        self._dictionary = dictionary

    def get_dictionary(self):
        return self._dictionary
