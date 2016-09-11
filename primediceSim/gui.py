from tkinter import *
from tkinter.ttk import *

import matplotlib
matplotlib.use("TkAgg")     # Allow matplotlib to work with Tkinter
# Import MUST come after matplotlib.use() is called!!
from matplotlib import pyplot as plt


class Gui:
    def __init__(self, simulation):
        """Display the inputs for the configuration values and their values"""

        self.sim = simulation   # A starting simulation with default values

        self.master = Tk()
        self.master.title("Primedice Simulator")

        self.balance_label, self.balance_input, self.balance_str = \
            self.make_balance_input()
        self.base_bet_label, self.base_bet_input, self.base_bet_str = \
            self.make_base_bet_input()
        self.payout_label, self.payout_input, self.payout_str = \
            self.make_payout_input()

        self.iterations_label, self.iterations_input, self.iterations_str = \
            self.make_iterations_input()
        self.loss_adder_label, self.loss_adder_input, self.loss_adder_str = \
            self.make_loss_adder_input()

        self.run_button = self.make_run_button()

        self.progress_label, self.progress_bar = self.make_progress_bar()

        self.graph_fig = self.make_graph()
        self.sim_results = None     # Placeholder for when results come in

        self.master.mainloop()

    def run_simulator(self):
        """Call the simulator to run with the settings given in the input
        boxes
        """

        self.update_settings()

        # Pass in the progress bar and the master so that the simulator can
        # update the progress bar and then refresh the screen when the progress
        # checkpoints are hit

        self.sim_results = self.sim.run(self.progress_bar, self.master)
        self.graph_results()

    def make_run_button(self):
        """Construct a button that runs the simulation"""

        run_button = Button(
            self.master, text="Run", command=self.run_simulator)
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
        """Construct and return an input field for the iterations value"""
        iterations_label = Label(self.master, text="Iterations:")
        iterations_label.grid(row=3, column=0)

        iterations_str = StringVar()
        iterations_str.set(str(self.sim.config.get_iterations()))

        iterations_input = Entry(self.master, textvariable=iterations_str)
        iterations_input.grid(row=3, column=1)

        return iterations_label, iterations_input, iterations_str

    def make_loss_adder_input(self):
        """Construct and return an input field for the loss adder value"""

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

        progress_bar = Progressbar(length=200)
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

    @staticmethod
    def make_graph():

        fig = plt.figure()
        fig.subplots_adjust(hspace=.35)

        return fig

    def graph_results(self):
        """Display the average simulation results on a graph"""
        # fig = plt.figure()
        # fig.subplots_adjust(hspace=.35)

        # median_x_values = [num for num in
        #                          range(len(results.get_meaningful_medians()))]
        # median_y_values = results.get_meaningful_medians()

        # print("Meaningful medians:", results.get_meaningful_medians())
        # print("Enumerated meaningful medians:",
        #       list(enumerate(results.get_meaningful_medians())))
        # print("Zipped enumerated meaningful medians:",
        #       list(zip(*enumerate(results.get_meaningful_medians()))))

        print("[Progress] Graphing results...")

        median_x_values, median_y_values = \
            zip(*enumerate(self.sim_results.get_median_balances()))
        median_graph = self.graph_fig.add_subplot(2, 1, 1)

        median_graph.plot(median_x_values, median_y_values)

        median_graph.set_title("Simulation Result Medians")
        median_graph.set_xlabel("Roll #")
        median_graph.set_ylabel("Median Balance")

        mean_graph = self.graph_fig.add_subplot(2, 1, 2)

        mean_values_to_graph = \
            self.sim_results.get_average_balances()
        mean_x_values, mean_y_values = \
            zip(*enumerate(mean_values_to_graph))
        mean_graph.plot(mean_x_values, mean_y_values)

        mean_graph.set_title("Simulation Result Means")
        mean_graph.set_xlabel("Roll #")
        mean_graph.set_ylabel("Mean Balance")

        plt.show()
