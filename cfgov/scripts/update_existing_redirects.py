from wagtail.contrib.redirects.models import Redirect


outdated_patterns = [('/policy-compliance/guidance', '/compliance')]


# This script is for use on November 25, 2020, when we'll be migrating
# cf.gov to a new IA. Delete this script after the migration is done.
# Run this from the command line with this:
#   cfgov/manage.py runscript update_existing_redirects
#   cfgov/manage.py runscript update_existing_redirects --script-args update
def run(*args):
    if 'update' in args:
        dry_run = False
    else:
        dry_run = True

    for (old_pattern, new_pattern) in outdated_patterns:
        matching_redirects = Redirect.objects.filter(
            old_path__startswith=old_pattern
        )
        total = len(matching_redirects)

        for redirect in matching_redirects:
            old_path = redirect.old_path
            updated_path = old_path.replace(old_pattern, new_pattern)
            if dry_run:
                print(f'{old_path} -> {updated_path}')
            else:
                print(f"updating {old_path} -> {updated_path}")
                redirect.old_path = updated_path
                redirect.save()

        if dry_run:
            print(f'\n\nSummary: Would update {total} redirects matching {old_pattern}')  # noqa E501
            print('run the following command to update them:')
            print('  ./cfgov/manage.py runscript update_existing_redirects --script-args update')  # noqa E501
        else:
            print(f'\n\nSummary: Updated {total} redirects')
