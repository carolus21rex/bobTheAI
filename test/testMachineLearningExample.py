import math
import unittest
import app.machineLearningExample as MLE


class TestMachineLearningProgram(unittest.TestCase):

    def test_clamp_function(self):
        # Test the clamp function with values within and outside the range
        self.assertEqual(MLE.clamp(5, 1, 10), 5, "Clamp should return the value within the range.")
        self.assertEqual(MLE.clamp(15, 1, 10), 10, "Clamp should return the maximum value.")
        self.assertEqual(MLE.clamp(-5, 1, 10), 1, "Clamp should return the minimum value.")

    def test_correctRange_function(self):
        # Create an instance of the Intelligence class
        intelligence = MLE.Intelligence()

        # Set initial thresholds outside the range
        intelligence.threshold_Score1 = -5
        intelligence.threshold_Score2 = 15000

        # Call correctRange to adjust thresholds
        MLE.correctRange(intelligence)

        # Assert that thresholds are now within the range
        self.assertTrue(MLE.data_min <= intelligence.threshold_Score1 <= MLE.data_max,
                        "Threshold_Score1 is not within the range.")
        self.assertTrue(MLE.data_min <= intelligence.threshold_Score2 <= MLE.data_max,
                        "Threshold_Score2 is not within the range.")

    def test_intelligence_str_method(self):
        # Create an instance of the Intelligence class
        intelligence = MLE.Intelligence()

        # Test the __str__ method
        expected_str = "Threshold Score1: 0\nThreshold Score2: 0"
        self.assertEqual(str(intelligence), expected_str, f"The __str__ method should return "
                                                          f"the correct string, {expected_str}.")

    def test_full_program(self):
        intelligence = MLE.Intelligence()
        MLE.trainModel(intelligence)

        standardDeviation1 = MLE.threshold1/math.sqrt(MLE.count_test_data)
        standardDeviation2 = MLE.threshold2/math.sqrt(MLE.count_test_data)

        # 99.7% of the time the returned value will fall within 3 standard deviations.
        expectedRange1 = 3 * standardDeviation1
        expectedRange2 = 3 * standardDeviation2

        assert (MLE.threshold1 - expectedRange1 <= intelligence.threshold_Score1
                <= MLE.threshold1 + expectedRange1), \
            f"Threshold_Score1 is not within the expected range."
        assert (MLE.threshold1 - expectedRange2 <= intelligence.threshold_Score2
                <= MLE.threshold2 + expectedRange2), \
            f"Threshold_Score2 is not within the expected range."


if __name__ == '__main__':
    unittest.main()
