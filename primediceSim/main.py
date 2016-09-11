#!/usr/bin/env python3

import time

from primediceSim.gui import Gui
from primediceSim.configuration import Configuration
from primediceSim.account import Account
from primediceSim.simulation import Simulation


class Program:
    """Contain all of the elements of the program"""

    def __init__(self):
        self.config = Configuration(base_bet=1, payout=2, loss_adder=100)
        self.account = Account(balance=200)
        self.sim = Simulation(self.config, self.account)

        # Hold the gui as nothing until the program is called to run
        self.gui = None

    def run(self):
        """Create the gui, setting the program into motion"""

        self.gui = Gui(self.sim)


def main():
    """Call the experiment function"""

    start_time = time.time()

    program = Program()
    program.run()

    time_taken = str((time.time() - start_time))[:5]
    print("\n[Time] Total run time: --- %s seconds ---" % time_taken)

if __name__ == "__main__":
    main()
