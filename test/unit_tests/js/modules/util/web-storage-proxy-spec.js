import {
  webStorageProxy
} from '../../../../../cfgov/unprocessed/js/modules/util/web-storage-proxy.js';

describe( 'web-storage-proxy', () => {
  beforeEach( () => {
    window.sessionStorage.clear();
    window.localStorage.clear();
  } );

  describe( '.setItem()', () => {
    it( 'should set an item of "bar" for the key "foo" in sessionStorage', () => {
      webStorageProxy.setItem( 'foo', 'bar', window.sessionStorage );
      expect( window.sessionStorage.getItem( 'foo' ) ).toBe( 'bar' );
      expect( window.localStorage.getItem( 'foo' ) ).toBeNull();
    } );

    it( 'should set an item of "baz" for the key "foo" in localStorage', () => {
      webStorageProxy.setItem( 'foo', 'baz', window.localStorage );
      expect( window.localStorage.getItem( 'foo' ) ).toBe( 'baz' );
      expect( window.sessionStorage.getItem( 'foo' ) ).toBeNull();
    } );

    it( 'should default to sessionStorage is storage arg is omitted', () => {
      webStorageProxy.setItem( 'foo', 'bar' );
      expect( window.sessionStorage.getItem( 'foo' ) ).toBe( 'bar' );
      expect( window.localStorage.getItem( 'foo' ) ).toBeNull();
    } );

    it( 'should default to sessionStorage if storage arg is a string', () => {
      webStorageProxy.setItem( 'foo', 'baz', 'bar' );
      expect( window.sessionStorage.getItem( 'foo' ) ).toBe( 'baz' );
      expect( window.localStorage.getItem( 'foo' ) ).toBeNull();
    } );

    it( 'should default to sessionStorage if storage arg is a boolean', () => {
      webStorageProxy.setItem( 'foo', 'baz', true );
      expect( window.sessionStorage.getItem( 'foo' ) ).toBe( 'baz' );
      expect( window.localStorage.getItem( 'foo' ) ).toBeNull();
    } );
  } );


  describe( '.getItem()', () => {
    beforeEach( () => {
      window.sessionStorage.setItem( 'foo', 'bar' );
      window.localStorage.setItem( 'foo', 'baz' );
    } );

    it( 'should return an item of "bar" for the key "foo" in sessionStorage',
      () => {
        const item = webStorageProxy.getItem( 'foo', window.sessionStorage );
        expect( item ).toBe( 'bar' );
      }
    );

    it( 'should return an item of "baz" for the key "foo" in localStorage',
      () => {
        const item = webStorageProxy.getItem( 'foo', window.localStorage );
        expect( item ).toBe( 'baz' );
      }
    );

    it( 'should default to sessionStorage if storage arg is omitted', () => {
      const item = webStorageProxy.getItem( 'foo' );
      expect( item ).toBe( 'bar' );
    } );

    it( 'should default to sessionStorage if storage arg is a string', () => {
      const item = webStorageProxy.getItem( 'foo', 'baz' );
      expect( item ).toBe( 'bar' );
    } );

    it( 'should default to sessionStorage if storage arg is a boolean', () => {
      const item = webStorageProxy.getItem( 'foo', false );
      expect( item ).toBe( 'bar' );
    } );
  } );

  describe( '.removeItem()', () => {
    beforeEach( () => {
      window.sessionStorage.setItem( 'foo', 'bar' );
      window.localStorage.setItem( 'foo', 'baz' );
    } );

    it( 'should remove the key "foo" in sessionStorage', () => {
      webStorageProxy.removeItem( 'foo', window.sessionStorage );
      expect( window.sessionStorage.getItem( 'foo' ) ).toBeNull();
    } );

    it( 'should remove the key "foo" in localStorage', () => {
      webStorageProxy.removeItem( 'foo', window.localStorage );
      expect( window.localStorage.getItem( 'foo' ) ).toBeNull();
    } );

    it( 'should default to sessionStorage if storage arg is omitted', () => {
      webStorageProxy.removeItem( 'foo' );
      expect( window.sessionStorage.getItem( 'foo' ) ).toBeNull();
    } );

    it( 'should default to sessionStorage if storage arg is a string', () => {
      webStorageProxy.removeItem( 'foo', 'baz' );
      expect( window.sessionStorage.getItem( 'foo' ) ).toBeNull();
    } );

    it( 'should default to sessionStorage if storage arg is a boolean', () => {
      webStorageProxy.removeItem( 'foo', true );
      expect( window.sessionStorage.getItem( 'foo' ) ).toBeNull();
    } );

    it( 'should do nothing if passed key does not exist', () => {
      const removed = webStorageProxy.removeItem( 'baz' );
      expect( window.sessionStorage.getItem( 'foo' ) ).toBe( 'bar' );
      expect( removed ).toBe( false );
    } );
  } );

  describe( '.setStorage()', () => {
    beforeEach( () => {
      webStorageProxy.setStorage( window.localStorage );
    } );

    it( 'should default to storage set in setStorage ' +
        'if storage arg is omitted in setItem', () => {
      webStorageProxy.setItem( 'foo', 'bar' );
      expect( window.localStorage.getItem( 'foo' ) ).toBe( 'bar' );
      expect( window.sessionStorage.getItem( 'foo' ) ).toBeNull();
    } );

    it( 'should default to storage set in setStorage ' +
        'if storage arg is omitted in getItem', () => {
      window.localStorage.setItem( 'foo', 'bar' );
      window.sessionStorage.setItem( 'foo', 'baz' );

      const item = webStorageProxy.getItem( 'foo' );

      expect( item ).toBe( 'bar' );
      expect( item ).not.toBe( 'baz' );
    } );

    it( 'should default to storage set in setStorage ' +
        'if storage arg is omitted in removeItem', () => {
      window.localStorage.setItem( 'foo', 'bar' );
      window.sessionStorage.setItem( 'foo', 'baz' );

      webStorageProxy.removeItem( 'foo', window.localStorage );
      expect( window.localStorage.getItem( 'foo' ) ).toBeNull();
      expect( window.sessionStorage.getItem( 'foo' ) ).toBe( 'baz' );
    } );

    it( 'should throw an error if passed arg is empty', () => {
      function storageError() {
        webStorageProxy.setStorage();
      }
      expect( storageError ).toThrow( Error );
    } );

    it( 'should throw an error if passed arg is a string', () => {
      function storageError() {
        webStorageProxy.setStorage( 'string' );
      }
      expect( storageError ).toThrow( Error );
    } );

    it( 'should throw an error if passed arg is a boolean', () => {
      function storageError() {
        webStorageProxy.setStorage( true );
      }
      expect( storageError ).toThrow( Error );
    } );

    it( 'should set storage to an object if ' +
        'sessionStorage is undefined', () => {
      let UNDEFINED;
      webStorageProxy.setItem( 'foo', 'bar', UNDEFINED );
      expect( webStorageProxy.getItem( 'foo' ) ).toEqual( 'bar' );
    } );

    it( 'should set storage to an object if sessionStorage is null', () => {
      webStorageProxy.setItem( 'foo', 'bar', null );
      expect( webStorageProxy.getItem( 'foo' ) ).toEqual( 'bar' );
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
