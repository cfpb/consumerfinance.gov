let tabGroups;
let tabLinks;
let tabContents;

/**
 * Initialize the functionality of a group of tabs with content.
 */
function init() {
  tabGroups = document.querySelectorAll( '.tabs-layout' );

  tabGroups.forEach( tabGroup => {
    tabLinks = tabGroup.querySelectorAll( '.tab-link' );
    tabContents = tabGroup.querySelectorAll( '.tab-content' );

    tabLinks.forEach( tabLink => {
      _bindTabLink( tabGroup, tabLink, tabContents );
    } );

    // Hide all but the first tab.
    for ( let i = 1; i < tabContents.length; i++ ) {
      tabContents[i].classList.add( 'u-hidden' );
    }
  } );
}

/**
 *
 * @param {HTMLNode} tabGroup - HTML element parent of tabs and tabs-content.
 * @param {HTMLNode} tabLink - HTML element for links in tabs.
 */
function _bindTabLink( tabGroup, tabLink, tabContents ) {
  tabLink.addEventListener( 'click', _tabLinkClicked );
  const tabs = tabGroup.querySelectorAll( '.tab-list' );

  /**
   * Handle a click of a tab.
   * @param {MouseEvent} evt - Event object for a click on a tab.
   */
  function _tabLinkClicked( evt ) {
    evt.preventDefault();

    const target = evt.target;
    const tabLi = target.parentNode;
    const current = tabGroup.querySelector( target.getAttribute( 'href' ) );

    tabs.forEach( tab => tab.classList.remove( 'active-tab' ) );
    tabLi.classList.add( 'active-tab' );
    tabContents.forEach( tabContent => tabContent.classList.add( 'u-hidden' ) );
    current.classList.remove( 'u-hidden' );
  }
}

module.exports = { init };
