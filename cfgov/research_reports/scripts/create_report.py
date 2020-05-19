import subprocess

from v1.models.base import CFGOVPage
from v1.models.browse_page import BrowsePage

trial_identifier="programmatic-trial-4"
reports_parent_page = CFGOVPage.objects.get(id=1113)
existing_report = BrowsePage.objects.get(id=13966)   # barf

def get_pandoc_output(report_file_location):
    pandoc_command = ["pandoc", "-f", "docx", "-t", "html", "--standalone", report_file_location]
    result = subprocess.run(pandoc_command, stdout=subprocess.PIPE, universal_newlines=True)
    return result.stdout


def copy_existing_report():
    new_attrs = {"title": trial_identifier, "slug": trial_identifier}
    return existing_report.copy(keep_live=False, copy_revisions=False, update_attrs=new_attrs)

def update_content_block(page, new_content):
    page.content.stream_data[0]['value'] = new_content

def save_page(page, publish=False):
    revision = page.save_revision()
    page.save()
    if publish:
        revision.publish()


# Invoke this script from the cfgov-refresh root with this command:
#     cfgov/manage.py runscript create_report --script-args word/doc/file/location.docx
def run(*args):
    docx_report_location = args[0]
    print(" *** running pandoc conversion... ***")
    new_content = get_pandoc_output(docx_report_location)
    print(" *** making a new page (copying existing report) ***")
    new_report = copy_existing_report()
    print(" *** customizing the new page with pandoc output ***")
    update_content_block(new_report, new_content)
    print(" *** saving the new page ***")
    save_page(new_report, True)


# parent.add_child(instance=pg)
# https://speakerdeck.com/williln/what-the-wagtail-docs-dont-tell-you?slide=34
