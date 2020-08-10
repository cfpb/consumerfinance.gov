import {
  addEventListenerToSelector,
  track
} from './util/analytics-util';

/*
Buying a House /owning-a-home/loan-estimate/
Buying a House /owning-a-home/closing-disclosure/
*/

export default function( label ) {

  const trackingLabel = `${ label } Interaction`;

  const expandableStates = {};
  let lastExpandable;

  /**
   * Record state (expanded or collapsed) of expandables.
   * @param {string} id - The unique HTML ID of an expandable.
   */
  function recordExpandableState( id ) {
    if ( !expandableStates[id] ) {
      expandableStates[id] = true;
    } else if ( lastExpandable === id ) {
      expandableStates[id] = !expandableStates[id];
    }
    lastExpandable = id;
  }

  /**
   * Record state (expanded or collapsed) of expandables.
   * @param {string} expandable - An expandable HTML element.
   * @returns {boolean} True if the expandable is animating, false otherwise.
   */
  function isAnimatingExpandable( expandable ) {
    let isAnimating = false;

    if ( expandable.classList.contains( 'o-expandable__expanding' ) ||
         expandable.classList.contains( 'o-expandable__collapsing' ) ) {
      isAnimating = true;
    }

    return isAnimating;
  }

  /**
   * @param {MouseEvent} event - Mouse event from the click.
   */
  function trackTabLinkClick( event ) {
    const target = event.target;
    const text = target.textContent.trim();
    track( trackingLabel, 'Tab click', text );
  }

  /**
   * @param {MouseEvent} event - Mouse event from the click.
   */
  function trackFormExplainerPageLinkClick( event ) {
    const target = event.target;
    const pageNumber = 'Page ' + target.getAttribute( 'data-page' );
    track( trackingLabel, 'Page link click', pageNumber );
  }

  /**
   * @param {MouseEvent} event - Mouse event from the click.
   */
  function trackFormExplainerPageButtonClick( event ) {
    const target = event.currentTarget;
    const currentPageDom =
      document.querySelector( '.form-explainer_page-link.current-page' );
    const currentPage = 'Page ' + currentPageDom.getAttribute( 'data-page' );
    let action = 'Next Page button clicked';
    if ( target.classList.contains( 'prev' ) ) {
      action = 'Previous Page button clicked';
    }
    track( trackingLabel, action, currentPage );
  }

  /**
   * @param {MouseEvent} event - Mouse event from the click.
   */
  function trackExpandableTargetsClick( event ) {
    const elem = event.currentTarget;
    const expandable = elem.parentNode;
    const expandableID = expandable.id;
    if ( isAnimatingExpandable( expandable ) ) { return; }
    recordExpandableState( expandableID );

    const tab = document.querySelector( '.active-tab' );
    const tabText = tab.querySelector( '.tab-label' ).textContent.trim();
    let action = 'Expandable collapsed - ' + tabText;
    const label = elem.querySelector( '.o-expandable_label' );
    const text = label.textContent.trim();
    if ( expandableStates[expandableID] === true ) {
      action = 'Expandable expanded - ' + tabText;
    }
    track( trackingLabel, action, text );
  }

  /**
   * @param {MouseEvent} event - Mouse event from the click.
   */
  function trackImageMapOverlayClick( event ) {
    const target = event.target;
    const href = target.getAttribute( 'href' );
    const text = target.textContent.trim();

    let action = 'Image Overlay click - expandable collapsed';
    const expandable = document.querySelector( href );
    const expandableID = expandable.id;
    if ( isAnimatingExpandable( expandable ) ) { return; }
    recordExpandableState( expandableID );
    if ( expandableStates[expandableID] === true ) {
      action = 'Image Overlay click - expandable expanded';
    }
    track( trackingLabel, action, text );
  }

  addEventListenerToSelector(
    '.tab-link', 'click', trackTabLinkClick
  );
  addEventListenerToSelector(
    '.form-explainer_page-link', 'click', trackFormExplainerPageLinkClick
  );
  addEventListenerToSelector(
    '.form-explainer_page-buttons button', 'click',
    trackFormExplainerPageButtonClick
  );
  addEventListenerToSelector(
    '.o-expandable_target', 'mouseup', trackExpandableTargetsClick
  );
  addEventListenerToSelector(
    '.image-map_overlay', 'click', trackImageMapOverlayClick
  );
}
