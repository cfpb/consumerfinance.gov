/* ==========================================================================
 Polyfill for addEventListener and removeEventListener.
 Modified from https://developer.mozilla.org/en-US/docs/Web
             /API/EventTarget/removeEventListener
             #Polyfill_to_support_older_browsers.
 ========================================================================== */

'use strict';

if ( !Element.prototype.addEventListener ) {
  var oListeners = {};
  function runListeners( oEvent ) {
    if ( !oEvent ) {
      oEvent = window.event;

      // Set target equal to srcElement if event target is not defined (IE8).
      if ( typeof oEvent.target === 'undefined' ) {
        oEvent.target = oEvent.srcElement;
      }
    }
    for ( var iLstId = 0, iElId = 0, oEvtListeners = oListeners[oEvent.type];
          iElId < oEvtListeners.aEls.length; iElId++ ) {
      if ( oEvtListeners.aEls[iElId] === this ) {
        for ( iLstId; iLstId < oEvtListeners.aEvts[iElId].length; iLstId++ ) {
          oEvtListeners.aEvts[iElId][iLstId].call( this, oEvent );
        }
        break;
      }
    }
  }
  // NOTE: useCapture (will be ignored!).
  Element.prototype.addEventListener = function( sEventType, fListener ) {
    if ( oListeners.hasOwnProperty( sEventType ) ) {
      var oEvtListeners = oListeners[sEventType];
      for ( var nElIdx = -1, iElId = 0; iElId < oEvtListeners.aEls.length;
            iElId++ ) {
        if ( oEvtListeners.aEls[iElId] === this ) { nElIdx = iElId; break; }
      }
      if ( nElIdx === -1 ) {
        oEvtListeners.aEls.push( this );
        oEvtListeners.aEvts.push( [ fListener ] );
        this['on' + sEventType] = runListeners;
      } else {
        var aElListeners = oEvtListeners.aEvts[nElIdx];
        if ( this['on' + sEventType] !== runListeners ) {
          aElListeners.splice( 0 );
          this['on' + sEventType] = runListeners;
        }
        for ( var iLstId = 0; iLstId < aElListeners.length; iLstId++ ) {
          if ( aElListeners[iLstId] === fListener ) {
            return;
          }
        }
        aElListeners.push( fListener );
      }
    } else {
      oListeners[sEventType] = { aEls: [ this ], aEvts: [ [ fListener ] ]};
      this['on' + sEventType] = runListeners;
    }
  };
  // NOTE: useCapture (will be ignored!).
  Element.prototype.removeEventListener = function( sEventType, fListener ) {
    if ( !oListeners.hasOwnProperty( sEventType ) ) {
      return;
    }
    var oEvtListeners = oListeners[sEventType];
    for ( var nElIdx = -1, iElId = 0; iElId < oEvtListeners.aEls.length;
          iElId++ ) {
      if ( oEvtListeners.aEls[iElId] === this ) {
        nElIdx = iElId; break;
      }
    }
    if ( nElIdx === -1 ) {
      return;
    }
    for ( var iLstId = 0, aElListeners = oEvtListeners.aEvts[nElIdx];
          iLstId < aElListeners.length; iLstId++ ) {
      if ( aElListeners[iLstId] === fListener ) {
        aElListeners.splice( iLstId, 1 );
      }
    }
  };
}
