import json


def update_existing_page(target, existing_page, new_root):
    # perform a little surgery on the content json
    # maybe there's a better way?
    content_dict = json.loads(existing_page.specific.to_json())
    content_dict['url_path'] = target.url_path
    content_dict['pk'] = target.pk

    if target == new_root:
        # We're editing a root page. Exciting!
        # Let's not change the title or slug
        content_dict['title'] = target.title
        content_dict['slug'] = target.slug

    updated_json = json.dumps(content_dict)
    new_revision = target.revisions.create(content_json=updated_json)
    new_revision.publish()
    return target


def copy_into(target, existing_page, new_root):
    return existing_page.copy(to=target)
