import random
import copy
import time
import numpy as np
import itertools


class Simulation:
    """Contain the simulation function and store the data of each simulation"""

    def __init__(self, config, account, random_seed=None):
        self.config = config
        self.account = account

        self.current_bet = config.get_base_bet()
        self.total_balance_lists = []
        random.seed(random_seed)

    def roll(self):

        """Simulate one 'dice roll' and return True if the roll was won by the
        user or False if the roll was lost"""

        # Pick a random number between 0 and 100 out to two decimal places.
        roll_value = random.randrange(0, 10000) / 100
        # print()
        # print("Roll under value:", self.config.get_roll_under_value())
        # print("Roll:", roll_value)
        if roll_value < self.config.get_roll_under_value():
            win = True
        else:
            win = False

        return win

    def increase_bet(self):
        """Increase the current bet by the amount specified by the loss adder
        amount.
        """

        self.current_bet += \
            self.current_bet * self.config.get_loss_adder_decimal()

    def reset_bet(self):
        """Change the current best back to the bet value from the
        configuration.
        """

        self.current_bet = self.config.get_base_bet()

    def lose_roll(self):
        """Simulate a lost roll by increasing the bet by the specified amount
        """

        self.increase_bet()

    def win_roll(self, account):
        """Simulate a won roll by increasing the balance"""

        reward = self.current_bet * self.config.get_payout()
        account.add(reward)
        self.reset_bet()

    def single_sim(self):
        """Simulate a single round of betting until bankruptcy.
        Return a result object containing the results of that one simulation.
        """

        self.reset_bet()
        sim_account = copy.copy(self.account)

        # Create a list of the balance after each roll
        # Start out with initial amount for 0 graph point
        all_balances = [sim_account.get_balance()]
        while sim_account.get_balance() >= self.current_bet:
            sim_account.subtract(self.current_bet)

            if self.roll():
                self.win_roll(sim_account)
            else:
                self.lose_roll()
            all_balances.append(sim_account.get_balance())

        if len(all_balances) == 0:
            print("[WARNING] The given configurations do not allow for a" +
                  " single roll")

        sim_result = Results(balances=all_balances)

        return sim_result

    def print_progress(self, sim_num, progress_checks, screen, progress_bar):
        """Print the current progress of the simulation.
        progress_checks is the amount of progress checks
        that the user wants to be printed during each simulation.
        """
        progress_ticks = 100 / progress_checks

        if sim_num % (self.config.get_iterations() / progress_checks) == 0:
            progress_bar.step(progress_ticks)
            screen.update()

    def verify_progress_checks(self, progress_checks):
        """Check if the progress_checks value is greater than iterations, and
        fix it if so
        """

        # The number of progress checks must be less than the number of
        # iterations in order for the progress bar to work properly.

        if progress_checks > self.config.get_iterations() or \
                progress_checks <= 0:   # The value should also not be negative
            # If this case does arise, set the progress checks to be the same
            # as the number of iterations, simplifying calculations
            progress_checks = self.config.get_iterations()

        return progress_checks

    def print_settings(self):
        """Print the settings that are being accessed by the simulation"""

        print("\n[MESSAGE] Running new simulation\n")
        print("Balance:", self.account.get_balance(), "\n")
        print("Base bet:", self.config.get_base_bet())
        print("Payout:", self.config.get_payout())
        print("Iterations:", self.config.get_iterations())
        print("Loss adder:", self.config.get_loss_adder(), "\n")

    def run(self, progress_bar, screen, progress_checks=50):
        """Run several simulations and return the average of them all"""

        progress_checks = self.verify_progress_checks(progress_checks)

        # Takes the progress bar and the screen in order to update
        # the progress bar and refresh the screen when necessary

        self.print_settings()

        print("[Progress] Running simulations...\n")
        start_time = time.time()

        # Keep a running total of rolls from all simulations to calculate
        # overall average.
        total_rolls_result = 0
        # Keep a running total of average balance from all simulations to
        # calculate overall average.
        total_balance_result = 0
        self.total_balance_lists = []
        each_sim_result = []

        iterations = self.config.get_iterations()
        for sim_num in range(iterations):
            self.print_progress(sim_num, progress_checks, screen, progress_bar)
            sim_result = self.single_sim()
            each_sim_result.append(sim_result)
            total_rolls_result += sim_result.get_rolls_until_bankrupt()
            total_balance_result += sim_result.get_average_balance()
            self.total_balance_lists.append(sim_result.get_balances())

        sim_result = AverageResults(each_sim_result)
        sim_result.print_results()

        time_taken = str((time.time() - start_time))[:5]
        print("[Time] Time taken: --- %s seconds ---" % time_taken, "\n")

        return sim_result


