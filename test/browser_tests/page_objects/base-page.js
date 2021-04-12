const { setDefaultTimeout } = require( '@cucumber/cucumber' );

setDefaultTimeout( 60 * 1000 );

class BasePage {
  async gotoURL( url ) {
    const gotoUrl = url || this.URL || '/';
    await browser.get( gotoUrl );
    await this.setElements();

    try {
      await this.disableAnimations();
      return this.removeExternalScripts();
    } catch ( error ) {
      return Promise.resolve();
    }
  }

  removeExternalScripts() {

    /**
     * Remove any exernal scripts.
     * @param {Object} browser Protractor browser object.
     */
    function _removeScripts() {
      [].forEach.call(
        document.querySelectorAll( 'script, style, link' ),
        function( script ) {
          var src = script.href || script.src; // eslint-disable-line no-var
          if ( src && src.indexOf( 'localhost' ) === -1 ) {
            script.parentNode.removeChild( script );
          }
        }
      );
    }

    return browser.executeScript( _removeScripts );
  }

  disableAnimations() {

    /**
     * Disable CSS3 animations when running tests.
     * @param {Object} browser Protractor browser object.
     */
    function _disableAnimations() {
      var style = document.createElement( 'style' ); // eslint-disable-line no-var
      style.type = 'text/css';
      style.innerHTML = '* { transition-duration: .1ms !important; }';
      document.body.appendChild( style );
    }

    return browser.executeScript( _disableAnimations );
  }

  setElements() {
    // Noop function, which should be overridden when setting page elements.
  }

  static async dismissAlert() {
    function _accepAlert( alert ) {
      if ( alert ) {
        return alert.accept();
      }
      return Promise.resolve();
    }

    try {
      const alertObj = await browser.switchTo().alert();
      await _accepAlert( alertObj );
    } catch ( error ) {
      Promise.resolve();
    }
  }
}

module.exports = BasePage;
