const BASE_JS_PATH = '../../../../cfgov/unprocessed/js/';
const chai = require( 'chai' );
const expect = chai.expect;
const sinon = require( 'sinon' );
let sandbox;

const behavior = require( BASE_JS_PATH + 'modules/util/behavior' );

const HTML_SNIPPET =
  `<a href="#main" id="skip-nav">Skip to main content</a>
   <a class="o-mega-menu_content-link o-mega-menu_content-1-link"
      data-js-hook="behavior_flyout-menu_trigger">
        Consumer Tools
  </a>
  <a class="o-mega-menu_content-link o-mega-menu_content-1-link"
     data-js-hook="behavior_flyout-menu_trigger">
        Educational Resources
  </a>
  <div data-js-hook="behavior_flyout-menu">
      <div data-js-hook="behavior_flyout-menu_content"></div>
  </div>`;

function triggerEvent( target, eventType, eventOption ) {
  const event = document.createEvent( 'Event' );
  if ( eventType === 'keyup' ) {
    event.keyCode = eventOption || '';
  }
  event.initEvent( eventType, true, true );
  target.dispatchEvent( event );
}

describe( 'behavior', function() {
  let containerDom;
  let behaviorElmDom;
  const selector = 'data-js-hook=behavior_flyout-menu';

  before( () => {
    this.jsdom = require( 'jsdom-global' )( HTML_SNIPPET );
  } );

  after( () => this.jsdom() );

  beforeEach( () => {
    sandbox = sinon.sandbox.create();
    document.body.innerHTML = HTML_SNIPPET;
    containerDom = document.querySelector( '[' + selector + ']' );
    behaviorElmDom = document.querySelector( '[' + selector + '_content]' );
  } );

  afterEach( () => {
    sandbox.restore();
  } );

  describe( 'attach function', () => {
    it( 'should register an event callback when passed a Node',
      function() {
        const spy = sinon.spy();
        const linkDom = document.querySelector( 'a[href^="#"]' );
        behavior.attach( linkDom, 'click', spy );
        triggerEvent( linkDom, 'click' );
        expect( spy.called ).to.equal( true );
      } );

    it( 'should register an event callback when passed a NodeList', () => {
      const spy = sinon.spy();
      const behaviorDom = behavior.find( 'flyout-menu_trigger' );
      behavior.attach( behaviorDom, 'mouseover', spy );
      triggerEvent( behaviorDom[0], 'mouseover' );
      expect( spy.called ).to.equal( true );
    } );

    it( 'should register an event callback when passed a behavior selector',
      () => {
        const spy = sinon.spy();
        const behaviorDom = behavior.find( 'flyout-menu_trigger' );
        behavior.attach( 'flyout-menu_trigger', 'mouseover', spy );
        triggerEvent( behaviorDom[0], 'mouseover' );
        expect( spy.called ).to.equal( true );
      } );

    it( 'should register an event callback when passed a dom selector', () => {
      const spy = sinon.spy();
      const linkDom = document.querySelector( 'a[href^="#"]' );
      behavior.attach( 'a[href^="#"]', 'click', spy );
      triggerEvent( linkDom, 'click' );
      expect( spy.called ).to.equal( true );
    } );
  } );

  describe( 'checkBehaviorDom function ', () => {
    it( 'should throw an error if element DOM not found', () => {
      const errMsg = 'behavior_flyout-menu ' +
                     'behavior not found on passed DOM node!';
      function errFunc() {
        behavior.checkBehaviorDom( null, 'behavior_flyout-menu' );
      }
      expect( errFunc ).to.throw( Error, errMsg );
    } );

    it( 'should throw an error if behavior attribute not found', () => {
      const errMsg = 'mock-attr behavior not found on passed DOM node!';
      function errFunc() {
        behavior.checkBehaviorDom( containerDom, 'mock-attr' );
      }
      expect( errFunc ).to.throw( Error, errMsg );
    } );

    it( 'should return the correct HTMLElement ' +
        'when direct element is searched', () => {
      const dom = behavior.checkBehaviorDom( containerDom,
        'behavior_flyout-menu' );
      expect( dom ).to.be.equal( containerDom );
    } );

    it( 'should return the correct HTMLElement ' +
        'when child element is searched', () => {
      const dom = behavior.checkBehaviorDom( behaviorElmDom,
        'behavior_flyout-menu_content' );
      expect( dom ).to.be.equal( behaviorElmDom );
    } );
  } );

  describe( 'find function', () => {
    it( 'should find all elements with the specific behavior hook', () => {
      let behaviorDom = behavior.find( 'flyout-menu_trigger' );
      expect( behaviorDom.length === 2 ).to.equal( true );
      behaviorDom = behavior.find( 'flyout-menu_content' );
      expect( behaviorDom.length === 1 ).to.equal( true );
    } );

    it( 'should throw an error when passed an invalid behavior selector',
      () => {
        const behaviorSelector = 'a[href^="#"]';
        const errorMsg = '[data-js-hook*=behavior_' +
                       behaviorSelector + '] not found in DOM!';
        const findFunction = behavior.find.bind( this, behaviorSelector );
        expect( findFunction ).to.throw( Error, errorMsg );
      } );
  } );

  describe( 'remove function', () => {
    it( 'should remove the event callback for the specific behavior hook',
      () => {
        const spy = sinon.spy();
        const linkDom = document.querySelector( 'a[href^="#"]' );
        behavior.attach( linkDom, 'click', spy );
        triggerEvent( linkDom, 'click' );
        expect( spy.called ).to.equal( true );
        spy.reset();
        behavior.remove( linkDom, 'click', spy );
        triggerEvent( linkDom, 'click' );
        expect( spy.called ).to.equal( false );
      } );
  } );
} );
