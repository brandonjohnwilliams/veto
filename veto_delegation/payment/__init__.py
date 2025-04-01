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

def creating_session(subsession):
    pass

# PAGES
class Instructions(Page):
    pass

class Payment(Page):
    @staticmethod
    def vars_for_template(player):

        PartOnePay = player.participant.vars.get('PartOnePayoff')
        BonusPay = player.participant.vars.get('BonusPay')
        Round = player.participant.vars.get('PayRound')

        PartTwo = 1 if player.participant.label == player.session.vars.get('PartTwoPay') else 0
        PartThree = 1 if player.participant.label == player.session.vars.get('PartThreePay') else 0
        PartFourGive= 1 if player.participant.label == player.session.vars.get('PartFourPayGive') else 0
        PartFourReceive = 1 if player.participant.label == player.session.vars.get('PartFourPayReceive') else 0

        return dict(
            PartOnePay=PartOnePay,
            Bonus=BonusPay,
            Round=Round,
            PartTwo=PartTwo,
            PartThree=PartThree,
            PartFourGive=PartFourGive,
            PartFourReceive=PartFourReceive,
        )


class Conclusion(WaitPage):
    pass

page_sequence = [Instructions, Payment, Conclusion]
