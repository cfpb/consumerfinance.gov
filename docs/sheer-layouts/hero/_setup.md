# hero.html

## CMS setup

The first thing you will need is hero content. Currently heroes are only
supported within WP views under the `related_hero` custom field. This points
to the slug of a hero and when `$sheer index` is run the contents of that hero
will be available for the view which contains it. For example if `related_hero`
is set for the `blog` view a `hero` propert will be added to the `blog` view
during the indexing process.

## Template setup

1. Import `hero.html` and set it to `hero`.

        {% import "hero.html" as hero %}

2. Import `post_macros.html` and set it to `post_macros`.

        {% import "hero.html" as hero %}
        {% import "post-macros.html" as post_macros with context %}

3. Add the hero block to your template and call the `hero.render()` macro. Pass
   it a `hero` property from a view and the `post_macros` variable.

        {% block hero %}
            {{ hero.render(view.hero, post_macros) }}
        {% endblock %}
