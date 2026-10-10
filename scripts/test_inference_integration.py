import unittest

from ml.pipeline.inference import analyze_workload


class TestInferenceIntegration(unittest.TestCase):
    def setUp(self):
        self.features = {
            "active_tasks": 3,
            "cpu_capacity": 1.0,
            "memory_capacity": 1.0,
            "avg_priority": 1.0,
            "max_priority": 2.0,
            "elapsed_minutes": 10.0,
            "trace_hour": 12,
            "day_of_trace": 1,
            "is_peak_period": 0,
        }

    def test_prediction_without_actual_measurements(self):
        result = analyze_workload(self.features)
        self.assertEqual(result["status"], "prediction_completed")
        self.assertIsNone(result["resources"]["cpu"]["actual"])
        self.assertEqual(result["waste_analysis"]["status"], "not_available")
        self.assertEqual(result["power"]["status"], "not_predicted")

    def test_end_to_end_analysis_with_actual_measurements(self):
        inputs = {
            **self.features,
            "actual_cpu": 0.8,
            "actual_memory": 0.7,
        }
        result = analyze_workload(inputs)

        self.assertEqual(result["status"], "prediction_completed")
        self.assertEqual(
            result["waste_analysis"]["status"],
            "heuristic_analysis_completed",
        )
        self.assertIn("score", result["waste_analysis"]["waste_score"])
        self.assertEqual(
            result["root_cause_analysis"]["status"],
            "root_cause_hypotheses_generated",
        )
        self.assertEqual(
            result["recommendations"]["integration"]["status"],
            "phase6_phase7_integration_completed",
        )
        self.assertEqual(result["power"]["status"], "not_predicted")
        self.assertIn("status", result["savings_estimate"])


if __name__ == "__main__":
    unittest.main()
