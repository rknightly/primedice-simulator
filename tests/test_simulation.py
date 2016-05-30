from unittest import TestCase


class TestRoll(TestCase):
    """Assure that the rolling method functions appropriately, with the ability
    to win and lose when the roll is low or too high, respectively
    """

    def setUp(self):
        from primedice_sim import Account

        # Account is not relevant to rolls, but still necessary for setup
        self.account = Account(balance=100)

    def test_win(self):
        from primedice_sim import Configuration, Simulation

        config = Configuration(base_bet=1, payout=2)
        simulation = Simulation(config=config, account=self.account,
                                random_seed=20)
        # First roll with random_seed(20) is 24.77
        # Roll under value is 49.5 with payout=2
        self.assertTrue(simulation.roll(), "Lost roll that should have been"
                                           " won with standard payout (2)")

    def test_lose(self):
        from primedice_sim import Simulation, Configuration

        config = Configuration(base_bet=1, payout=2)
        simulation = Simulation(config=config, account=self.account,
                                random_seed=12)
        # First roll with random_seed(12) is 77.75
        # Roll under value is 49.5 with payout=2
        self.assertFalse(simulation.roll(), "Lost roll that should have been "
                                            "won with standard payout (2)")

    def test_win_high_payout(self):
        from primedice_sim import Configuration, Simulation

        config = Configuration(base_bet=1, payout=3)
        simulation = Simulation(config=config, account=self.account,
                                random_seed=20)
        # First roll with random_seed(20) is 24.77
        # Roll under value is 33.00 with payout=3
        self.assertTrue(simulation.roll(), "Lost roll that should have been "
                                           "won with high payout (3)")

    def test_lose_high_payout(self):
        from primedice_sim import Configuration, Simulation

        config = Configuration(base_bet=1, payout=3)
        simulation = Simulation(config=config, account=self.account,
                                random_seed=5)
        # First roll with random_seed(5) is 41.85
        # Roll under value is 33.00 with payout=3
        self.assertFalse(simulation.roll(), "Won roll that should have been "
                                            "lost with high payout (3)")

    def test_win_low_payout(self):
        from primedice_sim import Configuration, Simulation

        config = Configuration(base_bet=1, payout=1.5)
        simulation = Simulation(config=config, account=self.account,
                                random_seed=5)
        # First roll with random_seed(5) is 41.85
        # Roll under value is 66.00 with payout=1.5
        self.assertTrue(simulation.roll, "Lost roll that should have been won"
                                         " with low payout (1.5)")

    def test_lose_low_payout(self):
        from primedice_sim import Configuration, Simulation

        config = Configuration(base_bet=1, payout=1.5)
        simulation = Simulation(config=config, account=self.account,
                                random_seed=12)
        # First roll with random_seed(12) is 77.75
        # Roll under value is 66.00 with payout=1.5
        self.assertFalse(simulation.roll(), "Won roll that should have been "
                                            "lost with low_payout (1.5)")

    def test_multiple_rolls(self):
        from primedice_sim import Simulation, Configuration

        config = Configuration(base_bet=1, payout=2)

        simulation = Simulation(config=config, account=self.account,
                                random_seed=10)
        # Generated numbers with random seed of 10 are:
        # 93.61, 5.33, 70.26, 79.06, 94.71
        # A win is made by rolling a number less than 49.5 in this case
        # The sequence should then be loss, win, loss, loss, loss
        self.assertFalse(simulation.roll(), "Failed first roll of multiple"
                                            " rolls")
        self.assertTrue(simulation.roll(), "Failed second roll of multiple"
                                           " rolls")
        self.assertFalse(simulation.roll(), "Failed third roll of multiple"
                                            " rolls")
        self.assertFalse(simulation.roll(), "Failed fourth roll of multiple"
                                            " rolls")
        self.assertFalse(simulation.roll(), "Failed fifth roll if multiple"
                                            "rolls")


class TestIncreaseBet(TestCase):
    """Ensure that the bet is increased appropriately when the increase_bet
    method is called
    """

    def setUp(self):
        from primedice_sim import Account

        # Account is not relevant to the test, but still necessary for setup
        self.account = Account(balance=50)

    def test_increase_integer(self):
        from primedice_sim import Configuration, Simulation

        config = Configuration(base_bet=4, payout=2, loss_adder=100)
        simulation = Simulation(config=config, account=self.account)

        simulation.increase_bet()
        self.assertEqual(simulation.current_bet, 8,
                         "Current bet was not increased properly in Test 1")

    def test_increase_float(self):
        from primedice_sim import Configuration, Simulation
        config = Configuration(base_bet=1, payout=3, loss_adder=50)
        simulation = Simulation(config=config, account=self.account)
        simulation.increase_bet()
        self.assertEqual(simulation.current_bet, 1.5,
                         "Current bet was not increased properly in Test 2")


