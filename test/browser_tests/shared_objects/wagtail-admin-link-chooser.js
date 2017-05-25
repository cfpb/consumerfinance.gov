
'use strict';


let EC = protractor.ExpectedConditions;

let elements = {
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

let selectedLink = {
  type: LINK_TYPES.INTERNAL
};

function enterSearchText( text ) {
  let searchInput = element( by.css( elements.searchInput ) );

  return browser.wait( EC.visibilityOf( searchInput ), 500 )
         .then( function() {
            searchInput.sendKeys( text );
         } );
}

function getLinkAttributes( linkSelector ) {
  function _getLinkAttributes( _linkSelector ) {
    var linkElement = document.querySelector( _linkSelector );
    var attributes;

    if ( linkElement ) {
      var linkAttributes = linkElement.attributes;
      attributes = {
        dataUrl:       linkAttributes['data-title'].value,
        editUrl:       linkAttributes['data-id'].value,
        href:          linkAttributes['href'].value,
        id:            linkAttributes['data-id'].value,
        linkType:      'page',
        title:         linkAttributes['data-title'].value,
        parentId:      linkAttributes['data-parent-id'].value
      }
    }

    return attributes;
  }

  return browser.executeScript( _getLinkAttributes, linkSelector );
}

function getLinkHTML(linkAttributes, linkType=selectedLink.type ) {
  let internalLinkHTML = `<a href="${linkAttributes.href}"` +
                         ` data-id="${linkAttributes.id}"` +
                         ` data-parent-id="${linkAttributes.parentId}"` +
                         ` data-linktype="${linkAttributes.linkType}"` +
                         ` data-original-title="${linkAttributes.title}"`+
                         ` title="">${linkAttributes.title}</a>`;

  let mailLinkHTML = `<a href="maiilto:${linkAttributes.url}"` +
                     ` data-original-title="${linkAttributes.title}"`+
                     ` title="">${linkAttributes.title}</a>`;

  let externallLinkHTML = `<a href="${linkAttributes.url}"` +
                          ` data-original-title="${linkAttributes.title}"`+
                          ` title="">${linkAttributes.title}</a>`;

  let linkTypesHTML = {
    0: internalLinkHTML,
    1: externallLinkHTML,
    2: mailLinkHTML
  }

  return linkTypesHTML[linkType];
}

function setLinkAttributes( linkAttributes={} ) {
  selectedLink.attributes = linkAttributes

  return Promise.resolve( linkAttributes );
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
  let linkSelector = `.modal a[data-title=${linkTitle}]`;
  let cfgovLink = element( by.css( linkSelector ) );

  return cfgovLink.click()
         .then( function( HTML ) {

           return setSelectedLink( linkSelector );
         } );
}

function setSelectedLinkProperty( property, value ) {

  return selectedLink[property] = value;
}

let linkChooser = {
  enterSearchText:          enterSearchText,
  LINK_TYPES:               LINK_TYPES,
  selectedLink:             selectedLink,
  selectPageLink:           selectPageLink,
  setSelectedLinkProperty:  setSelectedLinkProperty
};

module.exports = linkChooser;
