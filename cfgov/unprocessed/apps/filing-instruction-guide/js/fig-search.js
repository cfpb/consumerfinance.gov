import search from 'ctrl-f';

const buttonText = 'Search this guide';

// See https://fusejs.io/api/options.html
const searchOptions = {
  keys: [ 'contents' ],
  includeMatches: true,
  includeScore: true,
  minMatchCharLength: 3,
  ignoreLocation: true,
  threshold: 0.4
};

/* Each searchable item (an HTML section with a heading and some paragraphs)
   is tagged with a `data-search-section` attribute in the jinja2 template */
const sections = [ ...document.querySelectorAll( '[data-search-section]' ) ];

/**
 * Generate a list of structured items to search
 * @param {array} sections - HTML elements containing FIG headings and
 * paragraphs of content
 * @returns {array} Structured list of objects to be passed to search engine
 */
const getSearchData = sections => {
  if ( !sections ) return [];
  return sections.map( ( section, i ) => {
    const heading = section.querySelector( '.o-fig_heading' );
    const link = heading.querySelector( '[id]' ).getAttribute( 'id' );
    return {
      id: i,
      title: heading.textContent.replace( /^\s+|\s+$/g, '' ),
      contents: section.textContent.split( '\n' ).join( ' ' ),
      link: '#' + link
    };
  } );
};

const searchContainer = document.getElementById( 'ctrl-f' );
const searchData = getSearchData( sections );

search( searchContainer, { buttonText, searchOptions, searchData } );

export { getSearchData };
