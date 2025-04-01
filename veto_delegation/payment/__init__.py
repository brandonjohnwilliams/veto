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
    NUM_ROUNDS = 6

    single = 0

class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    lottery = models.StringField()

def creating_session(subsession):
    pass

# PAGES
class Instructions(Page):
    pass

class Payment(Page):
    @staticmethod
    def vars_for_template(player):
        participant = player.participant

        PartOnePay = participant.vars.get('PartOnePayoff')
        BonusPay = participant.vars.get('BonusPay')
        Round = participant.vars.get('PayRound')

        PartTwo = 1 if participant.label == player.session.vars.get('PartTwoPay') else 0
        PartThree = 1 if participant.label == player.session.vars.get('PartThreePay') else 0
        PartFour = 1 if participant.label == player.session.vars.get('PartFourPay') else 0

        return dict(
            PartOnePay=PartOnePay,
            BonusPay=BonusPay,
            Round=Round,
            PartTwo=PartTwo,
            PartThree=PartThree,
            PartFour=PartFour,
        )


class Conclusion(WaitPage):
    pass

page_sequence = [Instructions, Payment, Conclusion]
