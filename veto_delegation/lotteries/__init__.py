from otree.api import *
import json
import random
import numpy as np


doc = """
Risk preferences
"""


class C(BaseConstants):
    NAME_IN_URL = 'lotteries'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1

    single = 0

class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    lottery = models.StringField()


# FUNCTIONS
def set_payoffs(player):
    payoff_matrix = {
        0: [8, 26, 21, 16, 11, 10, 10],
        1: [12, 30, 25, 20, 15, 12, 11],
        2: [16, 25, 30, 25, 20, 15, 12],
        3: [20, 20, 25, 30, 25, 20, 15],
        4: [24, 15, 20, 25, 30, 25, 20],
        5: [28, 12, 15, 20, 25, 30, 25],
        6: [32, 11, 12, 15, 20, 25, 30],
        7: [36, 10, 11, 12, 15, 20, 25],
        8: [40, 10, 10, 11, 12, 15, 20]
    }

    # Convert minSlider and maxSlider to integers
    min_Slider = int(player.minSlider)
    max_Slider = int(player.maxSlider)

    robotChoices = [payoff_matrix[0][player.vetoer_bias]]  # Start with row 0 value
    # Iterate over all rows (1-8) and replace out-of-range values with 0
    robotChoices.extend([
        payoff_matrix[y][player.vetoer_bias] if min_Slider <= y <= max_Slider else 0
        for y in range(1, len(payoff_matrix))  # Start from 1 to avoid duplicate row 0
    ])

    print("Robot ideal X=", player.vetoer_bias, "Robot choices=", robotChoices)

    robotMax = max(robotChoices)
    robotChoice = robotChoices.index(robotMax)  # Index within X
    player.robotChoice = robotChoice
    print(robotChoice)

    player.payoff = payoff_matrix[robotChoice][0]
    print(player.payoff)


def creating_session(subsession):

    for player in subsession.get_players():
        # Load the JSON file
        with open("dice_rolls.json", "r") as f:
            dice_rolls = json.load(f)

        # Randomly select an index
        random_index = random.choice(list(dice_rolls.keys()))

        # Get the corresponding dice rolls
        selected_roll = dice_rolls[random_index]

        # Select a distribution
        if subsession.round_number == 1:
            # Generate a single random permutation of [1, 2, 3] and store it
            player.participant.sample = random.sample([1, 2, 3], k=3)

        dist = player.participant.sample[subsession.round_number-1]

        # Assign on ordering
        player.drawLow = min(selected_roll)
        player.drawMed = sorted(selected_roll)[1]  # Median value
        player.drawHigh = max(selected_roll)

        if dist == 1:
            player.roundType = 1
            player.vetoer_bias = player.drawLow
            player.roundName = "lowest"

        elif dist == 2:
            player.roundType = 2
            player.vetoer_bias = player.drawMed
            player.roundName = "middle"

        else:
            player.roundType = 3
            player.vetoer_bias = player.drawHigh
            player.roundName = "highest"

# PAGES


class Instructions(Page):
    pass

class lotteries(Page):
    form_model = 'player'
    form_fields = ['lottery']

class Waiting(WaitPage):
    wait_for_all_groups = True

    body_text = "Waiting for all participants to complete Part Three."

page_sequence = [Instructions, lotteries, Waiting]
