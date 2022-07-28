from v1.util import ref


def clean_categories(selected_categories):
    """This is a (hopefully) temporary solution for dealing w/ the fact
    that we show Blog and Reports as options for filtering, but
    aren't categories themselves. Rather, they consist of sub-categories,
    but since we aren't showing those sub-categories to the end user,
    selecting the parent category is equivalent to all of them
    getting checked. The mapping of Blog and Reports to their
    respective categories exists in cfgov/v1/util/ref.py
    """
    if not selected_categories:
        return None
    subcategories_dict = dict(ref.categories)
    for unicorn in ["blog", "newsroom", "research-reports"]:
        if unicorn in selected_categories:
            if unicorn == "research-reports":
                unicorn = "Research Report"
            for category in subcategories_dict[unicorn.title()]:
                selected_categories.append(category[0].lower())
    return selected_categories
