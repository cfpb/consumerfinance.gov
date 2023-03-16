// This is a workaround to an issue in fbjs.
// See https://github.com/facebook/fbjs/issues/290
global = globalThis;

const env = location.hostname.split('.')[0];

const body = document.querySelector('body');
body.setAttribute('data-env', env);
