from otree.api import Bot, Submission
import random
import time
from . import *

class PlayerBot(Bot):
    def play_round(self):

        if self.player.round_number == 1:
            yield Submission(Instructions, check_html=False)


        # Randomize dictator choice
        choice = random.randint(1, 4)


        yield dictator, {
            'dictator_choice': choice,
        }

