import random
import logging

from retry_helper import RetryManager

logging.basicConfig(level=logging.DEBUG)


class Game:
    def __init__(self):
        self.max_number = 6

    def roll_six_on_dice(self):
        number = random.randint(1, self.max_number)
        if number != self.max_number:
            print("You roll", number)
            raise ValueError("Bad luck")
        else:
            print(f"Hurray you roll {self.max_number}!!!")

    def reset_func(self, text):
        print(text, self.max_number)

    def roll_until_six(self):
        with RetryManager(max_attempts=3, wait_seconds=0, exceptions=(ValueError,), reset_func=self.reset_func,
                          reset_func_kwargs={'text': "Bad luck, try it again."}) as retry:
            while retry:
                with retry.attempt:
                    self.roll_six_on_dice()


Game().roll_until_six()
