import { checkDom, setInitFlag } from '../../../../../js/modules/util/atomic-helpers';
import inputView from '../input';
import transportationMap from '../../data/transportation-map';

const CLASSES = Object.freeze({
  CONTAINER: 'js-route-selection',
});

function ChoiceButtonView(element, { handleClick }) {
  const _dom = element;
  const _labelEl = _dom.querySelector('label');
  const _inputEl = _dom.querySelector('input');

  function _populateOptionLabel( route = {} ) {    
    const friendlyOption = transportationMap[route.transportation];
    const nextLabel = `Option ${ index + 1 }: ${ friendlyOption || '-' }`;
    _labelEl.textContent = nextLabel;
  }

  /**
   * Allow user to interact with this view's radio button form elements
   */
  function _enableChoice() {
    _dom.removeAttribute( 'disabled' );
  }

  /**
   * Disable route option selection radio button
   */
  function _disableChoice() {
    _dom.setAttribute( 'disabled', 'disabled' );
  }

  function _render({ route = {} } = {}) {
    _populateOptionLabel(route);

    if (route.transportation) {
      _enableChoice();
    } else {
      _disableChoice();
    }
  }

  return {
    init() {
      if (setInitFlag(_dom)) {
        inputView(_inputEl, {
          events: {
            'click': handleClick
          },
          type: 'radio'
        });

        /**
         * NOTE: Although all form controls are set to `disabled` in their templates,
         * we need to manually disable them again; all form controls are enabled once JS is detected.
         * This field is a special case in that it is the only form control which is
         * conditionally available based on data being input by the user.
        */
        _render();
      }
    },
    render: _render
  };
}

ChoiceButtonView.CLASSES = CLASSES;

export default ChoiceButtonView;
