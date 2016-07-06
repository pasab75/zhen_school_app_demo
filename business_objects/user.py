import db_access.db_users as users_table_access_layer

class User:
    def __init__(self, user_id=None,
                 first_name=None,
                 last_name=None,
                 e_mail=None,
                 user_role='0',
                 quest_index=None,
                 quest_progress=None,
                 current_lvl='1',
                 current_points='0',
                 last_active=None,
                 paid_through=None):

        self._user_id = user_id
        self._first_name = first_name
        self._last_name = last_name
        self._e_mail = e_mail
        self._user_role = user_role
        self._quest_index = quest_index
        self._quest_progress = quest_progress
        self._current_lvl = current_lvl
        self._current_points = current_points
        self._last_active = last_active
        self._paid_through = paid_through

    def get_database_format(self):
        return {
            'user_id': self._user_id,
            'first_name': self._first_name,
            'last_name': self._last_name,
            'e_mail': self._e_mail,
            'user_role': self._user_role,
            'quest_index': self._quest_index,
            'quest_progress': self._quest_progress,
            'current_lvl': self._current_lvl,
            'current_Points': self._current_points,
            'last_active': self._last_active,
            'paid_through': self._paid_through
        }

    def set_from_database(self, user):
        self._user_id = user['user_id']
        self._first_name = user['first_name']
        self._last_name = user['last_name']
        self._e_mail = user['e_mail']
        self._user_role = user['user_role']
        self._quest_index = user['quest_index']
        self._quest_progress = user['quest_progress']
        self._current_lvl = user['current_lvl']
        self._current_points = user['current_points']
        self._last_active = user['last_active']
        self._paid_through = user['paid_through']

