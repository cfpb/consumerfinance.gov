
( function( jQuery ) {

  function TextCount( element, options ) {
    this.element = element;
    this.elements = {};
    this.options = jQuery.extend( this.options, options || {} );
    this.isBound = false;
  }

  var TextCountAPI = {

    REGEXES:  {
      WHITESPACE: /\S+/gm,
      TAGS:       /(<([^>]+)>)/ig,
      TEMPLATE:   /\{\{\s?(.*?)\s?\}\}/g
    },

    SELECTORS: {
      CHARS_COUNT: '.text-count_chars-count',
      TEXT_COUNT:  '.text-count',
      WORD_COUNT:  '.text-count_word-count',
    },

    TEMPLATES: {
      CHAR_COUNT: [
        '<div class="text-count help" style="color:{{ stateColor }}">',
          '<span class="text-count_word-count">{{ wordCount }}</span>',
          ' words',
          ' - ',
          '<span class="text-count_chars-count">{{ charCount }}</span>',
          ' characters',
        '</div>'].join('')
    },

    getTemplateData: function getTemplateData( wordCount, charCount ) {
      return {
        char_count: charCount,
        word_count: wordCount
      }
    },

    getTemplateMarkup: function getTemplateMarkup( templateString, data ) {
      function replaceTokens( match, token ) {
        return data[token] || '';
      }

      return templateString.replace( this.REGEXES.TEMPLATE, replaceTokens );
    },

    getTextCount: function getTextCount( text ) {
      var NO_SPACE = '';
      var words = text.match( this.REGEXES.WHITESPACE );
      var textNoTags = text.replace( this.REGEXES.TAGS, NO_SPACE );

      return {
        charCount: textNoTags.length,
        wordCount: words ? words.length : 0,
      };
    },

    updateDOM: function updateDOM( params ) {
      if ( this.isBound === false ) {
        var data = this.getTemplateData( params.wordCount, params.charCount );
        var markup = this.getTemplateMarkup( this.TEMPLATES.CHAR_COUNT, data );
        params.element.append( markup );

        this._setElements();
        this.isBound = true;
      }

      this.elements.wordCount.html( params.wordCount );
      this.elements.charCount.html( params.charCount );
      this.elements.container.css( 'color', params.stateColor );
    },

    _setElements: function setElements() {
      var SELECTORS = this.SELECTORS;
      var element = this.element;
      var elements = this.elements;

      elements.charCount = element.find( SELECTORS.CHARS_COUNT );
      elements.container = element.find( SELECTORS.TEXT_COUNT );
      elements.wordCount = element.find( SELECTORS.WORD_COUNT );
    }
  }

  $.extend( TextCount.prototype, TextCountAPI );

  var EVENTS = {
    UPDATE_CHAR_LEN: 'update:character:length',
    HALLO_MODIFIED:  'hallomodified',
  }

  var stateColors = {
    alert:   '#ff0000',
    default: '#008000',
    warning: '#ffa500'
  };

  function HeroHeadingTextCount( element, options ) {
    this.element = element;
    this.options = jQuery.extend( this.options, options || {} );
    this.isBound = false;
    this.textCount = new TextCount( element );
    this.maxChars = this.options.thresholds.maxChars;
    this.maxWarningChars = this.options.thresholds.maxWarningChars;

    this._setElements();
    this._initializeEvents();
  }

  var HeroHeadingTextCountAPI = {

    SELECTORS: {
      INPUT:         'input',
      FIELD_CONTENT: '.field-content'
    },

    options: {
      stateColors: {
        alert:   '#ff0000',
        default: '#008000',
        warning: '#ffa500'
      },
      thresholds: {
        maxChars:        82,
        maxWarningChars: 41
      }

    },

    _initializeEvents: function _initializeEvents() {
      this.elements.input.on( 'keyup', $.proxy( this.eventListeners.inputModified, this ) );
    },

    eventListeners: {
      inputModified: function inputModified( event, data ) {
        var text = event.currentTarget.value;
        var textCount = this.textCount.getTextCount( text );
        var stateColor = this._getCharStateColor( textCount.charCount );
        var params = {
          element:    this.elements.fieldContent,
          wordCount:  textCount.wordCount,
          charCount:  textCount.charCount,
          stateColor: stateColor
        };

        this.textCount.updateDOM( params );
        this.element.trigger( {
          type:  EVENTS.UPDATE_CHAR_LEN,
          value: textCount
        } );
      }
    },

    _getCharStateColor: function _getCharStateColor( charCount ) {
      var stateColor = this.options.stateColors.default;

      if ( charCount > this.maxChars ) {
        stateColor = this.options.stateColors.alert;
      } else if ( charCount > this.maxWarningChars  ) {
        stateColor = this.options.stateColors.warning;
      }

      return stateColor;
    },

    _setElements: function _setElements() {
      var SELECTORS = this.SELECTORS;
      var elements = this.elements = {};

      elements.input = this.element.find( SELECTORS.INPUT );
      elements.fieldContent = this.element.find( SELECTORS.FIELD_CONTENT );
    }
  }

  $.extend( HeroHeadingTextCount.prototype, HeroHeadingTextCountAPI );

  jQuery.widget( 'IKS.HeroTextCount', {

    options: {
      stateColors: stateColors,
      thresholds: {
        oneLineHeader:     {
          header: 41,
          body:   [ 165, 186 ]
        },
        twoLineHeader:     {
          header: 82,
          body:   [ 108, 124 ]
        }
      }
    },

    SELECTORS: {
      FIELDS:             '.fields',
      FIELD_CONTENT:      '.field-content',
      HERO_BODY:          '.hero_body',
      HERO_HEADING:       '.hero_heading',
      HERO_HEADING_INPUT: '.hero_heading input',
      TEXT_AREA:          'textarea'
    },

    eventListeners: {
      halloModified: function halloModified() {
        this.textCount.updateDOM( this._getDOMData() );
      },

      headingModified: function headingModified( ) {
        this._setThresholds();
        this.textCount.updateDOM( this._getDOMData() );
      }
    },

    _create: function _create() {
      if ( this._isHeroBlock() === false ) {
        return;
      }

      this.maxChars = this.options.maxChars;
      this.maxWarningChars = this.options.maxWarningChars;

      this._setElements();
      this.textCount = new TextCount( this.elements.fieldContent );
      this.headingTextCount = new HeroHeadingTextCount( this.elements.heroHeading );
      this._initializeEvents();
      this._setThresholds();
    },

    _isHeroBlock: function _isHeroBlock() {
      return this.element.closest( this.SELECTORS.HERO_BODY ).length > 0;
    },

    _getDOMData: function _getDOMData() {
      var text = this.element.data( 'IKS-hallo' ).getContents();
      var textCount = this.textCount.getTextCount( text );
      var stateColor = this._getCharStateColor( textCount.charCount );

      return {
        element:    this.elements.fieldContent,
        wordCount:  textCount.wordCount,
        charCount:  textCount.charCount,
        stateColor: stateColor
      };
    },

    _getCharStateColor: function _getCharStateColor( charCount ) {
      var stateColor = this.options.stateColors.default;

      if ( charCount > this.maxChars ) {
        stateColor = this.options.stateColors.alert;
      } else if ( charCount > this.maxWarningChars  ) {
        stateColor = this.options.stateColors.warning;
      }

      return stateColor;
    },

    _initializeEvents: function _initializeEvents() {
      this.element.on(
        EVENTS.HALLO_MODIFIED,
        jQuery.proxy( this.eventListeners.halloModified, this )
      );

      this.elements.heroHeading.on(
        EVENTS.UPDATE_CHAR_LEN,
        jQuery.proxy( this.eventListeners.headingModified, this )
      );
    },

    _setElements: function _setElements() {
      var SELECTORS = this.SELECTORS;
      var elements = this.elements = {};

      elements.fieldContent = this.element.closest( SELECTORS.FIELD_CONTENT );
      elements.fields = elements.fieldContent.closest( SELECTORS.FIELDS );
      elements.heroHeading = elements.fields.find( SELECTORS.HERO_HEADING );
      elements.heroBody = elements.fields.find( SELECTORS.HERO_BODY );
      elements.heroHeadingInput = elements.fields.find( SELECTORS.HERO_HEADING_INPUT );
      elements.textArea = elements.fieldContent.find( SELECTORS.TEXT_AREA );
    },

    _setThresholds: function _setThresholds() {
      var headingTextCount = this.elements.heroHeadingInput.val().length;
      var oneLineThreshold = this.options.thresholds.oneLineHeader;
      var twoLineThreshold = this.options.thresholds.twoLineHeader;

      this.maxChars = oneLineThreshold.body[1];
      this.maxWarningChars = oneLineThreshold.body[0];

      if ( headingTextCount >= oneLineThreshold.header ) {
        this.maxChars = twoLineThreshold.body[1];
        this.maxWarningChars = twoLineThreshold.body[0];
      }
    }

  } );

  if ( 'registerHalloPlugin' in window ) {
    registerHalloPlugin( 'HeroTextCount' );
  }
} ( jQuery ) );
