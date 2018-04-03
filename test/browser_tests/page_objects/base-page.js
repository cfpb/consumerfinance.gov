class BasePage {
  async gotoURL( url ) {
    const gotoUrl = url || this.URL || '/';
    await browser.get( gotoUrl );
    await this.setElements();
    await this.disableAnimations();
    await this.removeExternalScripts();

    return BasePage.dismissAlert( gotoUrl );
  }

  removeExternalScripts() {

    /**
     * Remove any exernal scripts.
     * @param {Object} browser Protractor browser object.
     */
    function _removeScripts() {
      [].slice.call( document.querySelectorAll( 'script, style, link' ) )
        .filter( script => {
          const src = script.href || script.src;

          return src && src.indexOf( 'localhost' ) === -1;
        } )
        .forEach( script => script.parentNode.removeChild( script ) );
    }

    return browser.executeScript( _removeScripts );
  }

  disableAnimations() {

    /**
     * Disable CSS3 animations when running tests.
     * @param {Object} browser Protractor browser object.
     */
    function _disableAnimations() {
      const style = document.createElement( 'style' );
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
