/**
 * Adapted from
 * https://www.simoahava.com/analytics/track-browsing-behavior-in-google-analytics/#1-the-why-and-how-theory
 * for tracking tab navigation of the site.
 */

const TabNavigationTracking = ( () => {

  if ( !window.Storage ) {
    return;
  }

  /* Set to false if you only want to register "BACK/FORWARD"
     if either button was pressed. */
  const detailedBackForward = true;

  let openTabs = JSON.parse( localStorage.getItem( '_tab_ids' ) );
  let tabId = sessionStorage.getItem( '_tab_id' );
  let navPath = JSON.parse( sessionStorage.getItem( '_nav_path' ) );
  const curPage = document.location.href;
  let newTab = false;
  const origin = document.location.origin;

  let redirectCount;
  let navigationType;
  let prevInStack;
  let lastInStack;

  /**
   * Get the navigation path to a tab.
   * @returns {string} The navigation type.
   */
  function getBackForwardNavigation() {

    if ( detailedBackForward === false ) {
      return 'BACK/FORWARD';
    }

    if ( navPath.length < 2 ) {
      return 'FORWARD';
    }

    prevInStack = navPath[navPath.length - 2];
    lastInStack = navPath[navPath.length - 1];

    if ( prevInStack === curPage || lastInStack === curPage ) {
      return 'BACK';
    }
    return 'FORWARD';
  }

  /**
   * Remove the tracked tab.
   */
  function removeTabOnUnload() {

    let index;

    // Get the most recent values from storage
    openTabs = JSON.parse( localStorage.getItem( '_tab_ids' ) );
    tabId = sessionStorage.getItem( '_tab_id' );

    if ( openTabs !== null && tabId !== null ) {
      index = openTabs.indexOf( tabId );
      if ( index > -1 ) {
        openTabs.splice( index, 1 );
      }
      localStorage.setItem( '_tab_ids', JSON.stringify( openTabs ) );
    }

  }

  /**
   * @returns {string} A unique ID for the tab.
   */
  function generateTabId() {

    // From https://stackoverflow.com/a/8809472/2367037
    let d = new Date().getTime();
    if ( typeof performance !== 'undefined' &&
         typeof performance.now === 'function' ) {
      // Use high-precision timer if available.
      d += performance.now();
    }
    return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace( /[xy]/g, c => {
      const r = ( d + Math.random() * 16 ) % 16 | 0;
      d = Math.floor( d / 16 );
      return ( c === 'x' ? r : r & 0x3 | 0x8 ).toString( 16 );
    } );

  }

  /**
   *
   * @param {number} type - Describes how the navigation to this page was done.
   * @param {boolean} isNewTab - Whether we're validating a new tab or not.
   * @returns {boolean} Return false if new tab and any other navigation type than
   *   NAVIGATE or OTHER. Otherwise return true.
   */
  function validNavigation( type, isNewTab ) {
    return !( isNewTab === true && ( type !== 0 && type !== 255 ) );
  }

  if ( tabId === null ) {
    tabId = generateTabId();
    newTab = true;
    sessionStorage.setItem( '_tab_id', tabId );
  }

  openTabs = openTabs || [];

  if ( openTabs.indexOf( tabId ) === -1 ) {
    openTabs.push( tabId );
    localStorage.setItem( '_tab_ids', JSON.stringify( openTabs ) );
  }

  const tabCount = openTabs.length;

  if ( window.PerformanceNavigation ) {
    navPath = navPath || [];
    redirectCount = window.performance.navigation.redirectCount;
    // Only track new tabs if type is NAVIGATE or OTHER
    const navigationTypeID = window.performance.navigation.type;
    if ( validNavigation( navigationTypeID, newTab ) ) {
      switch ( navigationTypeID ) {
        case 0:
          navigationType = 'NAVIGATE';
          navPath.push( curPage );
          break;
        case 1:
          navigationType = 'RELOAD';
          if ( navPath.length === 0 || navPath[navPath.length - 1] !== curPage ) {
            navPath.push( curPage );
          }
          break;
        case 2:
          navigationType = getBackForwardNavigation();
          if ( navigationType === 'FORWARD' ) {
            // Only push if not coming from external domain
            if ( document.referrer.indexOf( origin ) > -1 ) {
              navPath.push( curPage );
            }
          } else if ( navigationType === 'BACK' ) {
            // Only remove last if not coming from external domain
            if ( lastInStack !== curPage ) {
              navPath.pop();
            }
          } else {
            navPath.push( curPage );
          }
          break;
        default:
          navigationType = 'OTHER';
          navPath.push( curPage );
      }
    } else {
      navPath.push( curPage );
    }
    sessionStorage.setItem( '_nav_path', JSON.stringify( navPath ) );
  }

  window.addEventListener( 'beforeunload', removeTabOnUnload );

  const payload = {
    tabCount: tabCount,
    redirectCount: redirectCount,
    navigationType: navigationType,
    newTab: newTab === true ? 'New' : 'Existing',
    tabId: tabId
  };

  // Set the data model keys directly so they can be used in the Page View tag
  window.google_tag_manager['GTM-KMMLRS'].dataLayer.set(
    'browsingBehavior',
    payload
  );

  // Also push to dataLayer
  window.dataLayer.push( {
    event: 'custom.navigation',
    browsingBehavior: payload
  } );

} )();
