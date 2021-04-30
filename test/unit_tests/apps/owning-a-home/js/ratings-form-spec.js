import * as ratingsForm from '../../../../../cfgov/unprocessed/apps/owning-a-home/js/ratings-form.js';
import { simulateEvent } from '../../../../util/simulate-event.js';

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
    ratingsForm.init();

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
