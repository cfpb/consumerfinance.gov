from datetime import datetime
import sys


def handle_error(fn):
    """
    Will save a screenshot of the current page if the method fails
    """
    from functools import wraps

    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            return fn(*args, **kwargs)
        except Exception:
            filename = datetime.now().isoformat()
            print("kwargs: %s" % kwargs)
            try:
                args[0].base.get_screenshot(filename)
            except Exception:
                print ("HANDLER FAILURE:", sys.exc_info())

            raise

    return wrapper
