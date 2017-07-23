'use strict';

var $ = require( 'jquery' );
var sticky = require( 'jquery-sticky' );
var debounce = require( 'debounce' );

const atomicHelpers = require( '../../modules/util/atomic-helpers' );
const ExpandableGroup = require( '../../organisms/ExpandableGroup' );
atomicHelpers.instantiateAll( '.o-expandable-group', ExpandableGroup );

require( 'jquery.scrollto' );

var formExplainer = {
  pageCount:   0,
  currentPage: 1,
  pageName:    'form'
};

// Constants. These variables should not change.
var $WRAPPER;
var $TABS;
var $PAGINATION;
var $WINDOW;
var TOTAL;

// Keys to sections on page.
// TODO: Determine whether this is used.
var termsList = '.explain_terms';

// TODO: define category list in calling page, and
// also pass it to form-explainer.html to construct tabs
var CATEGORIES = [ 'checklist', 'definitions' ];
var DEFAULT_TYPE = 'checklist';
var $INITIAL_TAB;

var resized;

var stickBottom = 'js-sticky-bottom';

formExplainer.getPageEl = function( pageNum ) {
  return $( '#explain_page-' + pageNum );
};

formExplainer.getPageElements = function( pageNum ) {
  var $page = formExplainer.getPageEl( pageNum );

  return {
    $page:            $page,
    $imageMap:        $page.find( '.image-map' ),
    $imageMapImage:   $page.find( '.image-map_image' ),
    $imageMapWrapper: $page.find( '.image-map_wrapper' ),
    $terms:           $page.find( '.terms' )
  };
};

formExplainer.calculateNewImageWidth = function( imageWidth, imageHeight, windowHeight ) {
  var imageMapImageRatio = ( imageWidth + 2 ) / ( imageHeight + 2 );

  return ( windowHeight - 60 ) * imageMapImageRatio + 30;
};

formExplainer.resizeImage = function( els, $window, windowResize ) {

  var pageWidth = els.$page.width();
  var $image = els.$imageMapImage;
  var currentHeight = $image.height();
  var currentWidth = $image.width();
  var actualWidth = $image.data( 'actual-width' );
  var actualHeight = $image.data( 'actual-height' );
  var windowHeight = $window.innerHeight() - 60;
  var newWidth;
  var newWidthPercentage;

  // If the image is too tall for the window, resize it proportionally,
  // then update the adjacent terms column width to fit.
  // On window resize, also check if image is now too small & resize,
  // but only if we've stored the actual image dimensions for comparison.
  if ( currentHeight > windowHeight || windowResize && actualWidth && actualHeight ) {
    // determine new width
    newWidth = formExplainer.calculateNewImageWidth( currentWidth, currentHeight, $window.height() );
    if ( newWidth > actualWidth ) {
      newWidth = actualWidth;
    }
    // update element widths
    newWidthPercentage = newWidth / pageWidth * 100;
    // on screen less than 800px wide, the terms need a minimum 33%
    // width or they become too narrow to read
    if ( $window.width() <= 800 && newWidthPercentage > 67 ) {
      newWidthPercentage = 67;
    }
    els.$imageMap.css( 'width', newWidthPercentage + '%' );
    $PAGINATION.css( 'width', newWidthPercentage + '%' );
    els.$terms.css( 'width', 100 - newWidthPercentage + '%' );
  }
};

formExplainer.setImageElementWidths = function( els ) {
  // When the sticky plugin is applied to the image, it adds position fixed,
  // and the image's width is no longer constrained to its parent.
  // To fix this we will give it its own width that is equal to the parent.
  // (IE8 wants a width on the wrapper too)
  var containerWidth = els.$imageMap.width();
  els.$imageMapWrapper.width( containerWidth );
  els.$imageMapImage.width( containerWidth );
};

formExplainer.storeImageDimensions = function( $image ) {
  $image.data( 'actual-width', $image.width() );
  $image.data( 'actual-height', $image.height() );
};

formExplainer.stickImage = function( $el ) {
  $el.sticky( { topSpacing: 30 } );
};

/**
 * Limit .image-map_image to the height of the window and then adjust the two
 * columns to match.
 * @param {Object} els - TODO: Add description.
 * @param {number} pageNum - TODO: Add description.
 */
