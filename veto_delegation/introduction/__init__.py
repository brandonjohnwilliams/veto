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
class Introduction(Page):
    pass

class PartOne(Page):
    @staticmethod
    def vars_for_template(player):
        return dict(
            single=player.single,
            chat=player.chat,
        )



class Payoffs(Page):
    @staticmethod
    def js_vars(player):
        return dict(
            selectedX=C.setZero,  # Selecting 0 removes the highlighted column
        )

class PayoffsSeller(Page):
    pass
    @staticmethod
    def js_vars(player):
        return dict(
            selectedX=0,
        )

class PayoffsBuyer(Page):
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
    pass

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

    # template_name = 'SellerWaitPage.html'
    #
    # @staticmethod
    # def js_vars(player):
    #     return dict(
    #         round_type=C.round_type,
    #         single=player.single,
    #         fromM=1,
    #         toM=8,
    #     )
    #
    # @staticmethod
    # def vars_for_template(player: Player):
    #     return dict(
    #         roundType=C.round_type,
    #         single=player.single,
    #     )

class BuyersChoice(Page):
    pass

class BuyersView(Page):
    form_model = 'player'
    form_fields = ['minSlider', 'maxSlider']

    @staticmethod
    def js_vars(player):
        return dict(
            selectedX=2, # Selecting 0 removes the column
            fromM=player.minSlider,
            toM=player.maxSlider,
            round_type=2,
            response=1,
        )

    @staticmethod
    def vars_for_template(player):
        return dict(
            selectedX=2, # Selecting 0 removes the column
            fromM=player.minSlider,
            toM=player.maxSlider,
        )

class Results(Page):
    timeout_seconds = 15
    @staticmethod
    def js_vars(player):
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


class PayoffsRecap(Page):
    @staticmethod
    def js_vars(player):
        return dict(
            selectedX=C.setZero,  # Selecting 0 removes the column
        )


page_sequence = [
    # Introduction, PartOne, PayoffsSeller, DeterminingX, RoundTiming,

    # Start here for no instructions on screen
    ExampleDraws,
    # SellersChoice,
    SellerView,
    SellerWait,
    # BuyersChoice,
    BuyersView,
    PayoffsRecap]
