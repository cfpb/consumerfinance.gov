import FilterableListControls from '../../organisms/FilterableListControls';
import { checkDom, setInitFlag } from '../../modules/util/atomic-helpers';
const _dom = document.querySelector('.filters')
let _filterableListControls = new FilterableListControls(
     _dom.querySelector( `.${ FilterableListControls.BASE_CLASS }` )
);
    
_filterableListControls.init();