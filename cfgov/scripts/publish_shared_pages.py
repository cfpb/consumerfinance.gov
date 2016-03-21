import json
from v1.models import CFGOVPage

def run():
    for page in CFGOVPage.objects.shared():
        page.live = True
        page.save()
        latest = page.get_latest_revision()
        content_json = json.loads(latest.content_json)
        content_json['live'] = True
        latest.content_json = json.dumps(content_json)
        latest.save()
