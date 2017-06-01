'use strict';


class BasePage {
  gotoURL( url ) {
    const gotoUrl = url || this.URL || '/';

    return browser.get( gotoUrl )
           .then( function() {
             BasePage.dismissAlert( gotoUrl );
           } );
  }

  static dismissAlert( ) {
    function _accepAlert( alert ) {
      if ( alert ) {
        return alert.accept();
      }

      return Promise.resolve();
    }

    function _noOp( ) {

      return;
    }

    return browser
           .switchTo()
           .alert()
           .then( _accepAlert )
           .catch( _noOp );
  }
}

module.exports = BasePage;
