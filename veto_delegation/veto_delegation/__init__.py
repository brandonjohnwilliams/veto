from otree.api import *
import json
import random

doc = """
Veto Delegation
"""


class C(BaseConstants):
    NAME_IN_URL = 'veto_delegation'
    PLAYERS_PER_GROUP = 2
    NUM_ROUNDS = 15
    REMATCH_INTERVAL = 5  # Reassign roles after every X rounds

    SELLER_ROLE = 'Seller'
    BUYER_ROLE = 'Buyer'

    single = 0

    setZero = 0  # define as such to remove buyer payoff column


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    minSlider = models.IntegerField()  # defines the left side of the delegated range
    maxSlider = models.IntegerField()  # defines the right side of the delegated range

    response = models.IntegerField()  # numerical response of the vetoer

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
    single = models.IntegerField()


# FUNCTIONS
def set_payoffs(group):
    payoff_matrix = {
        0: [4, 25, 20, 15, 10, 5, 4],
        1: [8, 30, 25, 20, 15, 10, 5],
        2: [12, 25, 30, 25, 20, 15, 10],
        3: [16, 20, 25, 30, 25, 20, 15],
        4: [20, 15, 20, 25, 30, 25, 20],
        5: [24, 10, 15, 20, 25, 30, 25],
        6: [28, 5, 10, 15, 20, 25, 30],
        7: [32, 4, 5, 10, 15, 20, 25],
        8: [36, 3, 4, 5, 10, 15, 20]
    }
    p1 = group.get_player_by_id(1)
    p2 = group.get_player_by_id(2)

    p1.payoff = payoff_matrix[group.response][0]
    p2.payoff = payoff_matrix[group.response][group.vetoer_bias]

    print(f"Seller payoff: {p1.payoff}")
    print(f"Buyer payoff: {p2.payoff}")


def creating_session(subsession):

    for player in subsession.get_players():
        if player.subsession.session.config['take_it_or_leave_it']:
            player.single = 1
        else:
            player.single = 0

    # Sets role for 1-5 then reverses for 6-10 and then reverts for 11-15
    if 5 < subsession.round_number < 11:
        subsession.group_randomly(fixed_id_in_group=True)
        matrix = subsession.get_group_matrix()

        for row in matrix:
            row.reverse()

        subsession.set_group_matrix(matrix)
    else:
        subsession.group_randomly(fixed_id_in_group=True)

    # Load the JSON file
    with open("dice_rolls.json", "r") as f:
        dice_rolls = json.load(f)

    # Randomly select an index
    random_index = random.choice(list(dice_rolls.keys()))

    # Select a distribution
    dist = random.choice([1, 2, 3])

    # Get the corresponding dice rolls
    selected_roll = dice_rolls[random_index]

    for group in subsession.get_groups():

        # Assign on ordering
        group.drawLow = min(selected_roll)
        group.drawMed = sorted(selected_roll)[1]  # Median value
        group.drawHigh = max(selected_roll)

        if dist == 1:
            group.roundType = 1
            group.vetoer_bias = group.drawLow
            group.roundName = "low"

        elif dist == 2:
            group.roundType = 2
            group.vetoer_bias = group.drawMed
            group.roundName = "middle"

        else:
            group.roundType = 3
            group.vetoer_bias = group.drawHigh
            group.roundName = "high"


# PAGES
class RolesIntro(Page):
    timeout_seconds = 15

    @staticmethod
    def is_displayed(player):
        return (player.round_number - 1) % C.REMATCH_INTERVAL == 0


class Roles(Page):
    @staticmethod
    def js_vars(player):
        group = player.group
        return dict(
            selectedX=group.vetoer_bias,
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


class Chat(Page):
    @staticmethod
    def is_displayed(player):
        return player.session.config['chat'] == True

    @staticmethod
    def js_vars(player):
        group = player.group
        return dict(
            selectedX=group.vetoer_bias,
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


class Proposal(Page):
    form_model = 'group'
    form_fields = ['minSlider', 'maxSlider']

    @staticmethod
    def is_displayed(player):
        return player.role == C.SELLER_ROLE

    @staticmethod
    def js_vars(player):
        return dict(
            round_type=player.group.roundType,
            selectedX=C.setZero,
            fromM=1,
            toM=8,
            single=player.single
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


class WaitForP1(WaitPage):
    title_text = "Please wait"
    body_text = "Waiting for the Seller to make his or her choice"


class Response(Page):
    form_model = 'group'
    form_fields = ['response']

    @staticmethod
    def is_displayed(player):
        return player.role == C.BUYER_ROLE

    @staticmethod
    def js_vars(player):
        group = player.group
        return dict(
            selectedX=player.group.vetoer_bias,
            fromM=group.minSlider,
            toM=group.maxSlider,
            response=1,
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

    @staticmethod
    def before_next_page(player, timeout_happened):
        print("Player select: ", player.group.response)


class WaitForP2(WaitPage):
    title_text = "Please wait"
    body_text = "Waiting for the Buyer to make his or her choice"

    after_all_players_arrive = set_payoffs


class Results(Page):
    timeout_seconds = 15
    @staticmethod
    def js_vars(player):

        # Initialize empty lists
        roundName_list = []
        idealX_list = []
        offerMin_list = []
        offerMax_list = []
        choice_list = []
        payoff_list = []

        # Loop through each round
        for i in range(1,player.round_number + 1):  # Assuming num_rounds is defined
            prev_player = player.in_round(i)

            # Append values from the respective round
            roundName_list.append(prev_player.group.roundName)
            idealX_list.append(prev_player.group.vetoer_bias)
            offerMin_list.append(prev_player.group.minSlider)
            offerMax_list.append(prev_player.group.maxSlider)
            choice_list.append(prev_player.group.response)
            payoff_list.append(prev_player.payoff)


        return dict(
            round=player.round_number,

            # loop these variables
            idealX=idealX_list,
            offerMin=offerMin_list,
            offerMax=offerMax_list,
            choice=choice_list,
            payoff=payoff_list,
            roundName=roundName_list,
        )





page_sequence = [RolesIntro, Roles, Chat, Proposal, WaitForP1, Response, WaitForP2, Results]
