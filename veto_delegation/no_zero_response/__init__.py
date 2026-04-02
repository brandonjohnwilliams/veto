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
    setZero = 0


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    single = models.IntegerField()

    minSlider = models.IntegerField()
    maxSlider = models.IntegerField()
    selectedX = models.IntegerField()

    response = models.IntegerField()

    roundType = models.IntegerField()
    roundName = models.StringField()

    responder = models.IntegerField()

    thetaRange = models.IntegerField(blank=True)


# FUNCTIONS
payoff_matrix = {
    0: [8,  26, 21, 16, 13, 11,  9],
    1: [12, 30, 25, 20, 15, 12, 10],
    2: [16, 25, 30, 25, 20, 15, 12],
    3: [20, 20, 25, 30, 25, 20, 15],
    4: [24, 15, 20, 25, 30, 25, 20],
    5: [28, 12, 15, 20, 25, 30, 25],
    6: [32, 10, 12, 15, 20, 25, 30],
    7: [36,  9, 10, 12, 15, 20, 25],
    8: [40,  8,  9, 10, 12, 15, 20],
}


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

        label_key = str(player.participant.label_id)
        subject_assignment = subject_assignment_dict[label_key]
        matching_group = subject_assignment['MatchingGroup']

        period_match = period_matching_dict[round_num]
        player_id = str(player.participant.label_id)

        match = next(
            (row for row in period_match if str(row["responder"]) == player_id),
            None
        )
        if match is None:
            raise ValueError(f"No proposer match found for player_id={player_id}")

        L = int(match["L"])
        M = int(match["M"])
        H = int(match["H"])

        urn_type = urn_assignment_dict[session_key][f"MatchingGroup{matching_group}"][round_num]['urn']
        urn_key = urn_type.split()[-1]

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
    def vars_for_template(player):
        test = player.subsession.session.config['test']
        return dict(test=test)


class Roles(Page):
    timeout_seconds = 15

    @staticmethod
    def vars_for_template(player):
        return dict(
            round_type=player.roundType,
            single=player.single,
            selectedX=player.selectedX,
            roundName=player.roundName,
        )

    @staticmethod
    def js_vars(player):
        return dict(
            round_type=player.roundType,
            single=player.single,
            selectedX=player.selectedX,
            roundName=player.roundName,
        )

    @staticmethod
    def before_next_page(player, timeout_happened):
        if player.subsession.session.config['test'] == 1:
            player.minSlider = 3
            player.maxSlider = 3
        else:
            proposer_list = player.participant.proposer
            proposer_id = proposer_list[player.round_number - 1]

            matched_player = next(
                p for p in player.subsession.get_players()
                if p.participant.label_id == proposer_id
            )

            # print(matched_player.participant.sliders)

            i = 2 * (player.round_number - 1)
            player.minSlider = matched_player.participant.sliders[i]
            player.maxSlider = matched_player.participant.sliders[i + 1]


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

    @staticmethod
    def before_next_page(player, timeout_happened):
        # Initialize on first round
        if player.round_number == 1:
            player.participant.responses = []

        # Responder payoff: payoff_matrix[response][selectedX]
        player.payoff = payoff_matrix[player.response][player.selectedX]
        player.participant.responses.append(player.response)

        # Look up proposer and write their payoff back to their participant.vars
        proposer_id = player.participant.proposer[player.round_number - 1]
        proposer = next(
            p for p in player.subsession.get_players()
            if p.participant.label_id == proposer_id
        )

        if 'received_responses' not in proposer.participant.vars:
            proposer.participant.received_responses = []

        # Proposer payoff: payoff_matrix[response][0]
        proposer_payoff = payoff_matrix[player.response][0]

        proposer.participant.received_responses.append({
            'round': player.round_number,
            'responder_id': player.participant.label_id,
            'response': player.response,
            'proposer_payoff': proposer_payoff,
        })

        # print(
        #     f"[Round {player.round_number}] "
        #     f"Responder {player.participant.label_id} (selectedX={player.selectedX}) → "
        #     f"Proposer {proposer_id} | "
        #     f"Response: {player.response} | "
        #     f"Responder payoff: {player.payoff} | "
        #     f"Proposer payoff: {proposer_payoff}"
        # )



