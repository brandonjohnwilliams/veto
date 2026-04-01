from otree.api import Bot, Submission
import random
import time
from . import *

class PlayerBot(Bot):
    def play_round(self):

        if self.player.round_number == 1:
            yield Submission(Instructions, check_html=False)

        yield Submission(Roles, check_html=False)

        # Randomize slider inputs
        max_slider = random.randint(1, 8)
        if self.player.single == 1:
            min_slider = max_slider
        else:
            min_slider = random.randint(1, max_slider)

        yield robot, {
            'minSlider': min_slider,
            'maxSlider': max_slider,
        }

