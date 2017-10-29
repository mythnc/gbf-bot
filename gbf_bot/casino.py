from fractions import Fraction
import logging
from os.path import join
import random
import sys
import time
import pyautogui
from . import images_dir
from . import poker_config as config
from . import utility
from .components import Button

logger = logging.getLogger(__name__)

poker_dir = join(images_dir, 'poker')
doubleup_dir = join(poker_dir, 'doubleup')

card_match = "XX23456789TJQKA"
numbers = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
suits = ['S', 'C', 'D', 'H']
cards_name = [suit + number + '.png' for suit in suits for number in numbers]\
             + ["JOKER.png"]


class PokerBot:
    logger = logging.getLogger(__name__ + '.PokerBot')

    def __init__(self):
        self.cards = [config['card' + str(i)] for i in range(5)]
        self.card_size = config['card size']
        self.start = Button('poker_start.png', config['start'])
        self.ok = self.start
        self.yes = Button('poker_yes.png', config['yes'])
        self.no = Button('poker_no.png', config['no'])
        self.play_time = config['play time']
        self.logger = logging.getLogger(__name__ + '.' + PokerBot.__name__)

    @staticmethod
    def detect_cards():
        base_images = utility.screenshot(0, 1/3, 1, 1/6)
        count = 0
        cards = [None] * 5
        for card_name in cards_name:
            confidence = 0.97
            if card_name[1] in ('J', 'Q', 'K'):
                confidence = 0.98
            found = pyautogui.locate(join(poker_dir, card_name), base_images,
                                     confidence=confidence)
            if found:
                PokerBot.logger.debug(card_name)
                count += 1
                i = (found[0] - 41) // 77
                cards[i] = card_name.split('.')[0]
            # hope there is no error
            #if count == 5:
            #    break
        return cards

    def click(self, card_index, duration=0.15):
        center_point = self.cards[card_index]
        return utility.click(center_point, self.card_size, duration)

    @staticmethod
    def is_double_up():
        while True:
            base_images = utility.screenshot(0, 1/4, 1, 1/12)
            result = pyautogui.locate(join(poker_dir, 'to_double_up.png'), base_images,
                                      confidence=0.9)
            if result is not None:
                return True
            result = pyautogui.locate(join(poker_dir, 'to_retry.png'), base_images,
                                      confidence=0.9)
            if result is not None:
                return False
            time.sleep(0.5)

    def activate(self):
        pyautogui.PAUSE = 1

        self.logger.info('poker bot start')
        start_time = time.time()
        current_time = time.time()
        time.sleep(1)
        self.start.double_click()
        while current_time - start_time <= self.play_time:
            time.sleep(2)
            cards = PokerBot.detect_cards()
            self.logger.info(cards)
            poker = Poker(cards)
            hold_cards_index = poker.play()
            hold_cards_index.sort()
            pyautogui.PAUSE = 0.2
            for card_index in hold_cards_index:
                self.click(card_index)
                time.sleep(0.1 * random.random())
            pyautogui.PAUSE = 1
            self.ok.click()
            time.sleep(2.5 + 0.1 * random.random())
            if PokerBot.is_double_up():
                self.logger.info('play double up')
                self.yes.click()
                DoubleUpBot().activate()
            self.logger.info('new game')
            self.start.click()
            current_time = time.time()

        self.logger.info('poker bot end')
        sys.exit(0)


class DoubleUpBot:
    cards_name = [suit + number + '.png' for suit in suits for number in numbers]
    logger = logging.getLogger(__name__ + '.DoubleUpBot')

    def __init__(self):
        self.low = Button('poker_yes.png', config['yes'])
        self.high = Button('poker_no.png', config['no'])
        self.logger = logging.getLogger(__name__ + '.' + DoubleUpBot.__name__)
        self.yes = self.low

    @staticmethod
    def detect_card():
        base_images = utility.screenshot(0, 1/4, 1, 1/4)
        for card_name in DoubleUpBot.cards_name:
            confidence = 0.95
            if card_name[1] in ('J', 'Q', 'K'):
                confidence = 0.94
            found = pyautogui.locate(join(doubleup_dir, card_name), base_images,
                                     confidence=confidence)
            if found:
                DoubleUpBot.logger.info(card_name.split('.')[0])
                return card_name

        # confidence has to be adjusted
        DoubleUpBot.logger.warning('No card could be found')
        return None

    @staticmethod
    def is_continue():
        while True:
            base_images = utility.screenshot(0, 1/5, 1, 1/12)
            result = pyautogui.locate(join(doubleup_dir, 'continue.png'),
                                      base_images, confidence=0.9)
            if result is not None:
                return True
            result = pyautogui.locate(join(doubleup_dir, 'finished1.png'),
                                      base_images, confidence=0.9)
            if result is not None:
                return False
            result = pyautogui.locate(join(doubleup_dir, 'finished2.png'),
                                      base_images, confidence=0.9)
            if result is not None:
                return False
            time.sleep(0.5)

    def activate(self):
        time.sleep(1)
        doubleup = DoubleUp()
        for _ in range(10):
            card = DoubleUpBot.detect_card()
            result = doubleup.play(card[1])
            if result == 'high':
                self.high.click()
            elif result == 'low':
                self.low.click()
            time.sleep(1.75 + 0.1 * random.random())
            if DoubleUpBot.is_continue():
                self.yes.click()
                time.sleep(1.75 + 0.1 * random.random())
            else:
                return


