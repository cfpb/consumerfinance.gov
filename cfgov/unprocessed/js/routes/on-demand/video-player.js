/* ==========================================================================
   Scripts for Video Player module.
   ========================================================================== */

import VideoPlayer from '../../organisms/VideoPlayer';
import { instantiateAll } from '@cfpb/cfpb-atomic-component';

instantiateAll(`.${VideoPlayer.BASE_CLASS}`, VideoPlayer);
