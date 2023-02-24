/* ==========================================================================
   Initialization script for Featured Content Module.
   ========================================================================== */

import FeaturedContentModule from '../../organisms/FeaturedContentModule';
import { instantiateAll } from '@cfpb/cfpb-atomic-component';

instantiateAll(`.${FeaturedContentModule.BASE_CLASS}`, FeaturedContentModule);
