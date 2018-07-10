from threading import local


_active = local()


def get_request():
    return _active.request
