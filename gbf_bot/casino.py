class Poker:
    card_match = "XX23456789TJQKA"

    def __init__(self, cards):
        self.cards = cards
        self.numbers = [Poker.card_match.index(c[1:]) 
                        for c in cards if c != "JOKER"]
        self.numbers.sort()
        self.suits = [c[:1] for c in cards if c != "JOKER"]
        self.has_joker = "JOKER" in cards

    def two_pair(self):
        pair1 = self.kind(2)
        pair2 = self.kind(2, is_reversed=True)
        if pair1 != pair2:
            return (pair1, pair2)
        return None

    def kind(self, size, is_reversed=False):
        numbers = self.numbers
        if is_reversed:
            numbers = reversed(self.numbers)
        for number in numbers:
            if self.numbers.count(number) == size:
                return number
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
