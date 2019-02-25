import Expandable from 'cf-expandables/src/Expandable';
import Multiselect from '../../../js/molecules/Multiselect';
import { instantiateAll } from '../../../js/modules/util/atomic-helpers';

const multiSelects = instantiateAll(
  '.o-filterable-list-controls select[multiple]',
  Multiselect
);

const expandables = Expandable.init();
const expandable = expandables[0];

// If multiselects exist on the form, iterate over them.
multiSelects.forEach( multiSelect => {
  multiSelect.addEventListener( 'expandBegin', function refresh() {
    window.setTimeout(
      expandable.transition.expand.bind( expandable.transition ),
      250
    );
  } );

  multiSelect.addEventListener( 'expandEnd', function refresh() {
    window.setTimeout(
      expandable.transition.expand.bind( expandable.transition ),
      250
    );
  } );
} );
