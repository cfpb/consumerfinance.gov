from __future__ import unicode_literals


def roman_to_int(roman):
    """
    Convert a unicode lowercase Roman numeral to an integer.
    This is python3-compliant and assumes unicode strings. So if you test
    either function in Python2 in a Django shell, be sure to import
    unicode_literals or use explicit unicode strings, such as u'iii'.
    """

    if not isinstance(roman, type("")):
        return
    nums = {'m': 1000, 'd': 500, 'c': 100, 'l': 50, 'x': 10, 'v': 5, 'i': 1}
    total = 0
    for i in range(len(roman)):
        try:
            value = nums[roman[i]]
            if i + 1 < len(roman) and nums[roman[i + 1]] > value:
                total -= value
            else:
                total += value
        except KeyError:
            return
    if int_to_roman(total) == roman:
        return total
    else:
        return


def int_to_roman(num):
    """Convert an integer to a lowercase Roman numeral, as used in regs."""
    if not isinstance(num, type(1)):
        raise TypeError("Expected integer, got {}".format(type(num)))
    if num < 1 or num > 3999:
        raise ValueError("Argument must be between 1 and 3999")
    int_values = (1000, 900, 500, 400, 100, 90, 50, 40,
                  10, 9, 5, 4, 1)
    numerals = ('m', 'cm', 'd', 'cd', 'c', 'xc', 'l', 'xl',
                'x', 'ix', 'v', 'iv', 'i')
    result = []
    for i in range(len(int_values)):
        count = int(num / int_values[i])
        result.append(numerals[i] * count)
        num -= int_values[i] * count
    return ''.join(result)
