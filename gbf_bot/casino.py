from datetime import datetime
from fractions import Fraction
import logging
from os.path import join
import random
import sys
import time

import pyautogui

from .constants import images_dir, poker_config as config
from .components import Button, AppWindow, Mouse


logger = logging.getLogger(__name__)

poker_dir = join(images_dir, "poker")
doubleup_dir = join(poker_dir, "doubleup")

card_match = "XX23456789TJQKA"
numbers = ["2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K", "A"]
suits = ["S", "C", "D", "H"]


class NoneInCardsException(Exception):
    pass


def save_image(im):
    today = datetime.now()
    file_name = str(today).split(".")[0].translate({ord(c): "" for c in " :-"})
    im.save("{}.png".format(file_name))


class PokerBot:
    cards_name = [suit + number + ".png" for suit in suits for number in numbers] + ["JOKER.png"]
    logger = logging.getLogger(__name__ + ".PokerBot")

    def __init__(self):
        self.cards = [config["card" + str(i)] for i in range(5)]
        self.card_size = config["card size"]
        self.start = Button("poker_start.png", config["start"])
        self.ok = self.start
        self.yes = Button("poker_yes.png", config["yes"])
        self.no = Button("poker_no.png", config["no"])
        self.play_time = config["play time"]
        self.mouse_position = None
        self.used_chips = 0
        self.got_chips = 0
        self.logger = logging.getLogger(__name__ + "." + PokerBot.__name__)

    @staticmethod
    def detect_cards():
        base_image = AppWindow.screenshot((0, 1 / 3, 1, 1 / 6))
        cards = [None] * 5
        for card_name in PokerBot.cards_name:
            found = pyautogui.locate(join(poker_dir, card_name), base_image, confidence=0.97)
            if found:
                PokerBot.logger.debug(card_name)
                i = (found[0] - 41) // 77
                cards[i] = card_name.split(".")[0]

        PokerBot.logger.info(cards)
        # Current algorithm can't figure out this kind of cards
        if None in cards:
            PokerBot.logger.warning("None in cards. Hold all.")
            save_image(base_image)
            raise NoneInCardsException()
        return cards

    def click(self, card_index, duration=0.15):
        center_point = self.cards[card_index]
        return Mouse.click(center_point, self.card_size, duration)

    @staticmethod
    def is_double_up():
        while True:
            base_image = AppWindow.screenshot((0, 1 / 4, 1, 1 / 12))
            result = pyautogui.locate(join(poker_dir, "to_double_up.png"), base_image, confidence=0.9)
            if result is not None:
                return True
            result = pyautogui.locate(join(poker_dir, "to_retry.png"), base_image, confidence=0.9)
            if result is not None:
                return False
            time.sleep(0.5)

    def is_over_play_time(self, start_time):
        return time.time() - start_time > self.play_time

    def start_new_game(self):
        self.logger.info("\nnew game")
        self.used_chips += 1
        if self.mouse_position != self.start:
            self.start.click()
            self.mouse_position = self.start
        else:
            Mouse.click_again()

    @staticmethod
    def check_result(poker):
        if len(poker.hold_cards_index) == 5:
            return

        pyautogui.PAUSE = 0.2
        cards = PokerBot.detect_cards()
        pyautogui.PAUSE = 1
        poker.new_cards(cards)
        poker.calculate()

    def activate(self):
        pyautogui.PAUSE = 1

        self.logger.info("poker bot start")
        start_time = time.time()
        time.sleep(1)
        self.start.click()
        poker = Poker()
        try:
            while not self.is_over_play_time(start_time):
                self.start_new_game()
                time.sleep(2)
                try:
                    cards = PokerBot.detect_cards()
                    poker.new_game(cards)
                    hold_cards_index = poker.calculate()
                except NoneInCardsException:
                    hold_cards_index = list(range(5))

                pyautogui.PAUSE = 0.2
                for card_index in hold_cards_index:
                    self.click(card_index)
                    time.sleep(0.2 * random.random())

                pyautogui.PAUSE = 1
                if hold_cards_index:
                    self.ok.click()
                else:
                    Mouse.click_again()
                time.sleep(2.5 + 0.2 * random.random())

                if PokerBot.is_double_up():
                    try:
                        self.check_result(poker)
                        chip = poker.earned_chips()
                    except NoneInCardsException:
                        chip = 1
                    self.logger.info("play double up")
                    self.yes.click()
                    self.got_chips += DoubleUpBot(chip).activate()
                    self.mouse_position = None

        except KeyboardInterrupt:
            pass
        except pyautogui.FailSafeException:
            pass
        except Exception as e:  # pylint: disable=broad-except
            self.logger.error(e)
        finally:
            self.do_statistics(start_time)
            self.logger.info("poker bot end")
            sys.exit(0)

    def do_statistics(self, start_time):
        play_time = time.time() - start_time
        minute = play_time // 60
        second = play_time % 60
        self.logger.info("\nplay time: %02d:%02d", minute, second)
        self.logger.info("used chips: %d", self.used_chips)
        self.logger.info("got chips: %d", self.got_chips)


