"""
Patterns for handling sections and paragraph levels in eCFR XML

## Paragraphs
- In most reg sections, IDs are wrapped in parentheses.
- In some, IDs bare, followed by a period.
- Except for interpretations, ID level should equal ID hyphen count + 1
- For interpretations, hyphen count starts after the 'Interp' token
- The standard indentation token scheme is a-1-i-A-1-i

What the parser needs to know:

- current id
- current level
- the next ID token
- whether the ID surfs, dives or rises, and if rising, how many levels

The IdLevelState object keeps track of IDs and indentation level.

## Appendices

Appendices indentation mostly follow a different indentation scheme: 1-i-A

## Interpretations
This is a type of Appendix that needs special handling, because its
paragraph references get inserted into section content when pages are rendered.

We break up interpretations by the sections they interpret and mark
individual paragraph references with a paragraph ID code.

In the XML, an interpretations' section may be HD1, HD2, or HD3.
Paragrpah references may be in HD2, HD3, P or I tags

Blessedly, interpretations for appendices don't carry paragraph references,
just an overall reference to the appendix.

Some appendix interpretations refer to multiple appendices. These don't get
inserted into section content.

"""

import re

from regulations3k.parser.integer_conversion import alpha_to_int, roman_to_int


class IdLevelState:
    """
    A class to manage paragraph IDs and keep track of indentation state.

    IDs swim like dolphins through a reg: surfing, diving, and rising.
    """

    def __init__(self):
        self.current_id = ""
        self.next_token = ""

    def level(self):
        return self.current_id.count("-") + 1

    def interp_level(self):
        return (
            self.current_id.partition("Interp")[-1].strip("-").count("-") + 1
        )

    def current_token(self):
        return self.current_id.split("-")[-1]

    def root_token(self):
        return self.current_id.split("-")[0]

    def surf(self):
        tokens = self.current_id.split("-")
        tokens[-1] = self.next_token
        self.current_id = "-".join(tokens)
        return self.current_id

    def dive(self):
        new_id = "-".join(
            [bit for bit in [self.current_id, self.next_token] if bit]
        )
        self.current_id = new_id
        return new_id

    def rise(self, levels_up):
        new_level_tokens = self.current_id.split("-")[:-levels_up]
        new_level_tokens[-1] = self.next_token
        self.current_id = "-".join(new_level_tokens)
        return "-".join(new_level_tokens)

    def roman_surf_test(self, token, next_token):
        """
        Determine whether a Roman token is the next logical Roman token.

        This test is for Roman levels 3 or 6, and checks whether the next token
        is both a Roman numeral and the next bigger Roman numeral.

        For instance 'v' is a valid Roman numeral. But if the the current
        Roman numeral doesn't evaluate to 4, the 'v' must be a level-1 marker.

        Some ambiguity can remain, when the next token is both the next valid
        Roman numeral and the next valid level-1 marker. This happens most
        often when the level-1 marker is "h." The parser defaults to diving
        in this case, which will be wrong sometimes.
        """
        if not token:
            return False
        for each in [token, next_token]:
            if not roman_to_int(each):
                return False
        return roman_to_int(next_token) == roman_to_int(token) + 1

    def alpha_surf_test(self, token, next_token):
        if not alpha_to_int(token):
            return False
        """Determine whether an alpha token is the next logical alpha token"""
        return alpha_to_int(next_token) == alpha_to_int(token) + 1

    def next_appendix_id_1a(self):
        """For appendices or intros that follow a 1-a indentation pattern."""
        _next = self.next_token
        if self.level() == 1:  # digit level
            if not self.current_id:
                self.current_id = _next
            if _next == "a":
                return self.dive()
            else:
                return self.surf()
        if self.level() == 2:  # lowercase-alpha level: 1-a
            if _next.isalpha():
                return self.surf()
            elif _next.isdigit():
                return self.rise(1)

    def next_appendix_id(self):
        """Appendices that follow a 1-i-A pattern."""
        _next = self.next_token
        if self.level() == 1:  # digit level
            if not self.current_id:
                self.current_id = _next
            if _next == "i":
                return self.dive()
            else:
                return self.surf()
        if self.level() == 2:  # roman level: 1-i
            if _next == "A":
                return self.dive()
            if self.roman_surf_test(self.current_token(), _next):
                return self.surf()
            else:
                return self.rise(1)
        if self.level() == 3:  # uppercase level: 1-i-A
            if _next.isupper():
                return self.surf()
            elif self.roman_surf_test(self.current_id.split("-")[-2], _next):
                return self.rise(1)
            else:
                return self.rise(2)

    def next_interp_id(self):
        """Interpretations that follow a [pid]-Interp-1-i-A pattern."""
        _next = self.next_token
        if not self.current_id:
            self.current_id = _next
            return _next
        if self.interp_level() == 1:  # digit level: [pid]-Interp-1
            if self.current_token() == "Interp":
                return self.dive()
            if _next == "i":
                return self.dive()
            else:
                return self.surf()
        if self.interp_level() == 2:  # roman level: [pid]-Interp-1-i
            if _next == "A":
                return self.dive()
            if self.roman_surf_test(self.current_token(), _next):
                return self.surf()
            else:
                return self.rise(1)
        if self.interp_level() == 3:  # uppercase level: [pid]-Interp-1-i-A
            if _next.isupper():
                return self.surf()
            elif self.roman_surf_test(self.current_id.split("-")[-2], _next):
                return self.rise(1)
            else:
                return self.rise(2)

    def next_id(self):
        """The standard section indentation pattern: a-1-i-A-1-i."""
        _next = self.next_token
        if self.level() == 1:  # lowercase-alpha level
            if not self.current_id:
                self.current_id = _next
            if _next == "1":
                return self.dive()
            else:
                return self.surf()
        if self.level() == 2:  # digit level: a-1
            if _next.isdigit():
                return self.surf()
            elif _next == "i":
                return self.dive()
            else:
                return self.rise(1)
        if self.level() == 3:  # roman level: a-1-i
            if _next == "A":
                return self.dive()
            if self.roman_surf_test(self.current_token(), _next):
                return self.surf()
            elif _next.isdigit():
                return self.rise(1)
            else:
                return self.rise(2)
        if self.level() == 4:  # alpha-upper level: a-1-i-A
            if _next == "1":
                return self.dive()
            elif _next.isupper():
                return self.surf()
            elif self.roman_surf_test(self.current_id.split("-")[-2], _next):
                return self.rise(1)
            elif _next.isdigit():
                return self.rise(2)
            else:
                return self.rise(3)
        if self.level() == 5:  # 2nd digit level: a-1-i-A-1
            token_int = int(self.current_token())
            if _next == "i":
                return self.dive()
            elif _next.isdigit() and int(_next) == token_int + 1:
                return self.surf()
            elif _next.isupper():
                return self.rise(1)
            elif roman_to_int(_next):
                return self.rise(2)
            elif _next.isdigit():
                return self.rise(3)
            else:
                return self.rise(4)
        if self.level() == 6:  # 2nd roman level: 'a-1-i-A-1-i'
            previous_token = self.current_id.split("-")[-2]
            if previous_token.isdigit():
                previous_digit = int(previous_token)
            else:
                previous_digit = None
            if self.roman_surf_test(self.current_token(), _next):
                return self.surf()
            elif (
                previous_digit
                and _next.isdigit()
                and int(_next) == previous_digit + 1
            ):
                return self.rise(1)
            elif _next.isupper():
                return self.rise(2)
            elif roman_to_int(_next):
                return self.rise(3)
            elif _next.isdigit():
                return self.rise(4)
            else:
                return self.rise(5)

    def roman_test(self, id_token):
        """
        Determine whether the root ID of a potential multi_ID paragraph
        is a roman numeral increment surfing levels 3 or 6
        (the roman levels of a-1-i-A-1-i)
        """
        roman_int = roman_to_int(id_token)
        if not roman_int:
            return False
        if self.level() not in [3, 6]:
            return False
        if roman_int - 1 == roman_to_int(self.current_token()):
            return True

    def token_validity_test(self, token):
        "Make sure a singleton token is some kind of valid ID."
        if (
            token.isdigit()
            or roman_to_int(token)
            or (token.isalpha() and len(token) == 1)
            or (token.isalpha() and len(token) == 2 and token[0] == token[1])
        ):
            return True
        else:
            return False

    def sniff_appendix_id_type(self, paragraphs):
        """
        Detect whether an appendix follows the section paragraph indentation
        scheme (a-1-i-A-1-i) or the appendix scheme (1-a)

        The sniffer should return 'section', 'appendix', or None.
        """
        for graph in paragraphs[:10]:
            if graph.text.startswith("(a)"):
                return "section"
            if graph.text.startswith("1."):
                return "appendix"

    def multiple_id_test(self, ids):
        """
        Decide, based on a paragraph's first two IDS,
        whether to proceed with multi-ID processing.

        Allowed multi-ID patterns are:
          (lowercase)(1) - and the lowercase cannot be a roman increment
          (digit)(i)
          (roman)(A)
          (uppercase)(1)
        """
        if len(ids) < 2:
            return
        root_token = ids[0]
        # levels 1 or 4
        if (
            root_token.isalpha()
            and len(root_token) < 3
            and not self.roman_test(root_token)
            and ids[1] == "1"
        ):
            good_ids = 2
            if len(ids) == 3 and ids[2] == "i":
                good_ids = 3
            return ids[:good_ids]
        # levels 2 or 5
        if root_token.isdigit() and ids[1] == "i":
            good_ids = 2
            if len(ids) == 3 and ids[2] == "A" and self.level() != 5:
                good_ids = 3
            return ids[:good_ids]
        # level 3
        if roman_to_int(root_token) and ids[1] == "A":
            good_ids = 2
            if len(ids) == 3 and ids[2] == "1":
                good_ids = 3
            return ids[:good_ids]
        # multiples not allowed at level 6

    def parse_appendix_graph(self, p_element, label):
        """Extract dot-based IDs, if any"""
        pid = ""
        graph_text = ""
        id_match = re.match(dot_id_patterns["any"], p_element.text)
        if id_match:
            id_token = id_match.group(1).replace("*", "")
            self.next_token = id_token
            pid = self.next_appendix_id() or ""
            graph_text += "\n{" + pid + "}\n"
            graph = (
                p_element.text.replace(
                    "{}.".format(pid), "**{}.**".format(pid), 1
                )
                .replace("  ", " ")
                .replace("** **", " ", 1)
            )
            graph_text += graph + "\n"
        else:
            graph_text += p_element.text + "\n"
        return graph_text


