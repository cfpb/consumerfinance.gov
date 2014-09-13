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

2. Within the hero block create a variable called `hero` and set it the `hero`
   property of the view it is associated with.

        {% block hero -%}
            {% set hero = get_document('views', 'blog').hero %}
        {%- endblock %}

3. Include the `hero.html` file.

        {% block hero -%}
            {% set hero = get_document('views', 'blog').hero %}
            {% include "hero.html" %}
        {%- endblock %}
