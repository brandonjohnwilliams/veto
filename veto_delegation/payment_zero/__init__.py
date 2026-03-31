from otree.api import *
import json
import random
import numpy as np


doc = """
Payment
"""


class C(BaseConstants):
    NAME_IN_URL = 'payment_zero'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1

    single = 0

class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    lottery = models.StringField()
    totalPay = models.IntegerField()
    label = models.IntegerField()

    # store payment values for quick access
    PartOnePay = models.IntegerField()
    PartTwoPay = models.IntegerField()
    PartTwoProposerPay = models.IntegerField()
    PartTwoResponderPay = models.IntegerField()
    PartThreePay1 = models.IntegerField()
    PartThreePay2 = models.IntegerField()
    PartThreePay3 = models.IntegerField()
    # PartFourGive = models.IntegerField()
    # PartFourReceive = models.IntegerField()
    PartFourPay1 = models.IntegerField()
    PartFourPay2 = models.IntegerField()
    PartFourPay3 = models.IntegerField()
    PartFivePay1 = models.IntegerField()
    PartFivePay2 = models.IntegerField()
    PartFivePay3 = models.IntegerField()
    PartThreePay = models.IntegerField()
    PartFourPay = models.IntegerField()
    PartFivePay = models.IntegerField()


    # survey variables

    age = models.IntegerField(label='What is your age?', min=0, max=100)
    gender = models.IntegerField(
        choices=[[0, 'Male'], [1, 'Female'], [2, 'Other']],
        label='Please select the gender you identify as',
        widget=widgets.RadioSelect,

    )
    year = models.IntegerField(
        choices=[[0, 'Freshman'], [1, 'Sophomore'], [2, 'Junior'], [3, 'Senior'], [4, 'Graduate Student']],
        label='Please select your year in college',
        widget=widgets.RadioSelect,

    )
    major = models.StringField(
        label='What is your major?'
    )
    race = models.IntegerField(label="What is your race/ethnicity?", widget=widgets.RadioSelectHorizontal,
                               choices=[[0, 'Asian'], [1, 'Black'], [2, 'Caucasian'], [3, 'Hispanic'], [4, 'Other']],
                               )
    language = models.IntegerField(label='What is your native language?', widget=widgets.RadioSelectHorizontal,
                                   choices=[[0, 'English'], [1, 'Other']],
                                   )

def creating_session(subsession):
    pass

# PAGES
class Survey(Page):
    form_model = 'player'
    form_fields = ['race', 'gender', 'age', 'language', 'year', 'major']

class Instructions(Page):
    pass

class Payment(Page):
    @staticmethod
    def vars_for_template(player):

        # Helper: safely convert participant.vars values to int, defaulting to 0
        def safe_get(key):
            val = player.participant.vars.get(key)
            return int(val) if val is not None else 0

        PartOnePay = safe_get('PartOnePayoff')
        BonusPay   = safe_get('BonusPay')
        Round      = player.participant.vars.get('PayRound')
        label      = int(player.participant.label)

        player.label     = label
        player.PartOnePay = PartOnePay

        # Initialize all payoff fields to 0 so oTree never reads an unset IntegerField
        player.PartTwoProposerPay = 0
        player.PartTwoResponderPay = 0
        player.PartThreePay1 = 0
        player.PartThreePay2 = 0
        player.PartThreePay3 = 0
        player.PartFourPay1  = 0
        player.PartFourPay2  = 0
        player.PartFourPay3  = 0
        player.PartFivePay1  = 0
        player.PartFivePay2  = 0
        player.PartFivePay3  = 0
        player.PartThreePay  = 0
        player.PartFourPay   = 0
        player.PartFivePay   = 0

        # Part Two
        if label == player.session.vars.get('PartTwoPayProposer'):
            player.PartTwoProposerPay = safe_get('PartTwoProposerPayoff')

        if label == player.session.vars.get('PartTwoPayResponder'):
            player.PartTwoResponderPay = safe_get('PartTwoResponderPayoff')

        # Part Three
        for key in ('PartThreePay1', 'PartThreePay2', 'PartThreePay3'):
            if label == player.session.vars.get(key):
                player.PartThreePay = safe_get('BonusPay')
                break

        # Part Four
        for key in ('PartFourPay1', 'PartFourPay2', 'PartFourPay3'):
            if label == player.session.vars.get(key):
                player.PartFourPay = safe_get('BonusPay')
                break

        # Part Five
        for key in ('PartFivePay1', 'PartFivePay2', 'PartFivePay3'):
            if label == player.session.vars.get(key):
                player.PartFivePay = safe_get('BonusPay')
                break

        player.totalPay = PartOnePay + BonusPay + 8

        return dict(
            PartOnePay=PartOnePay,
            Bonus=BonusPay,
            Round=Round,
            PartTwoProposer=player.PartTwoProposerPay,
            PartTwoResponder=player.PartTwoResponderPay,
            PartThree=player.field_maybe_none('PartThreePay') or 0,
            PartFour=player.PartFourPay,
            PartFive=player.PartFivePay,
            TotalPay=player.totalPay,
        )


class Conclusion(Page):
    pass

page_sequence = [Survey, Instructions, Payment, Conclusion]
