import TodoNotification from '../../../../../../cfgov/unprocessed/apps/youth-employment-success/js/views/todo-notification.js';
import TODO_FIXTURE from '../../fixtures/todo-alert.js';

const CONTAINER = 'alert-container';
const HTML = `
  <div id=${ CONTAINER }></div>
  ${ TODO_FIXTURE }
`;

describe( 'TodoNotification', () => {
  let instance;
  let container;

  beforeEach( () => {
    document.body.innerHTML = HTML;
    instance = new TodoNotification();
    container = document.getElementById( CONTAINER );
  } );

  afterEach( () => {
    document.body.innerHTML = '';
    container.innerHTML = null;
    container = null;
    instance = null;
  } );

  it( 'returns itself on init', () => {
    expect( instance.init( container ) ).toEqual( instance );
  } );

  it( 'throws an error if not initialized with a dom node', () => {
    expect( () => instance.init() ).toThrow();
  } );

  it( 'sets the notification element as a static property on init', () => {
    expect( instance.element ).toBe( null );

    instance.init( container );

    expect( instance.element ).toBeDefined();
  } );

  it( 'appends an alert to the container when .show is called', () => {
    instance.init( container );
    instance.show();

    const children = container.children;

    expect( children.length ).toBe( 1 );
    expect( children[0] ).toBe( document.querySelector(
      `.${ TodoNotification.CLASSES.CONTAINER }`
    ) );
  } );

  it( 'removes the `add` alert and appends the `remove` alert', () => {
    instance.init( container );
    instance.show();

    expect(
      document.querySelector( '.js-alert-content' )
        .textContent.indexOf( 'added' )
    ).toBeGreaterThan( -1 );

    instance.hide();

    expect(
      document.querySelector( '.js-alert-content' )
        .textContent.indexOf( 'removed' )
    ).toBeGreaterThan( -1 );
  } );

  it( 'removes the alert from the container when .hide is called', () => {
    jest.useFakeTimers();

    instance.init( container );

    instance.show();
    instance.hide();

    jest.runAllTimers();

    expect( container.children.length ).toBe( 0 );
  } );

  it( 'clears everything when .remove is called', () => {
    jest.useFakeTimers();

    instance.init( container );

    instance.show();
    instance.remove();

    jest.runAllTimers();

    expect( container.children.length ).toBe( 0 );

    instance.hide();
    instance.remove();

    expect( container.children.length ).toBe( 0 );
  } );
} );
