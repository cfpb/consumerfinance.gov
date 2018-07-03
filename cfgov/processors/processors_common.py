replacements = (
    ('/blog/', '/about-us/blog/'),
    ('/pressrelease/', '/about-us/newsroom/'),
    ('/speeches/', '/about-us/newsroom/'),
    ('/newsroom/', '/about-us/newsroom/'),
)


def update_path(path):
    for pattern, substitute in replacements:
        if path.startswith(pattern):
            new_path = path.replace(pattern, substitute)
            return new_path
    return path
