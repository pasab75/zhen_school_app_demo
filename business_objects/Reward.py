import db_access.db_rewards as db_access


class Reward:
    _class_code = None
    _reward_name = None
    _reward_description = None
    _required_points = None

    def __init__(self,
                 class_code=None,
                 reward_name=None,
                 reward_description=None,
                 required_points=None):
        self._class_code = class_code
        self._reward_name = reward_name
        self._reward_description = reward_description
        self._required_points = required_points

    def get_json(self):
        return {
            'name': self._reward_name,
            'description': self._reward_description,
            'points_required': self._required_points
        }

    def get_database_format(self):
        return {
            'class_code': self._class_code,
            'reward_name': self._reward_name,
            'reward_description': self._reward_description,
            'required_points': self._required_points
        }

    def set_from_database(self, reward):
        self._class_code = reward['class_code']
        self._reward_name = reward['reward_name']
        self._reward_description = reward['reward_description']
        self._required_points = reward['required_points']

    def save_new(self):
        db_a = db_access.RewardsTableAccess()
        db_a.save_new_reward(self)
        db_a.close_connection()
