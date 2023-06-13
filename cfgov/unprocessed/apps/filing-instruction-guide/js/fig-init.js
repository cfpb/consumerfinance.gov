import { SecondaryNav } from '../../../js/organisms/SecondaryNav.js';
import { init as figSidenavInit } from './fig-sidenav.js';
import { init as figSearchInit } from './fig-search.js';

let secondaryNav = SecondaryNav.init()[0];

figSidenavInit(secondaryNav);
figSearchInit(secondaryNav);
