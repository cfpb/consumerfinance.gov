const BASE_JS_PATH = '../../../../cfgov/unprocessed/js/';
const chai = require( 'chai' );
const expect = chai.expect;
const sinon = require( 'sinon' );
let feedBackLinkElement;
let ratingsInputs;
let sandbox;

const HTML_SNIPPET =
  `<form method="post"
        class="o-form
               oah-ratings-form
               block
               block__bg
               block__border
               block__padded-top">
      <fieldset class="o-form_fieldset u-reset">
          <legend class="a-legend">
              <span class="h4">Was this page helpful to you?</span>
          </legend>
          <div class="rating-inputs">
              <ul class="content-l m-list m-list__unstyled">
                  <li class="content-l_col content-l_col-1-3">
                      <div class="m-form-field
                                  m-form-field__radio
                                  m-form-field__lg-target">
                          <input class="a-radio"
                                 id="is_helpful_0"
                                 type="radio"
                                 name="is_helpful"
                                 value="0">
                          <label class="a-label"
                                 for="is_helpful_0">
                              Yes
                          </label>
                      </div>
                  </li>
                  <li class="content-l_col content-l_col-1-3">
                      <div class="m-form-field
                                  m-form-field__radio
                                  m-form-field__lg-target">
                              <input class="a-radio"
                                     id="is_helpful_1"
                                     type="radio"
                                     name="is_helpful"
                                     value="1">
                              <label class="a-label"
                                     for="is_helpful_1">
                                  No
                              </label>
                      </div>
                  </li>
                  <li class="content-l_col content-l_col-1-3">
                      <div class="rating-message message-column">
                          <span class="cf-icon cf-icon-approved-round
                                       rating-message_icon"></span>
                          <span class="rating-message_text">Thank you
                                       for your feedback!</span>
                      </div>
                  </li>
              </ul>
              <a class="a-link a-link__jump feedback-link"
                 href="/owning-a-home/feedback/">
                  <span class="a-link_text">Provide additional feedback</span>
              </a>
          </div>
      </fieldset>
  </form>`;

function triggerClickEvent( target ) {
  const event = document.createEvent( 'Event' );
  event.initEvent( 'click', true, true );
  target.dispatchEvent( event );

  event.initEvent( 'change', true, false );
  target.dispatchEvent( event );
}

describe( 'ratings-form', () => {
  before( () => {
    this.jsdom = require( 'jsdom-global' )( HTML_SNIPPET );
  } );

  after( () => this.jsdom() );

  beforeEach( () => {
    sandbox = sinon.sandbox.create();
    document.body.innerHTML = HTML_SNIPPET;
    require(
      BASE_JS_PATH + 'apps/owning-a-home/ratings-form'
    ).init();

    ratingsInputs = document.querySelectorAll( '.rating-inputs input' );
    feedBackLinkElement = document.querySelector( '.feedback-link' );
  } );

  afterEach( () => {
    sandbox.restore();
  } );

  it( 'should add the change event listener when init called', () => {
    triggerClickEvent( ratingsInputs[0] );

    expect( ratingsInputs[0].checked ).to.equal( true );
    expect( ratingsInputs[1].checked ).to.equal( false );
  } );

  it( 'should update the feeback link when an input is clicked', () => {
    triggerClickEvent( ratingsInputs[1] );

    expect( feedBackLinkElement.href ).to.contain( '?is_helpful=1' );
  } );

  it( 'should disable the ratings inputs when an input is clicked', () => {
    triggerClickEvent( ratingsInputs[0] );

    expect( ratingsInputs[0].disabled ).to.equal( true );
    expect( ratingsInputs[1].disabled ).to.equal( true );
  } );

} );
