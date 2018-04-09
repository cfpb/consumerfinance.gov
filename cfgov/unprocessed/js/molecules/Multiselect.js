// Required modules.
const arrayHelpers = require( '../modules/util/array-helpers' );
const atomicHelpers = require( '../modules/util/atomic-helpers' );
const bindEvent = require( '../modules/util/dom-events' ).bindEvent;
const domCreate = require( '../modules/util/dom-manipulators' ).create;
const queryOne = require( '../modules/util/dom-traverse' ).queryOne;
const standardType = require( '../modules/util/standard-type' );
const strings = require( '../modules/util/strings' );
const EventObserver = require( '../modules/util/EventObserver' );
const closeIcon = require(
  'svg-inline-loader!../../../../node_modules/cf-icons/src/icons/close.svg'
);
/**
 * Multiselect
 * @class
 *
 * @classdesc Initializes a new Multiselect molecule.
 *
 * @param {HTMLNode} element
 *   The DOM element within which to search for the molecule.
 * @returns {Multiselect} An instance.
 */
function Multiselect( element ) { // eslint-disable-line max-statements, inline-comments, max-len

  const BASE_CLASS = 'cf-multi-select';
  const LIST_CLASS = 'm-list';
  const CHECKBOX_INPUT_CLASS = 'a-checkbox';
  const TEXT_INPUT_CLASS = 'a-text-input';

  /* TODO: As the multiselect is developed further
     explore whether it should use an updated
     class name or data-* attribute in the
     markup so that it doesn't apply globally by default. */
  element.classList.add( BASE_CLASS );

  // Constants for direction.
  const DIR_PREV = 'prev';
  const DIR_NEXT = 'next';

  // Constants for key binding.
  const KEY_RETURN = 13;
  const KEY_ESCAPE = 27;
  const KEY_UP = 38;
  const KEY_DOWN = 40;
  const KEY_TAB = 9;

  // Search settings.
  const MIN_CHARS = 3;
  const MAX_SELECTIONS = 5;

  // Internal vars.
  let _dom = atomicHelpers.checkDom( element, BASE_CLASS );
  let _index = -1;
  let _isBlurSkipped = false;
  let _selectionsCount = 0;
  let _name;
  let _options;
  let _optionsData;
  let _filteredData;
  let _placeholder;

  // Markup elems, conver this to templating engine in the future.
  let _containerDom;
  let _selectionsDom;
  let _headerDom;
  let _searchDom;
  let _fieldsetDom;
  let _optionsDom;
  let _instance;

  /**
   * Set up and create the multi-select.
   * @returns {Multiselect|undefined} An instance,
   *   or undefined if it was already initialized.
   */
  function init() {
    if ( !atomicHelpers.setInitFlag( _dom ) ) {
      return standardType.UNDEFINED;
    }

    _instance = this;
    _name = _dom.name;
    _options = _dom.options || [];
    _placeholder = _dom.getAttribute( 'placeholder' );
    _filteredData = _optionsData = _sanitizeOptions( _options );

    if ( _optionsData.length > 0 ) {
      const newDom = _populateMarkup();

      /* Removes <select> element,
         and re-assign DOM reference. */
      _dom.parentNode.removeChild( _dom );
      _dom = newDom;

      /* We need to set init flag again since we've created a new <div>
         to replace the <select> element. */
      atomicHelpers.setInitFlag( _dom );

      _bindEvents();
    }

    return this;
  }

  /**
   * Expand the multi-select drop down.
   * @returns {Multiselect} An instance.
   */
  function expand() {
    _containerDom.classList.add( 'active' );
    _fieldsetDom.classList.remove( 'u-invisible' );
    _fieldsetDom.setAttribute( 'aria-hidden', false );
    _instance.dispatchEvent( 'expandBegin', { target: _instance } );

    return _instance;
  }

  /**
   * Collapse the multi-select drop down.
   * @returns {Multiselect} An instance.
   */
  function collapse() {
    _containerDom.classList.remove( 'active' );
    _fieldsetDom.classList.add( 'u-invisible' );
    _fieldsetDom.setAttribute( 'aria-hidden', true );
    _index = -1;
    _instance.dispatchEvent( 'expandEnd', { target: _instance } );

    return _instance;
  }

  /**
   * Cleans up a list of options for saving to memory.
   * @param   {Array} list The options from the parent select elem.
   * @returns {Array}      An array of option objects.
   */
  function _sanitizeOptions( list ) {
    let item;
    const cleaned = [];

    for ( let i = 0, len = list.length; i < len; i++ ) {
      item = list[i];

      // If the value isn't valid kill the script and prompt the developer.
      if ( !strings.stringValid( item.value ) ) {
        // TODO: Update to throw an error and handle the error vs logging.
        console.log( '\'' + item.value + '\' is not a valid value' );
        // TODO: Remove this line if the class is added via markup.
        element.classList.remove( BASE_CLASS );

        return false;
      }

      cleaned.push( {
        value:   item.value,
        text:    item.text,
        checked: item.defaultSelected
      } );
    }

    return cleaned;
  }

  /**
   * Populates and injects the markup for the custom multi-select.
   * @returns {HTMLNode} Newly created <div> element to hold the multiselect.
   */
  function _populateMarkup() {
    // Add a container for our markup
    _containerDom = domCreate( 'div', {
      className: BASE_CLASS,
      around:    _dom
    } );

    // Create all our markup but wait to manipulate the DOM just once
    _selectionsDom = domCreate( 'ul', {
      className: LIST_CLASS + ' ' +
                 LIST_CLASS + '__unstyled ' +
                 BASE_CLASS + '_choices',
      inside:    _containerDom
    } );

    _headerDom = domCreate( 'header', {
      className: BASE_CLASS + '_header'
    } );

    _searchDom = domCreate( 'input', {
      className:   BASE_CLASS + '_search ' + TEXT_INPUT_CLASS,
      type:        'text',
      placeholder: _placeholder || 'Choose up to five',
      inside:      _headerDom,
      id:          _name
    } );

    _fieldsetDom = domCreate( 'fieldset', {
      'className':   BASE_CLASS + '_fieldset u-invisible',
      'aria-hidden': 'true'
    } );

    _optionsDom = domCreate( 'ul', {
      className: LIST_CLASS + ' ' +
                 LIST_CLASS + '__unstyled ' +
                 BASE_CLASS + '_options',
      inside:    _fieldsetDom
    } );

    _optionsData.forEach( function( option ) {
      const _optionsItemDom = domCreate( 'li', {
        'data-option': option.value,
        'class': 'm-form-field m-form-field__checkbox'
      } );

      domCreate( 'input', {
        'id':     option.value,
        // Type must come before value or IE fails
        'type':    'checkbox',
        'value':   option.value,
        'name':    _name,
        'class':   CHECKBOX_INPUT_CLASS + ' ' + BASE_CLASS + '_checkbox',
        'inside':  _optionsItemDom,
        'checked': option.checked
      } );

      domCreate( 'label', {
        'for':         option.value,
        'textContent': option.text,
        'className':   BASE_CLASS + '_label a-label',
        'inside':      _optionsItemDom
      } );

      _optionsDom.appendChild( _optionsItemDom );

      if ( option.checked ) {
        const selectionsItemDom = domCreate( 'li', {
          'data-option': option.value,
          'class': 'm-form-field m-form-field__checkbox'
        } );

        domCreate( 'label', {
          'for':         option.value,
          'textContent': option.text,
          'className':   BASE_CLASS + '_label',
          'inside':      selectionsItemDom
        } );

        _selectionsDom.appendChild( selectionsItemDom );
        _selectionsCount += 1;
      }
    } );

    // Write our new markup to the DOM.
    _containerDom.appendChild( _headerDom );
    _containerDom.appendChild( _fieldsetDom );

    return _containerDom;
  }

  /**
   * Highlights an option in the list.
   * @param {string} direction Direction to highlight compared to the
   *                           current focus.
   */
  function _highlight( direction ) {
    const count = _filteredData.length;

    if ( direction === DIR_NEXT && _index < count - 1 ) {
      _index += 1;
    } else if ( direction === DIR_PREV && _index > -1 ) {
      _index -= 1;
    }

    if ( _index > -1 ) {
      const value = _filteredData[_index].value;
      const item = _optionsDom.querySelector( '[data-option="' + value + '"]' );
      const input = item.querySelector( 'input' );

      _isBlurSkipped = true;
      input.focus();
    } else {
      _isBlurSkipped = false;
      _searchDom.focus();
    }
  }

  /**
   * Tracks a user's selections and updates the list in the dom.
   * @param   {string} value The value of the option the user has chosen.
   */
  function _updateSelections( value ) {
    const optionIndex =
      arrayHelpers.indexOfObject( _optionsData, 'value', value );
    const option = _optionsData[optionIndex] || _optionsData[_index];

    if ( option ) {
      let _selectionsItemDom;

      if ( option.checked ) {
        if ( _optionsDom.classList.contains( 'max-selections' ) ) {
          _optionsDom.classList.remove( 'max-selections' );
        }

        const dataOptionSel = '[data-option="' + option.value + '"]';
        _selectionsItemDom = _selectionsDom.querySelector( dataOptionSel );

        if ( _selectionsItemDom ) {
          _selectionsDom.removeChild( _selectionsItemDom );
        }
        option.checked = false;
        _selectionsCount -= 1;
      } else {
        _selectionsItemDom = domCreate( 'li', {
          'data-option': option.value
        } );

        const _selectionsItemLabelDom = domCreate( 'label', {
          'innerHTML': option.text + closeIcon,
          'for':       option.value,
          'inside':    _selectionsItemDom
        } );

        _selectionsDom.appendChild( _selectionsItemDom );
        _selectionsItemDom.appendChild( _selectionsItemLabelDom );

        option.checked = true;
        _selectionsCount += 1;

        if ( _selectionsCount >= MAX_SELECTIONS ) {
          _optionsDom.classList.add( 'max-selections' );
        }
      }
    }

    _index = -1;
    _isBlurSkipped = false;

    if ( _fieldsetDom.getAttribute( 'aria-hidden' ) === 'false' ) {
      _searchDom.focus();
    }
  }

  /**
   * Evaluates the list of options based on the user's query in the
   * search input.
   * @param  {string} value Text the user has entered in the search query.
   */
  function _evaluate( value ) {
    _resetFilter();

    if ( value.length >= MIN_CHARS && _optionsData.length > 0 ) {
      _index = -1;

      _filteredData = _optionsData.filter( function( item ) {
        return strings.stringMatch( item.text, value );
      } );

      _filterResults();
    }
  }

  /**
   * Resets the search input and filtering.
   */
  function _resetSearch() {
    _searchDom.value = '';
    _resetFilter();
  }

  /**
   * Resets the filtered option list.
   */
  function _resetFilter() {
    _optionsDom.classList.remove( 'filtered', 'no-results' );

    for ( let i = 0, len = _optionsDom.children.length; i < len; i++ ) {
      _optionsDom.children[i].classList.remove( 'filter-match' );
    }

    _filteredData = _optionsData;
  }

  /**
   * Filters the list of options based on the results of the evaluate function.
   */
  function _filterResults() {
    _optionsDom.classList.add( 'filtered' );
    let _optionsItemDom;

    if ( _filteredData.length > 0 ) {
      _filteredData.forEach( function( option ) {
        _optionsItemDom =
          _optionsDom.querySelector( '[data-option="' + option.value + '"]' );

        _optionsItemDom.classList.add( 'filter-match' );
      } );
    } else {
      _noResults();
    }
  }

  /**
   * Updates the list of options to show the user there
   * are no matching results.
   */
  function _noResults() {
    _optionsDom.classList.add( 'no-results' );
    _optionsDom.classList.remove( 'filtered' );
  }

  /**
   * Binds events to the search input, option list, and checkboxes.
   */
  function _bindEvents() {
    const inputs = _optionsDom.querySelectorAll( 'input' );

    bindEvent( _searchDom, {
      input: function() {
        _evaluate( this.value );
      },
      focus: function() {
        expand();
      },
      blur: function() {
        if ( !_isBlurSkipped &&
              _fieldsetDom.getAttribute( 'aria-hidden' ) === 'false' ) {
          collapse();
        }
      },
      mousedown: function() {
        if ( _fieldsetDom.getAttribute( 'aria-hidden' ) === 'true' ) {
          expand();
        }
      },
      keydown: function( event ) {
        const key = event.keyCode;

        if ( _fieldsetDom.getAttribute( 'aria-hidden' ) === 'true' &&
             key !== KEY_TAB ) {
          expand();
        }

        if ( key === KEY_RETURN ) {
          event.preventDefault();
          _highlight( DIR_NEXT );
        } else if ( key === KEY_ESCAPE ) {
          _resetSearch();
          collapse();
        } else if ( key === KEY_DOWN ) {
          _highlight( DIR_NEXT );
        } else if ( key === KEY_TAB &&
                    !event.shiftKey &&
                    _fieldsetDom.getAttribute( 'aria-hidden' ) === 'false' ) {
          collapse();
        }
      }
    } );

    bindEvent( _optionsDom, {
      mousedown: function() {
        _isBlurSkipped = true;
      },
      keydown: function( event ) {
        const key = event.keyCode;
        const checked = event.target.checked;

        if ( key === KEY_RETURN ) {
          event.preventDefault();
          event.target.checked = !checked;

          queryOne( event.target ).dispatchEvent( 'change' );
        } else if ( key === KEY_ESCAPE ) {
          _searchDom.focus();
          collapse();
        } else if ( key === KEY_UP ) {
          _highlight( DIR_PREV );
        } else if ( key === KEY_DOWN ) {
          _highlight( DIR_NEXT );
        }
      }
    } );

    bindEvent( _fieldsetDom, {
      mousedown: function() {
        _isBlurSkipped = true;
      }
    } );

    for ( let i = 0, len = inputs.length; i < len; i++ ) {
      bindEvent( inputs[i], {
        change: _changeHandler
      } );
    }
  }

  /**
   * Handles the functions to trigger on the checkbox change.
   * @param   {Event} event The checkbox change event.
   */
  function _changeHandler( event ) {
    _updateSelections( event.target.value );
    _resetSearch();
  }

  // Attach public events.
  this.init = init;
  this.expand = expand;
  this.collapse = collapse;

  const eventObserver = new EventObserver();
  this.addEventListener = eventObserver.addEventListener;
  this.removeEventListener = eventObserver.removeEventListener;
  this.dispatchEvent = eventObserver.dispatchEvent;

  return this;
}

module.exports = Multiselect;
