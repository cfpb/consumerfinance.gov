# Filterable Lists

In order to expose a broad generic search across areas of our site we have implemented a custom Streamfield block [FilterableList](https://github.com/cfpb/consumerfinance.gov/blob/main/cfgov/v1/atomic_elements/organisms.py#L802) that allows a user to specify what filters are available, how to order results, and which pages should be included in the search.

- [How It Works](#how-it-works)
    - [FilterableListMixin](#filterablelistmixin)
    - [CategoryFilterableListMixin](#categoryfilterablelistmixin)
    - [Forms](#forms)
    - [Documents](#documents)
    - [Search](#search)

## How It Works