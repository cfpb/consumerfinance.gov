// Count all features included in the test page.
$('.feature-list').append(
  '<li class="feature-list_item">' +
  '<h3 class="feature-list_header">jQuery</h3>' +
  '<p>jQuery counts a total of ' +
  '<strong>' + ( $('.feature-list li').size() + 1 ) + '</strong> ' +
  'features.</p>' +
  '</li>'
);
