from django.core.management.base import BaseCommand, CommandError

import matplotlib.pyplot as plt

from tccp.enums import CreditTierColumns
from tccp.filterset import CardSurveyDataFilterSet
from tccp.models import CardSurveyData
from tccp.situations import SITUATIONS
from tccp.views import CardListView


def fmt(value):
    return (
        ("%.2f%%" % (100 * value)) if isinstance(value, float) else str(value)
    )


class Command(BaseCommand):
    help = "Validate TCCP dataset"

    def add_arguments(self, parser):
        parser.add_argument(
            "--save-charts",
            help="Save charts of card purchase APRs (requires matplotlib)",
            action="store_true",
        )

    def handle(self, **options):
        save_charts = options["save_charts"]

        summary_stats = CardSurveyData.objects.get_summary_statistics()

        if not summary_stats["count"]:
            raise CommandError("No cards in dataset!")

        cards = CardSurveyData.objects.with_ratings(
            summary_stats=summary_stats
        )

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

            purchase_apr_rating_counts = (
                CardListView.get_purchase_apr_rating_counts(
                    cards_for_tier.values("purchase_apr_for_tier_rating")
                )
            )

            # Write out counts for each rating label.
            for (
                rating_label,
                rating_count,
            ) in purchase_apr_rating_counts.items():
                self.stdout.write(f"{rating_label}: {rating_count}")

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

            # Dump out purchase APR charts, if specified.
            if save_charts:
                self.save_tier_specific_purchase_apr_chart(
                    tier_name,
                    tier_column,
                    cards_for_tier,
                    summary_stats,
                )

            self.stdout.write()

    def save_tier_specific_purchase_apr_chart(
        self, tier_name, tier_column, cards_for_tier, summary_stats
    ):
        plt.figure(figsize=(10, 6))

        cards = list(
            cards_for_tier.order_by("purchase_apr_for_tier_max").values(
                "purchase_apr_min",
                "purchase_apr_max",
                "purchase_apr_median",
                f"purchase_apr_{tier_column}",
                f"purchase_apr_{tier_column}_rating",
            )
        )

        # Plot min-max.
        min_maxes = {
            i: (100 * card["purchase_apr_min"], 100 * card["purchase_apr_max"])
            for i, card in enumerate(cards)
            if card["purchase_apr_min"] and card["purchase_apr_max"]
        }
        plt.vlines(
            list(min_maxes.keys()),
            ymin=[v[0] for v in min_maxes.values()],
            ymax=[v[1] for v in min_maxes.values()],
            color="lightgray",
            label="Global minimum - maximum",
        )

        # Plot global medians.
        global_medians = {
            i: 100 * card["purchase_apr_median"]
            for i, card in enumerate(cards)
            if card["purchase_apr_median"]
        }
        plt.plot(
            list(global_medians.keys()),
            list(global_medians.values()),
            label="Global median",
            linestyle="",
            marker="o",
        )

        # Plot tier-specific medians.
        tier_medians = {
            i: 100 * card[f"purchase_apr_{tier_column}"]
            for i, card in enumerate(cards)
            if card[f"purchase_apr_{tier_column}"]
        }
        plt.plot(
            list(tier_medians.keys()),
            list(tier_medians.values()),
            label="Tier-specific median",
            linestyle="",
            marker=".",
        )

        for rating, (percentile, color) in enumerate(
            [(25, "darkgreen"), (75, "gold")]
        ):
            pct_cards = [
                i
                for i, card in enumerate(cards)
                if card[f"purchase_apr_{tier_column}_rating"] == rating
            ]

            if not pct_cards:
                continue

            pct_index = max(pct_cards)

            pct_value = (
                100
                * summary_stats[f"purchase_apr_{tier_column}_pct{percentile}"]
            )

            plt.axvline(
                pct_index,
                label=(
                    f"{percentile}th Percentile (Index: {pct_index}): "
                    f"{pct_value:.2f}%"
                ),
                color=color,
            )

        plt.xlabel(f"Cards ({len(cards)}, sorted by purchase APR)")
        plt.ylabel("Purchase APR (%)")
        plt.title(f"Purchase APRs for tier: {tier_name}")
        plt.legend()
        plt.grid(True)

        filename = f"tccp-purchase-aprs-{tier_column}.png"
        self.stdout.write(f"Saving chart to {filename}.")
        plt.savefig(filename, bbox_inches="tight")
