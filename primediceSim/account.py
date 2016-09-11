class Account:
    """Contain the user's primedice account stats"""

    def __init__(self, balance):
        self.balance = int(balance)

    def set_balance(self, new_balance):
        """Change the balance to be the given value"""
        self.balance = int(new_balance)

    def add(self, amount_to_add):
        """Add to the current account balance"""

        # The balance should remain an integer, regardless of the amount added
        # to it
        self.balance += int(amount_to_add)

        return self.balance

    def subtract(self, new_val):
        """Subtract from the current account balance"""
        self.balance -= int(new_val)

        return self.balance

    def get_balance(self):
        """Return the current balance"""

        return int(self.balance)