class AverageResults:
    """Contain the average of the results of multiple simulations"""

    def __init__(self, results_list):
        self.results_list = results_list
        self.number_of_results = len(self.results_list)
        self.total_balances_list = [result.get_balances() for result in
                                    self.results_list]

        self.overall_average_balance = self.find_average_bal()
        self.average_rolls_until_bankrupt = \
            self.find_average_rolls_until_bankrupt()
        self.average_balances = self.find_average_balances()
        self.median_balances = self.find_median_balances()
        self.num_of_rolls = len(self.average_balances)

    def find_average_bal(self):
        """Calculate the average balance of all rolls before bankruptcy of
        each run
        """

        total = 0
        for result in self.results_list:
            total += result.get_average_balance()
        average = total // self.number_of_results

        return average

    def find_average_rolls_until_bankrupt(self):
        """Calculate the average number of rolls until bankruptcy in each
         run
         """

        total = 0
        # Average each individual result and find the average of those values
        for result in self.results_list:
            total += result.get_rolls_until_bankrupt()
        average = total // self.number_of_results

        return average

    def find_average_balances(self):
        """Find the average balances from the list of results"""

        print("[Progress] Calculating average balances...")
        start_time = time.time()

        # Produce a lists of lists that are all of the same length by adding
        # zeros to the end of any list that is too short.
        # Then, add the corresponding values of each list together to produce
        # one list of sums

        sum_list = [sum(balances) for balances in
                    itertools.zip_longest(*self.total_balances_list,
                                          fillvalue=0)]

        # Take the list of sums, and divide each one by the number of data
        # points to produce a mean value for each sum
        num_of_balances = len(self.total_balances_list)
        average_list = [total_balance // num_of_balances for
                        total_balance in sum_list]
        print("[Progress] Average balances calculated")
        time_taken = str((time.time() - start_time))[:5]
        print("[Time] Time taken: --- %s seconds ---" % time_taken, "\n")

        return average_list

    def find_median_balances(self):
        """Find the median balances from the list of results"""

        print("[Progress] Calculating median balances...")
        start_time = time.time()

        equal_length_total_balances = itertools.zip_longest(
            *self.total_balances_list, fillvalue=0)

        grouped_balances = zip(equal_length_total_balances)
        median_balances = []
        for balances in grouped_balances:
            median = int(np.median(balances))
            median_balances.append(median)
            # Stop calculating medians once they reach 0
            if median == 0:
                break
        print("[Progress] Median balances calculated")
        time_taken = str((time.time() - start_time))[:5]
        print("[Time] Time taken: --- %s seconds ---" % time_taken, "\n")

        return median_balances

    def get_average_balances(self):
        return self.average_balances

    def get_median_balances(self):
        return self.median_balances

    def print_results(self):
        """Print out the results saved with explaining labels"""
        print("\n[Results] Average rolls until bankruptcy: " +
              str(self.average_rolls_until_bankrupt))
        print("[Results] Average balance during run: " +
              str(self.overall_average_balance))

        print("\n======================================================")


class Results:
    """Contain the results of a simulation"""

    def __init__(self, balances):
        self.balances = balances
        # Initial balance does't count when counting the total rolls
        self.rolls_until_bankrupt = len(balances[1:])
        self.average_balance = np.mean(balances)

    def get_rolls_until_bankrupt(self):
        return self.rolls_until_bankrupt

    def get_average_balance(self):
        return self.average_balance

    def get_results(self):
        return self.rolls_until_bankrupt, self.average_balance

    def get_balances(self):
        return self.balances
