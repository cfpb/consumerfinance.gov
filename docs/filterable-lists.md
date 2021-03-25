# Filterable Lists

In order to expose a broad generic search across areas of our site we have implemented a custom Streamfield block [FilterableList](https://github.com/cfpb/consumerfinance.gov/blob/main/cfgov/v1/atomic_elements/organisms.py#L802) that allows a user to specify what filters are available, how to order results, and which pages should be included in the search.

- [How It Works](#how-it-works)
    - [FilterableListMixin](#filterablelistmixin)
    - [CategoryFilterableListMixin](#categoryfilterablelistmixin)
    - [Forms](#forms)
        - [FilterableListForm](#filterablelistform)
        - [EnforcementActionsFilterForm](#enforcementactionsfilterform)
        - [EventArchiveFilterForm](#eventarchivefilterform)
    - [Documents](#documents)
    - [Search](#search)
        - [FilterablePagesDocumentSearch](#filterablepagesdocumentsearch)
        - [EventFilterablePagesDocumentSearch](#eventfilterablepagesdocumentsearch)
        - [EnforcementActionFilterablePagesDocumentSearch](#enforcementactionfilterablepagesdocumentsearch)

## How It Works

The journey on how a page gets a filterable form is not necessarily a straight or simple path, but it is something that is important to know. To start, the page must support the FilterableList block within a Streamfield as we mentioned earlier, but from there we start to see some divergence. In order to utilize the FilterableList the page must support one of the following two classes: FilterableListMixin or CategoryFilterableListMixin

### FilterableListMixin

The more common mixin that pages will extend is the [FilterableListMixin](https://github.com/cfpb/consumerfinance.gov/blob/main/cfgov/v1/models/filterable_list_mixins.py#L15). This class defines several important methods such as `get_form_class` which define the form to use. We also have some methods that retrieve relevant information for the form to use such as `get_filterable_list_wagtail_block`, `get_filterable_root`, and `get_filterable_queryset`. The bulk of the work is done in the `get_context` method which is responsible for getting and populating the form, as well as processing the form, and returning the results to the user. 

### CategoryFilterableListMixin

The [CategoryFilterableListMixin](https://github.com/cfpb/consumerfinance.gov/blob/main/cfgov/v1/models/filterable_list_mixins.py#L199) is an extension of the base FilterableListMixin that exposes some new functionality. It modifies how `get_filterable_queryset` operates and that it gets an initial list of pages but limits them to only ones that also fall within a set of initial categories which can be definited as the variable `filterable_categories` on a given page. We can see this in action with both `Newsroom` and `Recent Updates` filterable pages.

### Forms

As of our initial release, our filterable forms can be broken into three specific forms, the FilterableListForm, EnforcementActionsFilterableListForm, and the EventArchiveFilterForm. The majority of our filterable lists rely on FilterableListForm and only a select one or two leverage the other forms.

#### FilterableListForm

This is the base form that the vast majority of cf.gov uses for filterable lists. It defines the core fields that are visible on the form as well as functions to assist in setting initial data and sanitizing form input. The import information regarding FilterableListForm is that it defines the function `get_page_set` which is responsible for invoking a search query. The logic regarding how to pass categories into the search object is due to the previously mentioned `CategoryFilterableListMixin` which modifies the initial search parameters to enforce a category search if and only if the `filterable_categories` list is passed into the form when initialized.

#### EnforcementActionsFilterForm

The EnforcementActionsFilterForm is an extension of FilterableListForm, adding on two fields specific to Enforcement Actions, and using a refined search class to provide search functionality against the new fields and a proper ordering by initial filing date.

#### EventArchiveFilterForm

The EventArchiveFilterForm is another extension of FilterableListForm, the only real modification being the invokation of an event specific search class that allows us to provide filtering based on event dates rather than page publication dates.

### Documents

There is currently only one type of document defined `FilterablePagesDocument` which is based off the `AbstractFilterPage` class. This document is responsible for housing data related to any of the filterable page types that extend AbstractFilterPage, including EnforcementActions, BlogPage, EventPage, and NewsRoomPage to name a few. In order to get fields that are specific to a page type, such as the status list for an Enforcement Action, you use the `prepare_field` function syntax. The use of `get_instances_from_related` is to enforce the auto updating of our index when changes occur to a specific page we have indexed rather than just the relation to `AbstractFilterPage` that is reflected in the database.

### Search

Search is the final piece of the puzzle, where we actually leverage a couple elasticsearch features to filter and match documents and return them in an ordered queryset. Before breaking down the search classes, its important to discuss the current implementation from an Elasticsearch perspective to understand how we're gathering results.

The expanded search for filterable lists is using a [multi-match](https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-multi-match-query.html) across the title, topic name, preview description, and content fields of all FilterablePagesDocument. We are leveraging a [phrase_prefix](https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-multi-match-query.html#type-phrase) matching style with a currently configured slop of 2, to allow for some looser matching restrictions. We also provide a boost score for matching to the title and topic name fields indicated with `^10` within the code base. This boost score is to enable better ordering by relevance when desired. Search currently supports two different methods of ordering results, relevance and date published. Relevance is calculated by the Elasticsearch engine when returning results, and the date published is calculated based on page publication date. Enforcement Actions define their own ordering logic based on initial filing date. 

#### FilterablePagesDocumentSearch

FilterablePagesDocumentSearch is the core search class that is used across the majority of our searching. It is invoked from FilterableListForm. This search class defines the common structure for our search function, as well as the base logic for filtering against all common fields and logic behind our multi-match and ordering steps. The core function called from outside the class is the `search` function which properly chains all of our filter/match/sorting logic and returns the resulting list as a django queryset.

#### EventFilterablePagesDocumentSearch

EventFilterablePagesDocumentSearch is an extension of FilterablePagesDocumentSearch that defines behavior specific to our Event search. The class overwrites one method from its parent, the `filter_date` function to change the behavior to filter based on fields specific to events, the start and end date of an event.

#### EnforcementActionsFilterableListForm

EnforcementActionsFilterableListForm is an extension of FilterablePagesDocumentSearch that exposes some additional filter logic through the `apply_specific_filters` function. We also see that `filter_date` and `order_results` have been overwritten to leverage the enforcement action specific fields, initial filing date.