from otree.api import Bot, Submission
import random
import time
from . import *

class PlayerBot(Bot):
    def play_round(self):


        yield Submission(LandingPage, check_html=False)

        time.sleep(15)
        yield Submission(Introduction, check_html=False)

        time.sleep(15)
        yield Submission(PartOne, check_html=False)

        time.sleep(15)
        yield Submission(PayoffsSeller, check_html=False)

        time.sleep(15)
        yield Submission(DeterminingX, check_html=False)

        time.sleep(15)
        yield Submission(RoundTiming, check_html=False)

        time.sleep(15)
        yield Submission(ExampleDraws, check_html=False)

        time.sleep(15)
        yield Submission(ChatOnly, check_html=False)

        # Randomize slider inputs
        max_slider = random.randint(1, 8)
        min_slider = random.randint(1, max_slider)

        time.sleep(15)
        yield SellerView, {
            'minSlider': min_slider,
            'maxSlider': max_slider,
        }

        # Random response: 0 or between min and max
        possible_responses = [0] + list(range(min_slider, max_slider + 1))
        response = random.choice(possible_responses)

        time.sleep(15)
        yield BuyersView, {
            'response': response,
        }

        time.sleep(15)
        yield Submission(Results, check_html=False)

        time.sleep(15)
        yield Submission(PayoffsRecap, check_html=False)
