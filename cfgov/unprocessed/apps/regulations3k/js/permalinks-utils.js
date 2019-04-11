// Array that tracks paragraph positions
let paragraphPositions;
const wayfinderOffset = 45;
const wayfinderRegex = {
  appendixTitle: /Appendix [A-Z]/,
  title: /§ 10[0-9].\.[0-9]*/g,
  marker: /\-/g
};

/**
 * scrollY - Get the Y coord of the current viewport. Older browsers don't
 * support `scrollY` so use whichever works.
 *
 * @returns {function} Browser-supported y offset method.
 */
const scrollY = () => window.scrollY || window.pageYOffset;

/**
 * getYLocation - Get Y location of provided element on the page.
 *
 * @param {node} el HTML element
 *
 * @returns {type} Description
 */
const getYLocation = el => {
  const elOffset = el.getBoundingClientRect().top;
  return scrollY() + elOffset - 30;
};

/**
 * getParagraphPositions - Get an array of all paragraphs with their IDs
 * mapped to their Y position (number of pixels from top of page).
 *
 * @param {nodelist} paragraphs Nodelist of HTML elements with IDs
 *
 * @returns {array} Array of objects w/ paragraph IDs and y positions.
 */
const getParagraphPositions = paragraphs => {
  let paragraphPos = [];

  // IE doesn't support `forEach` w/ node lists :/
  for ( let i = 0; i < paragraphs.length; i++ ) {
    paragraphPos.push( {
      id: paragraphs[i].id,
      position: getYLocation( paragraphs[i] )
    } );
  }

  // Convert it into an array and reverse it
  paragraphPos = Array.prototype.slice.apply( paragraphPos ).reverse();

  return paragraphPos;
};

/**
 * getCurrentParagraph - Get paragraph closest to viewport's current position.
 *
 * @param {int} currentPosition Current viewport Y coordinate
 * @param {array} paragraphs List of paragraphs on the page
 *
 * @returns {str} HTML ID of closest paragraph
 */
const getCurrentParagraph = ( currentPosition, paragraphs ) => {
  let currentId = null;
  // We're using a `for` loop so that we can `break` once a match is found
  for ( let i = 0; i < paragraphs.length; i++ ) {
    if ( currentPosition > paragraphs[i].position ) {
      currentId = paragraphs[i].id;
      break;
    }
  }
  return currentId;
};

/**
 * updateUrlHash - Update the page's URL hash w/ the closest paragraph
 *
 * @param {arr} paragraphs List of possible paragraphs on the page
 *
 * @returns {object} window object
 */
const updateUrlHash = () => {
  const currentParagraph = getCurrentParagraph( scrollY() + wayfinderOffset, paragraphPositions );
  // Setting the window state to `.` removes the URL hash
  const hash = currentParagraph ? `#${ currentParagraph }` : '.';
  return window.history.replaceState( null, null, hash );
};

/**
 * getCommentMarker - Does the legwork for the more complex comment markers
 *
 * @param {string} currentParagraph - id of the current paragraph
 *
 * @returns {string} formatted comment marker
 */
const getCommentMarker = currentParagraph => {
  let commentedSection;
  let commentedParagraph;
  let commentParagraph;
  const splitCurrentParagraph = currentParagraph.split( 'Interp' );
  const commentedParagraphID = splitCurrentParagraph[0].split( '-' );
  const commentParagraphID = splitCurrentParagraph[1]
    .split( '-' );
  commentedSection = commentedParagraphID[0];
  if ( commentedSection.match( /[A-Z]/ ) ) {
    commentedSection = 'app. ' + commentedParagraphID[0];
    commentedParagraph = '';
  } else {
    commentedParagraph = commentedParagraphID
      .slice( 1, -1 )
      .join( ')(' );
    commentedParagraph = '(' + commentedParagraph + ')';
  }
  commentParagraph = commentParagraphID
    .slice( 1 )
    .join( '.' );
  if ( commentParagraph !== '' ) {
    commentParagraph = '-' + commentParagraph;
  }

  return commentedSection + commentedParagraph + commentParagraph;
};

