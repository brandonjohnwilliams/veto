from otree.api import Bot, Submission
import random
from . import *


class PlayerBot(Bot):
    def play_round(self):

        if self.player.round_number == 1:
            possible_responses = [-5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 'ALWAYS_A']
            response = random.choice(possible_responses)

            yield ChoiceInstructions, {
                'response': response,
            }

        yield Submission(InstructionsFeedback, check_html=False)

        possible_responses = [-5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 'ALWAYS_A']
        response = random.choice(possible_responses)

        yield ChoiceInstructions, {
            'response': response,
        }