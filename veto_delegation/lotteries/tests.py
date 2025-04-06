from otree.api import Bot, Submission
import random
import time
from . import *

class PlayerBot(Bot):
    def play_round(self):

        if self.player.round_number == 1:
            yield Submission(Instructions, check_html=False)

        lottery = random.choice(["Lottery A", "Lottery B", "Lottery C", "Lottery D"])

        yield lotteries, {
            'lottery': lottery,
        }

