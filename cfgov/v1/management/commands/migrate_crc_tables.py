import re

from django.contrib.auth import get_user_model
from django.core.management.base import CommandError

import wagtail
from wagtail.actions.publish_page_revision import PublishPageRevisionAction
from wagtail.models import Page

import djclick as click

from v1.atomic_elements.tables import ConsumerReportingCompanyTable
from v1.models import DocumentDetailPage


User = get_user_model()


def locate_table_block(block):
    table_index = None

    for i, child_block in enumerate(block):
        if child_block.block_type != "table_block":
            continue

        if table_index is not None:
            raise RuntimeError("Multiple table blocks found")

        table_index = i

    return table_index


def locate_fwt_block_with_table_block(block):
    fwt_index = None
    fwt_table_index = None

    for i, child_block in enumerate(block):
        if child_block.block_type != "full_width_text":
            continue

        child_table_index = locate_table_block(child_block.value)

        if child_table_index is None:
            continue
        elif fwt_table_index is not None:
            raise RuntimeError("Multiple FWTs with table blocks found")

        fwt_index = i
        fwt_table_index = child_table_index

    return fwt_index, fwt_table_index


def extract_table_block_from_full_width_text(block):
    fwt_index, fwt_table_index = locate_fwt_block_with_table_block(block)

    if fwt_table_index is None:
        breakpoint()
        raise RuntimeError("Could not locate FWT with table block")

    fwt_block = block.pop(fwt_index)

    # Force population of the FWT block's raw data.
    fwt_block.value.raw_data[0]

    fwt_before = None
    fwt_after = None

    if fwt_table_index > 0:
        fwt_before = fwt_block.block.to_python(
            fwt_block.value.raw_data[:fwt_table_index]
        )

    if fwt_table_index < len(fwt_block.value) - 2:
        fwt_after = fwt_block.block.to_python(
            fwt_block.value.raw_data[fwt_table_index + 1 :]
        )

    table_block = fwt_block.value.pop(fwt_table_index)

    if fwt_after is not None:
        block.insert(fwt_index, ("full_width_text", fwt_after))

    block.insert(fwt_index, ("table_block", table_block.value))

    if fwt_before is not None:
        block.insert(fwt_index, ("full_width_text", fwt_before))


def fixup_spacing(s):
    s = re.sub(r"\s*(<|&lt;)/?br ?/?(>|&gt;)(</p>\s*<p>)?\s*", "<br/>", s)
    s = re.sub(r"\s*&nbsp;\s*", "", s)
    return s


def migrate_table_data(data):
    rows = data["data"]
    if len(rows) != 2 or len(rows[1]) != 3:
        raise RuntimeError("Unexpected table data format")

    website, phone, mailing_address = list(map(fixup_spacing, rows[1]))

    return {
        "website": website,
        "phone": phone,
        "mailing_address": mailing_address,
    }


def replace_table_block(block, table_index):
    table_block = block.pop(table_index)

    crc_table_data = migrate_table_data(table_block.value)

    crc_table_block = ConsumerReportingCompanyTable().to_python(crc_table_data)

    block.insert(table_index, ("crc_table", crc_table_block))


def edit_page_object(page):
    table_index = locate_table_block(page.content)

    if table_index is None:
        extract_table_block_from_full_width_text(page.content)

        table_index = locate_table_block(page.content)

        if table_index is None:
            raise RuntimeError(f"Can't locate table on page {page.url}")

    replace_table_block(page.content, table_index)

    return True


@click.command()
@click.argument("parent_page_id", type=int)
@click.argument("username")
@click.option("--dry-run", is_flag=True)
def command(parent_page_id, username, dry_run):
    parent_page = Page.objects.get(pk=parent_page_id).specific
    user = User.objects.get(**{User.USERNAME_FIELD: username})

    children = parent_page.get_children().type(DocumentDetailPage).specific()

    draft_children = children.filter(has_unpublished_changes=True)
    if draft_children.count():
        error = f"One or more pages under {parent_page.url} has unpublished changes: "
        error += ", ".join(
            f"{child.url} ({child.pk})" for child in draft_children
        )
        raise CommandError(error)

    for child in children:
        if wagtail.VERSION >= (4,):
            child = child.get_latest_revision_as_object()
        else:
            child = child.get_latest_revision_as_page()

        if not edit_page_object(child):
            continue

        if dry_run:
            continue

        revision = child.save_revision(user=user, log_action=True)

        action = PublishPageRevisionAction(revision, user=user, changed=True)
        action.execute(skip_permission_checks=True)
