from unittest import TestCase


class TestConfiguration(TestCase):
    def test_calc_win_chance(self):
        from primedice_sim import Configuration
        config = Configuration(base_bet=1, payout=2)
        self.assertEquals(config.calc_win_chance(), 49.5,
                          "Win chance incorrectly calculated in Test 1")

        config = Configuration(base_bet=1, payout=3)
        self.assertEquals(config.calc_win_chance(), 33.0,
                          "Win chance incorrectly calculated in Test 2")

        config = Configuration(base_bet=1, payout=1.5)
        self.assertEquals(config.calc_win_chance(), 66.0,
                          "Win chance incorrectly calculated in Test 3")
