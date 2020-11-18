import random
import logging

from retry_helper import RetryManager

logging.basicConfig(level=logging.DEBUG)


def roll_six_on_dice():
    number = random.randint(1, 6)
    if number != 6:
        print("You roll", number)
        raise ValueError
    else:
        print("Hurray you roll 6!!!")


def reset_func():
    print("Bad luck, try it again.")


with RetryManager(max_attempts=3, wait_seconds=0, exceptions=(ValueError,), reset_func=reset_func) as retry:
    while retry:
        with retry.attempt:
            roll_six_on_dice()
