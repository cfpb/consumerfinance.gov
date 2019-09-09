import { instantiateAll } from '../../../../modules/util/atomic-helpers';
import Expandable from 'cf-expandables/src/Expandable';
import Multiselect from '../../../../molecules/Multiselect';

const multiSelectsSelector = `.${ Multiselect.BASE_CLASS }`;

if ( document.querySelector( multiSelectsSelector ) ) {
  instantiateAll( multiSelectsSelector, Multiselect );
}

Expandable.init();
