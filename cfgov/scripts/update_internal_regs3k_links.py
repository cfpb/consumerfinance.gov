import logging

from regulations3k.models.django import Section


logger = logging.getLogger(__name__)


# This is a one-time script to update internal links within the Regs3k tool
# that were outdated when the regulations tool moved to a new URL,
# /policy-compliance/rulemaking/regulations/ to /rules-policy/regulations/.
# Delete this script after running it in Production, December 2020.
# Run it with the following command:
# cfgov/manage.py runscript update_internal_regs3k_links
def run():
    count = 0
    url_base = "/policy-compliance/rulemaking/regulations/"
    for section in Section.objects.all():
        # First, update any links to this reg section
        # /policy-compliance/rulemaking/regulations/[part]/[section]/#[pg]
        # to ../[section]/#[pg]
        part = section.subpart.label
        this_section = url_base + part + "/"
        update1 = section.contents.replace(this_section, "../")

        # Next, update any links to other reg sections
        # /policy-compliance/rulemaking/regulations/[part]/[section]/#[pg]
        # to ../../[part]/[section]/#[pg]
        update2 = update1.replace(url_base, "../../")

        section.contents = update2
        section.save()
        count += 1

    logger.info(f"Updated {count} regulation sections")
