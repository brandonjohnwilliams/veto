from otree.api import *
import json
import random
import numpy as np


doc = """
Other regarding
"""


class C(BaseConstants):
    NAME_IN_URL = 'dictator'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 3

    single = 0

class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    dictator_choice = models.IntegerField()
    dictator_type = models.IntegerField()


# FUNCTIONS
def set_payoffs(player):
    dictator = {
        1: {
            1: {"take": 20, "give": 30},
            2: {"take": 24, "give": 25},
            3: {"take": 28, "give": 20},
            4: {"take": 32, "give": 15}
        },
        2: {
            1: {"take": 16, "give": 25},
            2: {"take": 20, "give": 20},
            3: {"take": 24, "give": 15},
            4: {"take": 16, "give": 25}
        },
        3: {
            1: {"take": 28, "give": 25},
            2: {"take": 32, "give": 30},
            3: {"take": 36, "give": 25},
            4: {"take": 40, "give": 20}
        }
    }

    # # Use modulo in case rounds go beyond the list length
    # group_key = lottery_order[(player.round_number - 1) % len(lottery_order)]
    #
    # # Safely get the group dictionary
    # group_dict = all_lotteries.get(group_key)
    # if not group_dict:
    #     print(f"Group key {group_key} not found in all_lotteries.")
    #     return
    #
    # # Safely get the selected lottery details
    # selected_lottery = group_dict.get(player.lottery)
    # if not selected_lottery:
    #     print(f"Lottery {player.lottery} not found in {group_key}.")
    #     return
    #
    # # Get the "lot" dictionary
    # lot_distribution = selected_lottery.get("lot")
    #
    # # Optional: Save it in player or participant.vars for future use
    # player.participant.vars["lot_distribution"] = lot_distribution
    #
    # # Example: Pick a payoff from the lot using probabilities
    # # (This assumes the values in `lot_distribution` are percentages)
    # from random import choices
    #
    # outcomes = list(lot_distribution.keys())
    # weights = list(lot_distribution.values())
    #
    # chosen_outcome = choices(outcomes, weights=weights, k=1)[0]
    # player.payoff = chosen_outcome
    #
    # print(f"Round {player.round_number} - {player.lottery}: payoff set to {player.payoff}")


def creating_session(subsession):
    pass

# PAGES


class Instructions(Page):
    @staticmethod
    def is_displayed(player):
        return player.round_number == 1

    @staticmethod
    def before_next_page(player, timeout_happened):
        if player.round_number == 1:
            shuffled = [3, 1, 6]
            random.shuffle(shuffled)
            player.participant.vars['dictator_order'] = shuffled


class dictator(Page):
    form_model = 'player'
    form_fields = ['dictator_choice']
    @staticmethod
    def js_vars(player):
        player.dictator_type = player.participant.vars['dictator_order'][player.round_number - 1]


        # for setting the payoffs:

        dictator = {
            3: {
                1: {"take": 20, "give": 30},
                2: {"take": 24, "give": 25},
                3: {"take": 28, "give": 20},
                4: {"take": 32, "give": 15}
            },
            1: {
                1: {"take": 16, "give": 25},
                2: {"take": 20, "give": 20},
                3: {"take": 24, "give": 15},
                4: {"take": 28, "give": 12}
            },
            6: {
                1: {"take": 28, "give": 25},
                2: {"take": 32, "give": 30},
                3: {"take": 36, "give": 25},
                4: {"take": 40, "give": 20}
            }
        }

        dictatorDict = dictator[player.dictator_type]

        return dict(
            dictator=dictatorDict,
        )

    # @staticmethod
    # def before_next_page(player: Player, timeout_happened):
    #     set_payoffs(player)
    #
    #     # Run at the end
    #     if player.round_number == C.NUM_ROUNDS:
    #         # Check if the player is the lucky one
    #         lucky_player = int(player.participant.label)
    #         if lucky_player == int(player.session.vars['PartThreePay']):
    #             # Draw one of the rounds to pay
    #             lucky_round = random.randint(1, C.NUM_ROUNDS)
    #             lucky_draw = player.in_round(lucky_round)
    #             player.participant.vars['BonusPay'] = lucky_draw.payoff
    #             print(f"Paying {player.session.vars['PartThreePay']} a bonus of {player.participant.vars['BonusPay']}")

    @staticmethod
    def before_next_page(player, timeout_happened):

        #for testing:
        if timeout_happened:
            player.dictator_choice = 1

        dictator = {
            3: {
                1: {"take": 20, "give": 30},
                2: {"take": 24, "give": 25},
                3: {"take": 28, "give": 20},
                4: {"take": 32, "give": 15}
            },
            1: {
                1: {"take": 16, "give": 25},
                2: {"take": 20, "give": 20},
                3: {"take": 24, "give": 15},
                4: {"take": 28, "give": 12}
            },
            6: {
                1: {"take": 28, "give": 25},
                2: {"take": 32, "give": 30},
                3: {"take": 36, "give": 25},
                4: {"take": 40, "give": 20}
            }
        }

        # Run at the end
        if player.round_number == C.NUM_ROUNDS:
            # Check if the player is the lucky one
            lucky_player = int(player.participant.label)
            if lucky_player == int(player.session.vars['PartFourPayGive']):
                # Draw one of the rounds to pay
                lucky_round = random.randint(1, C.NUM_ROUNDS)
                lucky_draw = player.in_round(lucky_round)
                choice = lucky_draw.dictator_choice # save the choice within the type
                mapping = lucky_draw.dictator_type # save the type mapping
                player.participant.vars['BonusPay'] = dictator[mapping][choice]['take']
                player.session.vars['GiveAmount'] = dictator[mapping][choice]['give']
                print(
                    f"Storing {player.session.vars['GiveAmount']} to give.")
                print(f"Paying {player.session.vars['PartFourPayGive']} a bonus of {player.participant.vars['BonusPay']}")



class Waiting(WaitPage):
    @staticmethod
    def is_displayed(player):
        return player.round_number == C.NUM_ROUNDS



    wait_for_all_groups = True

    body_text = "Waiting for all participants to complete Part Four."

page_sequence = [Instructions, dictator, Waiting]
