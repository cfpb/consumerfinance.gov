'use strict';

var _stayInformedSection = element( by.css( '.o-email-signup' ) );

var _emailSubscribeForm = _stayInformedSection.element( by.css( 'form' ) );

var stayInformedSection = {

  stayInformedSection: _stayInformedSection,

  stayInformedSectionTitle:
  _stayInformedSection.element( by.css( '.m-slug-header .a-heading' ) ),

  emailSubscribeForm: _emailSubscribeForm,

  emailFormInput:
  _emailSubscribeForm.element( by.css( 'input[type="email"]' ) ),

  emailFormLabel: _emailSubscribeForm.element( by.css( 'label' ) ),

  emailFormHiddenField:
  _emailSubscribeForm.element( by.css( 'input[type="hidden"]' ) ),

  emailFormBtn: _emailSubscribeForm.element( by.css( 'input[type="submit"]' ) )

};

module.exports = stayInformedSection;
