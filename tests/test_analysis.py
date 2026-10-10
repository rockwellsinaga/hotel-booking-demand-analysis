import unittest
from analysis import summarize


class AnalysisTests(unittest.TestCase):
    def test_filters_city_hotels_and_uses_distribution_channel(self):
        rows = [
            {"hotel": "Resort Hotel", "is_canceled": "1", "arrival_date_year": "2017", "customer_type": "Transient", "distribution_channel": "TA/TO", "is_repeated_guest": "0", "lead_time": "120"},
            {"hotel": "Resort Hotel", "is_canceled": "0", "arrival_date_year": "2017", "customer_type": "Contract", "distribution_channel": "Direct", "is_repeated_guest": "1", "lead_time": "5"},
            {"hotel": "City Hotel", "is_canceled": "1", "arrival_date_year": "2017", "customer_type": "Transient", "distribution_channel": "TA/TO", "is_repeated_guest": "0", "lead_time": "120"},
        ]
        result = summarize(rows)
        self.assertEqual(result["bookings"], 2)
        self.assertEqual(result["cancellation_rate"], 0.5)
        self.assertEqual(result["by_distribution_channel"]["TA/TO"]["canceled"], 1)
        self.assertEqual(result["by_distribution_channel"]["Direct"]["not_canceled"], 1)
        self.assertEqual(result["repeated_guest_by_distribution_channel"]["Direct"]["repeated_guest_rate"], 1)

    def test_empty_groups_never_divide_by_zero(self):
        result = summarize([])
        self.assertIsNone(result["cancellation_rate"])


if __name__ == "__main__":
    unittest.main()
