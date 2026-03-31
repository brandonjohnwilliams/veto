from otree.api import Bot, Submission
import random
from . import *


class PlayerBot(Bot):
    def play_round(self):

        if self.player.round_number == 1:
            yield Submission(Intro, check_html=False)
            yield Submission(Instructions, check_html=False)
            yield Submission(RolesIntro, check_html=False)

        yield Submission(Roles, check_html=False)

        # Randomize slider inputs
        min_slider = random.randint(1, 8)
        max_slider = random.randint(min_slider, 8)

        yield Submission(Proposal, {
            'minSlider': min_slider,
            'maxSlider': max_slider,
            'thetaRange': random.randint(min_slider, max_slider),
        }, check_html=False)

        # NoZeroWait is only shown on round 3 when test == 0
        # (WaitPages are handled automatically by oTree bots)