import { add } from 'stickyfilljs';

const sticky = {
  init: () => {
    const stickies = document.querySelectorAll('[data-sticky]');

    add(stickies);
  },
};

export default sticky;
