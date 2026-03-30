from otree.api import *
import json
import random

doc = """
Mech Choice
"""


class C(BaseConstants):
    NAME_IN_URL = 'mech_choice'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 3

    # adding a comment here for version control

class Subsession(BaseSubsession):
    pass

class Group(BaseGroup):
    pass

class Player(BasePlayer):
    switch_point_practice = models.StringField(
        choices=[
            "-5", "-4", "-3", "-2", "-1", "0", "1", "2", "3", "4", "5", "ALWAYS_A"
        ]
    )
    switch_point = models.StringField(
        choices=[
            "-5", "-4", "-3", "-2", "-1", "0", "1", "2", "3", "4", "5", "ALWAYS_A"
        ]
    )
    urn_type = models.IntegerField()
    urn_name = models.StringField()

    single = models.IntegerField()


# FUNCTIONS
MPL_ROWS = [-5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 'ALWAYS_A']


def mpl_choice(switch_point, drawn_row):
    """
    Returns 'A' or 'B' given the player's switch_point and the drawn row.

    Switch point convention (matches the HTML):
      - Rows strictly below switch_point → Option A
      - Rows at or above switch_point    → Option B
      - ALWAYS_A                         → always Option A regardless of draw
    """
    if switch_point == 'ALWAYS_A':
        return 'A'
    if drawn_row == 'ALWAYS_A':
        # The drawn row is the ALWAYS_A row; player chose A for this row
        # only if their switch_point is also ALWAYS_A (handled above),
        # otherwise they have already switched to B before this row.
        return 'B' if switch_point <= 5 else 'A'
    return 'A' if drawn_row < int(switch_point) else 'B'


def mpl_payoff(choice, drawn_row, option_a_payoff, option_b_payoff):
    """
    Returns the payoff for the drawn row.

    Option A payoff = base + bonus if drawn_row < 0, else base.
    Option B payoff = base + bonus if drawn_row > 0, else base.
    The bonus equals abs(drawn_row) dollars.

    option_a_payoff and option_b_payoff are the base (x=0) payoffs
    for each option, passed in from the player's stored robot payoffs.
    """
    if drawn_row == 'ALWAYS_A':
        return option_a_payoff  # no bonus on ALWAYS_A row

    drawn_row = int(drawn_row)
    if choice == 'A':
        bonus = max(-drawn_row, 0)   # bonus only when drawn_row < 0
        return option_a_payoff + bonus
    else:
        bonus = max(drawn_row, 0)    # bonus only when drawn_row > 0
        return option_b_payoff + bonus

def creating_session(subsession):

    for player in subsession.get_players():
        if player.round_number == 1:
            player.urn_type = 1
            player.urn_name = "Low"
        elif player.round_number == 2:
            player.urn_type = 2
            player.urn_name = "Middle"
        else:
            player.urn_type = 3
            player.urn_name = "High"

        player.single = 1 if player.subsession.session.config['take_it_or_leave_it'] else 0

def switch_point_to_text(choice):
    if choice == "ALWAYS_A":
        return "Always take the single offer average."

    # If you're still using FloatField, convert carefully
    try:
        x = int(choice)
    except:
        return "Invalid choice"

    if x < 0:
        return f"Take a single offer average + ${abs(x)} or take the menu offer average."
    elif x == 0:
        return "Take the single offer average or take the menu offer average."
    else:
        return f"Take the single offer average or take the menu offer average + ${x}."
# PAGES



class ChoiceInstructions(Page):
    form_model = 'player'
    form_fields = ['switch_point_practice']

    @staticmethod
    def is_displayed(player):
        return player.round_number == 1

    @staticmethod
    def vars_for_template(player):
        return dict(
            single = player.single
        )

class InstructionsFeedback(Page):
    @staticmethod
    def is_displayed(player):
        return player.round_number == 1

    @staticmethod
    def vars_for_template(player):
        if player.session.config['test'] == 1:
            test = 1
        else:
            test = 0

        choice = player.switch_point_practice

        return dict(
            choice=choice,
            choice_text=switch_point_to_text(choice),
            test=test
        )

class Choice(Page):
    form_model = 'player'
    form_fields = ['switch_point']

    @staticmethod
    def vars_for_template(player):
        return dict(
            single = player.single,
            urn_name = player.urn_name
        )

    @staticmethod
    def before_next_page(player, timeout_happened):
        # Draw one row per round and store in session.vars
        for round_num in range(1, C.NUM_ROUNDS + 1):
            key = f'Part5{round_num}'
            if key not in player.session.vars:
                player.session.vars[key] = random.choice(MPL_ROWS)

        # Determine this player's choice and payoff for each round
        player.participant.vars['MPLResults'] = []

        for round_num in range(1, C.NUM_ROUNDS + 1):
            drawn_row = player.session.vars[f'MPLDraw_round{round_num}']
            round_player = player.in_round(round_num)
            switch_point = round_player.switch_point

            choice = mpl_choice(switch_point, drawn_row)

            # Retrieve the base robot payoffs stored from Part Three / Part Four
            option_a_payoff = round_player.PartFourPayoff  # single offer average
            option_b_payoff = round_player.PartThreePayoff  # menu offer average

            payoff = mpl_payoff(choice, drawn_row, option_a_payoff, option_b_payoff)

            player.participant.vars['MPLResults'].append({
                'round': round_num,
                'drawn_row': drawn_row,
                'switch_point': switch_point,
                'choice': choice,
                'payoff': payoff,
            })

            print(
                f"[MPL Round {round_num}] "
                f"Player {player.participant.label_id} | "
                f"Switch point: {switch_point} | "
                f"Drawn row: {drawn_row} | "
                f"Choice: {choice} | "
                f"Payoff: {payoff}"
            )

page_sequence = [ChoiceInstructions, InstructionsFeedback, Choice]
