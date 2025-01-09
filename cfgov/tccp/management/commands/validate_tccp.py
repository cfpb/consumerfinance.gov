from django.core.management.base import BaseCommand, CommandError

from tccp.enums import CreditTierColumns, PurchaseAPRRatings
from tccp.filterset import CardSurveyDataFilterSet
from tccp.models import CardSurveyData
from tccp.situations import SITUATIONS
from tccp.views import CardListView


def fmt(value):
    return ("%g%%" % (100 * value)) if isinstance(value, float) else str(value)


def fmt_range(min, max):
    if min == max:
        return fmt(min)
    else:
        return f"{fmt(min)} - {fmt(max)}"


class Command(BaseCommand):
    help = "Validate TCCP dataset"

    def handle(self, **options):
        summary_stats = CardSurveyData.objects.get_summary_statistics()

        if not summary_stats["count"]:
            raise CommandError("No cards in dataset!")

        all_cards = CardSurveyData.objects.all()
        self.stdout.write(f"{all_cards.count()} cards in database")

        invalid_cards = all_cards.only_invalid_aprs()
        self.stdout.write(f"{invalid_cards.count()} cards with invalid APRs")

        for i, invalid_card in enumerate(invalid_cards):
            self.stdout.write(f"{i + 1}: {invalid_card.slug}")

        self.stdout.write()

        cards = CardSurveyData.objects.exclude_invalid_aprs().with_ratings(
            summary_stats=summary_stats
        )

        apr_rating_lookup = dict(PurchaseAPRRatings)

        for tier_name, tier_column in CreditTierColumns:
            self.stdout.write(tier_name.upper())
            self.stdout.write("-" * len(tier_name))

            # Write out summary stats for each credit tier.
            for stat_name, stat_column in [
                ("Count", f"purchase_apr_{tier_column}_count"),
                ("Minimum", f"purchase_apr_{tier_column}_min"),
                ("Maximum", f"purchase_apr_{tier_column}_max"),
                ("25th percentile", f"purchase_apr_{tier_column}_pct25"),
                ("75th percentile", f"purchase_apr_{tier_column}_pct75"),
            ]:
                self.stdout.write(
                    f"{stat_name}: " + fmt(summary_stats[stat_column])
                )

            self.stdout.write()

            cards_for_tier = cards.for_credit_tier(tier_name)

            purchase_apr_rating_ranges = (
                CardListView.get_purchase_apr_rating_ranges(
                    cards_for_tier.values(
                        "purchase_apr_for_tier_max",
                        "purchase_apr_for_tier_rating",
                    )
                )
            )

            # Write out ranges for each rating label.
            for (
                rating,
                (rating_apr_min, rating_apr_max),
            ) in purchase_apr_rating_ranges.items():
                self.stdout.write(
                    f"{apr_rating_lookup[rating]}: "
                    + fmt_range(rating_apr_min, rating_apr_max)
                )

            self.stdout.write()

            # Write out situation-specific result counts.
            situation_counts = {
                situation.title: CardSurveyDataFilterSet(
                    {
                        "credit_tier": tier_name,
                        **situation.params,
                    },
                    queryset=cards,
                ).qs.count()
                for situation in SITUATIONS
            }

            for situation, count in situation_counts.items():
                self.stdout.write(f"{situation}: {count}")

            if not all(situation_counts.values()):
                raise CommandError("Situation with no results!")

            self.stdout.write()
