from gbf_bot.casino import Poker


class TestPoker:
    def test_play(self):
        # two pair
        poker = Poker(('S2', 'D2', 'H3', 'C3', 'C5'))
        assert poker.play() == [0, 1, 2, 3]
        # 3 kind
        poker = Poker(('S2', 'D2', 'H2', 'D4', 'C5'))
        assert poker.play() == [0, 1, 2]
        poker = Poker(('S2', 'D2', 'JOKER', 'D4', 'C5'))
        assert poker.play() == [0, 1, 2]
        # straight
        poker = Poker(('S2', 'D3', 'H6', 'D4', 'C5'))
        assert poker.play() == list(range(5))
        poker = Poker(('S2', 'D3', 'HA', 'D4', 'C5'))
        assert poker.play() == list(range(5))
        poker = Poker(('ST', 'DQ', 'HA', 'DK', 'CJ'))
        assert poker.play() == list(range(5))
        poker = Poker(['S6', 'D2', 'JOKER', 'C4', 'C5'])
        assert poker.play() == list(range(5))
        poker = Poker(['SA', 'H3', 'JOKER', 'C4', 'C5'])
        assert poker.play() == list(range(5))
        poker = Poker(['SA', 'DJ', 'JOKER', 'CK', 'CT'])
        assert poker.play() == list(range(5))
        # flush
        poker = Poker(['S2', 'H2', 'S3', 'H3', 'C3'])
        assert poker.play() == list(range(5))
        poker = Poker(['S6', 'S2', 'JOKER', 'S4', 'S5'])
        assert poker.play() == list(range(5))
        # full house
        poker = Poker(['S2', 'H2', 'JOKER', 'S3', 'H3'])
        assert poker.play() == list(range(5))
        poker = Poker(['D3', 'H2', 'JOKER', 'S3', 'D2'])
        assert poker.play() == list(range(5))
        # 4 kind
        poker = Poker(['S5', 'D5', 'H5', 'JOKER', 'C3'])
        assert poker.play() == [0, 1, 2, 3]
        poker = Poker(['S2', 'H2', 'JOKER', 'S3', 'D2'])
        assert poker.play() == [0, 1, 4, 2]
        # straight flush
        poker = Poker(['SA', 'S2', 'JOKER', 'S3', 'S4'])
        assert poker.play() == list(range(5))
        # 5 kind
        poker = Poker(['S5', 'D5', 'H5', 'C5', 'JOKER'])
        assert poker.play() == list(range(5))
        # joker
        poker = Poker(['S5', 'D6', 'HA', 'C8', 'JOKER'])
        assert poker.play() == [4]
        # one pair
        poker = Poker(['S5', 'D6', 'HA', 'C8', 'D5'])
        assert poker.play() == [0, 4]
        poker = Poker(('H5', 'D6', 'C7', 'C5', 'S3'))
        assert poker.play() == [0, 3]
        # 4 kind suits
        poker = Poker(['S5', 'S6', 'SA', 'S8', 'D9'])
        assert poker.play() == [0, 1, 2, 3]
        # no pair
        poker = Poker(['S5', 'D6', 'HA', 'C8', 'CK'])
        n = len(poker.play())
        assert n == 1 or n == 0

    def test_index_all(self):
        poker = Poker(('S2', 'D2', 'H3', 'C3', 'C5'))
        assert poker.index_all(2) == [0, 1]
        poker = Poker(('S3', 'D3', 'H3', 'C3', 'C5'))
        assert poker.index_all(3) == [0, 1, 2, 3]

    def test_two_pair(self):
        poker = Poker(('S2', 'D2', 'H3', 'C3', 'C5'))
        assert poker.two_pair() == (2, 3)
        poker = Poker(('SA', 'D2', 'H3', 'C3', 'C5'))
        assert poker.two_pair() is None
        
    def test_3_kind(self):
        poker = Poker(['S5', 'D5', 'H5', 'C2', 'C3'])
        assert poker.kind(3) == 5
        poker = Poker(['SA', 'D5', 'H5', 'C2', 'C3'])
        assert poker.kind(3) is None
        
    def test_4_kind(self):
        poker = Poker(['S5', 'D5', 'H5', 'C5', 'C3'])
        assert poker.kind(4) == 5
        poker = Poker(['S5', 'D5', 'CK', 'C5', 'C3'])
        assert poker.kind(4) is None

    def test_4_kind_suits(self):
        poker = Poker(['S5', 'S9', 'SA', 'S2', 'C3'])
        assert poker.kind(4, 'suits') == 'S'
        
    def test_is_straight(self):
        poker = Poker(['S6', 'D2', 'H3', 'C4', 'C5'])
        assert poker.is_straight() == True
        poker = Poker(['SA', 'D2', 'H3', 'C4', 'C5'])
        assert poker.is_straight() == True
        poker = Poker(['SA', 'DJ', 'HQ', 'CK', 'CT'])
        assert poker.is_straight() == True
        poker = Poker(['SA', 'DJ', 'HQ', 'CK', 'C9'])
        assert poker.is_straight() == False
        poker = Poker(('S2', 'D2', 'H3', 'C3', 'C5'))
        assert poker.is_straight() == False
        
    def test_flush(self):
        poker = Poker(['S6', 'S2', 'S3', 'S4', 'S5'])
        assert poker.is_flush() == True
        poker = Poker(['S6', 'S2', 'S3', 'S4', 'H5'])
        assert poker.is_flush() == False
        
    def test_full_house(self):
        poker = Poker(['S2', 'H2', 'S5', 'H3', 'C3'])
        assert poker.is_full_house() == False
        
    def test_is_straight_flush(self):
        poker = Poker(['SA', 'S2', 'S5', 'S3', 'S4'])
        assert poker.is_straight_flush() == True
        poker = Poker(['SA', 'S2', 'S5', 'S3', 'H4'])
        assert poker.is_straight_flush() == False
