import db_access.db_rewards as db_access
import business_objects.Reward as Reward


class RewardList:
    _reward_list = None

    def __init__(self,
                 reward_list=None):
        self._reward_list = reward_list

    def get_json(self):
        json_list = []
        for raw_reward in self._reward_list:
            new_reward = Reward.Reward()
            new_reward.set_from_database(raw_reward)
            reward_json = new_reward.get_json()
            json_list.append(reward_json)
        return json_list

    def set_from_database_by_class_code(self, class_code):
        db_a = db_access.RewardsTableAccess()
        self._reward_list = db_a.get_rewards_by_class_code(class_code)
        db_a.close_connection()
