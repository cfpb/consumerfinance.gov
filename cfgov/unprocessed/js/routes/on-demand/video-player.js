/* ==========================================================================
   Scripts for Video Player module.
   ========================================================================== */

import VideoPlayer from '../../organisms/VideoPlayer';
import { instantiateAll } from '@cfpb/cfpb-design-system';

instantiateAll(`.${VideoPlayer.BASE_CLASS}`, VideoPlayer);
