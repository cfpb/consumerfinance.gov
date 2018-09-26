// Array that tracks paragraph positions
let paragraphPositions;

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
  const currentParagraph = getCurrentParagraph( scrollY(), paragraphPositions );
  // Setting the window state to `.` removes the URL hash
  const hash = currentParagraph ? `#${ currentParagraph }` : '.';
  return window.history.replaceState( null, null, hash );
};


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
  getCurrentParagraph,
  getParagraphPositions,
  getYLocation,
  scrollY,
  updateParagraphPositions,
  updateUrlHash
};
