
'use strict';


class BasePage {
  gotoURL ( url ) {
    let gotoUrl = url || this.URL || '/';

    return browser.get( gotoUrl )
           .then( function() {
             BasePage.dismissAlert( gotoUrl );
           } )
  }

  static dismissAlert( url ) {
  	function _accepAlert( alert ) {
			if ( alert ) {
				return 	alert.accept();
			}
		}

		function _noOp( ) {
			return
		}

		return browser.switchTo()
		       .alert()
		       .catch( _noOp )
		       .then( _accepAlert );
  }
}

module.exports = BasePage;
