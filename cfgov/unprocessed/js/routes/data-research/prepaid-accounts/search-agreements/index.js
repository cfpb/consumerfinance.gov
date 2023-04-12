import { Expandable } from '@cfpb/cfpb-expandables';
import { Multiselect } from '@cfpb/cfpb-forms';
import { instantiateAll } from '@cfpb/cfpb-atomic-component';

const multiSelectsSelector = `.${Multiselect.BASE_CLASS}`;

if (document.querySelector(multiSelectsSelector)) {
  instantiateAll(multiSelectsSelector, Multiselect);
}

Expandable.init();
