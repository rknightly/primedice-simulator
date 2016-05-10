from primedice_sim import *

config = Configuration(base_bet=1, payout=2, loss_adder=100)
account = Account(balance=200)
sim = Simulation(config, account)
gui = None


def make_gui():
    """Create the gui, setting the program into motion"""
    global gui
    gui = Gui(sim)     # Expected result: screen appear with input fields and labels


def main():
    """Run the tests"""
    make_gui()

if __name__ == "__main__":
    main()
