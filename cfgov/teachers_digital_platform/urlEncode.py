from typing import List

from . import base36
from .assessments import Assessment, available_assessments, get_assessment

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
    parts = (base36.dumps(int(x)) for x in parts)
    return '.'.join(parts)


def _decode_num(encoded: str):
    parts = encoded.split('.')
    nums = [base36.loads(x) for x in parts]
    nums = nums[0:2]
    return float('.'.join(str(x) for x in nums))


def dumps(assessment: Assessment, subtotals: List[float], time: int):
    '''
    Encode info to a string
    '''
    subtotal_strs = (_encode_num(x) for x in subtotals)
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
    subtotals_enc = parts[1].split(':')
    time_enc = parts[2]

    if key not in available_assessments:
        return None

    assessment = get_assessment(key)
    subtotals = tuple(_decode_num(x) for x in subtotals_enc)
    time = _decode_time(time_enc)

    return {
        'assessment': assessment,
        'subtotals': subtotals,
        'time': time,
    }
