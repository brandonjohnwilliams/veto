from otree.api import *
import json
import random

doc = """
No walk away threat point (responses)
"""


class C(BaseConstants):
    NAME_IN_URL = 'no_zero_response'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 3

    single = 0

    setZero = 0  # define as such to remove buyer payoff column

class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    single = models.IntegerField()

    minSlider = models.IntegerField()  # defines the left side of the delegated range
    maxSlider = models.IntegerField()  # defines the right side of the delegated range
    selectedX = models.IntegerField()

    response = models.IntegerField()

    # Distributions
    roundType = models.IntegerField()
    roundName = models.StringField()

    # matching info
    responder = models.IntegerField()

    thetaRange = models.IntegerField(blank=True)


# FUNCTIONS
def set_payoffs(player):
    # do: redefine at the player level
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




def creating_session(subsession):
    with open('SubjectMatching2.json', 'r') as f:
        subject_matching = json.load(f)

    num_participants = str(subsession.session.num_participants)
    matching_dict = subject_matching[num_participants]
    subject_assignment_dict = matching_dict['subjectAssignment']
    urn_assignment_dict = matching_dict['urnAssignment']
    period_matching_dict = matching_dict['PeriodMatching']

    # Get session key
    session_key = f"Session{subsession.session.config['Session']}"

    # start at round 16 in JSON
    round_num = str(subsession.round_number + 15)

    for player in subsession.get_players():

        # assign group and subgroup
        label_key = str(player.participant.label_id)

        subject_assignment = subject_assignment_dict[label_key]
        matching_group = subject_assignment['MatchingGroup']

        period_match = period_matching_dict[round_num]

        player_id = str(player.participant.label_id)

        match = next(
            (
                row
                for row in period_match
                if str(row["responder"]) == player_id
            ),
            None
        )

        if match is None:
            raise ValueError(f"No proposer match found for player_id={player_id}")

        L = int(match["L"])
        M = int(match["M"])
        H = int(match["H"])

        # assign urn

        urn_type = urn_assignment_dict[session_key][f"MatchingGroup{matching_group}"][round_num]['urn']
        urn_key = urn_type.split()[-1]  # "L", "M", or "H"

        if urn_key == "M":
            player.roundType = 2
            player.roundName = "Middle"
            player.selectedX = M


        elif urn_key == "L":
            player.roundType = 1
            player.roundName = "Low"
            player.selectedX = L

        else:
            player.roundType = 3
            player.roundName = "High"
            player.selectedX = H

        player.single = 1 if player.subsession.session.config['take_it_or_leave_it'] else 0


# PAGES

class RolesIntro(Page):
    timeout_seconds = 15

    @staticmethod
    def is_displayed(player):
        return player.round_number == 1

    @staticmethod
    def before_next_page(player, timeout_happened):
        proposer_list = player.participant.proposer
        proposer_id = proposer_list[player.round_number - 1]

        matched_player = next(
            p for p in player.subsession.get_players()
            if p.participant.label_id == proposer_id
        )

        print(matched_player.participant.sliders)

        i = 2 * (player.round_number - 4)
        player.minSlider = matched_player.participant.sliders[i]
        player.maxSlider = matched_player.participant.sliders[i + 1]

        # print(player.minSlider)
        # print(player.maxSlider)




class Response(Page):
    form_model = 'player'
    form_fields = ['response']


    @staticmethod
    def js_vars(player):

        return dict(
            selectedX=player.selectedX,
            fromM=player.minSlider,
            toM=player.maxSlider,
            response=1,
        )

    @staticmethod
    def vars_for_template(player):
        return {
            "selectedX": player.selectedX,
            "roundName": player.roundName,
            "roundType": player.roundType,
            "minSlider": player.minSlider,
            "maxSlider": player.maxSlider,
        }




class Results(Page):
    timeout_seconds = 15

    @staticmethod
    def is_displayed(player):
        return player.round_number == 6

    @staticmethod
    def js_vars(player):

        # Initialize empty lists
        roundName_list = []
        idealX_list = []
        offerMin_list = []
        offerMax_list = []
        choice_list = []
        payoff_list = []
        role_list = []

        # Loop through each round
        for i in range(1, player.round_number + 1):  # Assuming num_rounds is defined
            prev_player = player.in_round(i)

            # Append values from the respective round
            roundName_list.append(prev_player.group.roundName)
            idealX_list.append(prev_player.group.vetoer_bias)
            offerMin_list.append(prev_player.group.minSlider)
            offerMax_list.append(prev_player.group.maxSlider)
            choice_list.append(prev_player.group.response)
            payoff_list.append(prev_player.payoff)
            role_list.append(prev_player.role)

        return dict(
            round=player.round_number,

            # loop these variables
            idealX=idealX_list,
            offerMin=offerMin_list,
            offerMax=offerMax_list,
            choice=choice_list,
            payoff=payoff_list,
            roundName=roundName_list,
            role=role_list,
        )

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        import random

        participant = player.participant

        # if it's the round to pay
        if player.round_number == player.participant.vars['PayRound']:
            player_in_selected_round = player.in_round(player.participant.vars['PayRound'])
            player.participant.PartOnePayoff = float(player_in_selected_round.payoff)
            # print("Paying for part one: ", player.participant.PartOnePayoff)

class NoZeroWait(WaitPage):
    # title_text = "Please wait"
    # body_text = "Waiting for the Buyer to make his or her choice"
    wait_for_all_groups = True

    @staticmethod
    def is_displayed(player):
        return player.round_number == 3

    template_name = 'NoZeroWait.html'


page_sequence = [RolesIntro, Response, NoZeroWait]
