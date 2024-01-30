/**
 * Initialize the functionality of a group of tabs with content.
 */
function init() {
  const tabGroups = document.querySelectorAll('.tabs-layout');
  let tabContents;

  let tabGroup;
  // forEach could be used here, but it's not supported in IE11.
  for (let i = 0, len = tabGroups.length; i < len; i++) {
    tabGroup = tabGroups[i];
    tabContents = tabGroup.querySelectorAll('.tab-content');
    tabGroup.querySelectorAll('.tab-content');

    _bindTabLink(tabGroup, tabContents);

    // Hide all but the first tab.
    for (let j = 1; j < tabContents.length; j++) {
      tabContents[j].classList.add('u-hidden');
    }
  }
}

/**
 * @param {HTMLElement} tabGroup - HTML element parent of tabs and tabs-content.
 * @param {HTMLElement} tabContents - HTML element for content in tabs.
 */
function _bindTabLink(tabGroup, tabContents) {
  tabGroup.addEventListener('click', _tabLinkClicked);
  const tabs = tabGroup.querySelectorAll('.tab-list');

  /**
   * Handle a click of a tab.
   * @param {MouseEvent} evt - Event object for a click on a tab.
   */
  function _tabLinkClicked(evt) {
    const target = evt.target;

    if (target.classList.contains('tab-link') === false) {
      return;
    }
    evt.preventDefault();

    const tabLi = target.parentNode;
    const current = tabGroup.querySelector(target.getAttribute('href'));

    // forEach could be used here, but it's not supported in IE11.
    for (let i = 0, len = tabs.length; i < len; i++) {
      tabs[i].classList.remove('active-tab');
    }
    tabLi.classList.add('active-tab');

    // forEach could be used here, but it's not supported in IE11.
    for (let j = 0, len = tabContents.length; j < len; j++) {
      tabContents[j].classList.add('u-hidden');
    }
    current.classList.remove('u-hidden');
  }
}

export { init };
