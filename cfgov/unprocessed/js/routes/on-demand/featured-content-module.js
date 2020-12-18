/* ==========================================================================
   Initialization script for Featured Content Module.
   ========================================================================== */

import FeaturedContentModule from '../../organisms/FeaturedContentModule';
import { instantiateAll } from '@cfpb/cfpb-atomic-component/src/utilities/atomic-helpers.js';

instantiateAll( `.${ FeaturedContentModule.BASE_CLASS }`, FeaturedContentModule );
