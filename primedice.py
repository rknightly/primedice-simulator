import decimal
import random
import time
import copy
from tkinter import *

class Gui:
    def __init__(self, default_account, default_config):

        self.def_account = default_account
        self.default_config = default_config
        
        self.master = Tk()
        self.master.title("Primedice Simulator")

        self.run_button = Button(self.master, text="Run",
                                 command=self.run_simulator)
        self.run_button.grid(row=0, column=0)

        self.given_str = StringVar()
        self.input_num = Entry(self.master,
                               textvariable=self.given_str)
        self.input_num.grid(row=1, column=0)

        self.counter = 0
        self.master.mainloop()

    def run_simulator(self):
        pass

class Configuration:
    """Contain all of the configurations of the different options that the primedice
    auto-better provides.
    """
	
    def __init__(self, base_bet, payout, iterations=100, loss_adder=0):
        """ These are the different settings that can be given to the auto-better.
        All of the values should be given as they are on the primedice screen. 
        payout - float multiplier between 1.01202 and 9900
        loss_adder - percent given as integer between 0 and 100.
        """
        self.base_bet = base_bet
        
        if not self.check_valid_payout(payout):
                print("[WARNING] Payout value entered was not within the range allowed by PrimeDice")
        
        self.payout = payout 
        self.loss_adder = loss_adder / 100 	# Turn the user-given percent into a decimal
        self.win_chance = self.calc_win_chance(payout)
        self.roll_under_value = self.win_chance
        self.iterations = iterations
	
    def calc_win_chance(self, payout):
        """Find the win chance that primedice will use with a given win payout."""
        
        # The equation used was found from taking data points from the primedice website 
        # and calculating the line of best fit. It is a power function, following the form
        # f(x) = kx^n where x is the win payout and f(x) is the win chance that primedice
        # allows. Apparently, they have chosen to make k = 98.998 and n = .99999
        # This way, with a high win payout, the chance of winning is low. At the same time,
        # with a low win payout, the chance of winning is much higher.
        
        decimal_places = 2
        win_chance = decimal.Decimal(98.998 * (payout ** -.99999))
        rounded_win_chance = round(win_chance, decimal_places)
        
        return rounded_win_chance
    
    def check_valid_payout(self, payout):
        """Ensure that the given payout is allowed by the site."""
        
        # Primedice enforces a minimum and maximum value for the payout to avoid the
        # Situation of having an absurdly high payout or win chance. The minimum and
        # maximum allowed values are given by the primedice website when an invalid
        # value is entered
        
        payout_minimum = 1.01202
        payout_maximum = 9900
        
        if payout_minimum <= payout and payout <= payout_maximum:
            valid = True
        else:
            valid = False
                
        return valid

    
    def get_base_bet(self):
        return self.base_bet
            
    def get_loss_adder(self):
        return self.loss_adder
            
    def get_payout(self):
        return self.payout

    def get_iterations(self):
        return self.iterations
            
    def get_roll_under_value(self):
        return self.roll_under_value

class Account:
    """Contain the user's primedice account stats"""
    
    def __init__(self, balance):
        self.balance = balance
            
    def add(self, amount):
        """Add to the current account balance"""

        self.balance += amount
        
        return self.balance
            
    def subtract(self, amount):
        """Subtract from the current account balance"""
        
        self.balance -= amount
        
        return self.balance
            
    def get_balance(self):
            
        return self.balance

class Results:
    """Contain the results of a simulation"""
    
    def __init__(self, rolls_until_bankrupt, final_balance):
        self.rolls_until_bankrupt = rolls_until_bankrupt
        self.final_balance = final_balance
            
    def get_results(self):
            return rolls_until_bankrupt, final_balance

class Simulation:
    """Contain the simulation function and store the data of each simulation"""

    def __init__(self, config, account):
        self.config = config
        self.account = account
            
    def roll(self):
        """Simulate one 'dice roll' and return True if the roll was won by the
        user or False if the roll was lost"""
        
        # Pick a random number between 0 and 100 out to two decimal places.
        roll_value = random.randrange(0, 10000)/100
        
        if roll_value < self.config.get_roll_under_value():
            win = True
        else:
            win = False
                
        return win
    
    def increase_bet(self):
        self.current_bet += self.current_bet * self.config.get_loss_adder()
    
    def reset_bet(self):
        self.current_bet = self.config.get_base_bet()
            
    def lose_roll(self, account):
        #print("Roll lost")
        self.increase_bet()
            
    def win_roll(self, account):
        reward = self.current_bet * self.config.get_payout()
        account.add(reward)
        #print("Roll won, +=", reward, "New bal:", account.get_balance())
        self.reset_bet()
                
    def single_sim(self):
        rolls = 0
        self.reset_bet()
        sim_account = copy.copy(self.account)
        
        #print("Start Balance: ", sim_account.get_balance())

        while sim_account.get_balance() > self.current_bet:
            rolls += 1
            sim_account.subtract(self.current_bet)
            
            #print("Current bet:", self.current_bet)
            #print("Balance: ", sim_account.get_balance())
            
            if self.roll():
                    self.win_roll(sim_account)			
            else:
                    self.lose_roll(sim_account)
            #print("================================")
        #print("\nTotal rolls:", rolls)
        #print("Final balance:", sim_account.get_balance())
        #print("Final bet:", self.current_bet)
        return rolls	
    
    def print_progress(self, sim_num, iterations, progress_checks):
        if sim_num % (iterations / progress_checks) == 0:
            progress_percent = int((sim_num / iterations) * 100)
            print("[Progress] " + str(progress_percent) + "% complete")
            
    def run(self, progress_checks = 10):
        total_result = 0
        iterations = self.config.get_iterations()
        for sim_num in range(iterations):
            self.print_progress(sim_num, iterations, progress_checks)
            sim_result = self.single_sim()
            total_result += sim_result
            #print("Sim result:", sim_result)
        sim_average = total_result / iterations
        
        print("\n[Results] Average rolls until bankruptcy: " + str(sim_average))
        
        return sim_average
    
class Expirement:
    """Run multiple simulations and show the data"""
    def __init__(self, config, account):
        pass
		
		

class Tests:
    """Contain test functions to make sure the code runs properly"""
    
    def __init__(self):
        self.config = Configuration(base_bet=1, loss_adder=100, payout=2)
        self.account = Account(balance=400)
        self.simulation = Simulation(self.config, self.account)
            
    def run(self):
        """Call whichever tests are currently meant to be run"""
        #self.multiple_sims()
    
    def multiple_sims(self):
        """Run multiple simulations and print the average result"""
        self.simulation.run(50)
            
    def single_simulation(self):
        """Run a single simulation and print the total rolls"""
        print(self.simulation.single_sim())
            
    def roller(self):
        """Run a series of rolls and print the results of those rolls"""
        for _ in range(20):
            print(self.simulation.roll())
        
class Program:
    def __init__(self):
        self.config = Configuration(base_bet=1, payout=2, loss_adder=100)
        self.account = Account(balance= 200)
        self.sim = Simulation(self.config, self.account)
        
        self.gui = Gui(self.account, self.sim)
        
def main():     
    """Call the expirement function"""
    
    start_time = time.time()
    
    #test = Tests()
    #test.run()
    program = Program()
    
    
    print("\nTime taken: --- %s seconds ---" % (time.time() - start_time))

main()
