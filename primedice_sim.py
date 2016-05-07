import decimal
import random
import time
import copy
from tkinter import *
from tkinter.ttk import *


class Gui:
    def __init__(self, simulation):
        """Display the inputs for the configuration values and their values"""

        self.sim = simulation

        self.master = Tk()
        self.master.title("Primedice Simulator")

        self.balance_label, self.balance_input, self.balance_str, = self.make_balance_input()
        self.base_bet_label, self.base_bet_input, self.base_bet_str = self.make_base_bet_input()
        self.payout_label, self.payout_input, self.payout_str = self.make_payout_input()
        self.iterations_label, self.iterations_input, self.iterations_str = self.make_iterations_input()
        self.loss_adder_label, self.loss_adder_input, self.loss_adder_str = self.make_loss_adder_input()

        self.run_button = self.make_run_button()

        self.progress_label, self.progress_bar = self.make_progress_bar()

        self.master.mainloop()

    def run_simulator(self):
        """Call the simulator to run with the settings given in the input boxes"""
        
        self.update_settings()

        # Pass in the progress bar and the master so that the simulator can update
        # the progress bar and then refresh the screen when the progress checkpoints
        # are hit

        self.sim.run(self.progress_bar, self.master)    

    def make_run_button(self):
        """Construct a button that runs the simulation"""
        
        run_button = Button(self.master, text="Run", command=self.run_simulator)
        run_button.grid(row=6, column=1)

        return run_button

    def make_balance_input(self):
        """Construct an input field for the balance value"""
        
        balance_label = Label(self.master, text="Balance:")
        balance_label.grid(row=0, column=0)

        balance_str = StringVar()
        balance_str.set(str(self.sim.account.get_balance()))

        balance_input = Entry(self.master, textvariable=balance_str)
        balance_input.grid(row=0, column=1)

        return balance_label, balance_input, balance_str

    def make_base_bet_input(self):
        """Construct an input field for the base bet value"""
        
        base_bet_label = Label(self.master, text="Base bet:")
        base_bet_label.grid(row=1, column=0)

        base_bet_str = StringVar()
        base_bet_str.set(str(self.sim.config.get_base_bet()))

        base_bet_input = Entry(self.master, textvariable=base_bet_str)
        base_bet_input.grid(row=1, column=1)

        return base_bet_label, base_bet_input, base_bet_str

    def make_payout_input(self):
        """Construct an input field for the payout value"""
        
        payout_label = Label(self.master, text="Payout:")
        payout_label.grid(row=2, column=0)

        payout_str = StringVar()
        payout_str.set(str(self.sim.config.get_payout()))

        payout_input = Entry(self.master, textvariable=payout_str)
        payout_input.grid(row=2, column=1)

        return payout_label, payout_input, payout_str

    def make_iterations_input(self):
        """Construct an input field for the iterations value"""
        iterations_label = Label(self.master, text="Iterations:")
        iterations_label.grid(row=3, column=0)

        iterations_str = StringVar()
        iterations_str.set(str(self.sim.config.get_iterations()))

        iterations_input = Entry(self.master, textvariable=iterations_str)
        iterations_input.grid(row=3, column=1)

        return iterations_label, iterations_input, iterations_str

    def make_loss_adder_input(self):
        """Construct an input field for the loss adder value"""

        loss_adder_label = Label(self.master, text="Loss Adder:")
        loss_adder_label.grid(row=4, column=0)

        loss_adder_str = StringVar()
        loss_adder_str.set(str(self.sim.config.get_loss_adder()))

        loss_adder_input = Entry(self.master, textvariable=loss_adder_str)
        loss_adder_input.grid(row=4, column=1)

        return loss_adder_label, loss_adder_input, loss_adder_str

    def make_progress_bar(self):
        """Make a bar to displays the progress of a task"""
        progress_label = Label(self.master, text="Progress:")
        progress_label.grid(row=7, column=0)

        progress_bar = Progressbar(length = 200)
        progress_bar.grid(row=7, column=1)

        return progress_label, progress_bar

    def update_settings(self):
        """Pull all of the values from the input fields and use them
        to update the appropriate value"""
        
        self.sim.account.set_balance(int(self.balance_str.get()))

        self.sim.config.set_base_bet(int(self.base_bet_str.get()))
        self.sim.config.set_payout(float(self.payout_str.get()))
        self.sim.config.set_iterations(int(self.iterations_str.get()))
        self.sim.config.set_loss_adder(int(self.loss_adder_str.get()))

