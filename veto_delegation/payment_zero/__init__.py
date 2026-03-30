from otree.api import *
import json
import random
import numpy as np


doc = """
Payment
"""


class C(BaseConstants):
    NAME_IN_URL = 'payment'
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
    PartThreePay1 = models.IntegerField()
    PartThreePay2 = models.IntegerField()
    PartThreePay3 = models.IntegerField()
    # PartFourGive = models.IntegerField()
    # PartFourReceive = models.IntegerField()
    PartFourPay1 = models.IntegerField()
    PartFourPay2 = models.IntegerField()
    PartFourPay3 = models.IntegerField()

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
    @staticmethod
    def before_next_page(player, timeout_happened):
        lucky_player = int(player.participant.label)
        if lucky_player == int(player.session.vars['PartFourPayReceive']):
            player.participant.vars['BonusPay'] = player.session.vars['GiveAmount']
            print(
                f"Paying {player.session.vars['PartFourPayReceive']} a bonus of {player.participant.vars['BonusPay']}")

class Payment(Page):
    @staticmethod
    def vars_for_template(player):

        PartOnePay = int(player.participant.vars.get('PartOnePayoff'))
        BonusPay = int(player.participant.vars.get('BonusPay'))
        Round = player.participant.vars.get('PayRound')

        label = int(player.participant.label)

        PartTwo_Proposer  = 1 if label == player.session.vars.get('PartTwoPayProposer')  else 0
        PartTwo_Responder = 1 if label == player.session.vars.get('PartTwoPayResponder') else 0
        PartThree1         = 1 if label == player.session.vars.get('PartThreePay1')         else 0
        PartThree2 = 1 if label == player.session.vars.get('PartThreePay2') else 0
        PartThree3 = 1 if label == player.session.vars.get('PartThreePay3') else 0
        PartFour1 = 1 if label == player.session.vars.get('PartFourPay1') else 0
        PartFour2 = 1 if label == player.session.vars.get('PartFourPay2') else 0
        PartFour3 = 1 if label == player.session.vars.get('PartFourPay3') else 0

        player.label = label
        player.PartOnePay = PartOnePay

        if PartTwo_Proposer == 1:
            player.PartTwoProposerPay = int(player.participant.vars.get('PartTwoProposerPayoff'))

        if PartTwo_Responder == 1:
            player.PartTwoResponderPay = int(player.participant.vars.get('PartTwoResponderPayoff'))

        if PartThree1 == 1:
            player.PartThreePay = int(player.participant.vars.get('BonusPay'))

        if PartThree2 == 1:
            player.PartThreePay = int(player.participant.vars.get('BonusPay'))

        if PartThree3 == 1:
            player.PartThreePay = int(player.participant.vars.get('BonusPay'))

        # if PartFourGive == 1:
        #     player.PartFourGive = int(player.participant.vars.get('BonusPay'))
        #
        # if PartFourReceive == 1:
        #     player.PartFourReceive = int(player.participant.vars.get('BonusPay'))

        if PartFour1 == 1:
            player.PartFourPay = int(player.participant.vars.get('BonusPay'))

        if PartFour2 == 1:
            player.PartFourPay = int(player.participant.vars.get('BonusPay'))

        if PartFour3 == 1:
            player.PartFourPay = int(player.participant.vars.get('BonusPay'))


        player.totalPay = int(
            PartOnePay
            + BonusPay
            + 8
        )
        #
        # print("------ DEBUGGING PAYOFF LOGIC ------")
        #
        # # Participant vars
        # print("participant.vars:")
        # for k, v in player.participant.vars.items():
        #     print(f"  {k}: {v}")
        #
        # # Session vars
        # print("\nsession.vars:")
        # for k, v in player.session.vars.items():
        #     print(f"  {k}: {v}")
        #
        # # Player attributes
        # print("\nplayer fields:")
        # print(f"  label: {player.participant.label}")
        # print(f"  round_number: {player.round_number}")
        # print(f"  minSlider: {getattr(player, 'minSlider', None)}")
        # print(f"  maxSlider: {getattr(player, 'maxSlider', None)}")
        # print(f"  vetoer_bias: {getattr(player, 'vetoer_bias', None)}")
        # print(f"  payoff: {player.payoff}")
        #
        # # Calculated variables
        # print("\nCalculated fields:")
        # try:
        #     label_int = int(player.participant.label)
        # except (TypeError, ValueError):
        #     label_int = None
        # print(f"  label_int: {label_int}")
        # print(f"  PartTwoPay: {player.session.vars.get('PartTwoPay')}")
        # print(f"  PartThreePay: {player.session.vars.get('PartThreePay')}")
        # print(f"  PartFourPayGive: {player.session.vars.get('PartFourPayGive')}")
        # print(f"  PartFourPayReceive: {player.session.vars.get('PartFourPayReceive')}")
        # print(f"  BonusPay: {player.participant.vars.get('BonusPay')}")
        # print(f"  PartOnePayoff: {player.participant.vars.get('PartOnePayoff')}")
        # print("------ END DEBUG ------\n")

        return dict(
            PartOnePay=PartOnePay,
            Bonus=BonusPay,
            Round=Round,
            PartTwo=PartTwo,
            PartThree=PartThree,
            PartFourGive=PartFourGive,
            PartFourReceive=PartFourReceive,
            TotalPay=player.totalPay
        )


class Conclusion(Page):
    pass

page_sequence = [Survey, Instructions, Payment, Conclusion]
