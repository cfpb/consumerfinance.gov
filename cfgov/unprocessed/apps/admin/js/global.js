// This is a workaround to an issue in fbjs.
// See https://github.com/facebook/fbjs/issues/290
// eslint-disable-next-line no-global-assign
global = globalThis;

const env = location.hostname.split('.')[0];

const body = document.querySelector('body');
body.setAttribute('data-env', env);

// Modify default document/image title generation to keep file extensions.
// See https://docs.wagtail.org/en/stable/advanced_topics/documents/title_generation_on_upload.html
// and https://docs.wagtail.org/en/stable/advanced_topics/images/title_generation_on_upload.html.
window.addEventListener('DOMContentLoaded', function () {
  const keepFilename = function (event) {
    event.detail.data.title = event.detail.filename;
  };

  document.addEventListener('wagtail:documents-upload', keepFilename);
  document.addEventListener('wagtail:images-upload', keepFilename);
});
