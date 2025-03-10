from otree.api import *
import numpy as np



doc = """
Introduction and instructions
"""


class C(BaseConstants):
    NAME_IN_URL = 'introduction'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1

    endowment = 25
    veto_amount = 0
    guarantee = 5

    single = 0
    round_type = 2 # defined only explicitly for the practice round

    setZero = 0  # define as such to remove buyer payoff column

class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    minSlider = models.IntegerField() # defines the left side of the delegated range
    maxSlider = models.IntegerField() # defines the right side of the delegated range

    response = models.IntegerField() # numerical response of the vetoer
    veto = models.BooleanField(blank=True, initial=False) # True if vetoed

    vetoer_bias = models.IntegerField()

    selectedX = models.IntegerField()


class Player(BasePlayer):
    quiz3 = models.BooleanField(label="Is 9 a prime number?")

# FUNCTIONS
# PAGES
class Introduction(Page):
    pass

class PartOne(Page):
    pass

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

class DeterminingX(Page):
    pass

class SellersChoice(Page):
    pass

class SellerView(Page):
    @staticmethod
    def js_vars(player):
        return dict(
            round_type=C.round_type,
        )

class BuyersChoice(Page):
    pass

class BuyersView(Page):
    @staticmethod
    def js_vars(player):
        return dict(
            selectedX=2, # Selecting 0 removes the column
            fromM=3,
            toM=6,
        )

class PayoffsRecap(Page):
    @staticmethod
    def js_vars(player):
        return dict(
            selectedX=C.setZero,  # Selecting 0 removes the column
        )



page_sequence = [Introduction, PartOne, Payoffs, PayoffsSeller, PayoffsBuyer, DeterminingX, SellersChoice, SellerView, BuyersChoice, BuyersView, PayoffsRecap]
