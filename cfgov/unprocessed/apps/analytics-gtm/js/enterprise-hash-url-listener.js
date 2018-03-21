var HashURLListener = (function() {
  var action = window.location.pathname + window.location.search + window.location.hash;
  action = action.replace("#", "GA_HASHTAG");
  var label = document.title;

  dataLayer.push({
    "event": 'Virtual Pageview',
    "action": action,
    "label": label
  });

})();
