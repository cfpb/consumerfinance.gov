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

    def __init__(self, store: Dict[str, str], survey_key: str):
        self.store = store
        self.key = survey_key

    def get(self, key: str):
        assert key in self.store
        return self.store[key]

    def building_blocks(self):
        bbs = []
        for i in range(3):
            bbs.append({
                'idx': i,
                'title': self.get(f'BB{i}'),
                'intro': self.get(f'BBIntro{i}'),
            })
        return bbs

    def level_from_position(self, pos_idx: int):
        """Map 6 car positions to 3 progress levels"""
        return [0, 0, 1, 1, 1, 2][pos_idx]

    def find_overall_progress(self, score: float):
        # Six positions map to 3 progress levels
        pos_idx = self._score_idx(f'{self.key} Overall', score)
        level_idx = self.level_from_position(pos_idx)
        heading, msg = self.get(f'{self.key} Overall{level_idx}').split('|')

        return {
            'level_idx': level_idx,
            'position_idx': pos_idx,
            'heading_html': heading,
            'msg_html': msg,
        }

    def find_bb_progress(self, part: int, score: float):
        # Six positions map to 3 progress levels
        pos_idx = self._score_idx(f'{self.key} BB{part}', score)
        level_idx = self.level_from_position(pos_idx)
        word = ['Planning', 'Habits', 'Knowledge'][part]

        return {
            'level_idx': level_idx,
            'position_idx': pos_idx,
            'msg_html': self.get(f'{self.key} {word}{level_idx}'),
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
    def factory(survey_key: str):
        store: Dict[str, str] = {}
        path = f'{dirname(__file__)}/survey-data/results-content.csv'
        with open(path, encoding='utf-8') as csv_file:
            reader = csv.DictReader(csv_file)
            for row in (_results_data_row(row) for row in reader):
                store[row['k']] = row['v']

        return ResultsContent(store, survey_key)
