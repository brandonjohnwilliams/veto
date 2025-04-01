from otree.api import *
import json
import random
import numpy as np


doc = """
Risk preferences
"""


class C(BaseConstants):
    NAME_IN_URL = 'lotteries'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 6

    single = 0

class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    lottery = models.StringField()


# FUNCTIONS
def set_payoffs(player):
    all_lotteries = {
        "DelLow": {
            "Lottery A": {
                "action": "{0} U [1,8]",
                "lot": {8: 0, 12: 30.0, 16: 25.0, 20: 20.0, 24: 15.0, 28: 5.0, 32: 5.0, 36: 0, 40: 0},
                "expec": 18.2,
            },
            "Lottery B": {
                "action": "{0} U [3,8]",
                "lot": {8: 30.0, 12: 0, 16: 0, 20: 45.0, 24: 15.0, 28: 5.0, 32: 5.0, 36: 0, 40: 0},
                "expec": 18.0,
            },
            "Lottery C": {
                "action": "{0} U [5,8]",
                "lot": {8: 55.0, 12: 0, 16: 0, 20: 0, 24: 0, 28: 40.0, 32: 5.0, 36: 0, 40: 0},
                "expec": 17.2,
            },
            "Lottery D": {
                "action": "{0} U [7,8]",
                "lot": {8: 75.0, 12: 0, 16: 0, 20: 0, 24: 0, 28: 0, 32: 0, 36: 25.0, 40: 0},
                "expec": 15.0,
            },
        },
        "TIOLILow": {
            "Lottery A": {
                "action": "{0,1}",
                "lot": {8: 0, 12: 100.0, 16: 0, 20: 0, 24: 0, 28: 0, 32: 0, 36: 0, 40: 0},
                "expec": 12.0,
            },
            "Lottery B": {
                "action": "{0,3}",
                "lot": {8: 30.0, 12: 0, 16: 0, 20: 70.0, 24: 0, 28: 0, 32: 0, 36: 0, 40: 0},
                "expec": 16.4,
            },
            "Lottery C": {
                "action": "{0,5}",
                "lot": {8: 55.0, 12: 0, 16: 0, 20: 0, 24: 0, 28: 45.0, 32: 0, 36: 0, 40: 0},
                "expec": 17.0,
            },
            "Lottery D": {
                "action": "{0,7}",
                "lot": {8: 75.0, 12: 0, 16: 0, 20: 0, 24: 0, 28: 0, 32: 0, 36: 25.0, 40: 0},
                "expec": 15.0,
            },
        },
        "DelMid": {
            "Lottery A": {
                "action": "{0} U [1,8]",
                "lot": {8: 0, 12: 10.0, 16: 15.0, 20: 25.0, 24: 25.0, 28: 15.0, 32: 10.0, 36: 0, 40: 0},
                "expec": 22.0,
            },
            "Lottery B": {
                "action": "{0} U [3,8]",
                "lot": {8: 10.0, 12: 0, 16: 0, 20: 40.0, 24: 25.0, 28: 15.0, 32: 10.0, 36: 0, 40: 0},
                "expec": 22.2,
            },
            "Lottery C": {
                "action": "{0} U [5,8]",
                "lot": {8: 25.0, 12: 0, 16: 0, 20: 0, 24: 0, 28: 65.0, 32: 10.0, 36: 0, 40: 0},
                "expec": 23.4,
            },
            "Lottery D": {
                "action": "{0} U [7,8]",
                "lot": {8: 50.0, 12: 0, 16: 0, 20: 0, 24: 0, 28: 0, 32: 0, 36: 50.0, 40: 0},
                "expec": 22.0,
            },
        },
        "TIOLIMid": {
            "Lottery A": {
                "action": "{0,1}",
                "lot": {8: 0, 12: 100.0, 16: 0, 20: 0, 24: 0, 28: 0, 32: 0, 36: 0, 40: 0},
                "expec": 12.0,
            },
            "Lottery B": {
                "action": "{0,3}",
                "lot": {8: 10.0, 12: 0, 16: 0, 20: 90.0, 24: 0, 28: 0, 32: 0, 36: 0, 40: 0},
                "expec": 18.8,
            },
            "Lottery C": {
                "action": "{0,5}",
                "lot": {8: 25.0, 12: 0, 16: 0, 20: 0, 24: 0, 28: 75.0, 32: 0, 36: 0, 40: 0},
                "expec": 23.0,
            },
            "Lottery D": {
                "action": "{0,7}",
                "lot": {8: 50.0, 12: 0, 16: 0, 20: 0, 24: 0, 28: 0, 32: 0, 36: 50.0, 40: 0},
                "expec": 22.0,
            },
        },
        "DelHigh": {
            "Lottery A": {
                "action": "{0} U [1,8]",
                "lot": {8: 0, 12: 5.0, 16: 5.0, 20: 15.0, 24: 20.0, 28: 25.0, 32: 30.0, 36: 0, 40: 0},
                "expec": 25.8,
            },
            "Lottery B": {
                "action": "{0} U [3,8]",
                "lot": {8: 5.0, 12: 0, 16: 0, 20: 20.0, 24: 20.0, 28: 25.0, 32: 30.0, 36: 0, 40: 0},
                "expec": 25.8,
            },
            "Lottery C": {
                "action": "{0} U [5,8]",
                "lot": {8: 10.0, 12: 0, 16: 0, 20: 0, 24: 0, 28: 60.0, 32: 30.0, 36: 0, 40: 0},
                "expec": 27.2,
            },
            "Lottery D": {
                "action": "{0} U [7,8]",
                "lot": {8: 25.0, 12: 0, 16: 0, 20: 0, 24: 0, 28: 0, 32: 0, 36: 75.0, 40: 0},
                "expec": 29.0,
            },
        },
        "TIOLIHigh": {
            "Lottery A": {
                "action": "{0,1}",
                "lot": {8: 0, 12: 100.0, 16: 0, 20: 0, 24: 0, 28: 0, 32: 0, 36: 0, 40: 0},
                "expec": 12.0,
            },
            "Lottery B": {
                "action": "{0,3}",
                "lot": {8: 5.0, 12: 0, 16: 0, 20: 95.0, 24: 0, 28: 0, 32: 0, 36: 0, 40: 0},
                "expec": 19.4,
            },
            "Lottery C": {
                "action": "{0,5}",
                "lot": {8: 10.0, 12: 0, 16: 0, 20: 0, 24: 0, 28: 90.0, 32: 0, 36: 0, 40: 0},
                "expec": 26.0,
            },
            "Lottery D": {
                "action": "{0,7}",
                "lot": {8: 25.0, 12: 0, 16: 0, 20: 0, 24: 0, 28: 0, 32: 0, 36: 75.0, 40: 0},
                "expec": 29.0,
            },
        },
    }

    # Define the round-to-group mapping
    lottery_order = [
        "DelLow",
        "TIOLILow",
        "DelMid",
        "TIOLIMid",
        "DelHigh",
        "TIOLIHigh",
    ]

    # Use modulo in case rounds go beyond the list length
    group_key = lottery_order[(player.round_number - 1) % len(lottery_order)]

    # Safely get the group dictionary
    group_dict = all_lotteries.get(group_key)
    if not group_dict:
        print(f"Group key {group_key} not found in all_lotteries.")
        return

    # Safely get the selected lottery details
    selected_lottery = group_dict.get(player.lottery)
    if not selected_lottery:
        print(f"Lottery {player.lottery} not found in {group_key}.")
        return

    # Get the "lot" dictionary
    lot_distribution = selected_lottery.get("lot")

    # Optional: Save it in player or participant.vars for future use
    player.participant.vars["lot_distribution"] = lot_distribution

    # Example: Pick a payoff from the lot using probabilities
    # (This assumes the values in `lot_distribution` are percentages)
    from random import choices

    outcomes = list(lot_distribution.keys())
    weights = list(lot_distribution.values())

    chosen_outcome = choices(outcomes, weights=weights, k=1)[0]
    player.payoff = chosen_outcome

    print(f"Round {player.round_number} - {player.lottery}: payoff set to {player.payoff}")


