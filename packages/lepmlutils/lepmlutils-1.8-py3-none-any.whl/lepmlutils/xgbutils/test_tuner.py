import unittest
import os
import pandas as pd
from .tuner import Tuner

class TestTuner(unittest.TestCase):
    def setUp(self):
        self.dirname = os.path.dirname(__file__)
        self.dataset = pd.read_csv(self.dirname + "/resources/train.csv")
        
        self.features = [ 
            "Age", 
            "SibSp", 
            "Parch", 
            "Fare", 
        ]
        self.target = [
            "Survived",
        ]

    def test_partitions_correctly(self):
        candidates = {
            'max_depth': range(4, 40, 10),
        }
        set_params = {
            "n_estimators": 40,
        }

        tuner = Tuner()
        results = tuner.tune(
            candidates,
            set_params,
            self.dataset,
            self.features,
            self.target,
            3,
        )

        self.assertEqual(4, len(results))
        for params in results:
            self.assertEqual(params["params"]["n_estimators"], 40)
        
        self.assertEqual(results[0]["params"]["max_depth"], 4)
        self.assertEqual(results[1]["params"]["max_depth"], 24)
        self.assertEqual(results[2]["params"]["max_depth"], 34)
        self.assertEqual(results[3]["params"]["max_depth"], 14)

        self.assertGreaterEqual(results[0]["test_score"], results[1]["test_score"])
        self.assertGreaterEqual(results[1]["test_score"], results[2]["test_score"])
        self.assertGreaterEqual(results[2]["test_score"], results[3]["test_score"])
    
    def test_runs_tunes_correctly(self):
        candidates = {
            'max_depth': range(2, 6),
            'n_estimators': range(10, 60, 10),
        }
        set_params = {
            # "n_estimators": 40,
        }

        tuner = Tuner()
        results = tuner.tune(
            candidates,
            set_params,
            self.dataset,
            self.features,
            self.target,
            3,
        )

        self.assertEqual(20, len(results))

