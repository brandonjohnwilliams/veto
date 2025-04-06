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
    quiz5 = models.IntegerField()
    quiz6 = models.IntegerField()
    quiz7 = models.IntegerField()
    quiz8 = models.IntegerField()

    attempts1 = models.IntegerField(initial=1)
    attempts2 = models.IntegerField(initial=1)
    attempts3 = models.IntegerField(initial=1)

    single = models.IntegerField()
    chat = models.IntegerField()

    minSlider = models.IntegerField()  # defines the left side of the delegated range
    maxSlider = models.IntegerField()  # defines the right side of the delegated range

    selectedX = models.IntegerField()
    vetoer_bias = models.IntegerField()

    response = models.IntegerField()

    sellerPayoff = models.IntegerField()
    buyerPayoff = models.IntegerField()

# FUNCTIONS
def creating_session(subsession):
    import random
    for player in subsession.get_players():
        player.vetoer_bias = random.randint(1, 6)

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
            player.attempts1 = player.attempts1 + 1
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
            player.attempts2 = player.attempts2 + 1
            return "One or more answers were incorrect."

class MinMaxQuestions(Page):
    form_model = 'player'
    form_fields = ['quiz5','quiz6','quiz7','quiz8']

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
            bias=player.vetoer_bias
        )

    @staticmethod
    def error_message(player: Player, values):
        payoff_matrix = {
            0: [8, 26, 21, 16, 13, 11, 9],
            1: [12, 30, 25, 20, 15, 12, 10],
            2: [16, 25, 30, 25, 20, 15, 12],
            3: [20, 20, 25, 30, 25, 20, 15],
            4: [24, 15, 20, 25, 30, 25, 20],
            5: [28, 12, 15, 20, 25, 30, 25],
            6: [32, 10, 12, 15, 20, 25, 30],
            7: [36, 9, 10, 12, 15, 20, 25],
            8: [40, 8, 9, 10, 12, 15, 20]
        }

        # Convert minSlider and maxSlider to integers
        import random

        min_Slider = int(player.minSlider)
        max_Slider = int(player.maxSlider)


        robotChoices = [payoff_matrix[0][player.vetoer_bias]]  # Start with row 0 value
        # Iterate over all rows (1-8) and replace out-of-range values with 0
        robotChoices.extend([
            payoff_matrix[y][player.vetoer_bias] if min_Slider <= y <= max_Slider else 0
            for y in range(1, len(payoff_matrix))  # Start from 1 to avoid duplicate row 0
        ])

        # print("Robot ideal X=", player.vetoer_bias, "Robot choices=", robotChoices)

        robotMax = max(robotChoices)
        robotChoice = robotChoices.index(robotMax)  # Index within X

        # Filter out zero values for finding the min
        nonzero_choices = [val for val in robotChoices if val != 0]

        if nonzero_choices:
            robotMin = min(nonzero_choices)
            robotChoiceMin = robotChoices.index(robotMin)
        else:
            robotMin = 0  # Or some fallback value if all entries are zero
            robotChoiceMin = -1  # Or some other signal indicating "no valid choice"

        print(f'Min: {robotMin} at {robotChoiceMin}; Max: {robotMax} at {robotChoice}')

        solutions = dict(quiz5=robotMax, quiz6=robotChoice,
                         quiz7=robotMin, quiz8=robotChoiceMin)

        if values != solutions:
            player.attempts3 = player.attempts3 + 1
            return "One or more answers were incorrect."


class WaitPage2(WaitPage):
    wait_for_all_groups = True

    body_text = "Waiting for all participants to complete the comprehension questions. Once everyone is ready, we will begin the main experiment."

page_sequence = [Introduction, ProposalProbs, ProposalMenu, ProposalQuestions, MinMaxQuestions, WaitPage2]
