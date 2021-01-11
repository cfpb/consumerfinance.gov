from elasticsearch_dsl import connections
from watchman.decorators import check


@check
def elasticsearch_health():
    es = connections.get_connection()
    health = es.cluster.health(level="shards")

    if (health["timed_out"] or health["status"] != "green"):
        ok = False
    else:
        ok = True

    return {"elasticsearch": {"ok": ok, "health": health}}
