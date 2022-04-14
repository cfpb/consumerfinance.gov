"""Handles rendering dynamic content in a survey results page.

A ResultsContent object holds content that may be output on a
results page based on the grade and scores for each part.
"""

import csv
from os.path import dirname
from typing import Dict


def _results_data_row(row: Dict[str, str]):
    """
    Transform the keys of each CSV row. If the CSV headers change,
    this will make a single place to fix it.
    """
    return {
        "k": row["Key"],
        "v": row["Content"],
    }


class ResultsContent:
    """Helps supply result page template with content"""

    def __init__(self, store: Dict[str, str], survey_key: str):
        """Use ResultsContent.factory() instead"""
        self.store = store
        self.key = survey_key

    def get(self, key: str):
        assert key in self.store
        return self.store[key]

    def building_blocks(self):
        """Get the names/intros for the 3 building blocks"""
        bbs = []
        for i in range(3):
            bbs.append(
                {
                    "idx": i,
                    "title": self.get(f"BB{i}"),
                    "intro": self.get(f"BBIntro{i}"),
                }
            )
        return bbs

    @staticmethod
    def level_from_position(pos_idx: int):
        """
        Map 6 car positions to 3 progress levels

        Given a car position int from 0-5, return a progress level 0-2
        """
        return [0, 0, 1, 1, 1, 2][pos_idx]

    def find_overall_progress(self, adjusted_score: float):
        """
        Given an adjusted score for the entire survey, return data
        useful for displaying the level of the user's progress and the
        position of the car.
        """
        pos_idx = self._score_idx(f"{self.key} Overall", adjusted_score)
        level_idx = self.level_from_position(pos_idx)
        heading, msg = self.get(f"{self.key} Overall{level_idx}").split("|")

        return {
            "level_idx": level_idx,
            "position_idx": pos_idx,
            "heading_html": heading,
            "msg_html": msg,
        }

    def find_bb_progress(self, part: int, score: float):
        """
        Given a part-level score, return data useful for displaying the
        level of the user's progress and the position of the car.
        """
        pos_idx = self._score_idx(f"{self.key} BB{part}", score)
        level_idx = self.level_from_position(pos_idx)
        word = ["Planning", "Habits", "Knowledge"][part]

        return {
            "level_idx": level_idx,
            "position_idx": pos_idx,
            "msg_html": self.get(f"{self.key} {word}{level_idx}"),
        }

    def _score_idx(self, key: str, score: float):
        values_str = self.get(key)
        if values_str is None:
            raise LookupError
        idx = 0
        minima = (int(x) for x in values_str.split(" "))
        for i, x in enumerate(minima):
            if score < x:
                break
            idx = i
        return idx

    @classmethod
    def factory(cls, survey_key: str):
        """Create a ResultsContent object for a particular survey"""
        store: Dict[str, str] = {}
        path = f"{dirname(__file__)}/survey-data/results-content.csv"
        with open(path, encoding="utf-8") as csv_file:
            reader = csv.DictReader(csv_file)
            for row in (_results_data_row(r) for r in reader):
                store[row["k"]] = row["v"]

        return cls(store, survey_key)
