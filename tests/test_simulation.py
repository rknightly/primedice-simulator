from unittest import TestCase


class TestSimulation(TestCase):

    def test_run(self):
        from primedice_sim import Configuration, Account, Simulation
        config = Configuration(base_bet=1, payout=2, iterations=1,
                               loss_adder=100)
        account = Account(balance=5)
        simulation = Simulation(config=config, account=account,
                                random_seed=4)

        sim_result = simulation.single_sim()
        self.assertEqual(sim_result.get_rolls_until_bankrupt(), 17)
        self.assertEqual(sim_result.get_balances(), [5, 6, 5, 7, 6, 4, 8, 9,
                                                     10, 11, 10, 8, 12, 13, 14,
                                                     13, 11, 7])

    def test_roll(self):

        self.assertEquals = (5, 5)

    def test_decrease_balance(self):
        self.assertEquals = (5, 5)
