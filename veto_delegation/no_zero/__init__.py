from otree.api import *
import json
import random

doc = """
No walk away threat point
"""


class C(BaseConstants):
    NAME_IN_URL = 'no_zero'
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

    # Distributions
    roundType = models.IntegerField()
    roundName = models.StringField()

    # matching infor
    responder = models.IntegerField()

    thetaRange = models.IntegerField(blank=True)




def creating_session(subsession):

    with open('SubjectMatching2.json', 'r') as f:
        subject_matching = json.load(f)

    num_participants = str(subsession.session.num_participants)
    matching_dict = subject_matching[num_participants]
    subject_assignment_dict = matching_dict['subjectAssignment']
    urn_assignment_dict = matching_dict['urnAssignment']
    period_matching_dict = matching_dict['PeriodMatching']

    session_key = f"Session{subsession.session.config['Session']}"
    round_num = str(subsession.round_number + 15)

    for player in subsession.get_players():

        player.participant.label_id = player.id_in_subsession
        label_key = str(player.participant.label_id)

        subject_assignment = subject_assignment_dict[label_key]
        matching_group = subject_assignment['MatchingGroup']
        player.participant.MatchingGroupZero = matching_group
        sub_group = subject_assignment['SubGroup']
        player.participant.SubGroupZero = sub_group

        urn_type = urn_assignment_dict[session_key][f"MatchingGroup{matching_group}"][round_num]['urn']
        urn_key = urn_type.split()[-1]

        if urn_key == "M":
            player.roundType = 2
            player.roundName = "Middle"
        elif urn_key == "L":
            player.roundType = 1
            player.roundName = "Low"
        else:
            player.roundType = 3
            player.roundName = "High"

        period_match = period_matching_dict[round_num]
        player_id = str(player.participant.label_id)

        # Find the row where this player is the responder → get their proposer
        proposer_match = next(
            (row for row in period_match if str(row["responder"]) == player_id),
            None
        )
        if proposer_match is None:
            raise ValueError(f"No proposer match found for player_id={player_id}")
        proposer = int(proposer_match["proposer"])

        # Find the row where this player is the proposer → get their responder
        responder_match = next(
            (row for row in period_match if str(row["proposer"]) == player_id),
            None
        )
        if responder_match is None:
            raise ValueError(f"No responder match found for player_id={player_id}")
        responder = int(responder_match["responder"])

        # Initialize lists on first round
        if player.roundType == 1:
            player.participant.proposer = []
            player.participant.responder = []  # <-- initialize responder list too

        player.participant.proposer.append(proposer)
        player.participant.responder.append(responder)  # <-- store responder

        # debugging / print
        # print(
        #     f"[Round {subsession.round_number}] "
        #     f"Player {player_id} | "
        #     f"Proposer (who proposed to me): {proposer} | "
        #     f"Responder (who I proposed to): {responder}"
        # )

        player.single = 1 if player.subsession.session.config['take_it_or_leave_it'] else 0


# PAGES
class Intro(Page):
    @staticmethod
    def is_displayed(player):
        return player.round_number == 1

    @staticmethod
    def vars_for_template(player):
        test = player.session.config['test']
        num_participants = player.session.num_participants
        percentage_chance = round((11 / num_participants) * 100) if num_participants > 0 else 0
        return dict(
            test = test,
            percentage_chance = percentage_chance
        )

class Instructions(Page):
    @staticmethod
    def is_displayed(player):
        return player.round_number == 1

    @staticmethod
    def vars_for_template(player):
        test = player.session.config['test']
        single = 1 if player.subsession.session.config['take_it_or_leave_it'] else 0
        return dict(
            test = test,
            single = single
        )

    @staticmethod
    def before_next_page(player, timeout_happened):
        player.participant.sliders = []

class RolesIntro(Page):
    timeout_seconds = 15

    @staticmethod
    def is_displayed(player):
        return player.round_number == 1

    @staticmethod
    def vars_for_template(player):
        test = player.session.config['test']
        single = 1 if player.subsession.session.config['take_it_or_leave_it'] else 0
        return dict(
            test = test,
            single = single
        )

class Roles(Page):
    timeout_seconds = 20
    @staticmethod
    def js_vars(player):
        return dict(
            roundName=player.roundName,
            roundType=player.roundType,
            round_type=player.roundType,
        )

    @staticmethod
    def vars_for_template(player):
        return {
            "roundName": player.roundName,
            "roundType": player.roundType,
            "chat": player.session.config['chat']
        }

class Proposal(Page):
    form_model = 'player'
    form_fields = ['minSlider', 'maxSlider', 'thetaRange']


    @staticmethod
    def js_vars(player):
        return dict(
            round_type=player.roundType,
            selectedX=C.setZero,
            fromM=1,
            toM=8,
            single=player.single
        )

    @staticmethod
    def vars_for_template(player):
        return {
            "roundName": player.roundName,
            "roundType": player.roundType,
        }


    @staticmethod
    def before_next_page(player, timeout_happened):
        participant = player.participant
        participant.sliders.append(player.minSlider)
        participant.sliders.append(player.maxSlider)




class Response(Page):
    form_model = 'player'
    form_fields = ['response']

    @staticmethod
    def is_displayed(player):
        return player.round_number > 3

    @staticmethod
    def js_vars(player):
        partner = player.get_others_in_group()[0]
        partner_history = partner.participant.vars.get('sliders')
        Minidx = player.round_number - 4
        Maxidx = player.round_number - 3
        minSlider = partner_history[Minidx]
        maxSlider = partner_history[Maxidx]
        print(minSlider, maxSlider)
        return dict(
            selectedX=player.group.vetoer_bias,
            fromM=minSlider,
            toM=maxSlider,
            response=1,
        )

    @staticmethod
    def vars_for_template(player):
        group = player.group
        partner = player.get_others_in_group()[0]
        partner_history = partner.participant.vars.get('sliders')
        Minidx = player.round_number - 4
        Maxidx = player.round_number - 3
        minSlider = partner_history[Minidx]
        maxSlider = partner_history[Maxidx]
        print(minSlider, maxSlider)
        return {
            "selectedX": group.vetoer_bias,
            "roundName": group.roundName,
            "roundType": group.roundType,
            "minSlider": minSlider,
            "maxSlider": maxSlider,
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

class NoZeroWait(WaitPage):
    # title_text = "Please wait"
    # body_text = "Waiting for the Buyer to make his or her choice"
    wait_for_all_groups = True

    @staticmethod
    def is_displayed(player):
        test = player.subsession.session.config['test']
        return player.round_number == 3 and test == 0

    template_name = 'NoZeroWait.html'


page_sequence = [Intro, Instructions, RolesIntro, Roles, Proposal, NoZeroWait]
