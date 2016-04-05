from bs4 import BeautifulSoup
from urlparse import urlsplit, urlunsplit

replacements = (('/blog/', '/about-us/blog/'),
                ('/pressrelease/','/about-us/newsroom/'),
                ('/speeches/','/about-us/newsroom/'),
                ('/newsroom/','/about-us/newsroom/'),
                )

def update_path(path):
    for pattern, substitute in replacements:
        if path.startswith(pattern):
            new_path = path.replace(pattern,substitute)
            return new_path
    return path

def fix_links(html):
    soup = BeautifulSoup(html, 'html.parser')
    for link in soup.findAll('a'):
        try:
            urldata = urlsplit(link['href'])
            new_path = update_path(urldata.path)
            new_href = urlunsplit((None, None, urldata.path, urldata.query,
                                  urldata.fragment))
            link['href'] = new_href
        except KeyError:
            # this means there's no href-- perhaps an <a name="foo"> link
            continue

    return soup.encode(formatter="html")
