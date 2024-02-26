from dataclasses import dataclass
from typing import List


@dataclass
class Situation:
    title: str
    details_intro_have: bool
    details: List[str]
    query: dict

    def __str__(self):
        return self.title


SITUATIONS = [
    Situation(
        title="Have a lower monthly payment",
        details_intro_have=True,
        details=["Low interest rates"],
        query={
            "ordering": "purchase_apr",
        },
    ),
    Situation(
        title="Transfer a balance",
        details_intro_have=True,
        details=[
            "Low balance transfer interest rates",
            "No balance transfer fee",
        ],
        query={
            "ordering": "transfer_apr",
            "no_balance_transfer_fee": True,
        },
    ),
    Situation(
        title="Make a big purchase",
        details_intro_have=True,
        details=[
            "Low purchase interest rates",
            (
                "Introductory interest rate offers",
                (
                    "(and give you more information on what to look out for with "
                    "introductory offers)"
                ),
            ),
        ],
        query={
            "ordering": "purchase_apr",
            "introductory_apr_offered": True,
        },
    ),
    Situation(
        title="Avoid annual fees",
        details_intro_have=True,
        details=["No annual fee"],
        query={
            "ordering": "purchase_apr",
            "no_account_fee": True,
        },
    ),
    Situation(
        title="Build credit",
        details_intro_have=False,
        details=["Are secured"],
        query={
            "ordering": "purchase_apr",
            "secured_card": True,
        },
    ),
    Situation(
        title="Earn rewards",
        details_intro_have=False,
        details=[
            (
                "Have rewards",
                "(like cash back, travel points, or other rewards)",
            )
        ],
        query={
            "ordering": "purchase_apr",
            "rewards": True,
        },
    ),
]


SituationChoices = [(situation, situation.title) for situation in SITUATIONS]


def get_situation_by_title(title):
    return {v: k for k, v in SituationChoices}[title]
