import db_access.db_users as users_table_access_layer
import flask.jsonify as jsonify
import datetime

class User:
    _user_id = None
    _first_name = None
    _last_name = None
    _e_mail = None
    _user_role = None
    _quest_index = None
    _current_lvl = None
    _current_points = None
    _last_active = None
    _paid_through = None

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
            'current_lvl': self._current_lvl,
            'current_Points': self._current_points,
            'last_active': self._last_active,
            'paid_through': self._paid_through
        }

    def jsonify(self):
        return jsonify(
            user_id=self._user_id,
            first_name=self._first_name,
            last_name=self._last_name,
            e_mail=self._e_mail,
            user_role=self._user_role,
            quest_index=self._quest_index,
            current_lvl=self._current_lvl,
            current_points=self._current_points,
            definition_allowed=self._definition_allowed,
            daily=self._daily
        )

    def set_from_database(self, user):
        self._user_id = user['user_id']
        self._first_name = user['first_name']
        self._last_name = user['last_name']
        self._e_mail = user['e_mail']
        self._user_role = user['user_role']
        self._quest_index = user['quest_index']
        self._current_lvl = user['current_lvl']
        self._current_points = user['current_points']
        self._last_active = user['last_active']
        self._paid_through = user['paid_through']

    def generate_from_id(self, id):
        dbconnect = users_table_access_layer.UserTableAccess()
        current_user = dbconnect.get_user_by_user_id(id)
        self.set_from_database(current_user)
        dbconnect.close_connection()

    def isPaid(self):
        currentTime = datetime.datetime.now()
        if self._paid_through is not None:
            if self._paid_through > currentTime:
                return True
        return False

