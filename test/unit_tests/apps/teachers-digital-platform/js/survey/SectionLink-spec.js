import SectionLink from '../../../../../../cfgov/unprocessed/apps/teachers-digital-platform/js/survey/SectionLink';
import HTML_SNIPPET from '../../html/survey-page';

describe( 'SectionLink', () => {
  let buttons;

  const colors = () => [ ...buttons ]
    .map( button => button.getAttribute( 'data-color' ) )
    .filter( color => color !== 'gray' );
  const texts = () => [ ...buttons ].map( button => button.textContent.replace( /\s+/g, ' ' ) );

  beforeEach( () => {
    document.body.innerHTML = HTML_SNIPPET;

    buttons = document.querySelectorAll( '.tdp-survey-section' );
  } );

  it( 'init should set up text', () => {
    SectionLink.init( {
      numAnswered: 1,
      pageIdx: 0,
      questionsByPage: [ 6, 2, 7, 3, 2 ]
    } );

    expect( texts()[0] ).toMatch( 'Section 1 (in progress)' );
    expect( texts()[0] ).toMatch( 'Questions 1–6' );
    expect( texts()[1] ).toMatch( 'Questions 7–8' );
    expect( texts()[2] ).toMatch( 'Questions 9–15' );
    expect( texts()[3] ).toMatch( 'Questions 16–18' );
    expect( texts()[4] ).toMatch( 'Questions 19–20' );
    expect( colors() ).toEqual( [ 'blue' ] );
  } );

  it( 'init on page 2', () => {
    SectionLink.init( {
      numAnswered: 6,
      pageIdx: 1,
      questionsByPage: [ 6, 2, 7, 3, 2 ]
    } );

    expect( texts()[0] ).toMatch( '(complete)' );
    expect( texts()[1] ).toMatch( 'Section 2 (in progress)' );
    expect( colors() ).toEqual( [ 'green', 'blue' ] );
  } );

  it( 'init editing page 1 from 2', () => {
    SectionLink.init( {
      numAnswered: 6,
      pageIdx: 0,
      questionsByPage: [ 6, 2, 7, 3, 2 ]
    } );

    expect( texts()[1] ).toMatch( 'Section 2 (in progress)' );
    expect( colors() ).toEqual( [ 'blue', 'white' ] );
  } );

  it( 'init editing page 1 from 3', () => {
    SectionLink.init( {
      numAnswered: 8,
      pageIdx: 0,
      questionsByPage: [ 6, 2, 7, 3, 2 ]
    } );

    expect( texts()[2] ).toMatch( 'Section 3 (in progress)' );
    expect( colors() ).toEqual( [ 'blue', 'green', 'white' ] );
  } );

  it( 'editing page 1', () => {
    SectionLink.init( {
      numAnswered: 6,
      pageIdx: 2,
      questionsByPage: [ 6, 2, 7, 3, 2 ]
    } );

    expect( buttons[0].getAttribute( 'href' ) ).toEqual( '../p1/' );
    expect( buttons[0].dataset.editable ).toEqual( '1' );
  } );

  it( 'prevents nav to uneditable sections', () => {
    SectionLink.init( {
      numAnswered: 6,
      pageIdx: 1,
      questionsByPage: [ 6, 2, 7, 3, 2 ]
    } );

    let clicks = 0;
    document.body.addEventListener( 'click', event => {
      clicks++;
    } );

    // Editable doesn't stop event
    expect( buttons[0].dataset.editable ).toEqual( '1' );
    buttons[0].click();
    expect( clicks ).toEqual( 1 );

    // Non-editable does
    expect( buttons[1].dataset.editable ).toEqual( '' );
    buttons[1].click();
    expect( clicks ).toEqual( 1 );
  } );

  it( 'responds to new answers', () => {
    SectionLink.init( {
      numAnswered: 1,
      pageIdx: 0,
      questionsByPage: [ 6, 2, 7, 3, 2 ]
    } );
    SectionLink.update( 6 );

    expect( buttons[0].getAttribute( 'data-checked' ) ).toEqual( '1' );
    expect( texts()[0] ).toMatch( '(complete)' );
  } );
} );
