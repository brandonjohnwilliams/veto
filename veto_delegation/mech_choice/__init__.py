from otree.api import *
import json
import random

doc = """
Mech Choice
"""


class C(BaseConstants):
    NAME_IN_URL = 'mech_choice'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1

    round_type = 2 # defined only explicitly for the practice round

    # adding a comment here for version control

class Subsession(BaseSubsession):
    pass

class Group(BaseGroup):
    pass

class Player(BasePlayer):
    switch_point = models.FloatField()

    single = models.IntegerField()


# FUNCTIONS

def creating_session(subsession):

    for player in subsession.get_players():
        if player.subsession.session.config['take_it_or_leave_it']:
            player.single = 1
        else:
            player.single = 0
        if player.subsession.session.config['chat']:
            player.chat = 1
        else:
            player.chat = 0

        player.single = 1 if player.subsession.session.config['take_it_or_leave_it'] else 0

# PAGES



class ChoiceInstructions(Page):
    form_model = 'player'
    form_fields = ['switch_point']

    @staticmethod
    def vars_for_template(player):
        return dict(
            single = player.single
        )

page_sequence = [ChoiceInstructions]
