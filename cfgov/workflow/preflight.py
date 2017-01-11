from django.core.exceptions import ObjectDoesNotExist

from workflow import strategies


class PreflightCheckFailed(Exception):
    pass


def preflight_check(page, new_root, relative_path):
    # the last value will always be an empty string
    path_components = relative_path.split('/')[:-1]

    parent = new_root

    if len(path_components) == 0:
        return strategies.update_existing_page, new_root

    if len(path_components) > 1:
        for slug in path_components[:-1]:
            parent = parent.get_children().get(slug=slug)

    new_slug = path_components[-1]

    try:
        existing_page = parent.get_children().get(slug=new_slug)
        if not isinstance(existing_page.specific, type(page.specific)):
            raise PreflightCheckFailed
        return strategies.update_existing_page, existing_page

    except ObjectDoesNotExist:
        return strategies.copy_into, parent
