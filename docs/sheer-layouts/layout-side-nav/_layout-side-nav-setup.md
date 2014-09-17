
## Template setup

1. In your section's directory create a _section-NAME.html file with the
   following variables:

        {% raw -%}
        {% set path = "/MY-NEW-SECTION/" %}
        {% set nav_items = [
            (path, "index", "My new section"),
            (path + "some-other-page/", "some-other-page", "Some other page")
        ] %}
        {%- endraw %}

   Each object in the `nav_items` array should follow this structure:
   HREF, ID, CAPTION. Edit and add to this array to list all of the pages
   that you want to represent in the side navigation.

2. Create a new template with the following two lines at the top of the file:

        {% raw -%}
        {% extends "layout-side-nav.html" %}
        {% import "_section-NAME.html" as section %}
        {%- endraw %}

   It's important that you import _section-NAME.html as `section`.

3. That's all you need. `layout-side-nav.html` look in the `section` variable
   for the `nav_items` variable and will automatically add the `side_nav` macro
   to the `content_sidebar` Jinja block. If you need to add content to the
   `content_sidebar` block please make sure to call
   {% raw %}`{{ super() }}`{% endraw %} so you don't overwrite the nav content.

## The active nav item state

- By default the active nav item is the nav item with the ID of `index`.
- To set a new active nav item create a global variable called `active_nav_id`
  in your template. Set it equal to the ID of the nav item that you want to be
  active. Using the example above we can make Press resources the active page by
  setting the following in the Press resources HTML file:

        {% raw -%}
        {% set active_nav_id = "press-resources" %}
        {%- endraw %}
