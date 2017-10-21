import random

class Poker:
    card_match = "XX23456789TJQKA"

    def __init__(self, cards):
        self.cards = cards
        self.numbers = [Poker.card_match.index(c[1:])
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

        self.logger.info(result)
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
        return result

    def index_all(self, x):
        # numbers
        if isinstance(x, int):
            string = Poker.card_match[x]
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
