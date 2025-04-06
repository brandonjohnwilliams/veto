from otree.api import Bot, Submission
import random
import time
from . import *

class PlayerBot(Bot):
    def play_round(self):

        yield Submission(LandingPage, check_html=False)
        yield Submission(Introduction, check_html=False)
        yield Submission(PartOne, check_html=False)
        yield Submission(PayoffsSeller, check_html=False)
        yield Submission(DeterminingX, check_html=False)
        yield Submission(RoundTiming, check_html=False)
        yield Submission(ExampleDraws, check_html=False)
        yield Submission(ChatOnly, check_html=False)

        # Randomize slider inputs
        max_slider = random.randint(1, 8)
        min_slider = random.randint(1, max_slider)

        yield SellerView, {
            'minSlider': min_slider,
            'maxSlider': max_slider,
        }
        # time.sleep(30) # causes 30 second delay on choice

        # Random response: 0 or between min and max
        possible_responses = [0] + list(range(min_slider, max_slider + 1))
        response = random.choice(possible_responses)

        yield BuyersView, {
            'response': response,
        }
        # time.sleep(15)

        yield Submission(Results, check_html=False)
        yield Submission(PayoffsRecap, check_html=False)
