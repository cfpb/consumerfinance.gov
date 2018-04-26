const BASE_JS_PATH = '../../../../../cfgov/unprocessed/apps/';

import { simulateEvent } from '../../../../util/simulate-event';

let feedBackLinkElement;
let ratingsInputs;

const HTML_SNIPPET = `
  <form method="post"
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
                          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 1200" class="cf-icon-svg rating-message_icon"><path d="M500 105.2c-276.1 0-500 223.9-500 500s223.9 500 500 500 500-223.9 500-500-223.9-500-500-500zm259 284.2L481.4 870.3c-8.2 14.1-22.7 23.4-39 24.8-1.4.1-2.9.2-4.3.2-14.8 0-28.9-6.6-38.4-18L244.4 690.9c-17.9-21-15.4-52.6 5.7-70.5 21-17.9 52.6-15.4 70.5 5.7.2.3.5.5.7.8l109.4 131.4 241.8-418.8c13.6-24 44.2-32.4 68.2-18.8 24 13.6 32.4 44.2 18.8 68.2l-.5.5z"/></svg>
                          <span class="rating-message_text">
                            Thank you for your feedback!
                          </span>
                      </div>
                  </li>
              </ul>
              <a class="a-link a-link__jump feedback-link"
                 href="/owning-a-home/feedback/">
                  <span class="a-link_text">Provide additional feedback</span>
              </a>
          </div>
      </fieldset>
  </form>
`;

describe( 'ratings-form', () => {

  beforeEach( () => {
    document.body.innerHTML = HTML_SNIPPET;
    require(
      BASE_JS_PATH + 'owning-a-home/js/ratings-form'
    ).init();

    ratingsInputs = document.querySelectorAll( '.rating-inputs input' );
    feedBackLinkElement = document.querySelector( '.feedback-link' );
  } );

  it( 'should add the change event listener when init called', () => {
    simulateEvent( 'click', ratingsInputs[0] );

    expect( ratingsInputs[0].checked ).toBe( true );
    expect( ratingsInputs[1].checked ).toBe( false );
  } );

  it( 'should update the feeback link when an input is clicked', () => {
    simulateEvent( 'click', ratingsInputs[1] );

    expect( feedBackLinkElement.href ).toContain( '?is_helpful=1' );
  } );

  it( 'should disable the ratings inputs when an input is clicked', () => {
    simulateEvent( 'click', ratingsInputs[0] );

    expect( ratingsInputs[0].disabled ).toBe( true );
    expect( ratingsInputs[1].disabled ).toBe( true );
  } );

} );
