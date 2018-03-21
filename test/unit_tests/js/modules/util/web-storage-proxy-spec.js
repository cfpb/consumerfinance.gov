const BASE_JS_PATH = '../../../../../cfgov/unprocessed/js/';
const webStorageProxy = require(
  BASE_JS_PATH + 'modules/util/web-storage-proxy.js'
);
const storageMock = require( '../../../../util/mock-web-storage' );

const setItem = webStorageProxy.setItem;
const getItem = webStorageProxy.getItem;
const removeItem = webStorageProxy.removeItem;
const setStorage = webStorageProxy.setStorage;

describe( 'web-storage-proxy', () => {
  beforeEach( () => {
    // Mock the window's web storage APIs.
    window.localStorage = storageMock( {} );
    window.sessionStorage = storageMock( {} );
  } );

  describe( '.setItem()', () => {
    it( 'should set an item of "bar" for the key "foo" in sessionStorage', () => {
      setItem( 'foo', 'bar', window.sessionStorage );
      expect( window.sessionStorage.getItem( 'foo' ) ).toBe( 'bar' );
      expect( window.localStorage.getItem( 'foo' ) ).toBeUndefined();
    } );

    it( 'should set an item of "baz" for the key "foo" in localStorage', () => {
      setItem( 'foo', 'baz', window.localStorage );
      expect( window.localStorage.getItem( 'foo' ) ).toBe( 'baz' );
      expect( window.sessionStorage.getItem( 'foo' ) ).toBeUndefined();
    } );

    it( 'should default to sessionStorage is storage arg is omitted', () => {
      setItem( 'foo', 'bar' );
      expect( window.sessionStorage.getItem( 'foo' ) ).toBe( 'bar' );
      expect( window.localStorage.getItem( 'foo' ) ).toBeUndefined();
    } );

    it( 'should default to sessionStorage if storage arg is a string', () => {
      setItem( 'foo', 'baz', 'bar' );
      expect( window.sessionStorage.getItem( 'foo' ) ).toBe( 'baz' );
      expect( window.localStorage.getItem( 'foo' ) ).toBeUndefined();
    } );

    it( 'should default to sessionStorage if storage arg is a boolean', () => {
      setItem( 'foo', 'baz', true );
      expect( window.sessionStorage.getItem( 'foo' ) ).toBe( 'baz' );
      expect( window.localStorage.getItem( 'foo' ) ).toBeUndefined();
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
        expect( item ).toBe( 'bar' );
      }
    );

    it( 'should return an item of "baz" for the key "foo" in localStorage',
      () => {
        const item = getItem( 'foo', window.localStorage );
        expect( item ).toBe( 'baz' );
      }
    );

    it( 'should default to sessionStorage if storage arg is omitted', () => {
      const item = getItem( 'foo' );
      expect( item ).toBe( 'bar' );
    } );

    it( 'should default to sessionStorage if storage arg is a string', () => {
      const item = getItem( 'foo', 'baz' );
      expect( item ).toBe( 'bar' );
    } );

    it( 'should default to sessionStorage if storage arg is a boolean', () => {
      const item = getItem( 'foo', false );
      expect( item ).toBe( 'bar' );
    } );
  } );

  describe( '.removeItem()', () => {
    beforeEach( () => {
      window.sessionStorage.setItem( 'foo', 'bar' );
      window.localStorage.setItem( 'foo', 'baz' );
    } );

    it( 'should remove the key "foo" in sessionStorage', () => {
      removeItem( 'foo', window.sessionStorage );
      expect( window.sessionStorage.getItem( 'foo' ) ).toBeUndefined();
    } );

    it( 'should remove the key "foo" in localStorage', () => {
      removeItem( 'foo', window.localStorage );
      expect( window.localStorage.getItem( 'foo' ) ).toBeUndefined();
    } );

    it( 'should default to sessionStorage if storage arg is omitted', () => {
      removeItem( 'foo' );
      expect( window.sessionStorage.getItem( 'foo' ) ).toBeUndefined();
    } );

    it( 'should default to sessionStorage if storage arg is a string', () => {
      removeItem( 'foo', 'baz' );
      expect( window.sessionStorage.getItem( 'foo' ) ).toBeUndefined();
    } );

    it( 'should default to sessionStorage if storage arg is a boolean', () => {
      removeItem( 'foo', true );
      expect( window.sessionStorage.getItem( 'foo' ) ).toBeUndefined();
    } );

    it( 'should do nothing if passed key does not exist', () => {
      const removed = removeItem( 'baz' );
      expect( window.sessionStorage.getItem( 'foo' ) ).toBe( 'bar' );
      expect( removed ).toBe( false );
    } );
  } );

  describe( '.setStorage()', () => {
    beforeEach( () => {
      setStorage( window.localStorage );
    } );

    it( 'should default to storage set in setStorage ' +
        'if storage arg is omitted in setItem', () => {
      setItem( 'foo', 'bar' );
      expect( window.localStorage.getItem( 'foo' ) ).toBe( 'bar' );
      expect( window.sessionStorage.getItem( 'foo' ) ).toBeUndefined();
    } );

    it( 'should default to storage set in setStorage ' +
        'if storage arg is omitted in getItem', () => {
      window.localStorage.setItem( 'foo', 'bar' );
      window.sessionStorage.setItem( 'foo', 'baz' );

      const item = getItem( 'foo' );

      expect( item ).toBe( 'bar' );
      expect( item ).not.toBe( 'baz' );
    } );

    it( 'should default to storage set in setStorage' +
        'if storage arg is omitted in removeItem', () => {
      window.localStorage.setItem( 'foo', 'bar' );
      window.sessionStorage.setItem( 'foo', 'baz' );

      removeItem( 'foo', window.localStorage );
      expect( window.localStorage.getItem( 'foo' ) ).toBeUndefined();
      expect( window.sessionStorage.getItem( 'foo' ) ).toBe( 'baz' );
    } );

    it( 'should throw an error if passed arg is empty', () => {
      function storageError() {
        setStorage();
      }
      expect( storageError ).toThrow( Error );
    } );

    it( 'should throw an error if passed arg is a string', () => {
      function storageError() {
        setStorage( 'string' );
      }
      expect( storageError ).toThrow( Error );
    } );

    it( 'should throw an error if passed arg is a boolean', () => {
      function storageError() {
        setStorage( true );
      }
      expect( storageError ).toThrow( Error );
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
