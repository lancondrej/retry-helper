import random
import logging
from retry_helper import RetryManager

logging.basicConfig(level=logging.DEBUG)


@RetryManager(max_attempts=3, wait_seconds=0, exceptions=(ValueError,))
def roll_six_on_dice():
    number = random.randint(1, 6)
    if number != 6:
        print("You roll", number)
        raise ValueError
    else:
        print("Hurray you roll 6!!!")


roll_six_on_dice()
