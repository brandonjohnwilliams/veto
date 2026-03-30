from otree.api import Bot, Submission
import random
import time
from . import *

class PlayerBot(Bot):
    def play_round(self):

        if self.player.round_number == 1:
            yield Submission(Begin, check_html=False)

        if (self.player.round_number - 1) % C.REMATCH_INTERVAL == 0:
            yield Submission(RolesIntro, check_html=False)

        yield Submission(Roles, check_html=False)

        if self.player.session.config['chat']:
            yield Submission(Chat, check_html=False)

        # Randomize slider inputs
        max_slider = random.randint(1, 8)
        min_slider = random.randint(1, max_slider)

        yield Proposal, {
            'minSlider': min_slider,
            'maxSlider': max_slider,
        }

