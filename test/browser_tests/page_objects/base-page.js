class BasePage {
  async gotoURL ( url ) {
    const gotoUrl = url || this.URL || '/';
    await browser.get( gotoUrl );
    await this.setElements();
    await this.disableAnimations();

    return BasePage.dismissAlert( gotoUrl );
  }

  removeExternalScripts() {
    [].slice.call( document.querySelectorAll( 'script, style, link' ) )
      .filter( script => {
        const src = script.href || script.src;

        return src && src.indexOf( 'localhost' ) === -1;
      } )
      .forEach( script => script.parentNode.removeChild( script ) );
  }

  disableAnimations() {

    /**
     * Disable CSS3 animations in when running tests.
     * @param {Object} browser Protractor browser object.
     */
    function _disableAnimations( ) {
      const style = document.createElement( 'style' );
      style.type = 'text/css';
      style.innerHTML = '* { transition-duration: .1ms !important; }';
      document.body.appendChild( style );
    }

    browser.executeScript( _disableAnimations );
  }

  setElements() { } // eslint-disable-line no-empty-function

  static async dismissAlert() {
    function _accepAlert( alert ) {
      if ( alert ) {
        return alert.accept( );
      }
      return Promise.resolve( );
    }

    try {
      const alertObj = await browser.switchTo( ).alert( );
      await _accepAlert( alertObj );
    } catch( error ) {
      Promise.resolve( );
    }
  }
}

module.exports = BasePage;
