from gbf_bot.casino import Poker


class TestPoker:
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
