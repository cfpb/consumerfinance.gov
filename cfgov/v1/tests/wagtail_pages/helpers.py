from wagtail.wagtailcore.blocks import StreamValue

from v1.models.home_page import HomePage


def save_page(page):
    page.save()
    return page.save_revision()


def save_new_page(child, root=None):
    if not root:
        root = HomePage.objects.get(title='CFGov')
    root.add_child(instance=child)
    return save_page(page=child)


def publish_page(child):
    revision = save_new_page(child=child)
    revision.publish()


def publish_changes(child):
    revision = save_page(page=child)
    revision.publish()


def set_page_stream_data(page, field_name, stream_data):
    field = getattr(page, field_name)
    stream_block = field.stream_block
    stream_value = StreamValue(stream_block, stream_data, is_lazy=True)
    setattr(page, field_name, stream_value)

    save_page(page)


def get_page_stream_data(page, field_name):
    field = getattr(page, field_name)
    return field.stream_data