class DoubleUpBot:
    cards_name = [suit + number + ".png" for suit in suits for number in numbers]
    logger = logging.getLogger(__name__ + ".DoubleUpBot")

    def __init__(self, chip):
        self.low = Button("poker_yes.png", config["yes"])
        self.high = Button("poker_no.png", config["no"])
        self.yes = self.low
        self.no = self.high
        self.mouse_position = self.yes
        self.chip = chip
        self.previous_number = ""
        self.card = ""
        self.logger = logging.getLogger(__name__ + "." + DoubleUpBot.__name__)

    @staticmethod
    def detect_card(is_final_round=False):
        base_image = AppWindow.screenshot((0, 1 / 4, 1, 1 / 4))
        if is_final_round:
            base_image = AppWindow.screenshot((3 / 7, 1 / 4, 2 / 7, 1 / 4))

        for card_name in DoubleUpBot.cards_name:
            confidence = 0.95
            if card_name[1] in ("J", "Q", "K"):
                confidence = 0.93
            found = pyautogui.locate(join(doubleup_dir, card_name), base_image, confidence=confidence)
            if found:
                DoubleUpBot.logger.info(card_name.split(".")[0])
                return card_name

        # confidence has to be adjusted
        DoubleUpBot.logger.warning("No card could be found")
        save_image(base_image)
        return None

    def is_continue(self):
        while True:
            base_image = AppWindow.screenshot((0, 1 / 5, 1, 1 / 12))
            result = pyautogui.locate(join(doubleup_dir, "continue.png"), base_image, confidence=0.9)
            if result is not None:
                return True

            result = pyautogui.locate(join(doubleup_dir, "lose.png"), base_image, confidence=0.9)
            if result is not None:
                self.chip = 0
                return False

            result = pyautogui.locate(join(doubleup_dir, "maximum.png"), base_image, confidence=0.9)
            if result is not None:
                card = DoubleUpBot.detect_card(True)
                if card_match.index(self.card[1]) != card_match.index(card[1]):
                    self.chip *= 2
                return False

            time.sleep(0.5)

    def activate(self):
        time.sleep(3)
        doubleup = DoubleUp()
        for round_ in range(1, 11):
            self.logger.info(f"\nround {round_}")
            self.card = DoubleUpBot.detect_card()
            if round_ > 1 and self.previous_number != self.card[1]:
                self.chip *= 2

            result = doubleup.play(self.card[1])

            result_map = {"high": self.high, "low": self.low}
            if self.mouse_position == result_map[result]:
                Mouse.click_again()
            else:
                result_map[result].click()
                self.mouse_position = result_map[result]
            time.sleep(2 + 0.1 * random.random())

            if not self.is_continue():
                self.logger.info(f"earned chips: {self.chip}")
                return self.chip

            if self.mouse_position == self.yes:
                Mouse.click_again()
            else:
                self.yes.click()
                self.mouse_position = self.yes
            self.previous_number = self.card[1]
            time.sleep(2 + 0.1 * random.random())


class DoubleUp:
    def __init__(self):
        self.numbers = list(range(2, 15)) * 4
        self.logger = logging.getLogger(__name__ + "." + DoubleUp.__name__)

    def high_prob(self, number):
        return Fraction(len([n for n in self.numbers if n > number]), len(self.numbers))

    def low_prob(self, number):
        return Fraction(len([n for n in self.numbers if n < number]), len(self.numbers))

    def play(self, string):
        number = card_match.index(string)
        self.numbers.remove(number)
        high = self.high_prob(number)
        self.logger.info(f"high: {float(high)}")
        low = self.low_prob(number)
        self.logger.info(f"low: {float(low)}")
        if high >= low:
            self.logger.info("press high")
            result = "high"
        elif high < low:
            self.logger.info("press low")
            result = "low"
        return result


