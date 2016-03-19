from flask import jsonify

class user:
    def __init__(self, user_id=None, first_name=None, last_name=None, e_mail=None, user_role='0',
                 current_activity_info=None, current_lvl='1', current_points='0', last_active=None, paid_through=None):
        self._dictionary = {'user_id': user_id,
                            'first_name': first_name,
                            'last_name': last_name,
                            'user_role': user_role,
                            'e_mail': e_mail,
                            'current_activity_info': current_activity_info,
                            'current_lvl': current_lvl,
                            'current_points': current_points,
                            'last_active': last_active,
                            'paid_through': paid_through
                            }

    def set_dictionary(self, dictionary):
        self._dictionary = dictionary

    def get_dictionary(self):
        return self._dictionary
