import beforeExpandableTransitionInit, {
  setInnerWidth, MOBILE_COLLAPSED_CLASS
} from '../../../../../cfgov/unprocessed/apps/teachers-digital-platform/js/expandable-mobile.js';

// Markup created with settings: is_expanded=true, is_collapsed_for_mobile=true
const HTML_SNIPPET = `
  <div id="test-div" data-qa-hook="expandable"
     class="o-expandable
            o-expandable__padded
            o-expandable__background
            ">
    <button class="o-expandable_header o-expandable_target" type="button">
        <span class="h4 o-expandable_header-left o-expandable_label">
            Building block
        </span>
        <span class="o-expandable_header-right o-expandable_link">
            <span class="o-expandable_cue o-expandable_cue-open">
                <span class="u-visually-hidden-on-mobile
                            u-visually-hidden">
                    Show
                </span>
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 1200" class="cf-icon-svg"><path d="M500 105.2c-276.1 0-500 223.9-500 500s223.9 500 500 500 500-223.9 500-500-223.9-500-500-500zm263.1 550.7H549.6v213.6c0 27.6-22.4 50-50 50s-50-22.4-50-50V655.9H236c-27.6 0-50-22.4-50-50s22.4-50 50-50h213.6V342.3c0-27.6 22.4-50 50-50s50 22.4 50 50v213.6h213.6c27.6 0 50 22.4 50 50s-22.5 50-50.1 50z"/></svg>
            </span>
            <span class="o-expandable_cue o-expandable_cue-close">
                <span class="u-visually-hidden-on-mobile
                             u-visually-hidden">
                    Hide   
                </span>
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 1200" class="cf-icon-svg"><path d="M500 105.2c-276.1 0-500 223.9-500 500s223.9 500 500 500 500-223.9 500-500-223.9-500-500-500zm263.1 550.7H236c-27.6 0-50-22.4-50-50s22.4-50 50-50h527.1c27.6 0 50 22.4 50 50s-22.4 50-50 50z"/></svg>
            </span>
        </span>
    </button>

    <div class="o-expandable_content
                o-expandable_content__onload-open
                o-expandable__mobile-collapsed">
            <div class="o-form_group u-mt15">
                <fieldset class="o-form_fieldset">
                    <ul class="m-list m-list__unstyled">
                        <li>
                            <div class="m-form-field m-form-field__checkbox">
                                <input type="checkbox" class="a-checkbox" aria-label="Executive function" id="building-block--executive-function" name="building_block" value="1">
                                <label class="a-label" for="building-block--executive-function">Executive function</label>
                            </div>
                        </li>
                    </ul>
                </fieldset>
            </div>
      </div>
  </div>
`;

global.console = { error: jest.fn(), log: jest.fn() };

let testDiv;
let expandableDiv;
const OPEN_DEFAULT_CLASS = 'o-expandable_content__onload-open';

describe( 'expandable-mobile', () => {

  beforeEach( () => {
    setInnerWidth( 1000 );
    // Load HTML fixture
    document.body.innerHTML = HTML_SNIPPET;
    testDiv = document.querySelector( '#test-div' );
    expandableDiv = document.querySelector( '#test-div .o-expandable_content' );
  } );

  it( 'should not throw any errors on init', () => {
    expect( () => beforeExpandableTransitionInit() ).not.toThrow();
  } );

  /**
   * These tests just need to show that beforeExpandableTransitionInit()
   * can conditionally remove some class names used in the
   * cfExpandables.init() process, and clean up its own class in the
   * "expandable" template organism.
   */

  it( 'should remove the OPEN_DEFAULT class on narrow innerWidth', () => {
    setInnerWidth( 900 );

    expect( expandableDiv.classList.contains( OPEN_DEFAULT_CLASS ) )
      .toEqual( true );
    beforeExpandableTransitionInit();
    expect( expandableDiv.classList.contains( OPEN_DEFAULT_CLASS ) )
      .toEqual( false );

  } );

  it( 'should leave the OPEN_DEFAULT class for tablet innerWidth', () => {
    setInnerWidth( 901 );

    expect( expandableDiv.classList.contains( OPEN_DEFAULT_CLASS ) )
      .toEqual( true );
    beforeExpandableTransitionInit();
    expect( expandableDiv.classList.contains( OPEN_DEFAULT_CLASS ) )
      .toEqual( true );

  } );

  it( 'should always remove its MOBILE_COLLAPSED_CLASS (narrow)', () => {
    setInnerWidth( 900 );

    beforeExpandableTransitionInit();
    expect( expandableDiv.classList.contains( MOBILE_COLLAPSED_CLASS ) )
      .toEqual( false );

  } );

  it( 'should always remove its MOBILE_COLLAPSED_CLASS (wide)', () => {
    setInnerWidth( 901 );

    beforeExpandableTransitionInit();
    expect( expandableDiv.classList.contains( MOBILE_COLLAPSED_CLASS ) )
      .toEqual( false );

  } );

} );
