from otree.api import *
import json
import random
import numpy as np


doc = """
Versus non-human model player in opposite mechanism
"""


class C(BaseConstants):
    NAME_IN_URL = 'opp_mechanism'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 3

    single = 0

    round_type = 1

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
    response = models.IntegerField()

    # Distributions
    roundType = models.IntegerField()
    roundName = models.StringField()


# FUNCTIONS
def set_payoffs(player):

    # # now not needed?
    # payoff_matrix = {
    #     0: [8, 26, 21, 16, 13, 11, 9],
    #     1: [12, 30, 25, 20, 15, 12, 10],
    #     2: [16, 25, 30, 25, 20, 15, 12],
    #     3: [20, 20, 25, 30, 25, 20, 15],
    #     4: [24, 15, 20, 25, 30, 25, 20],
    #     5: [28, 12, 15, 20, 25, 30, 25],
    #     6: [32, 10, 12, 15, 20, 25, 30],
    #     7: [36, 9, 10, 12, 15, 20, 25],
    #     8: [40, 8, 9, 10, 12, 15, 20]
    # }

    # Convert minSlider and maxSlider to integers
    min_Slider = str(player.minSlider if player.minSlider != 0 else 1)
    max_Slider = str(player.maxSlider if player.maxSlider != 0 else 1)

    # Load JSON file
    with open('expected_logit.json', 'r') as f:
        logit = json.load(f)

    # look in round type
    round_dict = logit[player.roundName]
    print("Looking in ", player.roundName)

    # reference player minX and maxX choices
    match_low_dict = round_dict[min_Slider]
    match_high_dict = match_low_dict[max_Slider]
    print("Player choices lead to dict: ", match_high_dict)

    # store matched value
    delegationPay = match_high_dict['SellerD']
    tioliPay = match_high_dict['SellerT']

    print("Delegation pay: ", delegationPay)
    print("TiOL pay: ", tioliPay)

    if player.single == 1:
        player.payoff = tioliPay
    else:
        player.payoff = delegationPay

    print("Paying: ", player.payoff)


def creating_session(subsession):

    for player in subsession.get_players():
        # Step 1: Select a distribution
        if subsession.round_number == 1:

            player.participant.sample = [1, 2, 3]

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

        # Step 6: Reverse to menu or take-it-or-leave-it
        player.single = 0 if player.subsession.session.config['take_it_or_leave_it'] else 1

# PAGES

class Instructions(Page):
    @staticmethod
    def is_displayed(player):
        return player.round_number == 1

    @staticmethod
    def vars_for_template(player):
        test=player.session.config['test']
        return dict(
            single=player.single,
            test=test,
        )


class SellerView(Page):
    form_model = 'player'
    form_fields = ['minSlider', 'maxSlider']

    @staticmethod
    def is_displayed(player):
        return player.round_number == 1

    @staticmethod
    def js_vars(player):
        return dict(
            round_type=C.round_type,
            single=player.single,
            fromM=1,
            toM=8,
        )

    @staticmethod
    def vars_for_template(player: Player):
        return dict(
            roundType=C.round_type,
            single=player.single,
        )


class SellerWait(WaitPage):
    wait_for_all_groups = True
    body_text = "Waiting for all participants to make their choice."

    @staticmethod
    def is_displayed(player):
        return player.round_number == 1

class BuyersView(Page):
    form_model = 'player'
    form_fields = ['response']

    @staticmethod
    def is_displayed(player):
        return player.round_number == 1

    @staticmethod
    def js_vars(player):
        return dict(
            selectedX=3, # Selecting 0 removes the column
            fromM=player.minSlider,
            toM=player.maxSlider,
            round_type=2,
            response=1,
        )

    @staticmethod
    def vars_for_template(player):
        return dict(
            selectedX=3, # Selecting 0 removes the column
            fromM=player.minSlider,
            toM=player.maxSlider,
        )

class BuyerWait(WaitPage):
    wait_for_all_groups = True
    body_text = "Waiting for all participants to make their choice."

    @staticmethod
    def is_displayed(player):
        return player.round_number == 1

class Intermediate(Page):
    @staticmethod
    def is_displayed(player):
        return player.round_number == 1

    @staticmethod
    def vars_for_template(player):
        test=player.session.config['test']
        return dict(
            single=player.single,
            test=test,
        )

class Roles(Page):
    timeout_seconds = 20
    @staticmethod
    def js_vars(player):
        group = player.group
        return dict(
            roundName=player.roundName,
            roundType=player.roundType,

        )

    @staticmethod
    def vars_for_template(player):
        return {
            "roundName": player.roundName,
            "roundType": player.roundType,
        }

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

        player.participant.vars[f"part4round{player.round_number}"] = player.payoff

        if player.session.config['test']:
            lucky_player = int(player.participant.id_in_session)

            for round_num in range(1, C.NUM_ROUNDS + 1):
                winner = round_num + 4
                if lucky_player == int(winner):
                    lucky_draw = player.in_round(round_num)
                    player.participant.vars['BonusPay'] = lucky_draw.payoff
                    print(
                        f"Part Four Round {round_num}: "
                        f"Paying player {lucky_player} a bonus of {player.participant.vars['BonusPay']}"
                    )
                    break  # a player can only win once, no need to check remaining rounds
                else:
                    print(f"Part Four Round {round_num}: Player {lucky_player} is not the winner.")
        else:

            # Check if the player is the lucky one
            lucky_player = int(player.participant.label_id)

            for round_num in range(1, C.NUM_ROUNDS + 1):
                winner = player.session.vars.get(f'PartFourPay{round_num}')
                if lucky_player == int(winner):
                    lucky_draw = player.in_round(round_num)
                    player.participant.vars['BonusPay'] = lucky_draw.payoff
                    print(
                        f"Part Four Round {round_num}: "
                        f"Paying player {lucky_player} a bonus of {player.participant.vars['BonusPay']}"
                    )
                    break  # a player can only win once, no need to check remaining rounds
                else:
                    print(f"Part Four Round {round_num}: Player {lucky_player} is not the winner.")


class WaitPage2(WaitPage):
    @staticmethod
    def is_displayed(player):
        return player.round_number == 3

    wait_for_all_groups = True

    body_text = "Waiting for all participants to complete Part Four."



page_sequence = [Instructions,
                 SellerView,
    SellerWait,
    BuyersView,
    BuyerWait,
    Intermediate,
    Roles,
    robot, WaitPage2]
