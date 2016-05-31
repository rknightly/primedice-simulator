from unittest import TestCase

class TestAdd(TestCase):
    """Ensure that the balance is appropriately added to"""

    def test_positive(self):
        from primedice_sim import Account
        account = Account(balance=20)
        account.add(5)
        self.assertEqual(account.get_balance(), 25,
                         "The balance was not appropriately added to when a "
                         "positive integer of 5 was added")

    def test_negative(self):
        from primedice_sim import Account
        account = Account(balance=20)
        account.add(-5)
        self.assertEqual(account.get_balance(), 15,
                         "The balance was not appropriately added to when a "
                         "negative integer of -5 was added")

    def test_zero(self):
        from primedice_sim import Account
        account = Account(balance=20)
        account.add(0)
        self.assertEqual(account.get_balance(), 20,
                         "The balance was did not remain the same when 0 was"
                         " added")

    def test_float(self):
        from primedice_sim import Account
        account = Account(balance=20)
        account.add(5.5)
        self.assertEqual(account.get_balance(), 25,
                         "The balance was not appropriately added to when a "
                         "float of 5.5 was added")


class TestSubtract(TestCase):
    """Ensure that the balance is appropriately subtracted from"""

    def test_positive(self):
        from primedice_sim import Account
        account = Account(balance=20)
        account.subtract(5)
        self.assertEqual(account.get_balance(), 15,
                         "The balance was not appropriately subtracted from"
                         " when a positive integer of 5 was subtracted")

    def test_negative(self):
        from primedice_sim import Account
        account = Account(balance=20)
        account.subtract(-5)
        self.assertEqual(account.get_balance(), 25,
                         "The balance was not appropriately subtracted from"
                         " to when a negative integer of -5 was subtracted")

    def test_zero(self):
        from primedice_sim import Account
        account = Account(balance=20)
        account.subtract(0)
        self.assertEqual(account.get_balance(), 20,
                         "The balance was did not remain the same when 0 was"
                         " subtracted")

    def test_float(self):
        from primedice_sim import Account
        account = Account(balance=20)
        account.subtract(5.5)
        self.assertEqual(account.get_balance(), 15,
                         "The balance was not appropriately subtracted from"
                         " when a float of 5.5 was subtracted")
