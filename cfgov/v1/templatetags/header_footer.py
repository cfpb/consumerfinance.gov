"""Render the website header and footer using Django templates.

The cf.gov header and footer templates are written in the Jinja2 template
language and are typically rendered as part of a Jinja2 template. This module
makes the hader and footer available to the Django template engine as well,
through two Django template tags. This allows for a custom header and footer
even on pages that aren't rendered using the Jinja2 engine.

An example Django template using these might look like:

    {% load header_footer %}

    {% include_header %}

    /* Other content here */

    {% include_footer %}

"""
from django import template
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe


register = template.Library()


def _render_jinja_template(template_name, context):
    html = render_to_string(
        template_name,
        context=context.flatten(),
        using='wagtail-env'
    )

    return mark_safe(html)


@register.simple_tag(takes_context=True)
def include_header(context):
    return _render_jinja_template('v1/header.html', context)


@register.simple_tag(takes_context=True)
def include_footer(context):
    return _render_jinja_template('v1/footer.html', context)
