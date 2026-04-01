from otree.api import Bot, Submission
import random
import time
from . import *


class PlayerBot(Bot):
    def play_round(self):

        if self.player.round_number == 1:
            yield Submission(RolesIntro, check_html=False)

        yield Submission(Roles, check_html=False)

        min_slider = self.player.minSlider
        max_slider = self.player.maxSlider
        possible_responses = list(range(min_slider, max_slider+1))
        response = random.choice(possible_responses)

        yield Response, {
            'response': response,
        }

        if self.player.round_number == 3:
            yield Submission(Results, check_html=False)

