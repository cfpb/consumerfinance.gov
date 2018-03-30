/**
 * Initialize the functionality of a group of tabs with content.
 */
function init() {
  const tabGroups = document.querySelectorAll( '.tabs-layout' );
  let tabContents;

  tabGroups.forEach( tabGroup => {
    tabContents = tabGroup.querySelectorAll( '.tab-content' );

    _bindTabLink( tabGroup, tabContents );

    // Hide all but the first tab.
    for ( let i = 1; i < tabContents.length; i++ ) {
      tabContents[i].classList.add( 'u-hidden' );
    }
  } );
}

/**
 * @param {HTMLNode} tabGroup - HTML element parent of tabs and tabs-content.
 * @param {HTMLNode} tabContents - HTML element for content in tabs.
 */
function _bindTabLink( tabGroup, tabContents ) {
  tabGroup.addEventListener( 'click', _tabLinkClicked );
  const tabs = tabGroup.querySelectorAll( '.tab-list' );

  /**
   * Handle a click of a tab.
   * @param {MouseEvent} evt - Event object for a click on a tab.
   */
  function _tabLinkClicked( evt ) {
    const target = evt.target;
    if ( target.tagName !== 'A' ) {
      return;
    }
    evt.preventDefault();

    const tabLi = target.parentNode;
    const current = tabGroup.querySelector( target.getAttribute( 'href' ) );

    tabs.forEach( tab => tab.classList.remove( 'active-tab' ) );
    tabLi.classList.add( 'active-tab' );
    tabContents.forEach( tabContent => tabContent.classList.add( 'u-hidden' ) );
    current.classList.remove( 'u-hidden' );
  }
}

module.exports = { init };
