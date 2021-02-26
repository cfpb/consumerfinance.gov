import Analytics from '../../../../cfgov/unprocessed/js/modules/Analytics';
let dataLayerOptions;
let getDataLayerOptions;
let UNDEFINED;

describe( 'Analytics', () => {
  beforeAll( () => {
    getDataLayerOptions = Analytics.getDataLayerOptions;
  } );

  beforeEach( () => {
    function push( object ) {
      if ( object.hasOwnProperty( 'eventCallback' ) &&
           typeof object.eventCallback === 'function' ) {
        return object.eventCallback();
      }
      return [].push.call( this, object );
    }
    window.dataLayer = [];
    window.dataLayer.push = push;
    delete window['google_tag_manager'];
    Analytics.tagManagerIsLoaded = false;

    dataLayerOptions = {
      event:        'Page Interaction',
      eventCallback: UNDEFINED,
      action:       '',
      label:        '',
      eventTimeout: 500
    };

  } );

  describe( '.init()', () => {
    it( 'should have a proper state after initialization', () => {
      expect( Analytics.tagManagerIsLoaded === false ).toBe( true );
      window['google_tag_manager'] = {};
      Analytics.init();
      expect( Analytics.tagManagerIsLoaded === true ).toBe( true );
    } );

    it( 'should properly set the google_tag_manager object', () => {
      const mockGTMObject = { testing: true };
      Analytics.init();
      expect( Analytics.tagManagerIsLoaded === false ).toBe( true );
      window['google_tag_manager'] = mockGTMObject;
      expect( Analytics.tagManagerIsLoaded === true ).toBe( true );
      expect( window.google_tag_manager ).toStrictEqual( mockGTMObject );
    } );
  } );

  describe( '.sendEvent()', () => {
    it( 'should properly add objects to the dataLayer Array', () => {
      const action = 'inbox:clicked';
      const label = 'text:null';
      const options = { ...dataLayerOptions,
        action: action,
        label:  label
      };
      window['google_tag_manager'] = {};
      Analytics.init();
      Analytics.sendEvent( getDataLayerOptions( action, label ) );
      expect( window.dataLayer.length === 1 ).toBe( true );
      expect( window.dataLayer[0] ).toStrictEqual( options );
    } );

    it( 'shouldn\'t add objects to the dataLayer Array if GTM is undefined',
      () => {
        const action = 'inbox:clicked';
        const label = 'text:null';
        delete window['google_tag_manager'];
        Analytics.init();
        Analytics.sendEvent( getDataLayerOptions( action, label ) );
        expect( window.dataLayer.length === 0 ).toBe( true );
      }
    );

    it( 'should invoke the callback if provided', () => {
      Analytics.init();
      const action = 'inbox:clicked';
      const label = 'text:null';
      const callback = {
        method: jest.fn()
      };
      const callbackSpy = jest.spyOn( callback, 'method' );
      window['google_tag_manager'] = {};
      Analytics.sendEvent(
        getDataLayerOptions( action, label, '', callback.method )
      );
      expect( callbackSpy ).toHaveBeenCalledTimes( 1 );

      // Check code branch for when Analytics.tagManagerIsLoaded is not set.
      Analytics.tagManagerIsLoaded = false;
      Analytics.sendEvent(
        getDataLayerOptions( action, label, '', callback.method )
      );
      expect( callbackSpy ).toHaveBeenCalledTimes( 2 );
    } );
  } );

  describe( '.sendEvents()', () => {
    it( 'should properly add objects to the dataLayer Array', () => {
      const options1 = getDataLayerOptions(
        { ...dataLayerOptions,
          action: 'inbox:clicked',
          label:  'text:label_1'
        }
      );
      const options2 = getDataLayerOptions(
        { ...dataLayerOptions,
          action: 'checbox:clicked',
          label:  'text:label_2'
        }
      );
      window['google_tag_manager'] = {};
      Analytics.init();
      Analytics.sendEvents( [ options1, options2 ] );
      expect( window.dataLayer.length === 2 ).toBe( true );
    } );

    it( 'shouldn\'t add objects to dataLayer Array if array isn\'t passed',
      () => {
        const options1 = getDataLayerOptions(
          { ...dataLayerOptions,
            action: 'inbox:clicked',
            label:  'text:label_1'
          }
        );
        const options2 = getDataLayerOptions(
          { ...dataLayerOptions,
            action: 'checbox:clicked',
            label:  'text:label_2'
          }
        );
        window['google_tag_manager'] = {};
        Analytics.init();
        Analytics.sendEvents( options1, options2 );
        expect( window.dataLayer.length === 0 ).toBe( true );
      }
    );
  } );

} );
