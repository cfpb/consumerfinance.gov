import Expandable from '@cfpb/cfpb-expandables/src/Expandable';
import Multiselect from '@cfpb/cfpb-forms/src/organisms/Multiselect';
import { instantiateAll } from '@cfpb/cfpb-atomic-component';

const multiSelectsSelector = `.${Multiselect.BASE_CLASS}`;

if (document.querySelector(multiSelectsSelector)) {
  instantiateAll(multiSelectsSelector, Multiselect);
}

Expandable.init();
