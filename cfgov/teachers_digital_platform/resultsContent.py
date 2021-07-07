import csv
from os.path import dirname
from typing import Dict


def _results_data_row(row: Dict[str, str]):
    return {
        'k': row['Key'],
        'v': row['Content'],
    }


class ResultsContent:
    """Helps supply result page template with content"""

    def __init__(self, store: Dict[str, str], assessment_key: str):
        self.store = store
        self.assessment_key = assessment_key

    def get(self, key: str):
        return self.store[key] if key in self.store else None

    def building_blocks(self):
        bbs = []
        for i in range(3):
            bbs.append({
                'idx': i,
                'title': self.get(f'BB{i}'),
                'intro': self.get(f'BBIntro{i}'),
            })
        return bbs

    def find_level(self, score: float):
        idx = self._score_idx(f'{self.assessment_key},Levels', score)
        return {
            'idx': idx,
            'title': self.get(f'Level{idx}'),
        }

    def find_area(self, part: int, score: float):
        idx = self._score_idx(f'{self.assessment_key},BB{part}', score)
        return {
            'idx': idx,
            'title': self.get(f'Area{idx}'),
            'desc': self.get(f'AreaDesc{idx}'),
        }

    def _score_idx(self, key: str, score: float):
        values_str = self.get(key)
        if values_str is None:
            raise LookupError
        idx = 0
        minima = (int(x) for x in values_str.split(' '))
        for i, x in enumerate(minima):
            if score < x:
                break
            idx = i
        return idx

    @staticmethod
    def factory(assessment_key: str):
        store: Dict[str, str] = {}
        path = f'{dirname(__file__)}/assessment-data/results-content.csv'
        with open(path, encoding='utf-8') as csv_file:
            reader = csv.DictReader(csv_file)
            for row in (_results_data_row(row) for row in reader):
                store[row['k']] = row['v']

        return ResultsContent(store, assessment_key)
