from paying_for_college.models import Notification, Program


error_msg = (
    "The only purge arguments that can be passed "
    "are 'notifications', 'programs' and 'test-programs'"
)
no_args_msg = (
    "You must supply an object type to purge: "
    "notifications, programs or test-programs"
)
object_map = {
    "notifications": Notification.objects.all(),
    "programs": Program.objects.all(),
    "test-programs": Program.objects.filter(test=True),
}


def purge(objects):
    """purge notification or program data"""
    objects = objects.lower()
    if not objects:
        return no_args_msg
    if objects not in object_map:
        return error_msg
    queryset = object_map[objects]
    msg = f"Purging {queryset.count()} {objects}"
    queryset.delete()
    return msg
