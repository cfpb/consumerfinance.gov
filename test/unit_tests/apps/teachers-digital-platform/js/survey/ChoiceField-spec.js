import ChoiceField from '../../../../../../cfgov/unprocessed/apps/teachers-digital-platform/js/survey/ChoiceField';
import { ANSWERS_SESS_KEY } from '../../../../../../cfgov/unprocessed/apps/teachers-digital-platform/js/survey/config';
import HTML_SNIPPET from '../../html/survey-page';

const $ = document.querySelector.bind( document );

describe( 'ChoiceField', () => {
  beforeEach( () => {
    document.body.innerHTML = HTML_SNIPPET;
  } );

  it( 'init should set up cache', () => {
    ChoiceField.init();

    expect( Object.keys( ChoiceField.cache ).length ).toEqual( 6 );
  } );

  it( 'restoreFromSession should sync from inputs', () => {
    sessionStorage.clear();
    const store = ChoiceField.restoreFromSession( ANSWERS_SESS_KEY );

    const answers = JSON.parse( sessionStorage.getItem( ANSWERS_SESS_KEY ) );
    expect( answers ).toEqual( { 'p1-q6': '3' } );
    expect( store ).toEqual( { 'p1-q6': '3' } );
  } );

  it( 'restoreFromSession should sync to inputs', () => {
    sessionStorage.clear();
    const answers = { 'p1-q2': '1' };
    sessionStorage.setItem( ANSWERS_SESS_KEY, JSON.stringify( answers ) );
    ChoiceField.restoreFromSession( ANSWERS_SESS_KEY );

    const input = $( 'input[name="p1-q6"][value="3"]' );
    expect( input.checked ).toBeTruthy();
  } );

  it( 'watchAndStore watches and updates store and field', () => {
    const onStoreUpdate = jest.fn();
    ChoiceField.watchAndStore( ANSWERS_SESS_KEY, {}, onStoreUpdate );

    $( 'label[for="id_p1-q3_1"]' ).click();

    expect( onStoreUpdate ).toHaveBeenCalled();
    const answers = JSON.parse( sessionStorage.getItem( ANSWERS_SESS_KEY ) );
    expect( answers ).toEqual( { 'p1-q3': '1' } );

    const field = ChoiceField.get( 'p1-q3' );
    expect( field.value ).toEqual( '1' );
  } );
} );
