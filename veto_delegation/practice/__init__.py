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
    quiz3 = models.BooleanField(label="Is 9 a prime number?")

# FUNCTIONS
# PAGES
class Introduction(Page):
    pass

class Instructions(Page):
    pass

class Practice(Page):
    pass

class Quiz(Page):
    form_model = 'player'
    form_fields = ['quiz3']

    @staticmethod
    def error_message(player: Player, values):
        solutions = dict(quiz3=False)

        if values != solutions:
            return "One or more answers were incorrect."

page_sequence = [Introduction, Instructions, Practice, Quiz]
