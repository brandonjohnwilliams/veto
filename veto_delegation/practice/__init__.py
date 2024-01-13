from otree.api import *
import numpy as np



doc = """
Practice Rounds
"""


class C(BaseConstants):
    NAME_IN_URL = 'practice'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1

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
# PAGES
class Introduction(Page):
    pass

class Practice(Page):
    pass

page_sequence = [Introduction, Practice]
