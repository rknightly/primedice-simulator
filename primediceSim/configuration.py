import decimal


class Configuration:
    """Contain all of the configurations of the different options that the
    primedice auto-better provides.
    """

    def __init__(self, base_bet, payout, iterations=100, loss_adder=100):
        """These are the different settings that can be given to the auto-better.
        All of the values should be given as they are on the primedice screen.
        payout - float multiplier between 1.01202 and 9900
        loss_adder_percent - percent given as integer between 0 and 100.
        """
        self.base_bet = base_bet

        self.payout = payout

        self.loss_adder = loss_adder

        # Turn the user-given percent into a decimal
        self.loss_adder_decimal = self.loss_adder / 100
        self.roll_under_value = self.calc_roll_under_value()
        self.iterations = iterations

    def calc_roll_under_value(self):
        """Find the win chance that primedice will use with a given win payout.
        """

        self.check_valid_payout()

        # The equation used was found from taking data points from the
        # primedice website and calculating the line of best fit. It is a power
        # function, following the form f(x) = kx^n where x is the win payout
        # and f(x) is the win chance that primedice allows. Apparently, they
        # have chosen to make k = 98.998 and n = .99999 This way, with a high
        # win payout, the chance of winning is low. At the same time, with a
        # low win payout, the chance of winning is much higher.
        decimal_places = 2
        win_chance = decimal.Decimal(98.998 * (self.payout ** -.99999))
        rounded_win_chance = round(win_chance, decimal_places)

        return rounded_win_chance

    def check_valid_payout(self):
        """Ensure that the given payout is allowed by the site.
        If it is not, print a [WARNING] message and continue.
        """

        # Primedice enforces a minimum and maximum value for the payout to
        # avoid the Situation of having an absurdly high payout or win chance.
        # The minimum and maximum allowed values are given by the primedice
        # website when an invalid value is entered

        payout_minimum = 1.01202
        payout_maximum = 9900

        if payout_minimum <= self.payout <= payout_maximum:
            valid = True
        else:
            print("[WARNING] Payout value entered was not within the range"
                  " allowed by PrimeDice")
            valid = False
            print(self.payout)

        return valid

    def set_base_bet(self, new_val):
        """Change the base_bet value to be the given input"""
        self.base_bet = new_val

    def set_payout(self, new_val):
        """Change the payout value to be the given input"""
        self.payout = new_val
        # The roll under value changes with the payout
        self.roll_under_value = self.calc_roll_under_value()

    def set_iterations(self, new_val):
        """Change the iterations value to be the given input"""
        self.iterations = new_val

    def set_loss_adder(self, new_val):
        """Change the loss adder value to be the given input, and update
        the loss adder percent value as well"""
        self.loss_adder = new_val

        # Turn the user-given percent into a decimal
        self.loss_adder_decimal = self.loss_adder / 100

    def get_base_bet(self):
        """Return the current base bet"""
        return self.base_bet

    def get_loss_adder(self):
        """Return the current loss adder as a percent"""
        return self.loss_adder

    def get_loss_adder_decimal(self):
        """Return the current loss adder as a percent"""
        return self.loss_adder_decimal

    def get_payout(self):
        """Return the current payout"""
        return self.payout

    def get_iterations(self):
        """Return the current iterations value"""
        return self.iterations

    def get_roll_under_value(self):
        """Return the current roll under value"""
        return self.roll_under_value
