from otree.api import *
import numpy as np



doc = """
Practice Rounds
"""


class C(BaseConstants):
    NAME_IN_URL = 'practice'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1

    round_type = 2 # defined only explicitly for the practice round

    setZero = 0  # define as such to remove buyer payoff column

class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass

class Player(BasePlayer):

    quiz1 = models.IntegerField()
    quiz2 = models.IntegerField()
    quiz3 = models.IntegerField()
    quiz4 = models.IntegerField()

    single = models.IntegerField()
    chat = models.IntegerField()

    minSlider = models.IntegerField()  # defines the left side of the delegated range
    maxSlider = models.IntegerField()  # defines the right side of the delegated range

    selectedX = models.IntegerField()

    response = models.IntegerField()

    sellerPayoff = models.IntegerField()
    buyerPayoff = models.IntegerField()

# FUNCTIONS
# PAGES
class Introduction(Page):
    pass

class ProposalProbs(Page):
    form_model = 'player'
    form_fields = ['quiz1', 'quiz2']
    @staticmethod
    def js_vars(player):
        if player.session.config['take_it_or_leave_it']==1:
            player.single = 1
        else: player.single = 0
        return dict(
            round_type=3,
            selectedX=C.setZero,
            fromM=1,
            toM=8,
            single=player.single,
        )

    @staticmethod
    def vars_for_template(player):
        return {
            "selectedX": 2,
            "roundName": "Middle",
            "roundType": 3,
        }

    @staticmethod
    def error_message(player: Player, values):
        solutions = dict(quiz1=5, quiz2=15)

        if values != solutions:
            return "One or more answers were incorrect."

class ProposalMenu(Page):
    form_model = 'player'
    form_fields = ['minSlider', 'maxSlider']
    @staticmethod
    def js_vars(player):
        return dict(
            round_type=3,
            single=player.single,
            fromM=1,
            toM=8,
        )

    @staticmethod
    def vars_for_template(player: Player):
        return dict(
            roundType=3,
            single=player.single,
        )

class ProposalQuestions(Page):
    form_model = 'player'
    form_fields = ['quiz3','quiz4']

    @staticmethod
    def js_vars(player):
        return dict(
            # selectedX=2, # Selecting 0 removes the column
            fromM=player.minSlider,
            toM=player.maxSlider,
            round_type=3,
            # response=1,
        )

    @staticmethod
    def vars_for_template(player):
        return dict(
            # selectedX=2, # Selecting 0 removes the column
            fromM=player.minSlider,
            toM=player.maxSlider,
            roundType=3,
        )

    @staticmethod
    def error_message(player: Player, values):
        solutions = dict(quiz3=0, quiz4=player.maxSlider)

        if values != solutions:
            return "One or more answers were incorrect."

class WaitPage2(WaitPage):
    wait_for_all_groups = True

    body_text = "Waiting for all participants to complete the practice. Once everyone is ready, we will begin the main experiment."

page_sequence = [Introduction, ProposalProbs, ProposalMenu, ProposalQuestions, WaitPage2]
