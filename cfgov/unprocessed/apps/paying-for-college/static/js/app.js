'use strict';

// Count all features included in the test page.
$('.feature-list').append(
  '<section class="feature-list_item' +
  ' block block__padded-top block__border-top">' +
  '<div class="feature-header">' +
  '<h1 class="feature-header_name">jQuery</h1>' +
  '</div>' +
  '<p>jQuery is working and counts a total of ' +
  '<strong>' + $('.feature-list_item').size() + '</strong> ' +
  'cf-components.</p>' +
  '</section>'
);
