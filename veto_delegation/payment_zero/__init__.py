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
    totalPay = models.FloatField()
    label = models.IntegerField()
    BonusPay = models.FloatField()

    # store payment values for quick access
    PartOnePay = models.FloatField()
    PartTwoPay = models.FloatField()
    PartTwoProposerPay = models.FloatField()
    PartTwoResponderPay = models.FloatField()
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
    PartThreePay = models.FloatField()
    PartFourPay = models.FloatField()
    PartFivePay = models.FloatField()


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
            return val if val is not None else 0

        PartOnePay = safe_get('PartOnePayoff')
        BonusPay   = float(player.participant.BonusPay)
        Round      = player.participant.vars.get('PayRound')
        label      = int(player.participant.label_id)

        player.label     = label
        player.PartOnePay = PartOnePay
        player.BonusPay = BonusPay
        print("Bonus: ", player.BonusPay)

        # Initialize all payoff fields to 0 so oTree never reads an unset IntegerField
        player.PartTwoPay = 0
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

        if player.participant.BonusPay > 0 :
            if label == player.session.vars.get('PartTwoPayProposer'):
                player.PartTwoPay = float(player.participant.BonusPay)
                player.PartTwoProposerPay = float(player.participant.BonusPay)
                print("Paying: ", label, player.participant.BonusPay)
            if label == player.session.vars.get('PartTwoPayResponder'):
                player.PartTwoPay = float(player.participant.BonusPay)
                player.PartTwoResponderPay = float(player.participant.BonusPay)
                print("Paying: ", label, player.participant.BonusPay)
            if label == player.session.vars.get('PartThreePay1'):
                player.PartThreePay = float(player.participant.BonusPay)
                print("Paying: ", label, player.participant.BonusPay)
            if label == player.session.vars.get('PartThreePay2'):
                player.PartThreePay = float(player.participant.BonusPay)
                print("Paying: ", label, player.participant.BonusPay)
            if label == player.session.vars.get('PartThreePay3'):
                player.PartThreePay = float(player.participant.BonusPay)
                print("Paying: ", label, player.participant.BonusPay)
            if label == player.session.vars.get('PartFourPay1'):
                player.PartFourPay = float(player.participant.BonusPay)
                print("Paying: ", label, player.participant.BonusPay)
            if label == player.session.vars.get('PartFourPay2'):
                player.PartFourPay = float(player.participant.BonusPay)
                print("Paying: ", label, player.participant.BonusPay)
            if label == player.session.vars.get('PartFourPay3'):
                player.PartFourPay = float(player.participant.BonusPay)
                print("Paying: ", label, player.participant.BonusPay)
            if label == player.session.vars.get('PartFivePay1'):
                player.PartFivePay = float(player.participant.BonusPay)
                print("Paying: ", label, player.participant.BonusPay)
            if label == player.session.vars.get('PartFivePay2'):
                player.PartFivePay = float(player.participant.BonusPay)
                print("Paying: ", label, player.participant.BonusPay)
            if label == player.session.vars.get('PartFivePay3'):
                player.PartFivePay = float(player.participant.BonusPay)
                print("Paying: ", label, player.participant.BonusPay)


        player.totalPay = float(PartOnePay + BonusPay + 8)

        return dict(
            PartOnePay=round(PartOnePay, 2),
            Bonus=round(BonusPay, 2),
            Round=Round,
            PartTwoProposer=round(float(player.PartTwoProposerPay), 2),
            PartTwoResponder=round(float(player.PartTwoResponderPay), 2),
            PartThree=round(float(player.PartThreePay), 2),
            PartFour=round(float(player.PartFourPay), 2),
            PartFive=round(float(player.PartFivePay), 2),
            TotalPay=round(float(player.totalPay), 2),
        )


class Conclusion(Page):
    pass

page_sequence = [Survey, Instructions, Payment, Conclusion]
