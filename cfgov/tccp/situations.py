from dataclasses import dataclass, field
from typing import List


@dataclass
class Situation:
    title: str
    details: List[str]
    details_intro_have: bool = field(default_factory=bool)
    query: dict = field(default_factory=dict)

    def __str__(self):
        return self.title


SITUATIONS = [
    Situation(
        title="Pay less interest",
        details_intro_have=True,
        details=["Low interest rates"],
        query={
            "ordering": "purchase_apr",
        },
    ),
    Situation(
        title="Transfer a balance",
        details=[
            "Low balance transfer interest rates",
        ],
        query={
            "ordering": "transfer_apr",
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
        details=["Are targeted for your credit score range"],
    ),
    Situation(
        title="Earn rewards",
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
