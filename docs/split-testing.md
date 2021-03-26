# Setting up a split testing experiment

One thing we like to do from time to time is test changes
on specific groups of pages and see how they perform.
We call this "split testing".
In contrast to traditional A/B testing,
where the change being tested is shown to a portion of the _audience_,
in the case of split testing,
the change is shown to everyone, but only on a subset of similar pages
(e.g., a group of related Ask CFPB answers).
We call this a subset of pages a "cluster".


## So you've been asked to set up a split testing experiment

Good news! The infrastructure has been put in place for you to do it easily.
It's set up so that the code being tested is isolated by a feature flag.
If you're not familiar with how our flags are set up,
[read the concepts overview in the django-flags concepts](https://cfpb.github.io/django-flags/#concepts).

### The flag condition

In order to check whether or not a page is part of a split testing cluster,
we registered a new flag condition in `cfgov/core/feature_flags.py`.

```python
@conditions.register('in split testing cluster')
def in_split_testing_cluster(cluster_group, page, clusters=CLUSTERS, **kwargs):
    cluster_group = clusters[cluster_group]
    lookup_value = getattr(page, 'split_test_id', page.id)
    return lookup_value in chain(*cluster_group.values())
```

This condition takes the following arguments:
- `cluster_group`: A string that identifies which group of clusters we want
  to check
- `page`: An instance of a Wagtail page that we want to look for in the
  cluster group
- `clusters`: A dictionary containing one or more named `cluster_group`s –
  by default, this points to a dictionary defined in our main cluster
  definition file (see ["Defining clusters"](#defining-clusters) below)

If the `page`'s `id` property is found in the `cluster_group`,
the condition returns `True`.
If the page has a `split_test_id` property defined, it will check that
instead of `page.id`. (More on that later.)

You do not need to modify anything in this file to set up a new experiment.

### Defining clusters

To run a split test we first have to know what pages we're testing.
Split testing clusters are typically defined in our main cluster definition
file at `cfgov/core/split_testing_clusters.py`.

Create a new dictionary with a meaningful name
and add the page IDs for the pages in your cluster(s) to it.
For example:

```python
ASK_CFPB_H1 = {
    18: [
        103, 160, 187, 337, 731, 767, 951, 1157, 1161, 1403, 1405, 1439, 1447,
        1567, 1695,
    ],
    34: [
        104, 105, 130, 205, 747, 841, 1423, 1791,
    ],
    38: [
        143, 184, 329, 331, 1165, 1637, 1787, 1789, 1797, 1921, 1923,
    ],
    49: [
        136, 161, 163, 164, 172, 176, 179, 180, 181, 188, 192, 336, 817, 1699,
        1983, 1989, 1995, 1997, 2001,
    ],
    93: [
        146, 226, 237, 318, 338, 545, 633, 811, 1215, 1463, 1507,
    ],
}
```

In the above example, there are five separate clusters,
_all_ of which will be part of the experiment.
The number being used for the keys doesn't matter to Python,
but it may be useful for internal tracking purposes.

As noted earlier, normally the page IDs inside the lists correspond to
Wagtail's page ID (most easily findable in the edit URL for a page),
but in this particular example, they are actually **Ask CFPB answer IDs**.
For Ask CFPB answer pages, we use the answer ID,
because that ID is frequently used in internal communications
for shorthand references to Ask answers.
All other page types use their Wagtail page ID value.

If you have cause to use something else for the lookup values,
you can define the `split_test_id` property in a page class.
For example:

```python
# cfgov/ask_cfpb/models/pages.py

class AnswerPage(CFGOVPage):
…
    # Overrides the default of page.id for comparing against split testing
    # clusters. See: core.feature_flags.in_split_testing_cluster
    @property
    def split_test_id(self):
        return self.answer_base.id
…
```

If you do this, remember to add a simple test:

```python
# cfgov/ask_cfpb/tests/models/test_pages.py

def test_answer_split_testing_id(self):
    """Confirm AnswerPage's split_testing_id is set to its answer_base.id,
    which is checked by the core.feature_flags.in_split_testing_cluster
    flag condition when doing split testing on Ask CFPB answer pages."""
    answer = self.answer1234
    page = answer.english_page
    self.assertEqual(page.split_test_id, answer.id)
```

You will also need to add a reference to your new dictionary
to the `CLUSTERS` dictionary at the bottom of the file:

```python
CLUSTERS = {
    'ASK_CFPB_H1': ASK_CFPB_H1,
}
```

### Creating and using the flag

[The new "in split testing cluster" condition](#the-flag-condition)
described earlier can be added to flags and used like any other feature flag.
For the example we started above, we first create the flag in our settings,
giving it the default condition with a parameter corresponding to the
cluster group name we created above:

```python
# cfgov/settings/base.py

…

# Feature flags
# All feature flags must be listed here with a dict of any hard-coded
# conditions or an empty dict. If the conditions dict is empty the flag will
# only be enabled if database conditions are added.
FLAGS = {
    …
    # SPLIT TESTING FLAGS

    # Ask CFPB page titles as H1s instead of H2s
    'ASK_CFPB_H1': {
        'in split testing cluster': 'ASK_CFPB_H1'
    },
    …
}

…
```

And then in our template we check the flag, passing in the current `page`,
and if the page's answer ID is found in a cluster, `flag_enabled()` is `True`,
and we see the `<h1>` instead of the `<h2>`.

```html
<!-- cfgov/jinja2/v1/ask-cfpb/answer-page.html -->

…

{% if flag_enabled('ASK_CFPB_H1', page=page) %}
    <h1>{{ page.question | striptags }}</h1>
{% else %}
    <h2>{{ page.question | striptags }}</h2>
{% endif %}

…
```

Setting the flag up with the default condition of `in_split_testing_cluster`
means that as soon as the code is deployed,
the flag is acting on pages in the cluster.

One the results of the test are known, you can set a new boolean flag condition
in Wagtail to have the flag always be `True`, if the test was successful,
or always be `False`, if the test was not successful.
This will make (or not make) the change on all pages touched by that flag
until you take the time to remove the flag entirely.
