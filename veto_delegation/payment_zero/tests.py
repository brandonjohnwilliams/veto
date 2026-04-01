from otree.api import Bot, Submission
import random
from . import *


class PlayerBot(Bot):
    def play_round(self):

        yield Submission(Survey, {
            'race': random.randint(0, 4),
            'gender': random.randint(0, 2),
            'age': random.randint(18, 65),
            'language': random.randint(0, 1),
            'year': random.randint(0, 4),
            'major': 'Economics',
        }, check_html=False)

        yield Submission(Instructions, check_html=False)

        yield Submission(Payment, check_html=False)

        yield Submission(Conclusion, check_html=False)