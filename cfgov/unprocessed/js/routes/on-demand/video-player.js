/* ==========================================================================
   Scripts for Video Player module.
   ========================================================================== */

import VideoPlayer from '../../organisms/VideoPlayer';
import { instantiateAll } from '../../modules/util/atomic-helpers';

instantiateAll( `.${ VideoPlayer.BASE_CLASS }`, VideoPlayer );
