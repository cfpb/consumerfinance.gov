from dataclasses import dataclass, field

from django.template import loader
from django.utils.safestring import mark_safe
from django.utils.text import slugify

from tccp import enums


@dataclass
class Situation:
    title: str
    params: dict = field(default_factory=dict)

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

    @property
    def results_html(self):
        return self.render("results")

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
    Situation("Pay less interest", {"ordering": "purchase_apr"}),
    Situation("Transfer a balance", {"ordering": "transfer_apr"}),
    Situation("Make a big purchase"),
    Situation("Avoid fees", {"no_account_fee": True}),
    Situation("Build credit"),
    Situation("Earn rewards", {"rewards": list(dict(enums.RewardsChoices))}),
]


SituationChoices = [(situation, situation.title) for situation in SITUATIONS]


def get_situation_by_title(title):
    return {v: k for k, v in SituationChoices}[title]
