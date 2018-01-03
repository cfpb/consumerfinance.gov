const BASE_JS_PATH = '../../../../cfgov/unprocessed/js/';

const chai = require( 'chai' );
const sinon = require( 'sinon' );
const expect = chai.expect;

describe( 'web-storage-proxy', () => {
  let webStorageProxy;
  let sandbox;
  let setItem;
  let getItem;
  let removeItem;
  let setStorage;

  before( () => {
    this.jsdom = require( 'jsdom-global' )();
    webStorageProxy =
      require( BASE_JS_PATH + 'modules/util/web-storage-proxy.js' );
    setItem = webStorageProxy.setItem;
    getItem = webStorageProxy.getItem;
    removeItem = webStorageProxy.removeItem;
    setStorage = webStorageProxy.setStorage;
    sandbox = sinon.sandbox.create();
  } );

  after( () => this.jsdom() );

  beforeEach( () => {
    // Storage Mock
    function storageMock() {
      const storage = {};

      return {
        setItem: function( key, value ) {
          storage[key] = value || '';
        },
        getItem: function( key ) {
          return storage[key];
        },
        removeItem: function( key ) {
          delete storage[key];
        },
        get length() {
          return Object.keys( storage ).length;
        },
        key: function( i ) {
          const keys = Object.keys( storage );
          return keys[i] || null;
        }
      };
    }
    // mock the localStorage
    window.localStorage = storageMock();
    // mock the sessionStorage
    window.sessionStorage = storageMock();
  } );

  afterEach( () => {
    sandbox.restore();
  } );

  describe( '.setItem()', () => {
    it( 'should set an item of "bar" for the key "foo" in sessionStorage',
      () => {
        setItem( 'foo', 'bar', window.sessionStorage );
        expect( window.sessionStorage.getItem( 'foo' ) ).to.equal( 'bar' );
        expect( window.localStorage.getItem( 'foo' ) ).to.be.undefined;
      }
    );

    it( 'should set an item of "baz" for the key "foo" in localStorage',
      () => {
        setItem( 'foo', 'baz', window.localStorage );
        expect( window.localStorage.getItem( 'foo' ) ).to.equal( 'baz' );
        expect( window.sessionStorage.getItem( 'foo' ) ).to.be.undefined;
      }
    );

    it( 'should default to sessionStorage is storage arg is omitted', () => {
      setItem( 'foo', 'bar' );
      expect( window.sessionStorage.getItem( 'foo' ) ).to.equal( 'bar' );
      expect( window.localStorage.getItem( 'foo' ) ).to.be.undefined;
    } );

    it( 'should default to sessionStorage if storage arg is a string', () => {
      setItem( 'foo', 'baz', 'bar' );
      expect( window.sessionStorage.getItem( 'foo' ) ).to.equal( 'baz' );
      expect( window.localStorage.getItem( 'foo' ) ).to.be.undefined;
    } );

    it( 'should default to sessionStorage if storage arg is a boolean', () => {
      setItem( 'foo', 'baz', true );
      expect( window.sessionStorage.getItem( 'foo' ) ).to.equal( 'baz' );
      expect( window.localStorage.getItem( 'foo' ) ).to.be.undefined;
    } );
  } );


  describe( '.getItem()', () => {
    beforeEach( () => {
      window.sessionStorage.setItem( 'foo', 'bar' );
      window.localStorage.setItem( 'foo', 'baz' );
    } );

    it( 'should return an item of "bar" for the key "foo" in sessionStorage',
      () => {
        const item = getItem( 'foo', window.sessionStorage );
        expect( item ).to.equal( 'bar' );
      }
    );

    it( 'should return an item of "baz" for the key "foo" in localStorage',
      () => {
        const item = getItem( 'foo', window.localStorage );
        expect( item ).to.equal( 'baz' );
      }
    );

    it( 'should default to sessionStorage if storage arg is omitted',
      () => {
        const item = getItem( 'foo' );
        expect( item ).to.equal( 'bar' );
      }
    );

    it( 'should default to sessionStorage if storage arg is a string',
      () => {
        const item = getItem( 'foo', 'baz' );
        expect( item ).to.equal( 'bar' );
      }
    );

    it( 'should default to sessionStorage if storage arg is a boolean',
      () => {
        const item = getItem( 'foo', false );
        expect( item ).to.equal( 'bar' );
      }
    );
  } );

  describe( '.removeItem()', () => {
    beforeEach( () => {
      window.sessionStorage.setItem( 'foo', 'bar' );
      window.localStorage.setItem( 'foo', 'baz' );
    } );

    it( 'should remove the key "foo" in sessionStorage', () => {
      removeItem( 'foo', window.sessionStorage );
      expect( window.sessionStorage.getItem( 'foo' ) ).to.be.undefined;
    } );

    it( 'should remove the key "foo" in localStorage', () => {
      removeItem( 'foo', window.localStorage );
      expect( window.localStorage.getItem( 'foo' ) ).to.be.undefined;
    } );

    it( 'should default to sessionStorage if storage arg is omitted', () => {
      removeItem( 'foo' );
      expect( window.sessionStorage.getItem( 'foo' ) ).to.be.undefined;
    } );

    it( 'should default to sessionStorage if storage arg is a string', () => {
      removeItem( 'foo', 'baz' );
      expect( window.sessionStorage.getItem( 'foo' ) ).to.be.undefined;
    } );

    it( 'should default to sessionStorage if storage arg is a boolean', () => {
      removeItem( 'foo', true );
      expect( window.sessionStorage.getItem( 'foo' ) ).to.be.undefined;
    } );

    it( 'should do nothing if passed key does not exist', () => {
      const removed = removeItem( 'baz' );
      expect( window.sessionStorage.getItem( 'foo' ) ).to.equal( 'bar' );
      expect( removed ).to.equal( false );
    } );
  } );

  describe( '.setStorage()', () => {
    beforeEach( () => {
      setStorage( window.localStorage );
    } );

    it( 'should default to storage set in setStorage ' +
        'if storage arg is omitted in setItem', () => {
      setItem( 'foo', 'bar' );
      expect( window.localStorage.getItem( 'foo' ) ).to.equal( 'bar' );
      expect( window.sessionStorage.getItem( 'foo' ) ).to.be.undefined;
    } );

    it( 'should default to storage set in setStorage ' +
        'if storage arg is omitted in getItem', () => {
      window.localStorage.setItem( 'foo', 'bar' );
      window.sessionStorage.setItem( 'foo', 'baz' );

      const item = getItem( 'foo' );

      expect( item ).to.equal( 'bar' );
      expect( item ).to.not.equal( 'baz' );
    } );

    it( 'should default to storage set in setStorage' +
        'if storage arg is omitted in removeItem', () => {
      window.localStorage.setItem( 'foo', 'bar' );
      window.sessionStorage.setItem( 'foo', 'baz' );

      removeItem( 'foo', window.localStorage );
      expect( window.localStorage.getItem( 'foo' ) ).to.be.undefined;
      expect( window.sessionStorage.getItem( 'foo' ) ).to.equal( 'baz' );
    } );

    it( 'should throw an error if passed arg is empty', () => {
      function storageError() {
        setStorage();
      }
      expect( storageError, Error ).to.throw( Error );
    } );

    it( 'should throw an error if passed arg is a string', () => {
      function storageError() {
        setStorage( 'string' );
      }
      expect( storageError, Error ).to.throw( Error );
    } );

    it( 'should throw an error if passed arg is a boolean', () => {
      function storageError() {
        setStorage( true );
      }
      expect( storageError, Error ).to.throw( Error );
    } );

    xit( 'should set storage to an object if sessionStorage throws an error',
      () => {

        /* TODO: If cookies are disabled, window.sessionStorage
           will throw a SecurityError and the internal storage will be
           an object literal. */
      }
    );
  } );
} );
