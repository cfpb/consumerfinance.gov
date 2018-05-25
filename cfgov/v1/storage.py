import inspect

from storages.backends.s3boto import S3BotoStorage


class WagtailOverwritingStorageMixin(object):
    """Django storage mixin to support file overwriting in Wagtail 1.13+.

    The Django storage backend convention is that if a file is uploaded to a
    storage backend with the same name as another file already stored on that
    backend, the new file's name will be changed:

    https://docs.djangoproject.com/en/2.0/ref/files/storage/#django.core.files.storage.Storage.get_available_name

    Specifically, the new file will have random characters appended to its
    filename (for example, a second upload of "test.txt" would become something
    like "test_abcdefg.txt").

    The convention is that typically storage backends will not support
    deliberate overwriting of files that they store. However, there are some
    backends that can support this behavior; for example if users desire to
    maintain a consistent relationship between source filename and filename
    in storage.

    Wagtail 1.13 included changes that broke support for backends with this
    overwriting behavior for both documents and images:

    https://github.com/wagtail/wagtail/pull/3821
    https://github.com/wagtail/wagtail/pull/3822

    The goal of these changes was to clean up old document/image files after
    the user uploads a new one. Consider an existing document uploaded from
    some filename "test.txt"; the source file was "test.txt" and the file on
    the storage backend will be "test.txt". If a user uses the Wagtail UI to
    replace the document's file with a new file "test2.txt", the change in
    1.13 tries to clean up the old file by deleting "test.txt" from the storage
    backend after "test2.txt" has been stored.

    The Wagtail logic looks roughly like this:

        - user uploads a new file for an existing document/image
        - store the new file to the storage backend
        - delete the document/image's old file from the storage backend

    This logic is sound as long as it is safe to assume that new uploads with
    identical filenames never overwrite each other and always get assigned a
    unique filename when stored. However, as described above, this may not
    always be the case.

    If, instead, files get overwritten, then the final delete that happens
    will in fact delete the new file that's just been stored.

    This mixin attempts to prevent this from happening. It uses the Python
    stack inspect capability to identify if a delete call is being invoked
    from the Wagtail document/image edit views, and, if so, skips that delete.
    """
    def delete(self, name):
        stack = inspect.stack()

        if self._should_skip_wagtail_delete(stack):
            return

        super(WagtailOverwritingStorageMixin, self).delete(name)

    def _should_skip_wagtail_delete(self, stack):
        """Given a call stack, determine whether delete should be skipped."""

        # See Python inspect documentation for structure of stack object:
        # https://docs.python.org/2/library/inspect.html#the-interpreter-stack
        caller_frame_record = stack[1]
        caller_frame_object = caller_frame_record[0]
        caller_frame_function_name = caller_frame_record[3]

        caller_module = inspect.getmodule(caller_frame_object)
        caller_module_name = caller_module.__name__

        called_from = caller_module_name + '.' + caller_frame_function_name

        # Only skip delete if it is being called by the wagtaildocs.edit or
        # wagtailimages.edit views. We want deletes called from other places
        # to work as expected.
        skip_for_these_callers = (
            'wagtail.wagtaildocs.views.documents.edit',
            'wagtail.wagtailimages.views.images.edit',
        )

        if called_from not in skip_for_these_callers:
            return

        # We know this delete is being called from by specific Wagtail views of
        # interest. Grab the variables from the stack that contain the filename
        # of the document/image being replaced and the filename of the new
        # document/image with which it is being replaced.
        original_file = caller_frame_object.f_locals['original_file']
        doc = caller_frame_object.f_locals['doc']

        # If these two filenames are the same, we don't want to go ahead with
        # the delete, because that will remove the new file that's just been
        # provided to replace the old file.
        #
        # If these two filenames are different, we should go ahead with the
        # deletion, because the intended Wagtail behavior is to clean up
        # the old file that is being replaced.
        return original_file.name == doc.file.name


class OverwritingS3Storage(WagtailOverwritingStorageMixin, S3BotoStorage):
    """Boto-based S3 Django storage that supports overwriting from Wagtail.

    Based on the django-storages boto-based storage backend defined here:

    https://github.com/jschneier/django-storages

    This storage has a default setting AWS_S3_FILE_OVERWRITE=True that
    overwrites existing files when files with the same name are uploaded.

    This class adds v1.storage.WagtailOverwritingStorageMixin to support
    that use case when using this storage in Wagtail 1.13+.
    """
    pass
