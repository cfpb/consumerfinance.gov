import { hostsAreEqual } from './util/analytics-util';

/* ********************************
Blast Analytics & Marketing
Create Source Attribution Cookie
******************************** */

const sourceCookies = {
  // Session length in milliseconds : default 30 mins.
  _sessionLength: 1800000,

  // Cookie domain name.
  _cookieDomain: '{{cookie domain}}',

  // Session cookie name.
  _sourceCookieName: '_A_source',

  // Session cookie name.
  _timeCookieName: '_A_time',

  // Classic analytics parameter mapping.
  _classicParameterMap: {
    gclid: 'utmgclid',
    source: 'utmcsr',
    campaign: 'utmccn',
    medium: 'utmcmd',
    keyword: 'utmctr',
    content: 'utmcct'
  },

  // Referral source.
  _referral: {
    gclid: '',
    source: '',
    campaign: '',
    medium: '',
    keyword: '',
    content: '',
    date: ''
  },

  _timeStamps: {
    visitCount: 0,
    currentVisit: ( new Date() ).getTime()
  },

  /**
   * Determine referral source
   * @param {string} host - A URL.
   * @param {string} query - A query string.
   * @param {string} referrer - A referrer URL.
   */
  update: function( host, query, referrer ) {
    const q = new Date();
    let sourceString = '';
    const timeString = '';
    let newSource = '';
    let newTime = '';

    this._referral.date = q.getTime();
    this._timeStamps.firstVisit = this._timeStamps.currentVisit;

    // Determine referral source
    this.parseDirect( host, query, referrer );
    this.parseReferral( host, query, referrer );
    this.parseOrganicSearch( host, query, referrer );
    this.parseUTMparameters( host, query, referrer );
    this.parseAdWords( host, query, referrer );

    // .parseSocialMedia(host, query, referrer)

    // Set temp source values.
    for ( const property in this._referral ) {
      if ( property !== 'date' && this._referral[property].length > 0 ) {
        newSource = newSource + this._classicParameterMap[property] + '=' +
                    this._referral[property].replace( /\s/g, '%20' ) + '|';
      }
    }

    // Remove trailing pipe.
    newSource = newSource.slice( 0, -1 );

    if ( this._getCookie( this._timeCookieName ) !== '' ) {
      this._timeStamps.firstVisit = Number( this._getCookie( this._timeCookieName ).split( /\./ )[1] );
      this._timeStamps.visitCount = Number( this._getCookie( this._timeCookieName ).split( /\./ )[0] );
      this._newSession = ( this._referral.date - Number( this._getCookie( this._timeCookieName ).split( /\./ )[2] ) ) > this._sessionLength;
    }

    if ( this._getCookie( this._sourceCookieName ) !== '' ) {
      sourceString = this._getCookie( this._sourceCookieName );

      if ( newSource === '' ) {
        newSource = sourceString;
      }
    }

    if ( ( sourceString !== decodeURIComponent( newSource ) ) ||
         this._newSession ) {
      /* check values
      set cookies */
      this._timeStamps.visitCount++;
      this._setCookie( this._sourceCookieName, newSource, 365 * 2, false );// .0208 visitAttribution._sessionLength*(1/24/60/60/1000);
      // trigger any dataLayer actions desired
      if ( this._timeStamps.visitCount === 1 ) {
        const vSource = newSource.split( '|' )[0].split( '=' )[1];
        const vMedium = newSource.split( '|' )[1].split( '=' )[1];
        const vCampaign = newSource.split( '|' )[2].split( '=' )[1];
        window.dataLayer.push( { firstSource: vSource, firstMedium: vMedium, firstCampaign: vCampaign, visitNumber: this._timeStamps.visitCount, event: 'visitCounter' } );
      } else {
        window.dataLayer.push( { visitNumber: this._timeStamps.visitCount, event: 'visitCounter' } );
      }
    }
    // Set time values.
    newTime = this._timeStamps.visitCount + '.' + this._timeStamps.firstVisit +
              '.' + this._timeStamps.currentVisit;

    // Set time cookie, updated current visit.
    this._setCookie( this._timeCookieName, newTime, 365 * 2, false );
  },


  /**
   * Check for AdWords referral
   * @param {string} host - A URL.
   * @param {string} query - A query string.
   * @param {string} referrer - A referrer URL.
   * @returns {Object} visitAttribution
   */
  parseAdWords: function( host, query, referrer ) {
    // Check for gclid or gclsrc
    if ( this._getQueryParameter( query, 'gclid' ) !== '' ||
         this._getQueryParameter( query, 'gclsrc' ) !== '' ) {
      this._referral.gclid = String( String( this._getQueryParameter( query, 'gclid' ) ) + this._getQueryParameter( query, 'gclsrc' ) );
      // source
      if ( this._getQueryParameter( query, 'utm_source' ) === '' ) {
        this._referral.source = 'google';
      } else {
        this._referral.source = this._getQueryParameter( query, 'utm_source' );
      }
      // medium
      if ( this._getQueryParameter( query, 'utm_medium' ) === '' ) {
        this._referral.medium = 'cpc';
      } else {
        this._referral.medium = this._getQueryParameter( query, 'utm_medium' );
      }
      // campaign
      if ( this._getQueryParameter( query, 'utm_campaign' ) === '' ) {
        this._referral.campaign = '(not set)';
      } else {
        this._referral.campaign = this._getQueryParameter( query, 'utm_campaign' );
      }
      // content
      if ( this._getQueryParameter( query, 'utm_content' ) === '' ) {
        this._referral.content = '';
      } else {
        this._referral.content = this._getQueryParameter( query, 'utm_content' );
      }
      // keyword
      if ( this._getQueryParameter( query, 'utm_term' ) === '' ) {
        this._referral.keyword = '(not provided)';
      } else {
        this._referral.keyword = this._getQueryParameter( query, 'utm_term' );
      }
    }

    // Return
    return this;
  },


  /**
   * Check for UTM parameters
   * @param {string} host - A URL.
   * @param {string} query - A query string.
   * @param {string} referrer - A referrer URL.
   * @returns {Object} visitAttribution
   */
  parseUTMparameters: function( host, query, referrer ) {
    // Check for gclid or gclsrc
    if ( this._getQueryParameter( query, 'utm_source' ) !== '' ) {
      // Set data
      this._referral.gclid = this._getQueryParameter( query, 'gclid' );
      this._referral.source = this._getQueryParameter( query, 'utm_source' );
      this._referral.medium = this._getQueryParameter( query, 'utm_medium' );
      this._referral.campaign = this._getQueryParameter( query, 'utm_campaign' );
      this._referral.content = this._getQueryParameter( query, 'utm_content' );
      this._referral.keyword = this._getQueryParameter( query, 'utm_term' );
    }

    // Return
    return this;
  },


  /**
   * Check for organic search referral
   * @param {string} host - A URL.
   * @param {string} query - A query string.
   * @param {string} referrer - A referrer URL.
   * @returns {Object} visitAttribution
   */
  parseOrganicSearch: function( host, query, referrer ) {
    // Referrer must not be the same host
    if ( hostsAreEqual( 'https://' + host, referrer ) === false ) {

      // Check for search engine
      const referrerMatch = referrer.match( /^https?:\/\/(.*\.search\.|www\.)?(google|bing|aol|yahoo|ask|comcast).([a-z]+)([\.a-z]{3,5})?\// );
      if ( referrerMatch !== null ) {
        // Referrer query string
        const referrer_query = this._getQueryString( referrer );

        // Referrer search term
        const referrer_search_term = this._getQueryParameter( referrer_query, 'q' );

        // Set data
        this._referral.gclid = '';
        this._referral.source = referrerMatch[2];
        this._referral.medium = 'organic';
        this._referral.campaign = '(not set)';
        this._referral.content = '';
        this._referral.keyword = referrer_search_term === '' ? '(not provided)' : referrer_search_term;
      }
    }

    // Return
    return this;
  },


  /**
   * Check for social media referral
   * @param {string} host - A URL.
   * @param {string} query - A query string.
   * @param {string} referrer - A referrer URL.
   * @returns {Object} visitAttribution
   */
  parseSocialMedia: function( host, query, referrer ) {
    // Referrer must not be the same host
    if ( typeof referrer === typeof '' && referrer.length > 0 &&
         hostsAreEqual( 'https://' + host, referrer ) === false ) {
      // Check for search engine
      const referrerMatch = referrer.match( /^https?:\/\/(www.)?(blogspot\.com|delicious\.com|deviantart\.com|disqus\.com|facebook\.com|faceparty\.com|fc2\.com|flickr\.com|flixster\.com|foursquare\.com|friendfeed\.com|friendster\.com|hi5\.com|linkedin\.com|livejournal\.com|myspace\.com|photobucket\.com|pinterest\.com|plus\.google\.com|reddit\.com|slideshare\.net|smugmug\.com|stumbleupon\.com|t\.co|tumblr\.com|twitter\.com|vimeo\.com|yelp\.com|youtube\.com)($|\/)/ );
      if ( referrerMatch !== null ) {
        // Get social network name
        const social_network = referrerMatch[2].split( '.' );

        // Set data
        this._referral.gclid = '';
        this._referral.source = social_network[0];
        this._referral.medium = 'social';
        this._referral.campaign = '(not set)';
        this._referral.content = '(not set)';
        this._referral.keyword = '(not set)';
      }
    }

    // Return
    return this;
  },


  /**
   * Check for website referral
   * @param {string} host - A URL.
   * @param {string} query - A query string.
   * @param {string} referrer - A referrer URL.
   * @returns {Object} visitAttribution
   */
  parseReferral: function( host, query, referrer ) {
    // Referrer must not be the same host
    if ( typeof referrer === typeof '' && referrer.length > 0 &&
         hostsAreEqual( 'https://' + host, referrer ) === false ) {
      // Check for search engine
      const referrerMatch = referrer.match( /^https?:\/\/([^\/]+)\/?(.*)$/ );
      if ( referrerMatch !== null ) {
        // Set data
        this._referral.gclid = '';
        this._referral.source = referrerMatch[1];
        this._referral.medium = 'referral';
        this._referral.campaign = '(not set)';
        this._referral.content = '/' + referrerMatch[2];
        this._referral.keyword = '';
      }
    }

    // Return
    return this;
  },


  /**
   * Check for direct
   * @param {string} host - A URL.
   * @param {string} query - A query string.
   * @param {string} referrer - A referrer URL.
   * @returns {Object} visitAttribution
   */
  parseDirect: function( host, query, referrer ) {

    if ( typeof referrer === typeof '' && referrer.length === 0 ) {

      // Set data
      this._referral.source = '(direct)';
      this._referral.medium = '(none)';
      this._referral.campaign = '(not set)';
    }

    // Return
    return this;
  },

  /**
   * Set cookie
   * @param {string} name - The key for the cookie value.
   * @param {string|Object} value - The cookie value.
   * @param {number} days - The lifetime of the cookie in days.
   * @param {boolean} escapeValue - Whether to escape the value or not.
   * @returns {Object} Referral
   */
  _setCookie: function( name, value, days, escapeValue ) {
    // Calculate expiration date
    const today = new Date();
    const expire = new Date();
    expire.setTime( today.getTime() + 3600000 * 24 * days );

    // Check if value is an object
    if ( typeof value === typeof {} ) {
      // JSON encode
      value = JSON.stringify( value );
    }

    if ( escapeValue !== false ) {
      value = escape( value );
    }

    // Set cookie
    document.cookie = name + '=' + value + ';expires=' + expire.toGMTString() + ';domain=.' + this._cookieDomain + ';path=/';

    // Return
    return this;
  },


  /**
   * Get cookie
   * @param {string} name - The key for the cookie value.
   * @returns {string} The cookie value.
   */
  _getCookie: function( name ) {
    // Get cookie value
    let value = ( document.cookie.match( '(^|; )' + name + '=([^;]*)' ) || 0 )[2];

    // Return empty string if cookie is not set
    let UNDEFINED;
    if ( value === UNDEFINED ) {
      value = '';
    }

    // Decode json
    try {
      return JSON.parse( decodeURIComponent( value ) );
    } catch ( e ) {
      // Do nothing.
    }

    // Return
    return decodeURIComponent( value );
  },


  /**
   * Get a query parameter value.
   * @param {string} queryString - A query string.
   * @param {string} key - The key for the query value.
   * @returns {string} The query parameter value.
   */
  _getQueryParameter: function( queryString, key ) {
    const query = queryString.substring( 1 );
    const vars = query.split( '&' );
    for ( let i = 0; i < vars.length; i++ ) {
      const pair = vars[i].split( '=' );
      if ( decodeURIComponent( pair[0] ) === key ) {
        return decodeURIComponent( pair[1] );
      }
    }
    return '';
  },


  /**
   * Get the query string.
   * @param {string} fullURL - A URL with query string.
   * @returns {string} - Just the query string of a full URL.
   */
  _getQueryString: function( fullURL ) {
    if ( typeof fullURL === typeof '' && fullURL.length > 0 ) {
      const url = document.createElement( 'a' );
      url.href = fullURL;

      let returnVal = url.search;

      if ( url.search === '' ) {
        returnVal = '?';
      }

      return returnVal;
    }

    // Return
    return '?';
  }
};

sourceCookies.update( document.location.host, document.location.search, document.referrer );
