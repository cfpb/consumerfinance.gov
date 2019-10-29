import Expandable from 'cf-expandables/src/Expandable';

const BUTTON_TEXT_SELECTOR = 'button .o-expandable_cue-open > span';
const TEXT_TO_REPLACE = 'Show';
const BUTTON_TEXT = 'Learn more';

const expandables = Array.prototype.slice.call(
  document.querySelectorAll(
    `${Expandable.prototype.ui.base}`
  )
);

expandables.forEach(expandable => {
  const openTextEl = expandable.element.querySelector(BUTTON_TEXT_SELECTOR);
  const openText = openTextEl.textContent;

  if (openText.indexOf(TEXT_TO_REPLACE) !== '-1') {
    openText.textContent = BUTTON_TEXT;
  }
});
