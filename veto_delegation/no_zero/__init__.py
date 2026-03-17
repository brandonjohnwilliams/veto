from otree.api import *
import json
import random

doc = """
No walk away threat point
"""


class C(BaseConstants):
    NAME_IN_URL = 'no_zero'
    PLAYERS_PER_GROUP = 2
    NUM_ROUNDS = 6

    single = 0

    setZero = 0  # define as such to remove buyer payoff column

    # roles just used for payment:

    SELLER_ROLE = 'Seller'
    BUYER_ROLE = 'Buyer'

class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    minSlider = models.IntegerField()  # defines the left side of the delegated range
    maxSlider = models.IntegerField()  # defines the right side of the delegated range

    response = models.IntegerField()  # numerical response of the vetoer

    # dice rolls
    vetoer_bias = models.IntegerField()

    # Distributions
    roundType = models.IntegerField()
    roundName = models.StringField()

    # Distribution slider on screen submit
    thetaRange = models.IntegerField(blank=True)


class Player(BasePlayer):
    single = models.IntegerField()

    minSlider = models.IntegerField()  # defines the left side of the delegated range
    maxSlider = models.IntegerField()  # defines the right side of the delegated range

    response = models.IntegerField()  # numerical response of the vetoer

    thetaRange = models.IntegerField(blank=True)


# FUNCTIONS
def set_payoffs(group):
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
    p1 = group.get_player_by_id(1)
    p2 = group.get_player_by_id(2)

    p1.payoff = payoff_matrix[group.response][0]
    p2.payoff = payoff_matrix[group.response][group.vetoer_bias]



def creating_session(subsession):

    if subsession.round_number <= 3:
        # need new json
        with open('SubjectMatching.json', 'r') as f:
            subject_matching = json.load(f)

        # Load relevant sections
        num_participants = str(subsession.session.num_participants)
        matching_dict = subject_matching[num_participants]
        subject_assignment = matching_dict['subjectAssignment']
        urn_assignment_dict = matching_dict['urnAssignment']
        period_matching_dict = matching_dict['PeriodMatching']

        # Get session key like "Session1"
        session_key = f"Session{subsession.session.config['Session']}"

        round_num = str(subsession.round_number)
        if round_num not in period_matching_dict:
            raise ValueError(f"Round {round_num} not found in PeriodMatching.")

        players = list(subsession.get_players())

        # Step 1: Build id map (otree_id → subject_id)
        id_map = {}

        # Generate payoff round outside of loop:
        payRound1 = random.randint(1, C.NUM_ROUNDS)
        payRound2 = payRound1

        for player, (subject_id_str, attributes) in zip(sorted(players, key=lambda p: p.id_in_subsession),
                                                        subject_assignment.items()):
            subject_id = int(subject_id_str)
            id_map[player.id_in_subsession] = subject_id
            player.participant.label = subject_id  # Save subject ID to label

            # Save attributes in participant.vars
            matching_group = attributes['MatchingGroup']
            player.participant.vars['MatchingGroup'] = attributes['MatchingGroup']
            player.participant.vars['SubGroup'] = attributes['SubGroup']

            # Generate PayRound for the MatchingGroup only in first round
            if player.round_number == 1:
                # Initialize BonusPay as zero
                player.participant.vars['BonusPay'] = 0
                if player.participant.vars['MatchingGroup'] == 1:
                    player.participant.vars['PayRound'] = payRound1
                else:
                    player.participant.vars['PayRound'] = payRound2
                # print("Paying round: ", player.participant.vars['PayRound'])

        # Step 2: Reverse map (subject_id → otree_id)
        subject_to_player_id = {v: k for k, v in id_map.items()}
        subsession.session.vars['subject_to_player_id'] = subject_to_player_id

        # Step 3: Create group matrix from PeriodMatching
        round_matches = period_matching_dict[round_num]
        group_matrix = []
        for match in round_matches:
            proposer_subject = match['proposer']
            responder_subject = match['responder']
            seller_otree_id = subject_to_player_id[proposer_subject]
            buyer_otree_id = subject_to_player_id[responder_subject]
            group_matrix.append([seller_otree_id, buyer_otree_id])
        subsession.set_group_matrix(group_matrix)

        # Step 4: Set any session config–based vars
        for player in subsession.get_players():
            player.single = 1 if player.subsession.session.config['take_it_or_leave_it'] else 0

        # Step 5: Assign roundType and selectedX using proposer only
        for match in round_matches:
            proposer_subject_id = match['proposer']
            proposer_otree_id = subject_to_player_id[proposer_subject_id]
            proposer_player = next(p for p in subsession.get_players() if p.id_in_subsession == proposer_otree_id)
            group = proposer_player.group

            # Get urn assignment
            matching_group = proposer_player.participant.vars['MatchingGroup']
            urn_type = urn_assignment_dict[session_key][f"MatchingGroup{matching_group}"][round_num]['urn']
            urn_key = urn_type.split()[-1]  # "L", "M", or "H"

            # Assign to group
            if urn_key == "M":
                group.roundType = 2
                group.roundName = "Middle"

            elif urn_key == "L":
                group.roundType = 1
                group.roundName = "Low"

            else:
                group.roundType = 3
                group.roundName = "High"

            group.vetoer_bias = match[urn_key]
            # Debug
            print(
                f"✅ Group {group.id_in_subsession}: proposer {proposer_subject_id}, urn {urn_type}, selectedX = {group.vetoer_bias}")
    else:

        # do the entire matching again with a re-indexed round number (round - 3)
        with open('SubjectMatching.json', 'r') as f:
            subject_matching = json.load(f)

        # Load relevant sections
        num_participants = str(subsession.session.num_participants)
        matching_dict = subject_matching[num_participants]
        subject_assignment = matching_dict['subjectAssignment']
        urn_assignment_dict = matching_dict['urnAssignment']
        period_matching_dict = matching_dict['PeriodMatching']

        # Get session key like "Session1"
        session_key = f"Session{subsession.session.config['Session']}"

        # Index back to original three rounds
        round_num = str(subsession.round_number - 3)
        if round_num not in period_matching_dict:
            raise ValueError(f"Round {round_num} not found in PeriodMatching.")

        players = list(subsession.get_players())

        # Step 1: Build id map (otree_id → subject_id)
        id_map = {}

        for player, (subject_id_str, attributes) in zip(sorted(players, key=lambda p: p.id_in_subsession),
                                                        subject_assignment.items()):
            subject_id = int(subject_id_str)
            id_map[player.id_in_subsession] = subject_id
            player.participant.label = subject_id  # Save subject ID to label

            # Save attributes in participant.vars
            matching_group = attributes['MatchingGroup']
            player.participant.vars['MatchingGroup'] = attributes['MatchingGroup']
            player.participant.vars['SubGroup'] = attributes['SubGroup']


        # Step 2: Reverse map (subject_id → otree_id)
        subject_to_player_id = {v: k for k, v in id_map.items()}
        subsession.session.vars['subject_to_player_id'] = subject_to_player_id

        # Step 3: Create group matrix from PeriodMatching
        round_matches = period_matching_dict[round_num]
        group_matrix = []
        for match in round_matches:
            proposer_subject = match['proposer']
            responder_subject = match['responder']
            seller_otree_id = subject_to_player_id[proposer_subject]
            buyer_otree_id = subject_to_player_id[responder_subject]
            group_matrix.append([seller_otree_id, buyer_otree_id])
        subsession.set_group_matrix(group_matrix)

        # Step 4: Set any session config–based vars
        for player in subsession.get_players():
            player.single = 1 if player.subsession.session.config['take_it_or_leave_it'] else 0

        # Step 5: Assign roundType and selectedX using proposer only
        for match in round_matches:
            proposer_subject_id = match['proposer']
            proposer_otree_id = subject_to_player_id[proposer_subject_id]
            proposer_player = next(p for p in subsession.get_players() if p.id_in_subsession == proposer_otree_id)
            group = proposer_player.group

            # Get urn assignment
            matching_group = proposer_player.participant.vars['MatchingGroup']
            urn_type = urn_assignment_dict[session_key][f"MatchingGroup{matching_group}"][round_num]['urn']
            urn_key = urn_type.split()[-1]  # "L", "M", or "H"

            # Assign to group
            if urn_key == "M":
                group.roundType = 2
                group.roundName = "Middle"

            elif urn_key == "L":
                group.roundType = 1
                group.roundName = "Low"

            else:
                group.roundType = 3
                group.roundName = "High"

            group.vetoer_bias = match[urn_key]
            # Debug
            print(
                f"✅ Group {group.id_in_subsession}: proposer {proposer_subject_id}, urn {urn_type}, selectedX = {group.vetoer_bias}")


