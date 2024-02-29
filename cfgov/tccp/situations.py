from dataclasses import dataclass, field
from typing import List


@dataclass
class Situation:
    title: str
    details_intro_have: bool
    details: List[str]
    query: dict = field(default_factory=dict)

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
        ],
    ),
    Situation(
        title="Avoid annual fees",
        details_intro_have=True,
        details=["No annual fee"],
        query={"no_account_fee": True},
    ),
    Situation(
        title="Build credit",
        details_intro_have=False,
        details=["Are targeted for your credit score range"],
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
        query={"rewards": True},
    ),
]


SituationChoices = [(situation, situation.title) for situation in SITUATIONS]


def get_situation_by_title(title):
    return {v: k for k, v in SituationChoices}[title]