class NoZeroWait(WaitPage):
    wait_for_all_groups = True

    @staticmethod
    def is_displayed(player):
        return player.round_number == 3

    template_name = 'NoZeroResponseWait.html'

    @staticmethod
    def after_all_players_arrive(subsession):
        players = subsession.get_players()

        if 'PartTwoPayRound' not in subsession.session.vars:
            subsession.session.vars['PartTwoPayRound'] = random.randint(1, 3)

        pay_round = subsession.session.vars['PartTwoPayRound']
        lucky_proposer_id = subsession.session.vars.get('PartTwoPayProposer')

        # Find the lucky Seller and their matched Buyer for the pay round
        lucky_proposer = next(
            (p for p in players if p.participant.label_id == lucky_proposer_id), None
        )

        lucky_responder_id = None
        if lucky_proposer:
            received = lucky_proposer.participant.vars.get('received_responses', [])
            match = next((r for r in received if r['round'] == pay_round), None)
            if match:
                lucky_responder_id = match['responder_id']
                subsession.session.vars['PartTwoPayResponder'] = lucky_responder_id

        # Now assign payoffs to all players
        for player in players:
            label = player.participant.label_id

            if label == lucky_proposer_id:
                received = player.participant.vars.get('received_responses', [])
                match = next((r for r in received if r['round'] == pay_round), None)
                player.participant.PartTwoProposerPayoff = float(match['proposer_payoff']) if match else 0.0
            else:
                player.participant.PartTwoProposerPayoff = 0.0

            if label == lucky_responder_id:
                responder_player = player.in_round(pay_round)
                player.participant.PartTwoResponderPayoff = float(responder_player.payoff)
            else:
                player.participant.PartTwoResponderPayoff = 0.0

            player.participant.PartTwoPayoff = (
                    player.participant.PartTwoProposerPayoff +
                    player.participant.PartTwoResponderPayoff
            )

            print(
                f"[Payment] Player {label} | "
                f"Pay round: {pay_round} | "
                f"Lucky proposer: {lucky_proposer_id} | "
                f"Lucky responder: {lucky_responder_id} | "
                f"Proposer payoff: {player.participant.PartTwoProposerPayoff} | "
                f"Responder payoff: {player.participant.PartTwoResponderPayoff} | "
                f"Total part two payoff: {player.participant.PartTwoPayoff}"
            )

class Results(Page):
    timeout_seconds = 15

    @staticmethod
    def is_displayed(player):
        return player.round_number == 3

    @staticmethod
    def js_vars(player):
        roundName_list = []
        idealX_list = []
        offerMin_list = []
        offerMax_list = []
        choice_list = []
        payoff_list = []
        role_list = []

        # --- Proposer (Seller) rounds ---
        sliders = player.participant.sliders
        received = player.participant.vars.get('received_responses', [])

        for i in range(3):
            prev_player = player.in_round(i + 1)
            roundName_list.append(prev_player.roundName)
            idealX_list.append("Unknown")
            offerMin_list.append(sliders[2 * i])
            offerMax_list.append(sliders[2 * i + 1])

            match = next((r for r in received if r['round'] == i + 1), None)
            choice_list.append(match['response'] if match else None)
            payoff_list.append(match['proposer_payoff'] if match else None)
            role_list.append("Seller")

        # --- Responder (Buyer) rounds ---
        for i in range(1, player.round_number + 1):
            prev_player = player.in_round(i)
            roundName_list.append(prev_player.roundName)
            idealX_list.append(prev_player.selectedX)
            offerMin_list.append(prev_player.minSlider)
            offerMax_list.append(prev_player.maxSlider)
            choice_list.append(prev_player.response)
            payoff_list.append(float(prev_player.payoff))
            role_list.append("Buyer")

        return dict(
            round=6,
            idealX=idealX_list,
            offerMin=offerMin_list,
            offerMax=offerMax_list,
            choice=choice_list,
            payoff=payoff_list,
            roundName=roundName_list,
            role=role_list,
        )

page_sequence = [RolesIntro, Roles, Response, NoZeroWait, Results]