/* ==========================================================================
   Initialization script for Featured Content Module.
   ========================================================================== */

import FeaturedContentModule from '../../organisms/FeaturedContentModule';
import { instantiateAll } from '@cfpb/cfpb-design-system/src/index.js';

instantiateAll(`.${FeaturedContentModule.BASE_CLASS}`, FeaturedContentModule);