class Configuration:
    """Contain all of the configurations of the different options that the primedice
    auto-better provides.
    """
    
    def __init__(self, base_bet, payout, iterations=100, loss_adder=0):
        """ These are the different settings that can be given to the auto-better.
        All of the values should be given as they are on the primedice screen. 
        payout - float multiplier between 1.01202 and 9900
        loss_adder_percent - percent given as integer between 0 and 100.
        """
        self.base_bet = base_bet
  
        self.payout = payout 

        self.loss_adder = loss_adder    # Turn the user-given percent into a decimal
        self.loss_adder_percent = self.loss_adder / 100 

        self.win_chance = self.calc_win_chance(payout)
        self.roll_under_value = self.win_chance
        self.iterations = iterations
    
    def calc_win_chance(self, payout):
        """Find the win chance that primedice will use with a given win payout."""
        
        self.check_valid_payout(payout)

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
        """Ensure that the given payout is allowed by the site.
        If it is not, print a [WARNING] message and continue."""
        
        # Primedice enforces a minimum and maximum value for the payout to avoid the
        # Situation of having an absurdly high payout or win chance. The minimum and
        # maximum allowed values are given by the primedice website when an invalid
        # value is entered
        
        payout_minimum = 1.01202
        payout_maximum = 9900
        
        if payout_minimum <= payout <= payout_maximum:
            valid = True
        else:
            print("[WARNING] Payout value entered was not within the range allowed by PrimeDice")
            valid = False
                
        return valid

    def set_base_bet(self, new_val):
        """Change the base_bet value to be the given input"""
        self.base_bet = new_val

    def set_payout(self, new_val):
        """Change the payout value to be the given input"""
        self.payout = new_val

    def set_iterations(self, new_val):
        """Change the iterations value to be the given input"""
        self.iterations = new_val

    def set_loss_adder(self, new_val):
        """Change the loss adder value to be the given input, and update
        the loss adder percent value as well"""
        self.loss_adder = new_val  # Turn the user-given percent into a decimal
        self.loss_adder_percent = self.loss_adder / 100 
    
    def get_base_bet(self):
        """Return the current base bet"""
        return self.base_bet
            
    def get_loss_adder(self):
        """Return the current loss adder"""
        return self.loss_adder

    def get_loss_adder_percent(self):
        """Return the curent loss adder as a percent"""
        return self.loss_adder_percent
            
    def get_payout(self):
        """Return the current payout"""
        return self.payout

    def get_iterations(self):
        """Return the current iterations value"""
        return self.iterations
            
    def get_roll_under_value(self):
        """Return the current roll under value"""
        return self.roll_under_value

class Account:
    """Contain the user's primedice account stats"""
    
    def __init__(self, balance):
        self.balance = balance
    
    def set_balance(self, new_balance):
        """Change the balance to be the given value"""
        self.balance = new_balance

    def add(self, new_val):
        """Add to the current account balance"""
        self.balance += new_val
        
        return self.balance
            
    def subtract(self, new_val):
        """Subtract from the current account balance"""
        self.balance -= new_val
        
        return self.balance
            
    def get_balance(self):
        """Return the current balance"""
        
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
        """Increase the current bet by the amount specified by the loss adder amount.""" 
        self.current_bet += self.current_bet * self.config.get_loss_adder_percent()
    
    def reset_bet(self):
        """Change the current best back to the bet value from the configuration."""
        self.current_bet = self.config.get_base_bet()
            
    def lose_roll(self, account):
        """Simulate a lost roll"""

        self.increase_bet()
            
    def win_roll(self, account):
        """Simulate a won roll"""

        reward = self.current_bet * self.config.get_payout()
        account.add(reward)
        self.reset_bet()
                
    def single_sim(self):
        """Simulate a sinle round of betting until bankruptcy.
        Return the amount of rolls before then.
        """
        
        rolls = 0
        self.reset_bet()
        sim_account = copy.copy(self.account)

        while sim_account.get_balance() > self.current_bet:
            rolls += 1
            sim_account.subtract(self.current_bet)
            
            if self.roll():
                    self.win_roll(sim_account)  
            else:
                    self.lose_roll(sim_account)

        return rolls    
    
    def print_progress(self, sim_num, iterations, progress_checks, screen):
        """Print the current progress of the simulation.
        progress_checks is just the amount of progress checks 
        that the user wants to be printed during each simulation.
        """
        progress_ticks = 100 / progress_checks

        if sim_num % (iterations / progress_checks) == 0:
            progress_percent = int((sim_num / iterations) * 100)
            self.progress_bar.step(progress_ticks)
            screen.update()

    def verify_progress_checks(self, progress_checks, iterations):
        """Check if the progress_checks value is greater than iterations, and fix it if so"""

        # The number of progress checks must be less than the number of iterations in order
        # For the progress bar to work properly.

        if progress_checks > iterations:
            # If this case does arise, just set the progress checks to be the same as the
            # number of iterations, simplifying calculations
            progress_checks = iterations

        return progress_checks

    def print_settings(self):
        """Print the settings that are being accessed by the simulation"""
        
        print("\n[MESSAGE] Running new simulation")
        print("Balance:", self.account.get_balance(), "\n")
        print("Base bet:", self.config.get_base_bet())
        print("Payout:", self.config.get_payout())
        print("Iterations:", self.config.get_iterations())
        print("Loss adder:", self.config.get_loss_adder())
            
    def run(self, progress_bar, screen, progress_checks = 50):
        """Run several simulations and return the average of them all"""

        progress_checks = self.verify_progress_checks(progress_checks, self.config.get_iterations())

        # Takes the progress bar and the screen in order to update
        # the progress bar and refresh the screen when necessary

        self.print_settings()
        self.progress_bar = progress_bar
        total_result = 0
        iterations = self.config.get_iterations()
        for sim_num in range(iterations):
            self.print_progress(sim_num, iterations, progress_checks, screen)
            sim_result = self.single_sim()
            total_result += sim_result
            #print("Sim result:", sim_result)
        sim_average = total_result / iterations
        
        print("[Results] Average rolls until bankruptcy: " + str(sim_average))
        print("\n======================================================")
        
        return sim_average

class Expirement:
    """Run multiple simulations and show the data"""
    
    def __init__(self, config, account):
        pass
        
class Program:
    """Contain all of the elements of the program"""
    
    def __init__(self):
        self.config = Configuration(base_bet=1, payout=2, loss_adder=100)
        self.account = Account(balance= 200)
        self.sim = Simulation(self.config, self.account)
        self.gui = Gui(self.sim)
        
def main():     
    """Call the expirement function"""
    
    start_time = time.time()
    
    #test = Tests()
    #test.run()
    program = Program()
    
    
    print("\nTime taken: --- %s seconds ---" % (time.time() - start_time))

if __name__ == "__main__":
    main()
