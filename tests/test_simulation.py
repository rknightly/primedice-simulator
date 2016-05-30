from unittest import TestCase


class TestRoll(TestCase):

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


class TestSimulation(TestCase):

    def test_increase_bet(self):
        from primedice_sim import Configuration, Account, Simulation

        config = Configuration(base_bet=4, payout=2, loss_adder=100)
        account = Account(balance=50)
        simulation = Simulation(config=config, account=account)

        simulation.increase_bet()
        self.assertEqual(simulation.current_bet, 8,
                         "Current bet was not increased properly in Test 1")

        config = Configuration(base_bet=1, payout=3, loss_adder=50)
        simulation = Simulation(config=config, account=account)
        simulation.increase_bet()
        self.assertEqual(simulation.current_bet, 1.5,
                         "Current bet was not increased properly in Test 2")

    def test_reset_bet(self):
        from primedice_sim import Configuration, Account, Simulation

        config = Configuration(base_bet=10, payout=2, loss_adder=200)
        account = Account(balance=1000)
        simulation = Simulation(config=config, account=account)
        for _ in range(6):
            simulation.increase_bet()
        simulation.reset_bet()
        self.assertEqual(simulation.current_bet, 10,
                         "Bet was not reset properly in Test 2")

        config = Configuration(base_bet=1, payout=5, loss_adder=100)
        simulation = Simulation(config=config, account=account)
        for _ in range(3):
            simulation.increase_bet()
        simulation.reset_bet()
        self.assertEqual(simulation.current_bet, 1,
                         "Bet was not reset properly in Test 2")

    def test_run(self):
        from primedice_sim import Configuration, Account, Simulation

        config = Configuration(base_bet=1, payout=2, iterations=1,
                               loss_adder=100)
        account = Account(balance=5)
        simulation = Simulation(config=config, account=account,
                                random_seed=4)

        sim_result = simulation.single_sim()
        self.assertEqual(sim_result.get_rolls_until_bankrupt(), 17,
                         "Incorrect number of rolls until bankrupt in Test 1")
        self.assertEqual(sim_result.get_balances(),
                         [5, 6, 5, 7, 6, 4, 8, 9, 10, 11, 10, 8, 12, 13, 14,
                          13, 11, 7],
                         "Incorrect sequence of balances in Test 1")

        config = Configuration(base_bet=2, payout=2, iterations=1,
                               loss_adder=100)
        account = Account(balance=10)
        simulation = Simulation(config=config, account=account, random_seed=12)
        sim_result = simulation.single_sim()
        self.assertEqual(sim_result.get_rolls_until_bankrupt(), 4,
                         "Incorrect number of rolls until bankrupt in Test 2")
        self.assertEqual(sim_result.get_balances(), [10, 8, 12, 10, 6],
                         "Incorrect sequence of balances in Test 2")
