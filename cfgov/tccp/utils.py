from django.utils.text import slugify


def get_card_slugifier():
    used_slugs = set()

    def slugify_card(card):
        extra = 0

        while True:
            slug = (
                slugify(card.institution_name)
                + "-"
                + slugify(card.product_name)
            )

            if extra:
                slug += f"-{extra}"

            if slug not in used_slugs:
                break

            extra += 1

        used_slugs.add(slug)
        return slug

    return slugify_card
