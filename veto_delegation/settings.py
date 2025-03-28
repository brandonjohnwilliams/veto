from os import environ

SESSION_CONFIGS = [
     dict(
         name='veto_delegation',
         display_name="Standard Treatment",
         app_sequence=[
             # 'introduction',
             # 'veto_delegation',
             'robot',
         ],
         num_demo_participants=2,
         take_it_or_leave_it=False,
         chat=False,
         ),
    # dict(
    #      name='veto_delegation_cheap',
    #      display_name="Cheap Talk",
    #      app_sequence=['practice','veto_delegation_cheap'],
    #      num_demo_participants=2,
    # ),
    # dict(
    #     name='veto_delegation_single',
    #     display_name="Single Point",
    #     app_sequence=['practice', 'veto_delegation_single'],
    #     num_demo_participants=2,
    # ),
]

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=1.00, participation_fee=0.00, doc=""
)

PARTICIPANT_FIELDS = ['sample']
SESSION_FIELDS = []

# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'en'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'USD'
USE_POINTS = True

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEMO_PAGE_INTRO_HTML = """ """

SECRET_KEY = '3896147596707'
