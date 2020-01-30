import Expandable from '@cfpb/cfpb-expandables/src/Expandable';
import Multiselect from '../../../../molecules/Multiselect';
import { instantiateAll } from '../../../../modules/util/atomic-helpers';

const multiSelectsSelector = `.${ Multiselect.BASE_CLASS }`;

if ( document.querySelector( multiSelectsSelector ) ) {
  instantiateAll( multiSelectsSelector, Multiselect );
}

Expandable.init();
