from typing import List

from . import base36
from .assessments import Assessment, assessments

# We won't need timestamps before this time
# DO NOT CHANGE THIS
_feature_launch_ts = 1623432061


def _encode_time(time: float):
    time = max(0, time - _feature_launch_ts)
    return base36.dumps(int(time))


def _decode_time(b36: str):
    return base36.loads(b36) + _feature_launch_ts


def _encode_num(score: float):
    parts = str(score).split('.')
    parts = map(lambda x: base36.dumps(int(x)), parts)
    return '.'.join(parts)


def _decode_num(encoded: str):
    parts = encoded.split('.')
    nums = map(lambda x: base36.loads(x), parts)
    nums = nums[0:2]
    return float('.'.join(nums))


def dumps(assessment: Assessment, subtotals: List[float], time: int):
    '''
    Encode info to a string
    '''
    subtotal_strs = map(lambda x: _encode_num(x), subtotals)
    time_str = _encode_time(time)

    return assessment.key + '|' + str(':'.join(subtotal_strs)) + '|' + time_str


def loads(encoded: str):
    '''
    Decode from string
    '''
    parts = encoded.split('|')

    if len(parts) != 3:
        return None

    key = parts[0]
    subtotals_enc = parts[1].split('.')
    time_enc = parts[2]

    if key not in assessments.keys():
        return None

    assessment = assessments[key]
    subtotals = map(lambda x: _decode_num(x), subtotals_enc)
    time = _decode_time(time_enc)

    return {
        'assessment': assessment,
        'subtotals': subtotals,
        'time': time,
    }
