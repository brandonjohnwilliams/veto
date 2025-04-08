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

    single = models.IntegerField()

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
        # Step 1: Select a distribution
        if subsession.round_number == 1:
            # Generate a single random permutation of [1, 2, 3] and store it
            player.participant.sample = random.sample([1, 2, 3], k=3)

        dist = player.participant.sample[subsession.round_number-1]

        # Step 2: Define ballData depending on dist
        if dist == 3:
            ball_data = [
                {"count": 1, "label": 1},
                {"count": 1, "label": 2},
                {"count": 3, "label": 3},
                {"count": 4, "label": 4},
                {"count": 5, "label": 5},
                {"count": 6, "label": 6},
            ]
        elif dist == 2:
            ball_data = [
                {"count": 2, "label": 1},
                {"count": 3, "label": 2},
                {"count": 5, "label": 3},
                {"count": 5, "label": 4},
                {"count": 3, "label": 5},
                {"count": 2, "label": 6},
            ]
        else:
            ball_data = [
                {"count": 6, "label": 1},
                {"count": 5, "label": 2},
                {"count": 4, "label": 3},
                {"count": 3, "label": 4},
                {"count": 1, "label": 5},
                {"count": 1, "label": 6},
            ]

        # Step 3: Build the weighted pool
        weighted_pool = []
        for spec in ball_data:
            weighted_pool.extend([spec["label"]] * spec["count"])

        # Step 4: Randomly draw one value
        selectedX = random.choice(weighted_pool)

        # Step 5: Store the value
        player.vetoer_bias = selectedX

        if dist == 1:
            player.roundType = 1
            player.roundName = "Low"

        elif dist == 2:
            player.roundType = 2
            player.roundName = "Middle"

        else:
            player.roundType = 3
            player.roundName = "High"

        # Step 6: Confirm menu or take-it-or-leave-it
        player.single = 1 if player.subsession.session.config['take_it_or_leave_it'] else 0

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
            single=player.single,
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
    def before_next_page(player, timeout_happened):
        set_payoffs(player)

        # Run at the end
        if player.round_number == C.NUM_ROUNDS:
            # Check if the player is the lucky one
            lucky_player = int(player.participant.label)
            if lucky_player == int(player.session.vars['PartTwoPay']):
                # Draw one of the rounds to pay
                lucky_round = random.randint(1, C.NUM_ROUNDS)
                lucky_draw = player.in_round(lucky_round)
                player.participant.vars['BonusPay'] = lucky_draw.payoff
                print(f"Part Two: Paying {player.session.vars['PartTwoPay']} a bonus of {player.participant.vars['BonusPay']}")
            else:
                print("No robot award.")


class WaitPage2(WaitPage):
    @staticmethod
    def is_displayed(player):
        return player.round_number == 3

    wait_for_all_groups = True

    body_text = "Waiting for all participants to complete Part Two."



page_sequence = [Intro, Instructions, robot, WaitPage2]