# search patterns; not all are currently used
title_pattern = re.compile(r"PART ([^\-]+) \- ([^\(]+) \(?([^\)]+)?")

paren_id_patterns = {
    "any": r"\(([^\)]{1,7})\)[^\(]+",
    "initial": r"\(([^\)]{1,7})\)",
    "level_1_multiple": r"\((?P<ID1>[a-z]{1,2})\)(?P<phrase1>[^\(]+)\((?P<ID2>1)\)(?P<phrase2>[^\(]+)\((?P<ID3>i)\)?(?P<remainder>[^\n]+)",  # noqa: B950
    "lower": r"\(([a-z]{1,2})\)",
    "digit": r"\((\d{1,2})\)",
    "roman": r"\(([ivxlcdm]{1,5})\)",
    "upper": r"\(([A-Z]{1,2})\)",
}

dot_id_patterns = {
    "any": r"([^\.]{1,5})\.",
    "lower": r"([a-z]{1,2})\.",
    "digit": r"(\d{1,2})\.",
    "roman": r"([ivxlcdm]{1,5})\.",
    "upper": r"([A-Z]{1,2})\.",
}

interp_reference_pattern = r"(\d{1,3})(\([a-z]{1,2}\))?(\(\d{1,2}\))?(\([ivxlcdm]{1,5}\))?(\([A-Z]{1,2}\))?(\(\d{1,2}\))?(\([ivxlcdm]{1,5}\))?"  # noqa: B950
interp_inferred_section_pattern = r"(\([a-z]{1,2}\))(\(\d{1,2}\))?(\([ivxlcdm]{1,5}\))?(\([A-Z]{1,2}\))?(\(\d{1,2}\))?(\([ivxlcdm]{1,5}\))?"  # noqa: B950'

LEVEL_STATE = IdLevelState()
