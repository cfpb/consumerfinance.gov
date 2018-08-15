/**
 * Applies a focus state to the main content when a user clicks the skip navigation link.
 * Improves the usability of the skip navigation link across browsers & devices.
 */

function SkipNav() {
  const skip = document.getElementById( 'skip-nav' );
  const mainContent = document.getElementById( 'main' );

  skip.addEventListener( 'click', evt => {
    evt.preventDefault();
    mainContent.setAttribute( 'tabindex', '-1' );
    mainContent.focus();
  }, false );
}

module.exports = SkipNav;
