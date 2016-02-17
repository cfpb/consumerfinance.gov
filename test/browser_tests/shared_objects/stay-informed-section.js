'use strict';

var _getQAelement = require( '../util/qa-element' ).get;

var _stayInformedSection = _getQAelement( 'stay-informed-section' );

var _emailSubscribeForm =
_stayInformedSection.element( by.css( '#email-subscribe-form' ) );

var stayInformedSection = {

  stayInformedSection: _stayInformedSection,

  stayInformedSectionTitle:
  _stayInformedSection.element( by.css( '.header-slug_inner' ) ),

  emailSubscribeForm: _emailSubscribeForm,

  emailFormInput:
  _emailSubscribeForm.element( by.css( 'input[type="email"]' ) ),

  emailFormLabel: _emailSubscribeForm.element( by.css( 'label' ) ),

  emailFormDescription: _getQAelement( 'stay-informed-desc' ),

  emailFormHiddenField:
  _emailSubscribeForm.element( by.css( 'input[type="hidden"]' ) ),

  emailFormBtn: _emailSubscribeForm.element( by.css( 'input[type="submit"]' ) )

};

module.exports = stayInformedSection;
