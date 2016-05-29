from unittest import TestCase


class TestSimulation(TestCase):

    def test_roll(self):
        from primedice_sim import Configuration, Account, Simulation
        configuration = Configuration(base_bet=1, payout=2)
        account = Account(balance=10)
        simulation = Simulation(config=configuration, account=account,
                                random_seed=10)
        self.assertFalse(simulation.roll(), "Failed first roll")
        self.assertTrue(simulation.roll(), "Failed second roll")
        self.assertFalse(simulation.roll(), "Failed third roll")
        self.assertFalse(simulation.roll(), "Failed fourth roll")
        self.assertFalse(simulation.roll(), "Failed fifth roll")

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
