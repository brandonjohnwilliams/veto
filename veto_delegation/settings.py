from os import environ

SESSION_CONFIGS = [
     dict(
         name='veto_delegation',
         display_name="Standard Treatment",
         app_sequence=[
             'introduction',
             'practice',
             'veto_delegation',
             'robot',
             'lotteries',
             'dictator',
             'payment',
         ],

         num_demo_participants=20,
         take_it_or_leave_it=False,
         chat=False,
         use_browser_bots=False,
         Session=1,
         doc="""Set the session number to the total number in the treatment""",
         ),
    dict(
        name='mech_choice',
        display_name="Mechanism Choice",
        app_sequence=[
            # 'introduction',
            # 'practice',
            # 'veto_delegation',
            # 'no_zero',
            # 'no_zero_response',
            # 'avg_robot',
            # 'opp_mechanism',
            'mech_choice',
            'payment_zero',
        ],
        num_demo_participants=20,
        take_it_or_leave_it=False,
        chat=False,
        use_browser_bots=False,
        Session=1,
        test=1,
        doc="""Set the session number to the total number in the treatment""",
    ),
    dict(
        name='opener',
        display_name="opener",
        app_sequence=[
            'opener',
        ],
        num_demo_participants=1,
        hispanic_names=False,
        random_order=False,
    ),

]

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=1.00, participation_fee=0.00, doc=""
)

OTREE_PRODUCTION=1
DEBUG=False

PARTICIPANT_FIELDS = ['MatchingGroup', 'SubGroup', 'PayRound', 'PartOnePayoff', 'BonusPay', 'dictator_order', 'sliders',
                      'label_id', 'MatchingGroupZero', 'SubGroupZero',
                      'proposer', 'responder', 'responses', 'received_responses',
                      'PartTwoPayoff', 'PartTwoResponderPayoff', 'PartTwoProposerPayoff',]
SESSION_FIELDS = ['PartTwoPay', 'PartTwoPayProposer', 'PartTwoPayResponder',
                  'PartThreePay', 'PartThreePay1', 'PartThreePay2', 'PartThreePay3',
                  'part3round1', 'part3round2', 'part3round3',
                  'PartFourPayGive', 'PartFourPayReceive',
                  'PartFourPay1', 'PartFourPay2', 'PartFourPay3',
                  'part4round1', 'part4round2', 'part4round3',
                  'MPLResults',
                  'PartFivePay1', 'PartFivePay2', 'PartFivePay3',
                  'GiveAmount']

# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'en'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'USD'
USE_POINTS = False

ROOMS = [
    dict(
        name='test_room',
        display_name='Test Room',
    ),
    dict(
        name='test_room2',
        display_name='Test Room',
    )
]

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEMO_PAGE_INTRO_HTML = """ """

SECRET_KEY = '3896147596707'