def creating_session(subsession):
    pass

# PAGES


class Instructions(Page):
    @staticmethod
    def is_displayed(player):
        return player.round_number == 1

class lotteries(Page):
    form_model = 'player'
    form_fields = ['lottery']



    @staticmethod
    def js_vars(player):

        # for setting the lotteries:

        all_lotteries = {
            "DelLow": {
                "Lottery A": {
                    "action": "{0} U [1,8]",
                    "lot": {8: 0, 12: 30.0, 16: 25.0, 20: 20.0, 24: 15.0, 28: 5.0, 32: 5.0, 36: 0, 40: 0},
                    "expec": 18.2,
                },
                "Lottery B": {
                    "action": "{0} U [3,8]",
                    "lot": {8: 30.0, 12: 0, 16: 0, 20: 45.0, 24: 15.0, 28: 5.0, 32: 5.0, 36: 0, 40: 0},
                    "expec": 18.0,
                },
                "Lottery C": {
                    "action": "{0} U [5,8]",
                    "lot": {8: 55.0, 12: 0, 16: 0, 20: 0, 24: 0, 28: 40.0, 32: 5.0, 36: 0, 40: 0},
                    "expec": 17.2,
                },
                "Lottery D": {
                    "action": "{0} U [7,8]",
                    "lot": {8: 75.0, 12: 0, 16: 0, 20: 0, 24: 0, 28: 0, 32: 0, 36: 25.0, 40: 0},
                    "expec": 15.0,
                },
            },
            "TIOLILow": {
                "Lottery A": {
                    "action": "{0,1}",
                    "lot": {8: 0, 12: 100.0, 16: 0, 20: 0, 24: 0, 28: 0, 32: 0, 36: 0, 40: 0},
                    "expec": 12.0,
                },
                "Lottery B": {
                    "action": "{0,3}",
                    "lot": {8: 30.0, 12: 0, 16: 0, 20: 70.0, 24: 0, 28: 0, 32: 0, 36: 0, 40: 0},
                    "expec": 16.4,
                },
                "Lottery C": {
                    "action": "{0,5}",
                    "lot": {8: 55.0, 12: 0, 16: 0, 20: 0, 24: 0, 28: 45.0, 32: 0, 36: 0, 40: 0},
                    "expec": 17.0,
                },
                "Lottery D": {
                    "action": "{0,7}",
                    "lot": {8: 75.0, 12: 0, 16: 0, 20: 0, 24: 0, 28: 0, 32: 0, 36: 25.0, 40: 0},
                    "expec": 15.0,
                },
            },
            "DelMid": {
                "Lottery A": {
                    "action": "{0} U [1,8]",
                    "lot": {8: 0, 12: 10.0, 16: 15.0, 20: 25.0, 24: 25.0, 28: 15.0, 32: 10.0, 36: 0, 40: 0},
                    "expec": 22.0,
                },
                "Lottery B": {
                    "action": "{0} U [3,8]",
                    "lot": {8: 10.0, 12: 0, 16: 0, 20: 40.0, 24: 25.0, 28: 15.0, 32: 10.0, 36: 0, 40: 0},
                    "expec": 22.2,
                },
                "Lottery C": {
                    "action": "{0} U [5,8]",
                    "lot": {8: 25.0, 12: 0, 16: 0, 20: 0, 24: 0, 28: 65.0, 32: 10.0, 36: 0, 40: 0},
                    "expec": 23.4,
                },
                "Lottery D": {
                    "action": "{0} U [7,8]",
                    "lot": {8: 50.0, 12: 0, 16: 0, 20: 0, 24: 0, 28: 0, 32: 0, 36: 50.0, 40: 0},
                    "expec": 22.0,
                },
            },
            "TIOLIMid": {
                "Lottery A": {
                    "action": "{0,1}",
                    "lot": {8: 0, 12: 100.0, 16: 0, 20: 0, 24: 0, 28: 0, 32: 0, 36: 0, 40: 0},
                    "expec": 12.0,
                },
                "Lottery B": {
                    "action": "{0,3}",
                    "lot": {8: 10.0, 12: 0, 16: 0, 20: 90.0, 24: 0, 28: 0, 32: 0, 36: 0, 40: 0},
                    "expec": 18.8,
                },
                "Lottery C": {
                    "action": "{0,5}",
                    "lot": {8: 25.0, 12: 0, 16: 0, 20: 0, 24: 0, 28: 75.0, 32: 0, 36: 0, 40: 0},
                    "expec": 23.0,
                },
                "Lottery D": {
                    "action": "{0,7}",
                    "lot": {8: 50.0, 12: 0, 16: 0, 20: 0, 24: 0, 28: 0, 32: 0, 36: 50.0, 40: 0},
                    "expec": 22.0,
                },
            },
            "DelHigh": {
                "Lottery A": {
                    "action": "{0} U [1,8]",
                    "lot": {8: 0, 12: 5.0, 16: 5.0, 20: 15.0, 24: 20.0, 28: 25.0, 32: 30.0, 36: 0, 40: 0},
                    "expec": 25.8,
                },
                "Lottery B": {
                    "action": "{0} U [3,8]",
                    "lot": {8: 5.0, 12: 0, 16: 0, 20: 20.0, 24: 20.0, 28: 25.0, 32: 30.0, 36: 0, 40: 0},
                    "expec": 25.8,
                },
                "Lottery C": {
                    "action": "{0} U [5,8]",
                    "lot": {8: 10.0, 12: 0, 16: 0, 20: 0, 24: 0, 28: 60.0, 32: 30.0, 36: 0, 40: 0},
                    "expec": 27.2,
                },
                "Lottery D": {
                    "action": "{0} U [7,8]",
                    "lot": {8: 25.0, 12: 0, 16: 0, 20: 0, 24: 0, 28: 0, 32: 0, 36: 75.0, 40: 0},
                    "expec": 29.0,
                },
            },
            "TIOLIHigh": {
                "Lottery A": {
                    "action": "{0,1}",
                    "lot": {8: 0, 12: 100.0, 16: 0, 20: 0, 24: 0, 28: 0, 32: 0, 36: 0, 40: 0},
                    "expec": 12.0,
                },
                "Lottery B": {
                    "action": "{0,3}",
                    "lot": {8: 5.0, 12: 0, 16: 0, 20: 95.0, 24: 0, 28: 0, 32: 0, 36: 0, 40: 0},
                    "expec": 19.4,
                },
                "Lottery C": {
                    "action": "{0,5}",
                    "lot": {8: 10.0, 12: 0, 16: 0, 20: 0, 24: 0, 28: 90.0, 32: 0, 36: 0, 40: 0},
                    "expec": 26.0,
                },
                "Lottery D": {
                    "action": "{0,7}",
                    "lot": {8: 25.0, 12: 0, 16: 0, 20: 0, 24: 0, 28: 0, 32: 0, 36: 75.0, 40: 0},
                    "expec": 29.0,
                },
            },
        }

        lottery_order = [
            "DelLow",
            "TIOLILow",
            "DelMid",
            "TIOLIMid",
            "DelHigh",
            "TIOLIHigh",
        ]

        group_key = lottery_order[player.round_number - 1]
        lottery = all_lotteries[group_key]

        return dict(
            lottery=lottery,
        )

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        set_payoffs(player)

        # Run at the end
        if player.round_number == C.NUM_ROUNDS:
            # Check if the player is the lucky one
            lucky_player = int(player.participant.label)
            if lucky_player == int(player.session.vars['PartThreePay']):
                # Draw one of the rounds to pay
                lucky_round = random.randint(1, C.NUM_ROUNDS)
                lucky_draw = player.in_round(lucky_round)
                player.participant.vars['BonusPay'] = lucky_draw.payoff
                print(f"Paying {player.session.vars['PartThreePay']} a bonus of {player.participant.vars['BonusPay']}")



class Waiting(WaitPage):
    @staticmethod
    def is_displayed(player):
        return player.round_number == C.NUM_ROUNDS

    wait_for_all_groups = True

    body_text = "Waiting for all participants to complete Part Three."

page_sequence = [Instructions, lotteries, Waiting]
