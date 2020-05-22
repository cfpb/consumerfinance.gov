/* eslint max-len: "off" */

const _streamMenu = element.all( by.css( '.stream-menu' ) ).first();

function _getContentElement( selector ) {
  return _streamMenu.element( by.css( selector ) );
}

const content = {
  callToActionBtn:      _getContentElement( '.action-add-block-call_to_action' ),
  contentBtn:           _getContentElement( '.action-add-block-content' ),
  contentWithAnchorBtn: _getContentElement( '.action-add-block-content_with_anchor' ),
  emailSignupBtn:       _getContentElement( '.action-add-block-email_signup' ),
  expandableBtn:        _getContentElement( '.action-add-block-expandable' ),
  expandableGroupBtn:   _getContentElement( '.action-add-block-expandable_group' ),
  feedbackBtn:          _getContentElement( '.action-add-block-feedback' ),
  fullWidthTextBtn:     _getContentElement( '.action-add-block-full_width_text' ),
  mediaBtn:             _getContentElement( '.action-add-block-media' ),
  quoteBtn:             _getContentElement( '.action-add-block-quote' ),
  tableBlock:           _getContentElement( '.action-add-block-table_block' ),
  videoPlayerBtn:       _getContentElement( '.action-add-block-video_player' ),
  wellBtn:              _getContentElement( '.action-add-block-well' )
};

module.exports = content;
