from otree.api import Bot, Submission
import random
import time
from . import *

class PlayerBot(Bot):
    def play_round(self):


        yield Submission(Introduction, check_html=False)


        yield ProposalProbs, {
            'quiz1': 5,
            'quiz2': 15,
        }

        yield ProposalMenu, {
            'minSlider': 1,
            'maxSlider': 8,
        }

        yield ProposalQuestions, {
            'quiz3': 0,
            'quiz4': 8,
        }

        payoff_matrix = {
            0: [8, 26, 21, 16, 13, 11, 9],
            1: [12, 30, 25, 20, 15, 12, 10],
            2: [16, 25, 30, 25, 20, 15, 12],
            3: [20, 20, 25, 30, 25, 20, 15],
            4: [24, 15, 20, 25, 30, 25, 20],
            5: [28, 12, 15, 20, 25, 30, 25],
            6: [32, 10, 12, 15, 20, 25, 30],
            7: [36, 9, 10, 12, 15, 20, 25],
            8: [40, 8, 9, 10, 12, 15, 20]
        }

        robotChoices = [payoff_matrix[0][self.player.vetoer_bias]]  # Start with row 0 value
        # Iterate over all rows (1-8) and replace out-of-range values with 0
        robotChoices.extend([
            payoff_matrix[y][self.player.vetoer_bias] if 1 <= y <= 8 else 0
            for y in range(1, len(payoff_matrix))  # Start from 1 to avoid duplicate row 0
        ])

        # print("Robot ideal X=", player.vetoer_bias, "Robot choices=", robotChoices)

        robotMax = max(robotChoices)
        robotChoice = robotChoices.index(robotMax)  # Index within X

        # Filter out zero values for finding the min
        nonzero_choices = [val for val in robotChoices if val != 0]

        if nonzero_choices:
            robotMin = min(nonzero_choices)
            robotChoiceMin = robotChoices.index(robotMin)
        else:
            robotMin = 0  # Or some fallback value if all entries are zero
            robotChoiceMin = -1  # Or some other signal indicating "no valid choice"

        yield MinMaxQuestions, {
            'quiz5': robotMax,
            'quiz6': robotChoice,
            'quiz7': robotMin,
            'quiz8': robotChoiceMin,
        }

