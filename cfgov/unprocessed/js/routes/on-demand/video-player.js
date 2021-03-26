/* ==========================================================================
   Scripts for Video Player module.
   ========================================================================== */

import VideoPlayer from '../../organisms/VideoPlayer';
import { instantiateAll } from '@cfpb/cfpb-atomic-component/src/utilities/atomic-helpers.js';

instantiateAll( `.${ VideoPlayer.BASE_CLASS }`, VideoPlayer );
