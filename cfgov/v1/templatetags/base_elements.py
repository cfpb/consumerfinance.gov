"""Render website base template elements using Django templates.

Certain cf.gov base template elements are written in the Jinja2 template
language and are typically rendered as part of a Jinja2 template. This module
makes these template elements available to the Django template engine as well
through Django template tags. This allows for inclusion of these template
element even on pages that aren't rendered using the Jinja2 engine.

These elements include:

    - The page header.
    - The page footer.
    - Code that includes Modernizr.js and disables JS where appropriate.

An example Django template using these might look like:

    {% load base_elements %}

    {% include_header %}
    {% include_modernizr %}

    /* Other content here */

    {% include_footer %}

"""
from django import template
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe


register = template.Library()


def _render_jinja_template(template_name, context):
    html = render_to_string(
        template_name, context=context.flatten(), using="wagtail-env"
    )

    return mark_safe(html)


@register.simple_tag(takes_context=True)
def include_header(context):
    return _render_jinja_template("v1/header.html", context)


@register.simple_tag(takes_context=True)
def include_footer(context):
    return _render_jinja_template("v1/footer.html", context)


@register.simple_tag(takes_context=True)
def include_modernizr(context):
    return _render_jinja_template("v1/modernizr.html", context)
