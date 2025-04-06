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
    PartThreePay = models.IntegerField()
    PartFourGive = models.IntegerField()
    PartFourReceive = models.IntegerField()

def creating_session(subsession):
    pass

# PAGES
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

        PartTwo = 1 if int(player.participant.label) == player.session.vars.get('PartTwoPay') else 0
        PartThree = 1 if int(player.participant.label) == player.session.vars.get('PartThreePay') else 0
        PartFourGive= 1 if int(player.participant.label) == player.session.vars.get('PartFourPayGive') else 0
        PartFourReceive = 1 if int(player.participant.label) == player.session.vars.get('PartFourPayReceive') else 0
        print(PartTwo, PartThree, PartFourGive, PartFourReceive)

        player.totalPay = int(PartOnePay + BonusPay + 8)
        player.label = int(player.participant.label)
        player.PartOnePay = PartOnePay
        if PartTwo == 1:
            player.PartTwoPay = int(player.participant.vars.get('BonusPay'))
        if PartThree == 1:
            player.PartThreePay = int(player.participant.vars.get('BonusPay'))
        if PartFourGive == 1:
            player.PartFourGive = int(player.participant.vars.get('BonusPay'))
        if PartFourReceive == 1:
            player.PartFourReceive = int(player.participant.vars.get('BonusPay'))
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


class Conclusion(WaitPage):
    pass

page_sequence = [Instructions, Payment, Conclusion]