formExplainer.fitAndStickToWindow = function( els, pageNum ) {
  // http://stackoverflow.com/questions/318630/get-real-image-width-and-height-with-javascript-in-safari-chrome
  $( '<img/>' )
    .load( function() {
      // store image width for use in calculations on window resize
      if ( pageNum ) {
        formExplainer.storeImageDimensions( els.$imageMapImage );
      }

      // if image is too tall/small, fit it to window dimensions
      formExplainer.resizeImage( els, $WINDOW, !pageNum );

      // set width values on image elements
      formExplainer.setImageElementWidths( els );

      if ( pageNum || els.$imageMapImage.closest( '.sticky-wrapper' ).length === 0 ) {
        // stick image to window
        formExplainer.stickImage( els.$imageMapWrapper );
      }

      formExplainer.updateStickiness( els, $WINDOW.scrollTop() );

      // hide pages except for first
      if ( pageNum > 1 ) {
        els.$page.hide();
      }
    } )
    // This order is necessary so that IE8 doesn't fire the onload event
    // before the src is set for cached images
    // http://stackoverflow.com/questions/14429656/onload-callback-on-image-not-called-in-ie8
    .attr( 'src', els.$imageMapImage.attr( 'src' ) );
};

/**
 * Override sticky() if the viewport has been scrolled past $currentPage so that
 * the sticky element does not overlap content that comes after $currentPage.
 * @param {Object} els - TODO: Add description.
 * @param {Object} windowScrollTop - TODO: Add description.
 */
formExplainer.updateStickiness = function( els, windowScrollTop ) {
  var max = els.$page.offset().top + els.$page.height() - els.$imageMapWrapper.height();
  if ( windowScrollTop >= max && !els.$imageMapWrapper.hasClass( stickBottom ) ) {
    els.$imageMapWrapper.addClass( stickBottom );
  } else if ( windowScrollTop < max && els.$imageMapWrapper.hasClass( stickBottom ) ) {
    els.$imageMapWrapper.removeClass( stickBottom );
  }
};

/**
 * Paginate through the various form pages.
 * @param {Object} direction - TODO: Add description.
 */
function paginate( direction ) {
  var currentPage = formExplainer.currentPage;
  var increment = direction === 'next' ? 1 : -1;
  var newPage = currentPage + increment;

  // Move to the next or previous page if it's not the first or last page.
  if ( direction === 'next' && newPage <= formExplainer.pageCount ||
       direction === 'prev' && newPage >= 1 ) {
    loadPage( currentPage, newPage );
  }
}

function loadPage( lastPage, pageNum ) {
  formExplainer.currentPage = pageNum;
  $( '.form-explainer_page-link' ).removeClass( 'current-page' );
  $( '.form-explainer_page-link[data-page=' + pageNum + ']' ).addClass( 'current-page' );

  // Scroll the window up to the tabs.
  $.scrollTo( $( '.explain_pagination' ), {
    duration: 600,
    offset:   -30
  } );

  // After scrolling the window, fade out the current page.
  var fadeOutTimeout = window.setTimeout( function() {
    formExplainer.getPageEl( lastPage ).fadeOut( 450 );
    window.clearTimeout( fadeOutTimeout );
  }, 600 );

  // After fading out the current page, fade in the new page.
  var fadeInTimeout = window.setTimeout( function() {
    formExplainer.getPageEl( pageNum ).fadeIn( 700 );
    stickyHack();
    window.clearTimeout( fadeInTimeout );

    if ( resized ) {
      formExplainer.setupImage( pageNum );
    }
    // update paging buttons
    if ( formExplainer.pageCount > 1 ) {
      $( '.form-explainer_page-buttons button' ).removeClass( 'btn__disabled' );

      if ( pageNum === 1 ) {
        $( '.form-explainer_page-buttons .prev' ).addClass( 'btn__disabled' );
      } else if ( pageNum === formExplainer.pageCount ) {
        $( '.form-explainer_page-buttons .next' ).addClass( 'btn__disabled' );
      }
    }
  }, 1050 );
}

formExplainer.setupImage = function( pageNum, pageLoad ) {
  var pageEls = formExplainer.getPageElements( pageNum );
  if ( $WINDOW.width() >= 600 ) {
    // update widths & stickiness on larger screens
    // we only pass in the pageNum on pageLoad, when
    // pages after the first will be hidden once they're
    // fully loaded & we've calculated their widths
    formExplainer.fitAndStickToWindow( pageEls, pageLoad ? pageNum : null );
  } else if ( !pageLoad ) {
    // if this is called on screen resize instead of page load,
    // remove width values & call unstick on the imageWrapper
    pageEls.$imageMapWrapper.width( '' ).removeClass( stickBottom );
    pageEls.$imageMap.width( '' );
    pageEls.$imageMapImage.width( '' );
    pageEls.$terms.width( '' );
    pageEls.$imageMapWrapper.unstick();
  } else if ( pageNum > 1 ) {
    // on page load, hide pages except first
    pageEls.$page.hide();
  }
};

