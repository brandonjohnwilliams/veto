from otree.api import Bot, Submission
import random
from . import *

page_sequence = [Introduction, ChoiceInstructions, MakeChoice, Payment, Choice]
class PlayerBot(Bot):
    def play_round(self):

        if self.player.round_number == 1:

            yield Submission(Introduction, check_html=False)
            yield Submission(ChoiceInstructions, check_html=False)
            yield Submission(MakeChoice, check_html=False)
            yield Submission(Payment, check_html=False)


        possible_responses = [-5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 'ALWAYS_A']
        response = random.choice(possible_responses)

        yield Choice, {
            'switch_point': response,
        }