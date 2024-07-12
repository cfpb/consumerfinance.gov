/**
 * Used with modifications from
 * https://github.com/jfriend00/docReady/blob/master/docready.js
 *
 * The MIT License (MIT)
 *
 * Copyright (c) 2014, John Friend
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in all
 * copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
 * SOFTWARE.
 */

let readyList = [];
let readyFired = false;
let readyEventHandlersInstalled = false;

/**
 * Call this when the document is ready.
 * This function protects itself against being called more than once.
 */
function docReady() {
  if ( !readyFired ) {
    // This must be set to true before we start calling callbacks.
    readyFired = true;
    for ( let i = 0, len = readyList.length; i < len; i++ ) {
      /* If a callback here happens to add new ready handlers,
         the ready() function will see that it already fired
         and will schedule the callback to run right after
         this event loop finishes so all handlers will still execute
         in order and no new ones will be added to the readyList
         while we are processing the list. */
      readyList[i]();
    }
    // Allow any closures held by these functions to free.
    readyList = [];
  }
}

/**
 * Event handler function for when the load state changes.
 */
function readyStateChange() {
  if ( document.readyState === 'complete' ) {
    docReady();
  }
}

/* This is the one public interface
   ready(fn);
   the context argument is optional - if present, it will be passed
   as an argument to the callback */
/**
 * Call a callback function when the document is ready.
 * @param {Function} callback - A function to call when the document is loaded.
 */
function ready( callback ) {
  if ( typeof callback !== 'function' ) {
    throw new TypeError( 'callback for ready(fn) must be a function' );
  }

  /* If ready has already fired, then just schedule the callback
     to fire asynchronously, but right away. */
  if ( readyFired ) {
    setTimeout( () => callback(), 1 );
    return;
  }
  // Add the function to the list.
  readyList.push( callback );

  /* If document is already ready to go, schedule the ready function to run.
     IE is only safe when readyState is "complete",
     others are safe when readyState is "interactive". */
  if ( document.readyState === 'complete' ||
       ( !document.attachEvent && document.readyState === 'interactive' ) ) {
    setTimeout( docReady, 1 );
  } else if ( !readyEventHandlersInstalled ) {
    // Otherwise if we don't have event handlers installed, install them.
    if ( document.addEventListener ) {
      // First choice is DOMContentLoaded event.
      document.addEventListener( 'DOMContentLoaded', docReady, false );
      // Backup is window load event.
      window.addEventListener( 'load', docReady, false );
    } else {
      // Must be IE.
      document.attachEvent( 'onreadystatechange', readyStateChange );
      window.attachEvent( 'onload', docReady );
    }
    readyEventHandlersInstalled = true;
  }
}

export default ready;
