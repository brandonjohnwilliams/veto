from otree.api import *
import numpy as np



doc = """
Versus non-human player
"""


class C(BaseConstants):
    NAME_IN_URL = 'robot'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 3

    endowment = 25
    veto_amount = 0
    guarantee = 5

    single = 0
class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    minSlider = models.IntegerField() # defines the left side of the delegated range
    maxSlider = models.IntegerField() # defines the right side of the delegated range

    response = models.IntegerField() # numerical response of the vetoer
    veto = models.BooleanField(blank=True, initial=False) # True if vetoed

    vetoer_bias = 10
    round_type = 1


class Player(BasePlayer):
    pass

# FUNCTIONS



def set_payoffs(group):
    if group.veto == True:
        Player.payoff = C.veto_amount + C.guarantee
    else:
        Player.payoff = group.response + C.guarantee # linear loss from optimal (max)



# PAGES
class robot(Page):
    form_model = 'group'
    form_fields = ['minSlider','maxSlider']

    @staticmethod
    def js_vars(player):
        return dict(
            round_type=Group.round_type,
            single_treat=C.single,
        )

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        Y = [y for y in range(Group.minSlider, Group.maxSlider)]
        print(Y)
        cOutcome = C.endowment + C.guarantee - np.abs(Group.response - Group.vetoer_bias)
        print(cOutcome)
        cStar = Y[np.argmax(cOutcome)]
        cVeto = C.endowment + C.guarantee - np.abs(C.veto_amount - Group.vetoer_bias)
        print(cStar)
        if cStar < cVeto:
            Group.Veto = True
        else:
            Group.Veto = False
        print(Group.Veto)

        set_payoffs(Player)

class Results(Page):
    pass


page_sequence = [robot, Results]
