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

page_sequence = [ChoiceInstructions, InstructionsFeedback, Choice]
