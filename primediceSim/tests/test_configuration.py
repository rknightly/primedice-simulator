from unittest import TestCase
from primediceSim.configuration import Configuration

class TestCalcRollUnderValue(TestCase):
    """Make sure that the roll_under_value is appropriately calculated"""

    def test_mid_payout(self):
        config = Configuration(base_bet=1, payout=2)
        self.assertEquals(config.calc_roll_under_value(), 49.5,
                          "Roll under value incorrectly calculated with medium"
                          " payout of 2")

    def test_high_payout(self):
        config = Configuration(base_bet=1, payout=3)
        self.assertEquals(config.calc_roll_under_value(), 33.0,
                          "Roll under value incorrectly calculated with high"
                          " payout of 3")

    def test_low_payout(self):
        config = Configuration(base_bet=1, payout=1.5)
        self.assertEquals(config.calc_roll_under_value(), 66.0,
                          "Roll under value incorrectly calculated with low"
                          " payout of 1.5")


class TestCheckValidPayout(TestCase):
    """Ensure that the payout is appropriately checked for validity"""

    def test_valid_value(self):
        config = Configuration(base_bet=1, payout=3)
        self.assertTrue(config.check_valid_payout(), "Valid payout value of 3"
                                                     "was marked as invalid")

    def test_too_high(self):
        config = Configuration(base_bet=1, payout=10000)
        self.assertFalse(config.check_valid_payout(), "Invalid payout value of"
                                                      " 10000 was marked as"
                                                      " valid, but it is too"
                                                      "high")

    def test_too_low(self):
        config = Configuration(base_bet=1, payout=1)
        self.assertFalse(config.check_valid_payout(), "Invalid payout value of"
                                                      " 1 was marked as valid,"
                                                      " but it is too low")


class TestSetPayout(TestCase):
    """Ensure that payout and roll under values change accordingly"""

    def test_payout_change(self):
        config = Configuration(base_bet=2, payout=2)
        config.set_payout(3)
        self.assertEqual(config.get_payout(), 3, "Payout was not set"
                                                 " appropriately")

    def test_roll_under_change(self):
        config = Configuration(base_bet=2, payout=2)
        config.set_payout(3)
        self.assertEqual(config.get_roll_under_value(), 33.0,
                         "Roll under value was not also set when set_payout"
                         " was called")
