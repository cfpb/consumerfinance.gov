const BASE_JS_PATH = '../../../cfgov/unprocessed/js/';

const chai = require( 'chai' );
const expect = chai.expect;
const sinon = require( 'sinon' );
let sandbox;
let Analytics;
let dataLayerOptions;
let getDataLayerOptions;
let UNDEFINED;

describe( 'Analytics', () => {
  before( () => {
    this.jsdom = require( 'jsdom-global' )();
    Analytics = require( BASE_JS_PATH + 'modules/Analytics' );
    getDataLayerOptions = Analytics.getDataLayerOptions;
  } );

  after( () => this.jsdom() );

  beforeEach( () => {
    sandbox = sinon.sandbox.create();

    function push( object ) {
      if ( object.hasOwnProperty( 'eventCallback' ) &&
           typeof object.eventCallback === 'function' ) {
        return object.eventCallback();
      }
      return [].push.call( this, object );
    }
    window.dataLayer = [];
    window.dataLayer.push = push;

    delete window.google_tag_manager; // eslint-disable-line  camelcase
    Analytics.tagManagerIsLoaded = false;

    dataLayerOptions = {
      event:        'Page Interaction',
      eventCallback: UNDEFINED,
      action:       '',
      label:        '',
      eventTimeout: 500
    };

  } );

  afterEach( () => {
    sandbox.restore();
  } );

  describe( '.init()', () => {
    it( 'should have a proper state after initialization', () => {
      expect( Analytics.tagManagerIsLoaded === false ).to.be.true;
      window.google_tag_manager = {}; // eslint-disable-line  camelcase
      Analytics.init();
      expect( Analytics.tagManagerIsLoaded === true ).to.be.true;
    } );

    it( 'should properly set the google_tag_manager object', () => {
      const mockGTMObject = { testing: true };
      Analytics.init();
      expect( Analytics.tagManagerIsLoaded === false ).to.be.true;
      window.google_tag_manager = mockGTMObject; // eslint-disable-line  camelcase
      expect( Analytics.tagManagerIsLoaded === true ).to.be.true;
      expect( window.google_tag_manager ).to.deep.equal( mockGTMObject );
    } );
  } );

  describe( '.sendEvent()', () => {
    it( 'should properly add objects to the dataLayer Array', () => {
      const action = 'inbox:clicked';
      const label = 'text:null';
      const options = Object.assign( {}, dataLayerOptions, {
        action: action,
        label:  label
      } );
      window.google_tag_manager = {}; // eslint-disable-line  camelcase
      Analytics.init();
      Analytics.sendEvent( getDataLayerOptions( action, label ) );
      expect( window.dataLayer.length === 1 ).to.be.true;
      expect( window.dataLayer[0] ).to.deep.equal( options );
    } );

    it( "shouldn't add objects to the dataLayer Array if GTM is undefined",
      () => {
        const action = 'inbox:clicked';
        const label = 'text:null';
        delete window.google_tag_manager;
        Analytics.init();
        Analytics.sendEvent( getDataLayerOptions( action, label ) );
        expect( window.dataLayer.length === 0 ).to.be.true;
      }
    );

    it( 'should invoke the callback if provided', () => {
      Analytics.init();
      const action = 'inbox:clicked';
      const label = 'text:null';
      const callback = sinon.stub();
      window.google_tag_manager = {}; // eslint-disable-line  camelcase
      Analytics.sendEvent( getDataLayerOptions( action, label, '', callback ) );
      expect( callback.called ).to.be.true;
    } );
  } );

  describe( '.sendEvents()', () => {
    it( 'should properly add objects to the dataLayer Array', () => {
      const options1 = getDataLayerOptions(
        Object.assign( {}, dataLayerOptions, {
          action: 'inbox:clicked',
          label:  'text:label_1'
        } )
      );
      const options2 = getDataLayerOptions(
        Object.assign( {}, dataLayerOptions, {
          action: 'checbox:clicked',
          label:  'text:label_2'
        } )
      );
      window.google_tag_manager = {}; // eslint-disable-line  camelcase
      Analytics.init();
      Analytics.sendEvents( [ options1, options2 ] );
      expect( window.dataLayer.length === 2 ).to.be.true;
    } );

    it( "shouldn't add objects to the dataLayer Array if an array isn't passed",
      () => {
        const options1 = getDataLayerOptions(
          Object.assign( {}, dataLayerOptions, {
            action: 'inbox:clicked',
            label:  'text:label_1'
          } )
        );
        const options2 = getDataLayerOptions(
          Object.assign( {}, dataLayerOptions, {
            action: 'checbox:clicked',
            label:  'text:label_2'
          } )
        );
        window.google_tag_manager = {}; // eslint-disable-line  camelcase
        Analytics.init();
        Analytics.sendEvents( options1, options2 );
        expect( window.dataLayer.length === 0 ).to.be.true;
      }
    );
  } );

} );
