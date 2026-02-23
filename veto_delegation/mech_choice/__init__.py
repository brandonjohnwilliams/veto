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
    value = models.FloatField()

    single = models.IntegerField()

    minSlider = models.IntegerField() # defines the left side of the delegated range
    maxSlider = models.IntegerField() # defines the right side of the delegated range

    response = models.IntegerField()
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

# PAGES

class Instructions(Page):
    pass

class SellerView(Page):
    form_model = 'player'
    form_fields = ['minSlider', 'maxSlider']
    @staticmethod
    def js_vars(player):
        return dict(
            round_type=C.round_type,
            single=player.single,
            fromM=1,
            toM=8,
        )

    @staticmethod
    def vars_for_template(player: Player):
        return dict(
            roundType=C.round_type,
            single=player.single,
        )

class SellerWait(WaitPage):
    wait_for_all_groups = True
    body_text = "Waiting for all participants to make their choice."


class BuyersChoice(Page):
    pass

class BuyersView(Page):
    form_model = 'player'
    form_fields = ['response']

    @staticmethod
    def js_vars(player):
        return dict(
            selectedX=3, # Selecting 0 removes the column
            fromM=player.minSlider,
            toM=player.maxSlider,
            round_type=2,
            response=1,
        )

    @staticmethod
    def vars_for_template(player):
        return dict(
            selectedX=3, # Selecting 0 removes the column
            fromM=player.minSlider,
            toM=player.maxSlider,
        )

class BuyerWait(WaitPage):
    wait_for_all_groups = True
    body_text = "Waiting for all participants to make their choice."

class ChoiceInstructions(Page):
    pass

page_sequence = [Instructions,
                 SellerView,
                 # SellerWait,
                 BuyersView,
                 # BuyerWait,
                 ChoiceInstructions]
