import { analyticsSendEvent } from '@cfpb/cfpb-analytics';

(function () {
  let action =
    window.location.pathname + window.location.search + window.location.hash;
  action = action.replace('#', 'GA_HASHTAG');
  const label = document.title;

  analyticsSendEvent({ event: 'Virtual Pageview', action, label });
})();
