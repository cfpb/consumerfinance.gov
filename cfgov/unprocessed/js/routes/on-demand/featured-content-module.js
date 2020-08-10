/* ==========================================================================
   Initialization script for Featured Content Module.
   ========================================================================== */

import FeaturedContentModule from '../../organisms/FeaturedContentModule';
import { instantiateAll } from '../../modules/util/atomic-helpers';

instantiateAll( `.${ FeaturedContentModule.BASE_CLASS }`, FeaturedContentModule );
