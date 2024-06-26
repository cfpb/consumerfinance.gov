from dataclasses import dataclass, field
from itertools import chain

from django.template import loader
from django.utils.safestring import mark_safe
from django.utils.text import slugify

from tccp import enums


@dataclass
class Situation:
    title: str
    params: dict = field(default_factory=dict)
    speed_bumps: list = field(default_factory=list)

    def __str__(self):
        return self.title

    @property
    def slug(self):
        return slugify(self.title)

    def render(self, viewname):
        template = f"tccp/situations/{viewname}/{self.slug}.html"
        return mark_safe(loader.get_template(template).render())

    @property
    def select_html(self):
        return self.render("select")

    @classmethod
    def get_nonconflicting_params(cls, situations):
        """Get nonconflicting parameters for a list of situations.

        Consider a list of situation params like this:

          - situation 1: {"a": 1, "b": 2}
          - situation 2: {"c": [3, 4]}
          - situation 3: {"a": 5, "b": 2}

        This method drops parameter "a" because it is specified by two
        different situations with two different values. It keeps parameter "b"
        because, even though it is specified by two different situations, they
        both specify the same value. It keeps parameter "c" because it is only
        specified by one situation, even though it has multiple values for that
        situation.

        The list of combined parameters returned thus looks like:

        {"b": 2, "c": [3, 4]}
        """
        duplicate_keys = []
        unique_params = {}

        for situation in situations:
            for k, v in situation.params.items():
                if k in duplicate_keys:
                    continue

                if k in unique_params:
                    if v != unique_params[k]:
                        unique_params.pop(k)
                        duplicate_keys.append(k)

                    continue

                unique_params[k] = v

        return unique_params


SITUATIONS = [
    Situation(
        "Pay less interest",
        {"ordering": "purchase_apr"},
        [
            {
                "content": (
                    "Many small banks and credit unions offer lower interest "
                    "rates and could save you hundreds of dollars per year."
                ),
            }
        ],
    ),
    Situation(
        "Transfer a balance",
        {"ordering": "transfer_apr"},
        [
            {
                "content": (
                    "When transferring a balance, there's usually a transfer "
                    "fee and you're still likely to incur interest charges on "
                    "new purchases. It might be helpful to use a separate "
                    "card for new purchases with a lower purchase APR while "
                    "you pay down a transferred balance."
                ),
            }
        ],
    ),
    Situation(
        "Make a big purchase",
        {"ordering": "purchase_apr"},
        [
            {
                "content": (
                    "If you've carried balances in the past, or think you're "
                    "likely to do so, consider credit cards that have the "
                    "lowest interest rates."
                ),
            },
            {
                "content": (
                    "If a card has an introductory interest rate offer, "
                    "ensure you're on track to pay off the balance within the "
                    "promotional period, or you could end up owing more "
                    "interest than the original purchase amount."
                ),
            },
        ],
    ),
    Situation(
        "Avoid fees",
        {
            "ordering": "purchase_apr",
            "no_account_fee": True,
        },
    ),
    Situation(
        "Build credit",
        {"ordering": "purchase_apr"},
        [
            {
                "content": (
                    "If you're trying to build credit, only use a credit card "
                    "for necessary purchases and pay your credit card balance "
                    "in full every month."
                ),
                "link": (
                    "Learn about ways to build credit and your credit score."
                ),
                "url": (
                    "/ask-cfpb/"
                    "how-do-i-get-and-keep-a-good-credit-score-en-318/"
                ),
            }
        ],
    ),
    Situation(
        "Earn rewards",
        {
            "ordering": "purchase_apr",
            "rewards": list(dict(enums.RewardsChoices)),
        },
        [
            {
                "content": (
                    "If you carry a balance on your credit card, interest and "
                    "fees typically exceed the value of any rewards earned."
                ),
                "link": (
                    "Learn why rewards may not be as beneficial as they seem."
                ),
                "url": (
                    "/about-us/newsroom/"
                    "cfpb-report-highlights-consumer-frustrations-with-credit-card-"
                    "rewards-programs/"
                ),
            }
        ],
    ),
]


SituationChoices = [(situation, situation.title) for situation in SITUATIONS]


def get_situation_by_title(title):
    return {v: k for k, v in SituationChoices}[title]


class SituationSpeedBumps:
    INTERVAL = 5

    def __init__(self, situations):
        self.speed_bumps = list(chain(*(s.speed_bumps for s in situations)))

    def __getitem__(self, index):
        if index and not (index % self.INTERVAL):
            offset = index // self.INTERVAL - 1
            if offset <= len(self.speed_bumps):
                return self.speed_bumps[offset]
