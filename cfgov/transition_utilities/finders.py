from django.contrib.staticfiles.finders import FileSystemFinder


class NoPHPFileSystemFinder(FileSystemFinder):
    def find(self, path, all=False):
        if path.lower().endswith('.php'):
            return []
        else:
            return super(NoPHPFileSystemFinder, self).find(path, all=False)

    def list(self, ignore_patterns):
        ignore_patterns.append('*.php')
        return super(NoPHPFileSystemFinder, self).list(ignore_patterns)
