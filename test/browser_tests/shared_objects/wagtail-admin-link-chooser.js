const EC = protractor.ExpectedConditions;

const elements = {
  linkTypes:        '.modal .link-types',
  searchForm:       '.modal .search-form',
  searchInput:      '.modal .search-form input[name="q"]',
  pageListingTable: '.modal .listing.chooser'
};

const LINK_TYPES = {
  INTERNAL:  0,
  EXTERNAL:  1,
  EMAIL:     2
};

const selectedLink = {
  type: LINK_TYPES.INTERNAL
};

function enterSearchText( text ) {
  const searchInput = element( by.css( elements.searchInput ) );

  return browser.wait( EC.visibilityOf( searchInput ) )
    .then( function() {
      searchInput.sendKeys( text );
    } );
}

function getLinkAttributes( linkSelector ) {
  function _getLinkAttributes( _linkSelector ) {
    const linkElement = document.querySelector( _linkSelector );
    let attributes;

    if ( linkElement ) {
      const linkAttributes = linkElement.attributes;
      attributes = {
        dataUrl:       linkAttributes['data-title'].value,
        editUrl:       linkAttributes['data-id'].value,
        href:          linkAttributes['data-url'].value,
        id:            linkAttributes['data-id'].value,
        linkType:      'page',
        title:         linkAttributes['data-title'].value,
        parentId:      linkAttributes['data-parent-id'].value
      };
    }

    return attributes;
  }

  return browser.executeScript( _getLinkAttributes, linkSelector );
}

function getLinkHTML( linkAttributes, linkType = selectedLink.type ) {
  const internalLinkHTML = `<a href="${ linkAttributes.href }"` +
                         ` data-id="${ linkAttributes.id }"` +
                         ` data-parent-id="${ linkAttributes.parentId }"` +
                         ` data-linktype="${ linkAttributes.linkType }"` +
                         `>${ linkAttributes.title }</a>`;

  const mailLinkHTML = `<a href="maiilto:${ linkAttributes.url }"` +
                     ` data-original-title="${ linkAttributes.title }"` +
                     ` title="">${ linkAttributes.title }</a>`;

  const externallLinkHTML = `<a href="${ linkAttributes.url }"` +
                          ` data-original-title="${ linkAttributes.title }"` +
                          ` title="">${ linkAttributes.title }</a>`;

  const linkTypesHTML = {
    0: internalLinkHTML,
    1: externallLinkHTML,
    2: mailLinkHTML
  };

  return linkTypesHTML[linkType];
}

function setSelectedLink( linkSelector ) {

  return getLinkAttributes( linkSelector )
    .then( function( attributes ) {

      return setSelectedLinkProperty( 'attributes', attributes );
    } )
    .then( getLinkHTML )
    .then( function( HTML ) {

      return setSelectedLinkProperty( 'HTML', HTML );
    } );
}

function selectPageLink( linkTitle ) {
  const linkSelector = `.modal a[data-title=${ linkTitle }]`;
  const cfgovLink = element( by.css( linkSelector ) );

  return cfgovLink.click()
    .then( function() {

      return setSelectedLink( linkSelector );
    } );
}

function setSelectedLinkProperty( property, value ) {
  selectedLink[property] = value;

  return selectedLink[property];
}

const linkChooser = {
  enterSearchText:          enterSearchText,
  LINK_TYPES:               LINK_TYPES,
  selectedLink:             selectedLink,
  selectPageLink:           selectPageLink,
  setSelectedLinkProperty:  setSelectedLinkProperty
};

module.exports = linkChooser;
