import { checkDom, setInitFlag } from '@cfpb/cfpb-atomic-component/src/utilities/atomic-helpers.js';

const CLASSES = Object.freeze( {
  CHECKLIST_GROUP_CONTAINER: 'm-checklist-group'
} );

function checklistGroup( element, { selectedItems } ) {
  const _dom = checkDom( element, CLASSES.CHECKLIST_GROUP_CONTAINER );

  function _getChecklistItemNode( checkboxValue ) {
    const selector = `input[value="${ checkboxValue }"]`;
    return _dom.querySelector( selector );
  }

  function _isInput( node ) {
    return node.tagName === 'INPUT';
  }

  function _isChecked( checkbox ) {
    return checkbox.checked;
  }

  function _elementToUncheck( valueToUncheck ) {
    return function uncheckCheckbox() {
      const inputToUncheck = _getChecklistItemNode( valueToUncheck );
      inputToUncheck.checked = '';
    };
  }

  function _handleChecklistItemSelect( event ) {
    const node = event.target;

    if ( _isInput( node ) ) {
      const selectedItem = node.value;

      if ( _isChecked( node ) ) {
        if ( selectedItems.isMaxItemsSelected() ) {
          const lastSelectedVal = selectedItems.getLast();
          const uncheckCheckboxFn = _elementToUncheck( lastSelectedVal );

          selectedItems.remove( lastSelectedVal );

          /* the browser could schedule a repaint during uncheck op, so
             schedule the uncheck to happen at the beginning of the next
             stack frame */
          setTimeout( uncheckCheckboxFn, 0 );
        }
        selectedItems.add( selectedItem );
      } else {
        selectedItems.remove( selectedItem );
      }
    }
  }


  return {
    init() {
      if ( setInitFlag( _dom ) ) {
        _dom.addEventListener( 'click', _handleChecklistItemSelect );
      }
    }
  };
}

export default checklistGroup;
