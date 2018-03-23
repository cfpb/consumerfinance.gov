  // Wait a second then attach a listener to any play image.
  function _attachListener(){
    var videoPlayerBtnEls = document.querySelectorAll('.video-player_play-btn');
    var len = videoPlayerBtnEls.length;
    var videoPlayerBtnEl;
    if (len > 0) {
	    clearInterval(waitO);
      for (var i = 0; i < len; i++) {
        videoPlayerBtnEl = videoPlayerBtnEls[i];
        videoPlayerBtnEl.addEventListener('mousedown', _addAnalyticEvent);
        videoPlayerBtnEl.addEventListener('touchstart', _addAnalyticEvent);
      }

      function _addAnalyticEvent(){
        // Fire off the YT listener.
        dataLayer.push({
          'event' : 'YouTubeHiderButtonClicked'
        });

        // Tell GA about the image click.
        var h1El = document.querySelector('h1');
        var YTtitle = h1El.textContent.trim();
        dataLayer.push({
          'action': 'image click',
          'label' : YTtitle,
          'event' : 'YouTube Events'
        });
      }
    }
  }
  var waitO = setInterval(_attachListener, 1000);
