# layout-side-nav.html

## Setup

The following set up is needed to use this template.

1. In your directory, for example in /newsroom/, create a section-vars.html
   file with the following variables:

        {% set path = "/newsroom/" %}
        {% set nav_items = [
            (path, "index", "Newsroom"),
            (path + "press-resources/", "press-resources", "Press resources")
        ] -%}

   Each object in the `nav_items` array should follow this structure:
   HREF, ID, CAPTION. Edit and add to this array to list all of the pages
   that you want to represent in the side navigation.

2. Then create a new template with the following two lines at the top of the
   file.

        {% extends "layout-side-nav.html" %}
        {% import "section-vars.html" as section_vars %}

   Note that it's important that you import section-vars.html as
   `section_vars`.

## The active nav item state

- By default the active nav item is the nav item with the ID of `index`.
- To set a new active nav item create a global variable called
  `active_nav_id` in your page. Set it equal to the ID of the nav item that
  you want to be active. Using the example above we can make Press resources
  the active page by setting the following in the Press resources HTML file:

        {% set active_nav_id = "press-resources" -%}
