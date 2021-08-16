from typing import List

import base36

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


class UrlEncoder:
    """
    Encode/decode survey results to a string in a URL
    """
    def __init__(self, available_keys: List[str]):
        for key in available_keys:
            if len(key.split('_')) > 1:
                raise ValueError('keys cannot contain "_"')
        self.available_keys = available_keys

    def dumps(self, survey_key: str, subtotals: List[float], time: int):
        """
        Encode info to a string
        """
        if survey_key not in self.available_keys:
            raise ValueError(f'key {survey_key} is not valid')

        subtotal_strs = (_encode_num(x) for x in subtotals)
        time_str = _encode_time(time)

        return f'v1_{survey_key}_{str(":".join(subtotal_strs))}_{time_str}'

    def loads(self, encoded: str):
        """
        Decode from string
        """
        parts = encoded.split('_')

        if len(parts) != 4:
            return None

        # version = parts[0]
        key = parts[1]
        subtotals_enc = parts[2].split(':')
        time_enc = parts[3]

        if key not in self.available_keys:
            return None

        subtotals = tuple(_decode_num(x) for x in subtotals_enc)
        time = _decode_time(time_enc)

        return {
            'key': key,
            'subtotals': subtotals,
            'time': time,
        }