class TestResetBet(TestCase):
    """Ensure that the bet is appropriately reset to its initial value when
    reset_bet() is called
    """

    def setUp(self):
        from primedice_sim import Account
        self.account = Account(balance=100)

    def test_reset_single_roll(self):
        from primedice_sim import Configuration, Simulation

        config = Configuration(base_bet=7, payout=2, loss_adder=200)
        simulation = Simulation(config=config, account=self.account)
        simulation.increase_bet()
        simulation.reset_bet()

        self.assertEqual(simulation.current_bet, 7,
                         "Bet was not reset properly after it was increased a"
                         " single time")

    def test_reset_multiple_rolls(self):
        from primedice_sim import Configuration, Simulation

        config = Configuration(base_bet=10, payout=2, loss_adder=200)
        simulation = Simulation(config=config, account=self.account)
        for _ in range(6):
            simulation.increase_bet()
        simulation.reset_bet()

        self.assertEqual(simulation.current_bet, 10,
                         "Bet was not reset properly after it was increased"
                         " multiple times")

    def test_reset_without_rolling(self):
        from primedice_sim import Configuration, Simulation

        config = Configuration(base_bet=1, payout=5, loss_adder=100)
        simulation = Simulation(config=config, account=self.account)
        # No increases or decreases made
        simulation.reset_bet()

        self.assertEqual(simulation.current_bet, 1,
                         "Bet was not reset properly when no changes were made"
                         " between resets")


class TestLoseRoll(TestCase):
    """Assure that the bet is appropriately increased after a roll is lost"""

    def setUp(self):
        from primedice_sim import Account
        self.account = Account(balance=100)

    def test_single_lose_roll(self):
        from primedice_sim import Configuration, Simulation
        config = Configuration(base_bet=4, payout=2, loss_adder=100)
        simulation = Simulation(config=config, account=self.account)
        simulation.lose_roll()
        self.assertEqual(simulation.current_bet, 8,
                         "Bet was not correctly increased after single loss"
                         "with 100% loss increase")

    def test_multiple_loose_roll(self):
        from primedice_sim import Configuration, Simulation
        config = Configuration(base_bet=4, payout=2, loss_adder=100)
        simulation = Simulation(config=config, account=self.account)
        for _ in range(4):
            simulation.lose_roll()
        self.assertEqual(simulation.current_bet, 64,
                         "Bet was not correctly increased after multiple"
                         " losses with 100% loss increase")

    def test_frac_adder(self):
        from primedice_sim import Configuration, Simulation
        config = Configuration(base_bet=4, payout=2, loss_adder=50)
        simulation = Simulation(config=config, account=self.account)
        simulation.lose_roll()
        self.assertEqual(simulation.current_bet, 6,
                         "Bet was not correctly increased after single loss"
                         "with 50% loss increase")

    def test_lose_0_adder(self):
        from primedice_sim import Configuration, Simulation
        config = Configuration(base_bet=10, payout=2, loss_adder=0)
        simulation = Simulation(config=config, account=self.account)
        simulation.lose_roll()
        self.assertEqual(simulation.current_bet, 10,
                         "Bet did not remain constant after loss when"
                         "loss_adder was 0")


class TestSingleSim(TestCase):
    """Ensure that in a single simulation, the order of balances is correctly
    collected and returned.
    """

    def test_single_sim_base_1(self):
        from primedice_sim import Configuration, Account, Simulation

        config = Configuration(base_bet=1, payout=2, iterations=1,
                               loss_adder=100)
        account = Account(balance=5)
        simulation = Simulation(config=config, account=account,
                                random_seed=4)
        sim_result = simulation.single_sim()

        self.assertEqual(sim_result.get_balances(),
                         [5, 6, 5, 7, 6, 4, 8, 9, 10, 11, 10, 8, 12, 13, 14,
                          13, 11, 7], "Incorrect sequence of balances in "
                                      "single simulation, base_bet=1")

    def test_single_sim_base_2(self):
        from primedice_sim import Configuration, Account, Simulation

        config = Configuration(base_bet=2, payout=2, iterations=1,
                               loss_adder=100)
        account = Account(balance=10)
        simulation = Simulation(config=config, account=account, random_seed=12)
        sim_result = simulation.single_sim()

        self.assertEqual(sim_result.get_balances(), [10, 8, 12, 10, 6],
                         "Incorrect sequence of balances in single simulation,"
                         "base_bet=2")
