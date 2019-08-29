import {
	checkDom,
	instantiateAll
} from '../../modules/util/atomic-helpers';
import Expandable from 'cf-expandables/src/Expandable';
import Multiselect from '../../molecules/Multiselect';

const BASE_CLASS = 'filters';
const element = document.querySelector('.search_results');

if (element) {
	const _dom = checkDom( element, BASE_CLASS );
	const multiSelectsSelector = `.${ BASE_CLASS } .${ Multiselect.BASE_CLASS }`;

	instantiateAll( multiSelectsSelector, Multiselect );
}

Expandable.init();


