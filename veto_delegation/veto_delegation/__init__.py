from otree.api import *
import numpy as np



doc = """
Veto Delegation
"""


class C(BaseConstants):
    NAME_IN_URL = 'veto_delegation'
    PLAYERS_PER_GROUP = 2
    NUM_ROUNDS = 3

    endowment = 25
    veto_amount = 0
    guarantee = 5

    single = 0

    setZero = 0  # define as such to remove buyer payoff column


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    minSlider = models.IntegerField() # defines the left side of the delegated range
    maxSlider = models.IntegerField() # defines the right side of the delegated range

    response = models.IntegerField() # numerical response of the vetoer
    veto = models.BooleanField(blank=True, initial=False) # True if vetoed

    # dice rolls
    vetoer_bias = models.IntegerField()
    drawLow = models.IntegerField()
    drawMed = models.IntegerField()
    drawHigh = models.IntegerField()

    selectedX = models.IntegerField()

    # Distributions
    roundType = models.IntegerField()
    roundName = models.StringField()


class Player(BasePlayer):
    pass

# FUNCTIONS
def set_payoffs(group):
    p1 = group.get_player_by_id(1)
    p2 = group.get_player_by_id(2)
    if group.veto == True:
        p1.payoff = C.veto_amount + C.guarantee
        p2.payoff = C.endowment + C.guarantee - np.abs(C.veto_amount - group.vetoer_bias)
    else:
        p1.payoff = group.response + C.guarantee # linear loss from optimal (max)
        p2.payoff = C.endowment + C.guarantee - np.abs(group.response - group.vetoer_bias) # linear loss from optimal


def creating_session(subsession):
    # pulls dice rolls from preset spreadsheet

    import statistics
    import json
    import random

    # Load the JSON file
    with open("dice_rolls.json", "r") as f:
        dice_rolls = json.load(f)

    # Randomly select an index
    random_index = random.choice(list(dice_rolls.keys()))

    # Get the corresponding dice roll
    selected_roll = dice_rolls[random_index]

    print(f"Randomly selected index: {random_index}")
    print(f"Dice roll: {selected_roll}")

    for group in subsession.get_groups():

        # Assign on ordering
        group.drawLow = min(selected_roll)
        group.drawMed = sorted(selected_roll)[1]  # Median value
        group.drawHigh = max(selected_roll)

        if subsession.round_number == 1:
            group.roundType = 1
            group.vetoer_bias = group.drawLow
            group.roundName = "lowest"

        elif subsession.round_number == 2:
            group.roundType = 2
            group.vetoer_bias = group.drawMed
            group.roundName = "middle"

        else:
            group.roundType = 3
            group.vetoer_bias = group.drawHigh
            group.roundName = "highest"

# Use to check if bias draws are being pulled correctly:

# PAGES
class Proposal(Page):
    form_model = 'group'
    form_fields = ['minSlider','maxSlider']

    @staticmethod
    def is_displayed(player):
        return player.id_in_group == 1

    @staticmethod
    def js_vars(player):
        return dict(
            round_type=player.group.roundType,
        )

class WaitForP1(WaitPage):
    title_text = "Please wait"
    body_text = "Waiting for the seller to make his or her choice"


class Response(Page):
    form_model = 'group'
    form_fields = ['response','veto']

    @staticmethod
    def is_displayed(player):
        return player.id_in_group == 2

    @staticmethod
    def js_vars(player):
        group = player.group
        return dict(
            selectedX=player.group.vetoer_bias,
            fromM=group.minSlider,
            toM=group.maxSlider,
        )

    @staticmethod
    def vars_for_template(player):
        group = player.group
        return {
            "selectedX": group.vetoer_bias,
            "drawLow": group.drawLow,
            "drawMed": group.drawMed,
            "drawHigh": group.drawHigh,
            "roundName": group.roundName,
            "roundType": group.roundType,
        }


class WaitForP2(WaitPage):
    after_all_players_arrive = set_payoffs

class Results(Page):
    pass

page_sequence = [Proposal, WaitForP1, Response, WaitForP2, Results]