class DoubleUp:
    def __init__(self):
        self.numbers = list(range(2, 15)) * 4
        self.logger = logging.getLogger(__name__ + '.' + DoubleUp.__name__)

    def high_prob(self, number):
        return Fraction(len([n for n in self.numbers if n > number]), len(self.numbers))

    def low_prob(self, number):
        return Fraction(len([n for n in self.numbers if n < number]), len(self.numbers))

    def play(self, string):
        number = card_match.index(string)
        self.numbers.remove(number)
        high = self.high_prob(number)
        self.logger.info('high: ' + str(high))
        low = self.low_prob(number)
        self.logger.info('low: ' + str(low))
        if high >= low:
            self.logger.info('press high')
            return 'high'
        elif high < low:
            self.logger.info('press low')
            return 'low'


class Poker:
    def __init__(self, cards):
        self.cards = cards
        self.numbers = [card_match.index(c[1])
                        for c in cards if c != "JOKER"]
        self.numbers.sort()
        self.suits = [c[:1] for c in cards if c != "JOKER"]
        self.has_joker = "JOKER" in cards
        self.logger = logging.getLogger(__name__ + '.' + Poker.__name__)

    def play(self):
        '''return index of keep cards
        '''
        if self.has_joker:
            return self.play_with_joker()

        if self.is_straight_flush():
            self.logger.info('straight flush')
            result = list(range(5))
        elif self.kind(4):
            self.logger.info('4 kind')
            result = self.index_all(self.kind(4))
        elif self.is_full_house():
            self.logger.info('full house')
            result = list(range(5))
        elif self.is_flush():
            self.logger.info('flush')
            result = list(range(5))
        elif self.is_straight():
            self.logger.info('straight')
            result = list(range(5))
        elif self.kind(3):
            self.logger.info('3 kind')
            result = self.index_all(self.kind(3))
        elif self.two_pair():
            self.logger.info('2 pair')
            pairs = self.two_pair()
            indexes_2d = [self.index_all(pair) for pair in pairs]
            result = [n for index in indexes_2d for n in index]
        elif self.kind(2):
            self.logger.info('one pair')
            result = self.index_all(self.kind(2))
        elif self.kind(4, 'suits'):
            self.logger.info('4 kind of suits')
            result = self.index_all(self.kind(4, 'suits'))
        else:
            self.logger.info('no pair: random chose one or drop all')
            i = random.randint(0, 1)
            # drop all or random chose 1
            select = [[], [random.randint(0, 4)]]
            result = select[i]

        self.logger.debug(result)
        return result

    def play_with_joker(self):
        joker_index = [self.cards.index('JOKER')]

        interval = self.numbers[-1] - self.numbers[0]
        # 5 kind
        if self.kind(4) and self.has_joker:
            self.logger.info('5 kind')
            result = list(range(5))
        elif self.is_straight_flush():
            self.logger.info('straight flush')
            result = list(range(5))
        # 4 kind
        elif self.kind(3) and self.has_joker:
            self.logger.info('4 kind')
            result = self.index_all(self.kind(3)) + joker_index
        # full house
        elif self.two_pair() or self.kind(3):
            self.logger.info('full house')
            result = list(range(5))
        elif self.is_flush():
            self.logger.info('flush')
            result = list(range(5))
        # straight
        elif (self.is_straight() or (len(set(self.numbers)) == 4
                                     and (interval == 3 or interval == 4))):
            self.logger.info('straight')
            result = list(range(5))
        # 3 kind
        elif self.kind(2):
            self.logger.info('3 kind')
            result = self.index_all(self.kind(2)) + joker_index
        else:
            self.logger.info('no pair: chose joker')
            result = joker_index

        self.logger.debug(result)
        return result

    def index_all(self, x):
        # numbers
        if isinstance(x, int):
            string = card_match[x]
        # suits
        elif isinstance(x, str):
            string = x
        return [i for i, card in enumerate(self.cards) if string in card]

    def two_pair(self):
        pair1 = self.kind(2)
        pair2 = self.kind(2, is_reversed=True)
        if pair1 != pair2:
            return (pair1, pair2)
        return None

    def kind(self, size, cmp='numbers', is_reversed=False):
        d = {'numbers': self.numbers, 'suits': self.suits}
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

        if 14 == self.numbers[-1]:
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
        if self.is_straight() and self.is_flush():
            return True
        return False