class Poker:
    def __init__(self):
        self.cards = []
        self.numbers = []
        self.suits = []
        self.has_joker = False
        self.poker_hands = ""
        self.hold_cards_index = []
        self.logger = logging.getLogger(__name__ + "." + Poker.__name__)

    def new_game(self, cards):
        self.cards = cards
        self.numbers = [card_match.index(c[1]) for c in cards if c != "JOKER"]
        self.numbers.sort()
        self.suits = [c[:1] for c in cards if c != "JOKER"]
        self.has_joker = "JOKER" in cards
        self.poker_hands = None
        self.hold_cards_index = []

    def new_cards(self, cards):
        if len(self.hold_cards_index) == 5:
            return

        self.cards = cards
        self.numbers = [card_match.index(c[1]) for c in cards if c != "JOKER"]
        self.numbers.sort()
        self.suits = [c[:1] for c in cards if c != "JOKER"]
        self.has_joker = "JOKER" in cards

    def calculate(self):
        """Calculate poker hands and return the card index which want to
        hold in self.hold_cards_index.
        """
        if len(self.hold_cards_index) == 5:
            return

        if self.has_joker:
            return self.calculate_with_joker()

        if self.is_straight_flush():
            self.poker_hands = "straight flush"
            self.hold_cards_index = list(range(5))
        elif self.kind(4):
            self.poker_hands = "4 kind"
            self.hold_cards_index = self.index_all(self.kind(4))
        elif self.is_full_house():
            self.poker_hands = "full house"
            self.hold_cards_index = list(range(5))
        elif self.is_flush():
            self.poker_hands = "flush"
            self.hold_cards_index = list(range(5))
        elif self.is_straight():
            self.poker_hands = "straight"
            self.hold_cards_index = list(range(5))
        elif self.kind(3):
            self.poker_hands = "3 kind"
            self.hold_cards_index = self.index_all(self.kind(3))
        elif self.two_pair():
            self.poker_hands = "2 pair"
            pairs = self.two_pair()
            indexes_2d = [self.index_all(pair) for pair in pairs]
            self.hold_cards_index = [n for index in indexes_2d for n in index]
        elif self.kind(2):
            self.poker_hands = "1 pair"
            self.hold_cards_index = self.index_all(self.kind(2))
        elif self.kind(4, "suits"):
            self.poker_hands = "4 same suits"
            self.hold_cards_index = self.index_all(self.kind(4, "suits"))
        else:
            self.poker_hands = "no pair: random chose one or drop all"
            i = random.randint(0, 1)
            # drop all or random chose 1
            select = [[], [random.randint(0, 4)]]
            self.hold_cards_index = select[i]

        self.hold_cards_index.sort()
        self.logger.info(self.poker_hands)
        self.logger.debug(self.hold_cards_index)
        return self.hold_cards_index

    def calculate_with_joker(self):
        joker_index = [self.cards.index("JOKER")]

        interval = self.numbers[-1] - self.numbers[0]
        # 5 kind
        if self.kind(4):
            self.poker_hands = "5 kind"
            self.hold_cards_index = list(range(5))
        elif self.is_straight_flush():
            self.poker_hands = "straight flush"
            self.hold_cards_index = list(range(5))
        # 4 kind
        elif self.kind(3) and self.has_joker:
            self.poker_hands = "4 kind"
            self.hold_cards_index = self.index_all(self.kind(3)) + joker_index
        # full house
        elif self.two_pair() or self.kind(3):
            self.poker_hands = "full house"
            self.hold_cards_index = list(range(5))
        elif self.is_flush():
            self.poker_hands = "flush"
            self.hold_cards_index = list(range(5))
        # straight
        elif self.is_straight() or (len(set(self.numbers)) == 4 and (interval in [3, 4])):
            self.poker_hands = "straight"
            self.hold_cards_index = list(range(5))
        # 3 kind
        elif self.kind(2):
            self.poker_hands = "3 kind"
            self.hold_cards_index = self.index_all(self.kind(2)) + joker_index
        else:
            self.poker_hands = "no pair: chose joker"
            self.hold_cards_index = joker_index

        self.hold_cards_index.sort()
        self.logger.info(self.poker_hands)
        self.logger.debug(self.hold_cards_index)
        return self.hold_cards_index

    def index_all(self, x):
        # numbers
        if isinstance(x, int):
            string = card_match[x]
        # string
        elif isinstance(x, str):
            string = x
        return [i for i, card in enumerate(self.cards) if string in card and card != "JOKER"]

    def earned_chips(self):
        """Calculate and return earned chips."""
        chip_map = {
            "5 kind": 60,
            "straight flush": 25,
            "4 kind": 20,
            "full house": 10,
            "flush": 4,
            "straight": 3,
            "3 kind": 1,
            "2 pair": 1,
        }
        return chip_map[self.poker_hands]

    def two_pair(self):
        pair1 = self.kind(2)
        pair2 = self.kind(2, is_reversed=True)
        if pair1 != pair2:
            return (pair1, pair2)
        return None

    def kind(self, size, cmp="numbers", is_reversed=False):
        d = {"numbers": self.numbers, "suits": self.suits}
        compare = d[cmp]
        if is_reversed:
            compare = reversed(compare)
        for c in compare:
            if d[cmp].count(c) == size:
                return c
        return None

    def is_straight(self):
        if len(set(self.numbers)) != len(self.numbers):
            return False

        interval = self.numbers[-1] - self.numbers[0]
        if interval == 4:
            return True

        if self.numbers[-1] == 14:
            temp = list(self.numbers)
            self.numbers[-1] = 1
            self.numbers.sort()
            result = self.is_straight()
            self.numbers = temp
            return result

        return False

    def is_flush(self):
        return len(set(self.suits)) == 1

    def is_full_house(self):
        if self.kind(2) and self.kind(3):
            return True
        return False

    def is_straight_flush(self):
        return self.is_straight() and self.is_flush()
