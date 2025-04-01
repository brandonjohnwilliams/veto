from otree.api import *
import json
import random
import numpy as np


doc = """
Versus non-human player
"""


class C(BaseConstants):
    NAME_IN_URL = 'robot'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 3

    single = 0

class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    minSlider = models.IntegerField()  # defines the left side of the delegated range
    maxSlider = models.IntegerField()  # defines the right side of the delegated range

    robotChoice = models.IntegerField()  # numerical response of the robot buyer

    # dice rolls
    vetoer_bias = models.IntegerField()
    drawLow = models.IntegerField()
    drawMed = models.IntegerField()
    drawHigh = models.IntegerField()

    selectedX = models.IntegerField()

    # Distributions
    roundType = models.IntegerField()
    roundName = models.StringField()


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

    # print("Robot ideal X=", player.vetoer_bias, "Robot choices=", robotChoices)

    robotMax = max(robotChoices)
    robotChoice = robotChoices.index(robotMax)  # Index within X
    player.robotChoice = robotChoice
    # print(robotChoice)

    player.payoff = payoff_matrix[robotChoice][0]
    # print(player.payoff)


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
class Intro(Page):
    @staticmethod
    def is_displayed(player):
        return player.round_number == 1

class Instructions(Page):
    @staticmethod
    def is_displayed(player):
        return player.round_number == 1

class robot(Page):
    form_model = 'player'
    form_fields = ['minSlider','maxSlider']

    @staticmethod
    def js_vars(player):
        return dict(
            round_type=player.roundType,
            single_treat=C.single,
            fromM=1,
            toM=8,
            roundType=player.roundType,
        )

    @staticmethod
    def vars_for_template(player):
        return dict(
            roundType=player.roundType,
            roundName=player.roundName,
        )

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        set_payoffs(player)

# class Results(Page):
#     timeout_seconds = 15
#     @staticmethod
#     def js_vars(player):
#
#         # Initialize empty lists
#         roundName_list = []
#         idealX_list = []
#         offerMin_list = []
#         offerMax_list = []
#         choice_list = []
#         payoff_list = []
#
#         # Loop through each round
#         for i in range(1,player.round_number + 1):  # Assuming num_rounds is defined
#             prev_player = player.in_round(i)
#
#             # Append values from the respective round
#             roundName_list.append(prev_player.roundName)
#             idealX_list.append(prev_player.vetoer_bias)
#             offerMin_list.append(prev_player.minSlider)
#             offerMax_list.append(prev_player.maxSlider)
#             choice_list.append(prev_player.robotChoice)
#             payoff_list.append(prev_player.payoff)
#
#
#         return dict(
#             round=player.round_number,
#
#             # loop these variables
#             idealX=idealX_list,
#             offerMin=offerMin_list,
#             offerMax=offerMax_list,
#             choice=choice_list,
#             payoff=payoff_list,
#             roundName=roundName_list,
#         )
#
#     @staticmethod
#     def vars_for_template(player):
#         return dict(
#             round_type=player.roundType,
#             roundName=player.roundName,
#         )
#
#     @staticmethod
#     def before_next_page(player, timeout_happened):
#         # Run at the end
#         if player.round_number == C.NUM_ROUNDS:
#             # Check if the player is the lucky one
#             lucky_player = int(player.participant.label)
#             if lucky_player == int(player.session.vars['PartTwoPay']):
#                 # Draw one of the rounds to pay
#                 lucky_round = random.randint(1, C.NUM_ROUNDS)
#                 lucky_draw = player.in_round(lucky_round)
#                 player.participant.vars['BonusPay'] = lucky_draw.payoff
#                 print(f"Paying {player.session.vars['PartTwoPay']} a bonus of {player.participant.vars['BonusPay']}")

class WaitPage2(WaitPage):
    @staticmethod
    def is_displayed(player):
        return player.round_number == 3

    wait_for_all_groups = True

    body_text = "Waiting for all participants to complete Part Two."

page_sequence = [Intro, Instructions, robot, WaitPage2]
