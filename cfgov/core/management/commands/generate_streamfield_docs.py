import argparse
from collections import defaultdict

from django.apps import apps
from django.core.management.base import BaseCommand
from django.template import loader

from wagtail.wagtailcore.blocks import StreamBlock
from wagtail.wagtailcore.fields import StreamField
from wagtail.wagtailcore.models import Page


class Command(BaseCommand):
    help = 'Generate Wagtail StreamField block documentation'

    def add_arguments(self, parser):
        parser.add_argument('-o', '--output-file', type=argparse.FileType('w'),
                            default='-')

    def handle(self, *args, **options):
        blocks, models = get_blocks_and_models()

        template = loader.get_template('core/docs/streamfield-blocks.md')
        md = template.render({
            'blocks': blocks,
            'models': models,
        })

        options['output_file'].write(md)


def get_blocks_and_models():
    """Collect StreamField blocks and models with StreamFields."""
    blocks = defaultdict(dict)
    models = []

    for app_config in apps.get_app_configs():
        if app_config.name.startswith('wagtail'):
            continue

        for model in app_config.get_models():
            streamfields = []

            if model._meta.abstract:
                continue

            if issubclass(model, Page) and not model.is_creatable:
                continue

            for field in model._meta.fields:
                if not isinstance(field, StreamField):
                    continue

                field_name = '.'.join([
                    model.__module__,
                    model.__name__,
                    field.name,
                ])

                child_blocks = get_child_blocks(field.stream_block)

                field_blocks = []
                for block in child_blocks:
                    block_name = get_block_name(block)
                    block_fullname = get_block_fullname(block)

                    block_data = blocks.setdefault(block_name, {
                        'name': block_name,
                        'fullname': block_fullname,
                        'module': block.__module__,
                        'docstring': block.__doc__,
                        'template': getattr(block.meta, 'template', None),
                        'fields': set(),
                    })

                    block_data['fields'].add(field_name)

                    field_blocks.append(block_fullname)

                field_data = {
                    'name': field_name,
                    'required': not field.blank,
                    'blocks': field_blocks,
                }

                streamfields.append(field_data)

            if streamfields:
                models.append({
                    'name': model.__name__,
                    'fullname': model.__module__ + '.' + model.__name__,
                    'docstring': model.__doc__,
                    'ispage': issubclass(model, Page),
                    'streamfields': streamfields,
                })

    for block in blocks.values():
        block['fields'] = sorted(block['fields'])

    return list(blocks.values()), models


def get_block_name(block):
    return block.__class__.__name__


def get_block_fullname(block):
    return '.'.join([
        block.__class__.__module__,
        get_block_name(block),
    ])


def get_child_blocks(block, seen=None):
    if seen is None:
        seen = set()

    block_fullname = get_block_fullname(block)

    if block_fullname in seen:
        return []

    seen.add(block_fullname)

    if not isinstance(block, StreamBlock):
        child_blocks = [block]
    else:
        child_blocks = list(block.child_blocks.values())
        for child_block in child_blocks:
            child_blocks.extend(get_child_blocks(child_block, seen=seen))

    return child_blocks