# PAGES
class Intro(Page):
    @staticmethod
    def is_displayed(player):
        return player.round_number == 1

    @staticmethod
    def vars_for_template(player):
        test = player.session.config['test']
        return dict(
            test = test
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




class Roles(Page):
    timeout_seconds = 20
    @staticmethod
    def js_vars(player):
        group = player.group
        return dict(
            selectedX=group.vetoer_bias,
            roundName=group.roundName,
            roundType=group.roundType,
            round_type=player.group.roundType,
        )

    @staticmethod
    def vars_for_template(player):
        group = player.group
        return {
            "selectedX": group.vetoer_bias,
            "roundName": group.roundName,
            "roundType": group.roundType,
            "chat": player.session.config['chat']
        }

class Proposal(Page):
    form_model = 'player'
    form_fields = ['minSlider', 'maxSlider', 'thetaRange']


    @staticmethod
    def js_vars(player):
        return dict(
            round_type=player.group.roundType,
            selectedX=C.setZero,
            fromM=1,
            toM=8,
            single=player.single
        )

    @staticmethod
    def vars_for_template(player):
        group = player.group
        return {
            "selectedX": group.vetoer_bias,
            "roundName": group.roundName,
            "roundType": group.roundType,
        }

    @staticmethod
    def is_displayed(player):
        return player.round_number <= 3

    @staticmethod
    def before_next_page(player, timeout_happened):
        group = player.group
        participant = player.participant
        if player.role == 'Seller':
            participant.sliders.append(player.minSlider)
            participant.sliders.append(player.maxSlider)
            group.minSlider = player.minSlider
            group.maxSlider = player.maxSlider


class Response(Page):
    form_model = 'group'
    form_fields = ['response']

    @staticmethod
    def is_displayed(player):
        return player.round_number > 3

    @staticmethod
    def after_all_players_arrive(group):
        seller = group.get_player_by_id(1)  # or however you identify Seller

        if seller.role == 'Seller':  # use seller.role() if role is a method
            group.minSlider = seller.participant.sliders[group.round_number - 4]
            group.maxSlider = seller.participant.sliders[group.round_number - 3]

    @staticmethod
    def js_vars(player):
        group = player.group
        return dict(
            selectedX=player.group.vetoer_bias,
            fromM=group.minSlider,
            toM=group.maxSlider,
            response=1,
        )

    @staticmethod
    def vars_for_template(player):
        group = player.group
        return {
            "selectedX": group.vetoer_bias,
            "roundName": group.roundName,
            "roundType": group.roundType,
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


page_sequence = [Intro, Instructions, RolesIntro, Roles, Proposal, Response, Results, NoZeroWait]
