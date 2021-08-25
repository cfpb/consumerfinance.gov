from django.test import TestCase

from ..resultsContent import ResultsContent, _results_data_row


class ResultsContentTest(TestCase):

    def setUp(self):
        self.ResultsContent = ''

    def test_results_data_row(self):
        row = {'Key': 'test_key1', 'Content': 'test_value1'}
        test_array = _results_data_row(row)
        self.assertEqual(test_array, {'k': 'test_key1', 'v': 'test_value1'})

    def test_factory_elementary_school(self):
        rc = ResultsContent.factory('3-5')
        self.assertIsInstance(rc, ResultsContent)
        self.assertEqual(rc.store['BB0'], 'Planning and self-control')
        self.assertEqual(rc.key, '3-5')

    def test_factory_middle_school(self):
        rc = ResultsContent.factory('6-8')
        self.assertIsInstance(rc, ResultsContent)
        self.assertEqual(rc.store['BB0'], 'Planning and self-control')
        self.assertEqual(rc.key, '6-8')

    def test_factory_high_school(self):
        rc = ResultsContent.factory('9-12')
        self.assertIsInstance(rc, ResultsContent)
        self.assertEqual(rc.store['BB0'], 'Planning and self-control')
        self.assertEqual(rc.key, '9-12')

    def test_result_content_get(self):
        rc = ResultsContent.factory('3-5')
        self.assertEqual(rc.get('BB0'), 'Planning and self-control')

    def test_building_blocks(self):
        rc = ResultsContent.factory('3-5')
        bb = rc.building_blocks()
        self.assertIsNotNone(bb)
        for d in bb:
            keys = d.keys()
            self.assertIn('idx', keys)
            self.assertIn('title', keys)
            self.assertIn('intro', keys)

    def test_level_from_position(self):
        rc = ResultsContent.factory('3-5')
        self.assertEqual(rc.level_from_position(5), 2)
        self.assertEqual(rc.level_from_position(4), 1)
        self.assertEqual(rc.level_from_position(3), 1)
        self.assertEqual(rc.level_from_position(2), 1)
        self.assertEqual(rc.level_from_position(1), 0)
        self.assertEqual(rc.level_from_position(0), 0)

        # test out of range index
        with self.assertRaises(IndexError):
            rc.level_from_position(6)

        # test non-numeric index
        with self.assertRaises(TypeError):
            rc.level_from_position('fail')

    def test_find_overall_progress_elementary(self):
        rc = ResultsContent.factory('3-5')
        scores = {
            40: 0,
            49: 1,
            61: 2,
            70: 3,
            81: 4,
            90: 5
        }
        level_map = {
            0: 0,
            1: 0,
            2: 1,
            3: 1,
            4: 1,
            5: 2
        }

        for score, position in scores.items():
            op = rc.find_overall_progress(score)
            self.assertEqual(op['position_idx'], position)
            self.assertEqual(op['level_idx'], level_map[position])

            op = rc.find_overall_progress(score + 0.1)
            self.assertEqual(op['position_idx'], position)
            self.assertEqual(op['level_idx'], level_map[position])

            op = rc.find_overall_progress(score - 0.1)
            position = position - 1 if position > 0 else position
            self.assertEqual(op['position_idx'], position)
            self.assertEqual(op['level_idx'], level_map[position])

    def test_find_bb_progress(self):
        rc = ResultsContent.factory('3-5')
        scores = {
            0: {16: 0, 20: 1, 25: 2, 29: 3, 34: 4, 38: 5},
            1: {14: 0, 18: 1, 22: 2, 25: 3, 29: 4, 33: 5},
            2: {10: 0, 13: 1, 16: 2, 18: 3, 20: 4, 21: 5}
        }

        for part, v in scores.items():
            for score, position in v.items():
                bbp = rc.find_bb_progress(part, score)
                self.assertEqual(bbp['position_idx'], position)

                bbp = rc.find_bb_progress(part, score - 0.1)
                position = position - 1 if position > 0 else position
                self.assertEqual(bbp['position_idx'], position)

    def test_score_idx(self):
        rc = ResultsContent.factory('3-5')

        self.assertEqual(rc._score_idx('3-5 Overall', 94.3), 5)

        with self.assertRaises(AssertionError):
            rc._score_idx('3-12', 94.3)

        rc.store['noneVal'] = None
        with self.assertRaises(LookupError):
            rc._score_idx('noneVal', 94.3)
