// ********************************
//
// Blast Analytics & Marketing
// Create Source Attribution Cookie
//
// ********************************

var sourceCookies = {

	//zeroPad - prepends '0' before numbers 0-9
	zeroPad : function(n) {
		var r = n.toString();
		if (n <= 9 && n >= 0) {r = '0' + n.toString() };
		return r;
	},

	/**
	 * session length in milliseconds : defaul 30 mins
	 */
	_sessionLength : 1800000,

	/**
	 * Cookie domain name
	 */
	_cookieDomain : '{{cookie domain}}',

	/**
	 * Session cookie name
	 */
	_sourceCookieName : '_A_source',

	/**
	 * Session cookie name
	 */
	_timeCookieName : '_A_time',

	/**
	 * Classic analytics parameter mapping
	 */
	_classicParameterMap : {
		gclid    : 'utmgclid',
		source   : 'utmcsr',
		campaign : 'utmccn',
		medium   : 'utmcmd',
		keyword  : 'utmctr',
		content  : 'utmcct'
	},

	/**
	 * Referral source
	 */
	_referral : {
		gclid    : '',
		source   : '',
		campaign : '',
		medium   : '',
		keyword  : '',
		content  : '',
		date     : ''
	},

	_timeStamps : {
		visitCount : 0,
		currentVisit : (new Date()).getTime()
	},



	/**
	 * Determine referral source
	 * @param string host
	 * @param string query
	 * @param string referrer
	 * @return visitAttribution
	 */
	update : function(host, query, referrer)
	{
	    var q = new Date(); sourceString = timeString = newSource = newTime = "";
	    this._referral.date = q.getTime();
	    this._timeStamps.firstVisit = this._timeStamps.currentVisit;

		// Determine referral source
		this
			.parseDirect(host, query, referrer)
			.parseReferral(host, query, referrer)
			.parseOrganicSearch(host, query, referrer)
			.parseUTMparameters(host, query, referrer)
			.parseAdWords(host, query, referrer);

			//.parseSocialMedia(host, query, referrer)

		// set temp source values
		for(var property in this._referral){
			if(property != 'date' && this._referral[property].length > 0){
				newSource = newSource + this._classicParameterMap[property] + '=' + this._referral[property].replace(/\s/g, '%20') + '|';
			}
		}

		// Remove trailing pipe
		newSource = newSource.slice(0, -1);

		if (this._getCookie(this._timeCookieName) !== '') {
			this._timeStamps.firstVisit = Number((this._getCookie(this._timeCookieName)).split(/\./)[1]);
			this._timeStamps.visitCount = Number((this._getCookie(this._timeCookieName)).split(/\./)[0]);
			this._newSession = ( (this._referral.date - Number((this._getCookie(this._timeCookieName)).split(/\./)[2])) > this._sessionLength )
		}

		if (this._getCookie(this._sourceCookieName) !== '') {
			sourceString = this._getCookie(this._sourceCookieName);

			if(newSource == '') {
				newSource = sourceString;
			}
		}




		if( (sourceString != decodeURIComponent(newSource)) || this._newSession ) {
			// check values
			// set cookies
			this._timeStamps.visitCount++;
			this._setCookie(this._sourceCookieName, newSource, 365*2, false);//.0208 visitAttribution._sessionLength*(1/24/60/60/1000);
          	// trigger any dataLayer actions desired
            if (this._timeStamps.visitCount == 1) {
	            var vSource = newSource.split('|')[0].split('=')[1];
	            var vMedium = newSource.split('|')[1].split('=')[1];
	            var vCampaign = newSource.split('|')[2].split('=')[1];
				dataLayer.push({'firstSource':vSource, 'firstMedium':vMedium, 'firstCampaign':vCampaign, 'visitNumber':this._timeStamps.visitCount, 'event':'visitCounter'});
			} else {
              dataLayer.push({'visitNumber':this._timeStamps.visitCount, 'event':'visitCounter'});
            }
		}
		// set time values
		newTime = this._timeStamps.visitCount + "." + this._timeStamps.firstVisit + "." + this._timeStamps.currentVisit;

		// set time cookie, updated current visit
		this._setCookie(this._timeCookieName, newTime, 365*2, false);

		return
	},



	/**
	 * Check for AdWords referral
	 * @param string host
	 * @param string query
	 * @param string referrer
	 * @return visitAttribution
	 */
	parseAdWords : function(host, query, referrer)
	{
		// Check for gclid or gclsrc
		if(this._getQueryParameter(query, 'gclid') != '' || this._getQueryParameter(query, 'gclsrc') != '')
		{
			this._referral.gclid = '' + this._getQueryParameter(query, 'gclid') + this._getQueryParameter(query, 'gclsrc') + '';
			//source
			if (this._getQueryParameter(query, 'utm_source') != '')
				this._referral.source = this._getQueryParameter(query, 'utm_source');
			else
				this._referral.source = 'google';
			//medium
			if (this._getQueryParameter(query, 'utm_medium') != '')
				this._referral.medium = this._getQueryParameter(query, 'utm_medium');
			else
				this._referral.medium = 'cpc';
			//campaign
			if (this._getQueryParameter(query, 'utm_campaign') != '')
				this._referral.campaign	= this._getQueryParameter(query, 'utm_campaign');
			else
				this._referral.campaign	= '(not set)';
			//content
			if (this._getQueryParameter(query, 'utm_content') != '')
				this._referral.content = this._getQueryParameter(query, 'utm_content');
			else
				this._referral.content = '';
			//keyword
			if (this._getQueryParameter(query, 'utm_term') != '')
				this._referral.keyword = this._getQueryParameter(query, 'utm_term');
			else
				this._referral.keyword = '(not provided)';

		}

		// Return
		return this;
	},



	/**
	 * Check for UTM parameters
	 * @param string host
	 * @param string query
	 * @param string referrer
	 * @return visitAttribution
	 */
	parseUTMparameters : function(host, query, referrer)
	{
		// Check for gclid or gclsrc
		if(this._getQueryParameter(query, 'utm_source') != '')
		{
			// Set data
			this._referral.gclid = this._getQueryParameter(query, 'gclid');
			this._referral.source = this._getQueryParameter(query, 'utm_source');
			this._referral.medium = this._getQueryParameter(query, 'utm_medium');
			this._referral.campaign = this._getQueryParameter(query, 'utm_campaign');
			this._referral.content = this._getQueryParameter(query, 'utm_content');
			this._referral.keyword = this._getQueryParameter(query, 'utm_term');
		}

		// Return
		return this;
	},



	/**
	 * Check for organic search referral
	 * @param string host
	 * @param string query
	 * @param string referrer
	 * @return visitAttribution
	 */
	parseOrganicSearch : function(host, query, referrer)
	{
		// Referrer must not be the same host
		if(this._hostsAreEqual('http://' + host, referrer) === false)
		{

			// Check for search engine
			referrer_match = referrer.match(/^https?:\/\/(.*\.search\.|www\.)?(google|bing|aol|yahoo|ask|comcast).([a-z]+)([\.a-z]{3,5})?\//);
			if(referrer_match != null)
			{
				// Referrer query string
				var referrer_query = this._getQueryString(referrer);

				// Referrer search term
				var referrer_search_term = this._getQueryParameter(referrer_query, 'q');

				// Set data
				this._referral.gclid	= '';
				this._referral.source	= referrer_match[2];
				this._referral.medium	= 'organic';
				this._referral.campaign	= '(not set)';
				this._referral.content	= '';
				this._referral.keyword	= (referrer_search_term == '') ? '(not provided)' : referrer_search_term;
			}
		}

		// Return
		return this;
	},



	/**
	 * Check for social media referral
	 * @param string host
	 * @param string query
	 * @param string referrer
	 * @return visitAttribution
	 */
	parseSocialMedia : function(host, query, referrer)
	{
		// Referrer must not be the same host
		if(typeof(referrer) == typeof('') && referrer.length > 0 && this._hostsAreEqual('http://' + host, referrer) === false)
		{
			// Check for search engine
			referrer_match = referrer.match(/^https?:\/\/(www.)?(blogspot\.com|delicious\.com|deviantart\.com|disqus\.com|facebook\.com|faceparty\.com|fc2\.com|flickr\.com|flixster\.com|foursquare\.com|friendfeed\.com|friendster\.com|hi5\.com|linkedin\.com|livejournal\.com|myspace\.com|photobucket\.com|pinterest\.com|plus\.google\.com|reddit\.com|slideshare\.net|smugmug\.com|stumbleupon\.com|t\.co|tumblr\.com|twitter\.com|vimeo\.com|yelp\.com|youtube\.com)($|\/)/);
			if(referrer_match != null)
			{
				// Get social network name
				var social_network = referrer_match[2].split('.');

				// Set data
				this._referral.gclid	= '';
				this._referral.source	= social_network[0];
				this._referral.medium	= 'social';
				this._referral.campaign	= '(not set)';
				this._referral.content	= '(not set)';
				this._referral.keyword	= '(not set)';
			}
		}

		// Return
		return this;
	},



	/**
	 * Check for website referral
	 * @param string host
	 * @param string query
	 * @param string referrer
	 * @return visitAttribution
	 */
	parseReferral : function(host, query, referrer)
	{
		// Referrer must not be the same host
		if(typeof(referrer) == typeof('') && referrer.length > 0 && this._hostsAreEqual('http://' + host, referrer) === false)
		{
			// Check for search engine
			referrer_match = referrer.match(/^https?:\/\/([^\/]+)\/?(.*)$/);
			if(referrer_match != null)
			{
				// Set data
				this._referral.gclid	= '';
				this._referral.source	= referrer_match[1];
				this._referral.medium	= 'referral';
				this._referral.campaign	= '(not set)';
				this._referral.content	= '/' + referrer_match[2];
				this._referral.keyword	= '';
			}
		}

		// Return
		return this;
	},



	/**
	 * Check for direct
	 * @param string host
	 * @param string query
	 * @param string referrer
	 * @return visitAttribution
	 */
	parseDirect : function(host, query, referrer)
	{

		if(typeof(referrer) == typeof('') && referrer.length == 0)
		{

			// Set data
			this._referral.source	= '(direct)';
			this._referral.medium	= '(none)';
			this._referral.campaign	= '(not set)';
		}

		// Return
		return this;
	},



	/**
	 * Set cookie
	 * @param string name
	 * @param string|object value
	 * @param int days
	 * @return Referral
	 */
	_setCookie : function(name, value, days, escape_value)
	{
		// Calculate expiration date
		var today = new Date();
		var expire = new Date();
		expire.setTime(today.getTime() + 3600000 * 24 * days);

		// Check if value is an object
		if(typeof(value) == typeof({}))
		{
			// JSON encode
			value = JSON.stringify(value);
		}

		if(escape_value != false)
		{
			value = escape(value);
		}

		// Set cookie
		document.cookie = name + "=" + value + ";expires=" + expire.toGMTString() + ';domain=.' + this._cookieDomain + ';path=/';

		// Return
		return this;
	},



	/**
	 * Get cookie
	 * @param string name
	 * @return string
	 */
	_getCookie : function(name)
	{
		// Get cookie value
		var value = ((document.cookie.match('(^|; )' + name + '=([^;]*)')||0)[2]);

		// Return empty string if cookie is not set
		if(value == undefined)
		{
			value = '';
		}

		// Decode json
		try
		{
			return JSON.parse(decodeURIComponent(value));
		}catch(e){}

		// Return
		return decodeURIComponent(value);
	},



	/**
	 * Get a query parameter value
	 * @param string queryString
	 * @param string key
	 * @return string
	 */
	_getQueryParameter : function(queryString, key)
	{
	    var query = queryString.substring(1);
		var vars = query.split('&');
		for (var i = 0; i < vars.length; i++)
		{
	        var pair = vars[i].split('=');
			if (decodeURIComponent(pair[0]) == key)
			{
	            return decodeURIComponent(pair[1]);
			}
		}
		return '';
	},



	/**
	 * Get the query string
	 * @param string fullURL
	 * @return string
	 */
	_getQueryString : function(fullURL)
	{
		if(typeof(fullURL) == typeof('') && fullURL.length > 0)
		{
			url = document.createElement("a");
			url.href = fullURL;

			return (url.search != '') ? url.search : '?';
		}

		// Return
		return '?';
	},



	/**
	 * Check if two hosts are the same
	 * @param string host1
	 * @param string host2
	 * @return bool
	 */
	_hostsAreEqual : function(host1, host2)
	{
		h1 = document.createElement("a");
		h1.href = host1;

		h2 = document.createElement("a");
		h2.href = host2;

		// Check for www
		h1 = h1.host;
		if(h1.substring(0, 4) == 'www.')
		{
			h1 = h1.substring(4);
		}
		h2 = h2.host;
		if(h2.substring(0, 4) == 'www.')
		{
			h2 = h2.substring(4);
		}

		// Return
		return h1 == h2;
	}



}


sourceCookies.update(document.location.host, document.location.search, document.referrer);
