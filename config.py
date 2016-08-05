# put hard coded configuration stuff here instead of scattered around

local = True

host = '0.0.0.0'
port = 5000

ANDROID_CLIENT_ID = 'derpderp'
IOS_CLIENT_ID = 'derpderp'
WEB_CLIENT_ID = '334346238965-oliggj0124b9r4nhbdf4nuboiiha7ov3.apps.googleusercontent.com'

STATIC_FOLDER = "angular-frontend"

number_of_question_options = [10, 25, 50]

fraction_needed_for_quest_rewards = .75

max_multiplier = 5

number_of_multiple_choices = 4

reward_tiers = [
    {
        'text': 'reward 1',
        'description': 'reward 1 description goes here',
        'required amount': 1000
    },
    {
        'text': 'reward 2',
        'description': 'reward 2 description goes here',
        'required amount': 2000
    },
    {
        'text': 'reward 3',
        'description': 'reward 3 description goes here',
        'required amount': 3000
    },
    {
        'text': 'reward 4',
        'description': 'reward 4 description goes here',
        'required amount': 4000
    },
    {}
]