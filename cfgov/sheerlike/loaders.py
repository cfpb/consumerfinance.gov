from jinja2.loaders import FileSystemLoader


class FslibLoader(FileSystemLoader):

    def __init__(self, searchpath, mnt, encoding='utf-8', followlinks=False):
        self.mnt = mnt

    @property
    def searchpath(self):
        return self._searchpath

    @searchpath.setter
    def searchpath(self, paths):
        self._searchpath = paths
