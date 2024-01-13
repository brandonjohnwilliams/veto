import csv

from otree.api import *
import numpy as np



doc = """
Veto Delegation
"""


class C(BaseConstants):
    NAME_IN_URL = 'veto_delegation'
    PLAYERS_PER_GROUP = 2
    NUM_ROUNDS = 3

    endowment = 25
    veto_amount = 0
    guarantee = 5

class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    minSlider = models.IntegerField() # defines the left side of the delegated range
    maxSlider = models.IntegerField() # defines the right side of the delegated range

    response = models.IntegerField() # numerical response of the vetoer
    veto = models.BooleanField(blank=True, initial=False) # True if vetoed

    vetoer_bias = models.IntegerField()

class Player(BasePlayer):
    pass

# FUNCTIONS
def set_payoffs(group):
    p1 = group.get_player_by_id(1)
    p2 = group.get_player_by_id(2)
    if group.veto == True:
        p1.payoff = C.veto_amount + C.guarantee
        p2.payoff = C.endowment + C.guarantee - np.abs(C.veto_amount - group.vetoer_bias)
    else:
        p1.payoff = group.response + C.guarantee # linear loss from optimal (max)
        p2.payoff = C.endowment + C.guarantee - np.abs(group.response - group.vetoer_bias) # linear loss from optimal


def creating_session(subsession):
    # pulls dice rolls from preset spreadsheet

    import statistics
    import csv

    file_path = 'draws.csv'
    with open(file_path, 'r', encoding='utf-8-sig') as file:
        reader = csv.DictReader(file, delimiter = ",")
        rows = list(reader)

    round = subsession.round_number - 1

    # vetoes currently hard-coded as 1-min, 2-median, rest-max
    if subsession.round_number == 1:
        for group in subsession.get_groups():
            group.vetoer_bias = min(int(value) for value in rows[round].values())
    elif subsession.round_number == 2:
        for group in subsession.get_groups():
            group.vetoer_bias = statistics.median(int(value) for value in rows[round].values())
    else:
        for group in subsession.get_groups():
            group.vetoer_bias = max(int(value) for value in rows[round].values())

# Use to check if bias draws are being pulled correctly:
    # print(group.vetoer_bias)
# PAGES
class Proposal(Page):
    form_model = 'group'
    form_fields = ['minSlider','maxSlider']

    @staticmethod
    def is_displayed(player):
        return player.id_in_group == 1

class WaitForP1(WaitPage):
    pass


class Response(Page):
    form_model = 'group'
    form_fields = ['response','veto']

    @staticmethod
    def is_displayed(player):
        return player.id_in_group == 2

    @staticmethod
    def js_vars(player):
        return dict(
            vetoer_bias=str(player.group.vetoer_bias),
            lower_interval=str(player.group.minSlider),
            upper_interval=str(player.group.maxSlider),
        )

class WaitForP2(WaitPage):
    after_all_players_arrive = set_payoffs

class Results(Page):
    pass

page_sequence = [Proposal, WaitForP1, Response, WaitForP2, Results]