/**
 * getWayfinderInfo - process paragraph to create wayfinder
 * @param {string} paragraph - id of current paragraph
 * @param {string} sectionTitle - title of current section
 *
 * @returns {object} object of the values for wayfinder
 */
const getWayfinderInfo = ( paragraph, sectionTitle ) => {
  let sectionFormattedTitle;
  let paragraphMarker;
  // For interpretations, the wayfinder should look like "Comment 4(a)-1.iv.A"
  // Or like "Comment app. G-1.iv.A" for interpretations of appendices
  if ( sectionTitle.indexOf( 'Comment for ' ) === 0 ) {
    sectionFormattedTitle = 'Comment ';
    paragraphMarker = getCommentMarker( paragraph );
  } else if ( sectionTitle.indexOf( 'Appendix ' ) === 0 ) {
    // For appendices, the wayfinder should look like "Appendix A"
    sectionFormattedTitle = sectionTitle.match( wayfinderRegex.appendixTitle )[0];
    paragraphMarker = '';
  } else {
    // For sections of the main regulation text, the wayfinder should look like "§ 1026.5(b)(2)(ii)(A)(1)""
    sectionFormattedTitle = sectionTitle.match( wayfinderRegex.title )[0];
    paragraphMarker = '(' + paragraph.replace( wayfinderRegex.marker, ')(' ) + ')';
  }

  return {
    paragraphMarker: paragraphMarker,
    formattedTitle: sectionFormattedTitle
  };
};

/**
 * updateWayfinder - Update the Wayfinder element with current paragraph info
 */
const updateWayfinder = () => {
  const mainContent = document.querySelector( '.regulations3k' );
  const wayfinder = document.querySelector( '.o-regulations-wayfinder' );
  if ( wayfinder !== null && mainContent !== null ) {
    let paragraphMarker;
    let sectionFormattedTitle;
    let wayfinderInfo;
    const wayfinderLink = wayfinder.querySelector( '.o-regulations-wayfinder_link' );
    const currentParagraph = getCurrentParagraph( scrollY() + wayfinderOffset, paragraphPositions );

    if ( currentParagraph ) {
      const sectionTitle = wayfinder.dataset.section;
      wayfinderInfo = getWayfinderInfo( currentParagraph, sectionTitle );
      paragraphMarker = wayfinderInfo.paragraphMarker;
      sectionFormattedTitle = wayfinderInfo.formattedTitle;
      wayfinderLink.href = '#' + currentParagraph;
      mainContent.classList.add( 'show-wayfinder' );
    } else {
      sectionFormattedTitle = '';
      paragraphMarker = '';
      wayfinderLink.href = '#';
      mainContent.classList.remove( 'show-wayfinder' );
    }

    wayfinder.querySelector( '.o-regulations-wayfinder_section-title' ).textContent = sectionFormattedTitle;
    wayfinder.querySelector( '.o-regulations-wayfinder_marker' ).textContent = paragraphMarker;
  }

  document.querySelector( '.o-regulations-wayfinder_section-title' ).textContent = sectionFormattedTitle;
  document.querySelector( '.o-regulations-wayfinder_marker' ).textContent = paragraphMarker;
}

/**
 * updateParagraphPositions - Update the array that tracks paragraph positions
 *
 * @returns {type} Array of paragraph positions
 */
const updateParagraphPositions = () => {
  const paragraphs = document.querySelectorAll( '.regdown-block' );
  paragraphPositions = getParagraphPositions( paragraphs );
  return paragraphPositions;
};

/**
 * debounce - Ensure our callbacks fire only after the action has stopped
 *
 * @param {string} event Event name
 * @param {int} delay Time to wait in milliseconds
 * @param {function} cb Function to be called after action has stopped
 *
 * @returns {object} Timer
 */
const debounce = ( event, delay, cb ) => {
  let timeout;
  window.addEventListener( event, () => {
    window.clearTimeout( timeout );
    timeout = setTimeout( () => {
      cb();
    }, delay );
  }, false );
  return timeout;
};

module.exports = {
  debounce,
  getCommentMarker,
  getWayfinderInfo,
  getCurrentParagraph,
  getParagraphPositions,
  getYLocation,
  scrollY,
  updateParagraphPositions,
  updateUrlHash,
  updateWayfinder
};
