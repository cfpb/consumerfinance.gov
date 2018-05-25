import re

from regulations3k.scripts.roman import roman_to_int


"""
Patterns for handling paragraph levels in eCFR XML

In most reg sections, IDs are wrapped in parentheses.
In some, IDs bare, followed by a period.
In all cases, ID level should equal ID hyphen count + 1

What the parser needs to know:

- current id
- current level
- the next ID token
- whether the ID surfs, dives or rises, and if rising, how many levels
"""


class IdLevelState(object):
    """
    A class to manage IDs and keep track of state

    IDs swim like dolphins through a reg: surfing, diving, and rising.
    """
    current_id = ''
    next_token = ''

    def level(self):
        return self.current_id.count('-') + 1

    def current_token(self):
        return self.current_id.split('-')[-1]

    def surf(self):
        tokens = self.current_id.split('-')
        tokens[-1] = self.next_token
        self.current_id = "-".join(tokens)
        return self.current_id

    def dive(self):
        new_id = "-".join(
            [bit for bit in [self.current_id, self.next_token] if bit])
        self.current_id = new_id
        return new_id

    def rise(self, levels_up):
        tokens = self.current_id.split('-')[:-levels_up]
        tokens[-1] = self.next_token
        self.current_id = "-".join(tokens)
        return self.current_id

    def roman_surf_test(self):
        """
        Surf test for Roman levels 3 and 6.
        Only surf if the next token is both a valid roman numeral *and*
        it's the next logical roman numeral.
        For instance 'c' is a valid roman numeral, but we're probably not at
        roman numeral level 99. It's more likely a rise to 'c' at level 1.

        TODO: Name one of these levels Etruscan.
        """
        current_roman_int = roman_to_int(self.current_token())
        if not current_roman_int:
            return False
        next_roman = current_roman_int + 1
        if roman_to_int(self.next_token) == next_roman:
            return True
        else:
            return False

    def next_id(self):
        _next = self.next_token
        if self.level() == 1:  # alpha-lower level
            if not self.current_id:
                self.current_id = _next
            if _next == '1':
                return self.dive()
            else:
                return self.surf()
        if self.level() == 2:  # digit level
            if _next.isdigit():
                return self.surf()
            elif _next == 'i':
                return self.dive()
            else:
                return self.rise(1)
        if self.level() == 3:  # roman level
            if _next == 'A':
                return self.dive()
            elif self.roman_surf_test():
                return self.surf()
            elif _next.isdigit():
                return self.rise(1)
            else:
                return self.rise(2)
        if self.level() == 4:  # alpha-upper level
            if _next.isupper():
                return self.surf()
            elif _next == '1':
                return self.dive()
            elif roman_to_int(_next):
                return self.rise(1)
            elif _next.isdigit():
                return self.rise(2)
            else:
                return self.rise(3)
        if self.level() == 5:  # 2nd digit level: a-1-i-A-1
            token_int = int(self.current_token())
            if _next == 'i':
                return self.dive()
            elif (_next.isdigit()
                    and int(_next) == token_int + 1):
                return self.surf()
            elif _next.isupper():
                return self.rise(1)
            elif (roman_to_int(_next)):
                return self.rise(2)
            elif _next.isdigit():
                return self.rise(3)
            else:
                return self.rise(4)
        if self.level() == 6:  # 2nd roman level: 'a-1-i-A-1-i'
            previous_token = self.current_id.split('-')[-2]
            if previous_token.isdigit():
                previous_digit = int(previous_token)
            else:
                previous_digit = None
            if self.roman_surf_test():
                return self.surf()
            elif (previous_digit
                    and _next.isdigit()
                    and int(_next) == previous_digit + 1):
                return self.rise(1)
            elif _next.isupper():
                return self.rise(2)
            elif roman_to_int(_next):
                return self.rise(3)
            elif _next.isdigit():
                return self.rise(4)
            else:
                return self.rise(5)


# search patterns
title_pattern = re.compile(r'PART ([^\-]+) \- ([^\(]+) \(?([^\)]+)?')

paren_id_patterns = {
    'any': r'\(([^\)]{1,5})\)',
    'initial': r'\(([^\)]{1})\)',
    'lower': r'\(([a-z]{1,2})\)',
    'digit': r'\((\d{1,2})\)',
    'roman': r'\(([ivxlcdm]{1,5})\)',
    'upper': r'\(([A-Z]{1,2})\)',
}

dot_id_patterns = {
    'any': r'([^\.]{1,5})\.',
    'lower': r'([a-z]{1,2})\.',
    'digit': r'(\d{1,2})\.',
    'roman': r'([ivxlcdm]{1,5})\.',
    'upper': r'([A-Z]{1,2})\.',
}

# A place to document level patterns found in regulations

level_patterns = {
    'standard': {
        'pattern': 'a-1-i-A-1-i',
        'regs': ['B', 'C'],
        'type_sequence': [
            'lower', 'digit', 'roman', 'upper', 'digit', 'roman']
    },
    'definitions': {
        'pattern': '1-i',
        'regs': [],
        'type_sequence': ['digit', 'roman'],
    },
    'appendices': {
        'pattern': 'A1_a-1-i',
        'regs': ['B'],
        'type_sequence': ['alnum', 'lower', 'digit', 'roman'],
    },
    'interpretations': {
        'pattern': '',
        'regs': [''],
        'type_sequence': [],
    },
}
