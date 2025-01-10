from django.core.management.base import BaseCommand, CommandError

from wagtail.models import Page


class Command(BaseCommand):
    help = "Delete a Wagtail page or its children"

    def add_arguments(self, parser):
        parser.add_argument(
            "--slug",
            nargs="?",
            help="The slug for the page you wish to delete",
        )
        parser.add_argument(
            "--id", nargs="?", help="The ID for the page you wish to delete"
        )
        parser.add_argument("--children-only", action="store_true")
        parser.add_argument("--dry-run", action="store_true")

    def handle(self, *args, **options):
        slug = options["slug"]
        page_id = options["id"]
        children_only = options["children_only"]
        dry_run = options["dry_run"]

        if (slug is not None and page_id is not None) or (
            slug is None and page_id is None
        ):
            raise CommandError("Must supply a unique page slug or a page ID")

        if slug:
            page = Page.objects.get(slug=slug)
        else:
            page = Page.objects.get(pk=page_id)

        self.stdout.write(
            f"Deleting{' children of' if children_only else ''} "
            f'page "{page.title}", ID {page.pk}, slug {page.slug}'
        )

        if dry_run:
            self.stdout.write("Dry run, skipping delete.")
            return

        if children_only:
            page.get_descendants(inclusive=False).delete()
        else:
            page.delete()