formExplainer.initForm = function( $wrapper ) {
  // Loop through each page, setting its dimensions properly and activating the
  // sticky() plugin.

  var $pages = $wrapper.find( '.explain_page' );
  formExplainer.pageCount = $pages.length;
  if ( formExplainer.pageCount <= 1 ) {
    $( '.form-explainer_page-buttons' ).hide();
  }
  $pages.each( function( index ) {
    formExplainer.initPage( index + 1 );
  } );
};

/**
 * Initialize a page.
 * @param {Object} id - TODO: Add description.
 */
formExplainer.initPage = function( id ) {
  formExplainer.setupImage( id, true );
  formExplainer.setCategoryPlaceholders( id );
};

/**
 * Weird hack to get sticky() to update properly.
 * We're basically jinggling the window to force a sticky() repaint.
 * Sometimes it just needs a push I guess?
 */
function stickyHack() {
  $WINDOW.scrollTop( $WINDOW.scrollTop() + 1 );
  $WINDOW.scrollTop( $WINDOW.scrollTop() - 1 );
}

/**
 * Set category placeholders.
 * @param {Object} id - TODO: Add description.
 */
formExplainer.setCategoryPlaceholders = function( id ) {
  var $page = formExplainer.getPageEl( id );
  var placeholder;
  for ( var i = 0; i < CATEGORIES.length; i++ ) {
    var category = CATEGORIES[i];
    if ( !categoryHasContent( $page, category ) ) {
      placeholder = formExplainer.generatePlaceholderHtml( category );
      $page.find( '.explain_terms' ).append( placeholder );
    }
  }
};

formExplainer.generatePlaceholderHtml = function( category ) {
  return '<div class="o-expandable o-expandable__padded o-expandable__form-explainer ' +
              'o-expandable__form-explainer-' + category + ' ' +
              'o-expandable__form-explainer-placeholder">' +
    '<span class="o-expandable_header">' +
      'Click on "Get Definitions" above or page ahead to continue checking your ' + this.pageName + '.' +
    '</span>' +
  '</div>';
};

function categoryHasContent( $page, category ) {
  return $page.find( '.o-expandable__form-explainer-' + category ).length;
}

function filterExplainers( $currentTab, type ) {
  // Update the tab state
  $( '.explain_tabs .tab-list' ).removeClass( 'active-tab' );
  $currentTab.addClass( 'active-tab' );

  // Filter the expandables
  $WRAPPER.find( '.o-expandable__form-explainer' ).hide();
  $WRAPPER.find( '.image-map_overlay' ).hide();
  $WRAPPER.find( '.o-expandable__form-explainer-' + type ).show();
  $WRAPPER.find( '.image-map_overlay__' + type ).show();
}

function toggleScrollWatch() {
  $WINDOW.off( 'scroll.stickiness' );
  if ( $WINDOW.width() >= 600 ) {
    $WINDOW.on( 'scroll.stickiness', debounce(
      function() {
        var els = formExplainer.getPageElements( formExplainer.currentPage );
        formExplainer.updateStickiness( els, $WINDOW.scrollTop() );
      }, 20 ) );
  }
}

function addTabindex() {
  var $link = $( '.o-expandable__form-explainer .o-expandable_content a' );
  $link.attr( 'tabindex', 0 );
}

