from unittest import TestCase


class TestFindAverageBal(TestCase):
    """Ensure that the average balances are appropriately calculated"""

    def test_single_result(self):
        from primedice_sim import Results, AverageResults

        sample_result = Results([5, 6, 7, 5, 2])
        average_result = AverageResults([sample_result])
        self.assertEqual(average_result.overall_average_balance, 5,
                         "Average result was balance was incorrectly"
                         " calculated over one result with positive integers")

    def test_multiple_results(self):
        from primedice_sim import Results, AverageResults

        sample_results = [Results([5, 6, 7, 9, -2]), Results([2, 6, 8, 8]),
                          Results([0, 7, 14])]
        average_result = AverageResults(sample_results)
        self.assertEqual(average_result.overall_average_balance, 6,
                         "Average result was balance was incorrectly"
                         " calculated over multiple results with positive"
                         " integers")
