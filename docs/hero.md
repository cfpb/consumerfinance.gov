# hero.html

## CMS setup

The first thing you will need is hero content. Currently heroes are only
supported within WP views under the `related_hero` custom field. This points
to the slug of a hero and when `$sheer index` is run the contents of that hero
will be available for the view which contains it. For example if `related_hero`
is set for the `blog` view a `hero` propert will be added to the `blog` view
during the indexing process.

## Template setup

1. Add the hero block to your template.

        {% block hero -%}
        {%- endblock %}

2. In your template `import` the `hero.html` file and set it to the variable
   name `hero` like this:

        {% block hero -%}
            {% import "hero.html" as hero %}
        {%- endblock %}

3. Call the `hero.render` macro and pass it a `hero` property from a view. Also
   pass it the `post_macros` variable. That's it!

        {% block hero -%}
            {% import "hero.html" as hero %}
            {{ hero.render(view.hero, post_macros) }}
        {%- endblock %}