// Kick things off on document ready.
$( document ).ready( function() {
  // cache elements
  $WRAPPER = $( '.explain' );
  $TABS = $WRAPPER.find( '.explain_tabs' );
  $PAGINATION = $WRAPPER.find( '.explain_pagination' );
  $WINDOW = $( window );
  TOTAL = parseInt( $PAGINATION.find( '.pagination_total' ).text(), 10 );
  $INITIAL_TAB = $( '.tab-link[data-target="' + DEFAULT_TYPE + '"]' ).closest( '.tab-list' );

  // set up the form pages for display
  formExplainer.initForm( $WRAPPER );

  // filter initial state
  filterExplainers( $INITIAL_TAB, DEFAULT_TYPE );

  // add scroll listener for larger windows
  toggleScrollWatch();

  // set tabindex for links in expandables content
  addTabindex();

  // add resize listener
  var prevWindowWidth = $WINDOW.width();
  var prevWindowHeight = $WINDOW.height();
  var isIE = $( 'html' ).hasClass( 'lt-ie9' );

  $( window ).on( 'resize', debounce( function() {
    // resize things
    // apparently IE fires a window resize event when anything in the page
    // resizes, so for IE we need to check that the window dimensions have
    // actually changed
    if ( isIE ) {
      var currWindowHeight = $WINDOW.height();
      var currWindowWidth = $WINDOW.width();

      if ( currWindowHeight === prevWindowHeight &&
           currWindowWidth === prevWindowWidth ) {
        return;
      }

      prevWindowWidth = currWindowWidth;
      prevWindowHeight = currWindowHeight;
    }
    resized = true;
    formExplainer.setupImage( formExplainer.currentPage );
    toggleScrollWatch();
  } ) );

  // Pagination events
  $WRAPPER.find( '.form-explainer_page-buttons button' ).on( 'click', function( event ) {
    var $target = $( event.currentTarget );
    if ( !$target.hasClass( 'btn__disabled' ) ) {
      var direction = $target.hasClass( 'prev' ) ? 'prev' : 'next';
      paginate( direction );
    }
  } );

  $WRAPPER.find( '.form-explainer_page-link' ).on( 'click', function( event ) {
    var $target = $( event.currentTarget );
    var pageNum = Number( $target.data( 'page' ) );
    var currentPage = formExplainer.currentPage;

    if ( !$target.hasClass( 'disabled' ) && pageNum !== currentPage ) {
      loadPage( currentPage, pageNum );
    }
  } );

  // Filter the expandables via the tabs
  $WRAPPER.on( 'click', '.explain_tabs .tab-list', function() {
    var $selectedTab = $( this );
    var explainerType = $selectedTab.find( '[data-target]' ).data( 'target' );

    filterExplainers( $selectedTab, explainerType );

    $.scrollTo( $TABS, {
      duration: 200,
      offset:   -30
    } );
  } );

  var expandableTimeout;
  var delay = isIE ? 1000 : 700;

  function updateImagePositionAfterAnimation() {
    // Check image position after expandable animation to make sure it is not
    // overlapping the footer.
    window.clearTimeout( expandableTimeout );
    setTimeout( function() {
      if ( $WINDOW.width() > 600 ) {
        var els = formExplainer.getPageElements( formExplainer.currentPage );
        formExplainer.updateStickiness( els, $WINDOW.scrollTop() );
      }
    }, delay );
  }

  function openAndScrollToExpandable( $targetExpandable ) {
    // If there's an expandable open above the targeted expandable,
    // it will be closed when this expandable opens, so we need
    // to subtract its height from this expandable's offset in order
    // to get a position to use in scrolling this expandable into view
    var prevExpanded = $targetExpandable.prevAll( '.o-expandable__expanded' );
    var offset = 0;
    if ( prevExpanded.length ) {
      offset = $( prevExpanded[0] ).find( '.o-expandable_content' ).height();
    }
    var pos = $targetExpandable.offset().top - offset;
    $.scrollTo( pos, {
      duration: 200,
      offset:   -30
    } );

    console.log( 'scroll' );
    $targetExpandable.find( '.o-expandable_target' ).click();
  }

  // Update attention classes based on the expandable or image overlay
  // that was targeted.
  // Remove the attention class from all the expandables/overlays,
  // and then apply it to the target & its associated overlay
  // or expandable.
  function updateAttention( $target, className ) {
    var $associated;

    $( '.o-expandable__form-explainer, .image-map_overlay' ).removeClass( className );

    if ( typeof $target.attr( 'href' ) !== 'undefined' ) {
      $associated = $( $target.attr( 'href' ) );
    } else if ( typeof $target.attr( 'id' ) !== 'undefined' ) {
      $associated = $( '[href=#' + $target.attr( 'id' ) + ']' );
    }

    if ( typeof $associated !== 'undefined' ) {
      if ( className === 'has-attention' ) {
        $target.removeClass( 'hover-has-attention' );
        $associated.removeClass( 'hover-has-attention' );
      }
      $target.addClass( className );
      $associated.addClass( className );
    }
  }

  $WRAPPER.on( 'focus', '.o-expandable_target', function() {
    var $expandable = $( this ).closest( '.o-expandable__form-explainer' );
    updateAttention( $expandable, 'hover-has-attention' );
  } );

  $WRAPPER.on( 'mouseenter mouseleave', '.image-map_overlay, .o-expandable__form-explainer', function( event ) {
    event.preventDefault();
    updateAttention( $( this ), 'hover-has-attention' );
  } );

  // When an overlay is clicked, toggle the corresponding expandable and scroll
  // the page until it is in view.
  $WRAPPER.on( 'click', '.image-map_overlay', function( event ) {
    event.preventDefault();
    var $this = $( this ),
        itemID = $this.attr( 'href' ),
        $targetExpandable = $( itemID );
    updateAttention( $this, 'has-attention' );
    openAndScrollToExpandable( $targetExpandable );
    updateImagePositionAfterAnimation();
  } );

  $( '.o-expandable__form-explainer .o-expandable_target' ).on( 'keypress click', function( event ) {
    if ( event.which === 13 || event.type === 'click' ) {
      updateAttention( $( this ).closest( '.o-expandable__form-explainer' ), 'has-attention' );
      updateImagePositionAfterAnimation();
    }
  } );


} );

module.exports = formExplainer;
