from flask import jsonify


class user:
    def __init__(self, user_id=None, first_name=None, last_name=None, e_mail=None, user_role='0',
                 quest_index=None, quest_progress=None, current_lvl='1', current_points='0', last_active=None, paid_through=None):
        self._dictionary = {'user_id': user_id,
                            'first_name': first_name,
                            'last_name': last_name,
                            'user_role': user_role,
                            'e_mail': e_mail,
                            'quest_index': quest_index,
                            'quest_progress': quest_progress,
                            'current_lvl': current_lvl,
                            'current_points': current_points,
                            'last_active': last_active,
                            'paid_through': paid_through
                            }

    def set_dictionary(self, dictionary):
        self._dictionary = dictionary

    def get_dictionary(self):
        return self._dictionary

    def get_client_user(self):
        client_user = self._dictionary
        client_user.pop('user_id')
        client_user.pop('paid_through')
        client_user.pop('last_active')

        return client_user
