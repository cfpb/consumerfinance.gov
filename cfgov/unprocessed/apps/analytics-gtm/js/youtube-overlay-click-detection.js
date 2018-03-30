const waitO = setInterval( _attachListener, 1000 );

// Wait a second then attach a listener to any play image.
function _attachListener() {
  const videoPlayerBtnEls = document.querySelectorAll( '.video-player_play-btn' );
  const len = videoPlayerBtnEls.length;
  let videoPlayerBtnEl;
  if ( len > 0 ) {
    clearInterval( waitO );
    for ( let i = 0; i < len; i++ ) {
      videoPlayerBtnEl = videoPlayerBtnEls[i];
      videoPlayerBtnEl.addEventListener( 'mousedown', _addAnalyticEvent );
      videoPlayerBtnEl.addEventListener( 'touchstart', _addAnalyticEvent );
    }
  }
}

function _addAnalyticEvent() {
  // Fire off the YT listener.
  window.dataLayer.push( {
    event: 'YouTubeHiderButtonClicked'
  } );

  // Tell GA about the image click.
  const h1El = document.querySelector( 'h1' );
  const YTtitle = h1El.textContent.trim();
  window.dataLayer.push( {
    action: 'image click',
    label: YTtitle,
    event: 'YouTube Events'
  } );
}
