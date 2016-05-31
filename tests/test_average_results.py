from unittest import TestCase


class TestFindAverageBal(TestCase):
    """Ensure that the average balances are appropriately calculated"""

    def test_single_result(self):
        from primedice_sim import Results, AverageResults

        sample_result = Results([5, 6, 7, 5, 7])
        average_result = AverageResults([sample_result])
        self.assertEqual(average_result.overall_average_balance, 6,
                         "Average balance was incorrectly calculated over one"
                         " result")

    def test_multiple_results(self):
        from primedice_sim import Results, AverageResults

        sample_results = [Results([5, 6, 7, 9, -2]),
                          Results([2, 6, 8, 8]),
                          Results([0, 7, 14])]
        average_result = AverageResults(sample_results)
        self.assertEqual(average_result.overall_average_balance, 6,
                         "Average balance was incorrectly calculated over"
                         " multiple results")

    def test_float_results(self):
        from primedice_sim import Results, AverageResults

        sample_results = [Results([3, 5, 4, 1, 7]),
                          Results([5, 5, 10, 1])]

        average_result = AverageResults(sample_results)
        self.assertEqual(average_result.overall_average_balance, 4,
                         "Average balance was incorrectly calculated over"
                         " multiple results with a float average balance")


class TestFindAverageRollsUntilBankrupt(TestCase):
    """Ensure that the average rolls until bankrupt is found and returned
    properly
    """

    def test_single_result(self):
        from primedice_sim import Results, AverageResults

        sample_result = Results([5, 6, 7, 5, 7])
        average_result = AverageResults([sample_result])
        self.assertEqual(average_result.find_average_rolls_until_bankrupt(), 4,
                         "Average rolls until bankrupt was incorrectly"
                         " calculated over one result with positive integers")

    def test_multiple_results(self):
        from primedice_sim import Results, AverageResults

        sample_results = [Results([5, 6, 7, 9, -2]),
                          Results([2, 6, 8, 8]),
                          Results([0, 7, 14])]
        average_result = AverageResults(sample_results)
        self.assertEqual(average_result.find_average_rolls_until_bankrupt(), 3,
                         "Average rolls until bankrupt was incorrectly"
                         " calculated over multiple results")

    def test_float_average(self):
        from primedice_sim import Results, AverageResults

        sample_results = [Results([3, 5, 4, 1, 7]),
                          Results([5, 5, 10, 1])]

        average_result = AverageResults(sample_results)
        self.assertEqual(average_result.find_average_rolls_until_bankrupt(), 3,
                         "Average rolls until bankrupt was incorrectly"
                         " calculated over multiple results with a float"
                         " average rolls value")


class TestFindAverageBalances(TestCase):
    """Ensure that the sequence of average balances is properly found"""

    def test_single_result(self):
        from primedice_sim import Results, AverageResults

        sample_result = Results([5, 6, 7, 5, 7])
        average_result = AverageResults([sample_result])
        self.assertEqual(average_result.get_average_balances(),
                         [5, 6, 7, 5, 7],
                         "Average balances were incorrectly calculated over "
                         "one result with integers")

    def test_multiple_results(self):
        from primedice_sim import Results, AverageResults

        sample_results = [Results([5, 8, 10, 9, 12]),
                          Results([4, 6, 5, 12]),
                          Results([0, 7, 15])]
        average_result = AverageResults(sample_results)
        self.assertEqual(average_result.get_average_balances(),
                         [3, 7, 10, 7, 4],
                         "Average balances were incorrectly calculated over"
                         "multiple results with integers")

    def test_float_average(self):
        from primedice_sim import Results, AverageResults

        sample_results = [Results([3, 5, 4,  1, 7]),
                          Results([4, 5, 10, 1])]

        average_result = AverageResults(sample_results)
        self.assertEqual(average_result.find_average_balances(),
                         [3, 5, 7, 1, 3],
                         "Average balances were incorrectly calculated over"
                         " multiple results with float average values")


class TestFindMedianBalances(TestCase):
    """Ensure that the median balances are correctly calculated"""

    def test_single_result(self):
        from primedice_sim import Results, AverageResults

        sample_result = Results([5, 6, 7, 5, 7])
        average_result = AverageResults([sample_result])
        self.assertEqual(average_result.get_median_balances(),
                         [5, 6, 7, 5, 7],
                         "Median balances were incorrectly calculated over "
                         "one result with integers")

    def test_multiple_results(self):
        from primedice_sim import Results, AverageResults

        sample_results = [Results([5, 8, 10,  9, 12]),
                          Results([4, 6,  5, 12]),
                          Results([0, 7, 15])]
        average_result = AverageResults(sample_results)
        self.assertEqual(average_result.get_median_balances(),
                         [4, 7, 10, 9, 0],
                         "Median balances were incorrectly calculated over"
                         "multiple results with integers")

    def test_float_median(self):
        from primedice_sim import Results, AverageResults

        sample_results = [Results([3, 5,  4, 1, 7]),
                          Results([4, 5, 10, 1])]

        average_result = AverageResults(sample_results)
        self.assertEqual(average_result.find_median_balances(),
                         [3, 5, 7, 1, 3],
                         "Median balances were incorrectly calculated over"
                         " multiple results with float average values")

    def test_zeroes(self):
        from primedice_sim import Results, AverageResults

        sample_results = [Results([5, 8, 10, 9, 12, 14, 16, 14, 13, 10, 6]),
                          Results([4, 6, 5, 12]),
                          Results([0, 7, 15])]
        average_result = AverageResults(sample_results)
        self.assertEqual(average_result.get_median_balances(),
                         [4, 7, 10, 9, 0],
                         "Median balances were incorrectly calculated when"
                         "data contained several ending medians of 0")
