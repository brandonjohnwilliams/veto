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
        if self.player.role == C.SELLER_ROLE:
            yield Proposal, {
                'minSlider': min_slider,
                'maxSlider': max_slider,
            }

        # Random response: 0 or between min and max
        possible_responses = [0] + list(range(min_slider, max_slider + 1))
        response = random.choice(possible_responses)
        if self.player.role == C.BUYER_ROLE:
            yield Response, {
                'response': response,
            }

        yield Submission(Results, check_html=False)
