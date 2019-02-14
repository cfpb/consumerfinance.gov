// Required modules.
import * as arrayHelpers from '../modules/util/array-helpers';
import * as atomicHelpers from '../modules/util/atomic-helpers';
import { bindEvent } from '../modules/util/dom-events';
import { create } from '../modules/util/dom-manipulators';
import { stringMatch } from '../modules/util/strings';
import EventObserver from '../modules/util/EventObserver';
import MultiselectModel from './MultiselectModel';

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

  const BASE_CLASS = 'o-multiselect';
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

  // Internal vars.
  let _dom = atomicHelpers.checkDom( element, BASE_CLASS );
  let _isBlurSkipped = false;
  let _name;
  let _placeholder;
  let _model;
  let _options;
  let _optionsData;

  // Markup elems, conver this to templating engine in the future.
  let _containerDom;
  let _selectionsDom;
  let _headerDom;
  let _searchDom;
  let _fieldsetDom;
  let _optionsDom;
  const _optionItemDoms = [];
  let _instance;

  /**
   * Set up and create the multiselect.
   * @returns {Multiselect|undefined} An instance,
   *   or undefined if it was already initialized.
   */
  function init() {
    if ( !atomicHelpers.setInitFlag( _dom ) ) {
      let UNDEFINED;
      return UNDEFINED;
    }

    _instance = this;
    _name = _dom.name;
    _placeholder = _dom.getAttribute( 'placeholder' );
    _options = _dom.options || [];

    if ( _options.length > 0 ) {
      _model = new MultiselectModel( _options ).init();
      _optionsData = _model.getOptions();
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
   * Expand the multiselect drop down.
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
   * Collapse the multiselect drop down.
   * @returns {Multiselect} An instance.
   */
  function collapse() {
    _containerDom.classList.remove( 'active' );
    _fieldsetDom.classList.add( 'u-invisible' );
    _fieldsetDom.setAttribute( 'aria-hidden', true );
    _model.resetIndex();
    _instance.dispatchEvent( 'expandEnd', { target: _instance } );

    return _instance;
  }

  /**
   * Populates and injects the markup for the custom multiselect.
   * @returns {HTMLNode} Newly created <div> element to hold the multiselect.
   */
  function _populateMarkup() {
    // Add a container for our markup
    _containerDom = create( 'div', {
      className: BASE_CLASS,
      around:    _dom
    } );

    // Create all our markup but wait to manipulate the DOM just once
    _selectionsDom = create( 'ul', {
      className: LIST_CLASS + ' ' +
                 LIST_CLASS + '__unstyled ' +
                 BASE_CLASS + '_choices',
      inside:    _containerDom
    } );

    _headerDom = create( 'header', {
      className: BASE_CLASS + '_header'
    } );

    _searchDom = create( 'input', {
      className:   BASE_CLASS + '_search ' + TEXT_INPUT_CLASS,
      type:        'text',
      placeholder: _placeholder || 'Choose up to five',
      inside:      _headerDom,
      id:          _name
    } );

    _fieldsetDom = create( 'fieldset', {
      'className':   BASE_CLASS + '_fieldset u-invisible',
      'aria-hidden': 'true'
    } );

    _optionsDom = create( 'ul', {
      className: LIST_CLASS + ' ' +
                 LIST_CLASS + '__unstyled ' +
                 BASE_CLASS + '_options',
      inside:    _fieldsetDom
    } );

    _optionsData.forEach( function( option ) {
      const _optionsItemDom = create( 'li', {
        'data-option': option.value,
        'class': 'm-form-field m-form-field__checkbox'
      } );

      create( 'input', {
        'id':     option.value,
        // Type must come before value or IE fails
        'type':    'checkbox',
        'value':   option.value,
        'name':    _name,
        'class':   CHECKBOX_INPUT_CLASS + ' ' + BASE_CLASS + '_checkbox',
        'inside':  _optionsItemDom,
        'checked': option.checked
      } );

      create( 'label', {
        'for':         option.value,
        'textContent': option.text,
        'className':   BASE_CLASS + '_label a-label',
        'inside':      _optionsItemDom
      } );

      _optionItemDoms.push( _optionsItemDom );
      _optionsDom.appendChild( _optionsItemDom );

      if ( option.checked ) {
        const selectionsItemDom = create( 'li', {
          'data-option': option.value,
          'class': 'm-form-field m-form-field__checkbox'
        } );

        create( 'label', {
          'for':         option.value,
          'textContent': option.text,
          'className':   BASE_CLASS + '_label',
          'inside':      selectionsItemDom
        } );

        _selectionsDom.appendChild( selectionsItemDom );
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
    if ( direction === DIR_NEXT ) {
      _model.setIndex( _model.getIndex() + 1 );
    } else if ( direction === DIR_PREV ) {
      _model.setIndex( _model.getIndex() - 1 );
    }

    const index = _model.getIndex();
    if ( index > -1 ) {
      let filteredIndex = index;
      const filterIndices = _model.getFilterIndices();
      if ( filterIndices.length > 0 ) {
        filteredIndex = filterIndices[index];
      }
      const option = _model.getOption( filteredIndex );
      const value = option.value;
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
   * @param {string} value The value of the option the user has chosen.
   */
  function _updateSelections( value ) {
    const optionIndex = arrayHelpers.indexOfObject(
      _optionsData,
      'value',
      value
    );
    const option = _optionsData[optionIndex] || _optionsData[_model.getIndex()];

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
      } else {
        _selectionsItemDom = create( 'li', {
          'data-option': option.value
        } );

        const _selectionsItemLabelDom = create( 'label', {
          'innerHTML': option.text + closeIcon,
          'for':       option.value,
          'inside':    _selectionsItemDom
        } );

        _selectionsDom.appendChild( _selectionsItemDom );
        _selectionsItemDom.appendChild( _selectionsItemLabelDom );
      }
      _model.toggleOption( optionIndex );

      if ( _model.isAtMaxSelections() ) {
        _optionsDom.classList.add( 'max-selections' );
      }

      _instance.dispatchEvent( 'selectionsUpdated', { target: _instance } );
    }

    _model.resetIndex();
    _isBlurSkipped = false;

    if ( _fieldsetDom.getAttribute( 'aria-hidden' ) === 'false' ) {
      _searchDom.focus();
    }
  }

  /**
   * Evaluates the list of options based on the user's query in the
   * search input.
   * @param {string} value Text the user has entered in the search query.
   */
  function _evaluate( value ) {
    _resetFilter();
    _model.resetIndex();
    const matchedIndices = _model.filterIndices( value );
    _filterList( matchedIndices );
  }

  /**
   * Resets the search input and filtering.
   */
  function _resetSearch() {
    _searchDom.value = '';
    _resetFilter();
  }

  /**
   * Filter the options list.
   * Every time we filter we have two lists of indices:
   * - The matching options (filterIndices).
   * - The matching options of the last filter (_lastFilterIndices).
   * We need to turn off the filter for any of the last filter matches
   * that are not in the new set, and turn on the filter for the matches
   * that are not in the last set.
   * @param {Array} filterIndices - List of indices to filter from the options.
   * @returns {boolean} True if options are filtered, false otherwise.
   */
  function _filterList( filterIndices = [] ) {
    if ( filterIndices.length > 0 ) {
      _filterMatches( filterIndices );
      return true;
    }

    _filterNoMatches();
    return false;
  }

  /**
   * Resets the filtered option list.
   */
  function _resetFilter() {
    _optionsDom.classList.remove( 'u-filtered', 'u-no-results' );

    for ( let i = 0, len = _optionsDom.children.length; i < len; i++ ) {
      _optionsDom.children[i].classList.remove( 'u-filter-match' );
    }

    _model.clearFilter();
  }

  /**
   * Set the filtered matched state.
   * @param {Array} filterIndices - List of indices to filter from the options.
   */
  function _filterMatches( filterIndices ) {
    _optionsDom.classList.remove( 'u-no-results' );
    _optionsDom.classList.add( 'u-filtered' );
    _model.getLastFilterIndices().forEach( index => {
      _optionItemDoms[index].classList.remove( 'u-filter-match' );
    } );
    _model.getFilterIndices().forEach( index => {
      _optionItemDoms[index].classList.add( 'u-filter-match' );
    } );
  }

  /**
   * Updates the list of options to show the user there
   * are no matching results.
   */
  function _filterNoMatches() {
    _optionsDom.classList.add( 'u-no-results' );
    _optionsDom.classList.remove( 'u-filtered' );
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
        if ( _fieldsetDom.getAttribute( 'aria-hidden' ) === 'true' ) {
          expand();
        }
      },
      blur: function() {
        if ( !_isBlurSkipped &&
              _fieldsetDom.getAttribute( 'aria-hidden' ) === 'false' ) {
          collapse();
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
        const target = event.target;
        const checked = target.checked;

        if ( key === KEY_RETURN ) {
          event.preventDefault();

          /* Programmatically checking a checkbox does not fire a change event
          so we need to manually create an event and dispatch it from the input.
          */
          target.checked = !checked;
          const evt = document.createEvent( 'HTMLEvents' );
          evt.initEvent( 'change', false, true );
          target.dispatchEvent( evt );
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

export default Multiselect;
