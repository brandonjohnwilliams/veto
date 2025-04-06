from otree.api import *
import numpy as np



doc = """
Introduction and instructions
"""


class C(BaseConstants):
    NAME_IN_URL = 'introduction'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1

    round_type = 2 # defined only explicitly for the practice round

    setZero = 0  # define as such to remove buyer payoff column

class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    response = models.IntegerField() # numerical response of the vetoer    vetoer_bias = models.IntegerField()






class Player(BasePlayer):
    single = models.IntegerField()
    chat = models.IntegerField()

    minSlider = models.IntegerField() # defines the left side of the delegated range
    maxSlider = models.IntegerField() # defines the right side of the delegated range

    selectedX = models.IntegerField()

    response = models.IntegerField()

    sellerPayoff = models.IntegerField()
    buyerPayoff = models.IntegerField()

# FUNCTIONS


def creating_session(subsession):

    for player in subsession.get_players():
        if player.subsession.session.config['take_it_or_leave_it']:
            player.single = 1
        else:
            player.single = 0
        if player.subsession.session.config['chat']:
            player.chat = 1
        else:
            player.chat = 0

# PAGES
class LandingPage(Page):
    pass

class Introduction(Page):
    pass

class PartOne(Page):
    @staticmethod
    def vars_for_template(player):
        return dict(
            single=player.single,
            chat=player.chat,
        )

class PayoffsSeller(Page):
    pass
    @staticmethod
    def js_vars(player):
        return dict(
            selectedX=0,
        )

class PayoffsBuyerX(Page):
    pass
    @staticmethod
    def js_vars(player):
        return dict(
            selectedX=0,
        )

class DeterminingX(Page):
    pass

class RoundTiming(Page):
    @staticmethod
    def vars_for_template(player):
        return dict(
            single=player.single,
            chat=player.chat,
        )

class ExampleDraws(Page):
    timeout_seconds = 60

class ChatOnly(Page):
    @staticmethod
    def is_displayed(player):
        return player.session.config['chat'] == 1

class SellersChoice(Page):
    @staticmethod
    def vars_for_template(player):
        return dict(
            single=player.single,
            chat=player.chat,
        )

class SellerView(Page):
    form_model = 'player'
    form_fields = ['minSlider', 'maxSlider']
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


class BuyersChoice(Page):
    pass

class BuyersView(Page):
    form_model = 'player'
    form_fields = ['response']

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


class Results(Page):

    @staticmethod
    def js_vars(player):
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

        sellerPayoff = payoff_matrix[player.response][0]
        buyerPayoff = payoff_matrix[player.response][2]

        return dict(
            round=player.round_number,
            offerMin=player.minSlider,
            offerMax=player.maxSlider,
            choice=player.response,
            seller_payoff=sellerPayoff,
            buyer_payoff=buyerPayoff,
            roundName="Middle",
            role="Seller"
        )


class PayoffsRecap(Page):
    @staticmethod
    def js_vars(player):
        return dict(
            selectedX=C.setZero,  # Selecting 0 removes the column
            chat=player.chat,
        )

    @staticmethod
    def vars_for_template(player):
        return dict(
            chat=player.chat,
        )


page_sequence = [
    LandingPage, Introduction, PartOne, PayoffsSeller, DeterminingX, RoundTiming,

    ExampleDraws,
    ChatOnly,
    SellerView,
    SellerWait,
    BuyersView,
    BuyerWait,
    Results,
    PayoffsRecap]
