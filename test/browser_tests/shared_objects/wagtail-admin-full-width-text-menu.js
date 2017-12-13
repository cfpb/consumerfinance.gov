/* eslint max-len: "off" */


const fullWidthTextSelector = 'input[value=\'full_width_text\']' +
                            ' + .sequence-controls' +
                            ' + .sequence-member-inner';

function isActive( ) {
  function _getElement( selector ) {
    return document.querySelector( selector ) !== null;
  }

  return browser.executeScript( _getElement, fullWidthTextSelector );
}

function getMenuItems() {
  const _fullWidthText = element
    .all( by.css( fullWidthTextSelector ) )
    .first();

  function _getFullWidthTextElement( selector ) {

    return _fullWidthText.element( by.css( selector ) );
  }

  return {
    callToActionBtn:      _getFullWidthTextElement( '.action-add-block-cta' ),
    contentBtn:           _getFullWidthTextElement( '.action-add-block-content' ),
    contentWithAnchorBtn: _getFullWidthTextElement( '.action-add-block-image_text_25_75_group' ),
    imageInsetBtn:        _getFullWidthTextElement( '.action-add-block-image_inset' ),
    mediaBtn:             _getFullWidthTextElement( '.action-add-block-media' ),
    quoteBtn:             _getFullWidthTextElement( '.action-add-block-quote' ),
    relatedLinksBtn:      _getFullWidthTextElement( '.action-add-block-related_links' ),
    reusableTextBtn:      _getFullWidthTextElement( '.action-add-block-reusable_text' ),
    tableBlock:           _getFullWidthTextElement( '.action-add-block-table_block' )
  };

}

const fullWidthMenu = {
  isActive:     isActive,
  getMenuItems: getMenuItems
};

module.exports = fullWidthMenu;
