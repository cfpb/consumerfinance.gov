from v1.models import CFGOVPage

def run():
    for page in CFGOVPage.objects.shared():
        revision = page.get_latest_revision()
        revision.publish()
