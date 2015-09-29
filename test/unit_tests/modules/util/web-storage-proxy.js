'use strict';

var chai = require( 'chai' );
var sinon = require( 'sinon' );
var expect = chai.expect;
var jsdom = require( 'mocha-jsdom' );

describe( 'web-storage-proxy', function() {
  var webStorageProxy, sandbox, setItem, getItem, removeItem, setStorage;

  jsdom();

  before( function() {
    webStorageProxy =
      require( '../../../../cfgov/v1/preprocessed/js/modules/util/web-storage-proxy.js' );
    setItem = webStorageProxy.setItem;
    getItem = webStorageProxy.getItem;
    removeItem = webStorageProxy.removeItem;
    setStorage = webStorageProxy.setStorage;
    sandbox = sinon.sandbox.create();
  } );

  beforeEach( function() {
    // Storage Mock
    function storageMock() {
      var storage = {};

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
          var keys = Object.keys( storage );
          return keys[i] || null;
        }
      };
    }
    // mock the localStorage
    window.localStorage = storageMock();
    // mock the sessionStorage
    window.sessionStorage = storageMock();
  } );

  afterEach( function() {
    sandbox.restore();
  } );

  describe( 'setItem', function() {
    it( 'should set an item of "bar" for the key "foo" in sessionStorage',
      function() {
        setItem( 'foo', 'bar', window.sessionStorage );
        expect( window.sessionStorage.getItem( 'foo' ) ).to.equal( 'bar' );
        expect( window.localStorage.getItem( 'foo' ) ).to.be.undefined;
      }
    );

    it( 'should set an item of "baz" for the key "foo" in localStorage',
      function() {
        setItem( 'foo', 'baz', window.localStorage );
        expect( window.localStorage.getItem( 'foo' ) ).to.equal( 'baz' );
        expect( window.sessionStorage.getItem( 'foo' ) ).to.be.undefined;
      }
    );

    it( 'should default to sessionStorage is storage arg is omitted',
      function() {
        setItem( 'foo', 'bar' );
        expect( window.sessionStorage.getItem( 'foo' ) ).to.equal( 'bar' );
        expect( window.localStorage.getItem( 'foo' ) ).to.be.undefined;
      }
    );

    it( 'should default to sessionStorage if storage arg is a string',
      function() {
        setItem( 'foo', 'baz', 'bar' );
        expect( window.sessionStorage.getItem( 'foo' ) ).to.equal( 'baz' );
        expect( window.localStorage.getItem( 'foo' ) ).to.be.undefined;
      }
    );

    it( 'should default to sessionStorage if storage arg is a boolean',
      function() {
        setItem( 'foo', 'baz', true );
        expect( window.sessionStorage.getItem( 'foo' ) ).to.equal( 'baz' );
        expect( window.localStorage.getItem( 'foo' ) ).to.be.undefined;
      }
    );
  } );


  describe( 'getItem', function() {
    beforeEach( function() {
      window.sessionStorage.setItem( 'foo', 'bar' );
      window.localStorage.setItem( 'foo', 'baz' );
    } );

    it( 'should return an item of "bar" for the key "foo" in sessionStorage',
      function() {
        var item = getItem( 'foo', window.sessionStorage );
        expect( item ).to.equal( 'bar' );
      }
    );

    it( 'should return an item of "baz" for the key "foo" in localStorage',
      function() {
        var item = getItem( 'foo', window.localStorage );
        expect( item ).to.equal( 'baz' );
      }
    );

    it( 'should default to sessionStorage if storage arg is omitted',
      function() {
        var item = getItem( 'foo' );
        expect( item ).to.equal( 'bar' );
      }
    );

    it( 'should default to sessionStorage if storage arg is a string',
      function() {
        var item = getItem( 'foo', 'baz' );
        expect( item ).to.equal( 'bar' );
      }
    );

    it( 'should default to sessionStorage if storage arg is a boolean',
      function() {
        var item = getItem( 'foo', false );
        expect( item ).to.equal( 'bar' );
      }
    );
  } );

  describe( 'removeItem', function() {
    beforeEach( function() {
      window.sessionStorage.setItem( 'foo', 'bar' );
      window.localStorage.setItem( 'foo', 'baz' );
    } );

    it( 'should remove the key "foo" in sessionStorage',
      function() {
        removeItem( 'foo', window.sessionStorage );
        expect( window.sessionStorage.getItem( 'foo' ) ).to.be.undefined;
      }
    );

    it( 'should remove the key "foo" in localStorage',
      function() {
        removeItem( 'foo', window.localStorage );
        expect( window.localStorage.getItem( 'foo' ) ).to.be.undefined;
      }
    );

    it( 'should default to sessionStorage if storage arg is omitted',
      function() {
        removeItem( 'foo' );
        expect( window.sessionStorage.getItem( 'foo' ) ).to.be.undefined;
      }
    );

    it( 'should default to sessionStorage if storage arg is a string',
      function() {
        removeItem( 'foo', 'baz' );
        expect( window.sessionStorage.getItem( 'foo' ) ).to.be.undefined;
      }
    );

    it( 'should default to sessionStorage if storage arg is a boolean',
      function() {
        removeItem( 'foo', true );
        expect( window.sessionStorage.getItem( 'foo' ) ).to.be.undefined;
      }
    );

    it( 'should do nothing if passed key does not exist',
      function() {
        var removed = removeItem( 'baz' );
        expect( window.sessionStorage.getItem( 'foo' ) ).to.equal( 'bar' );
        expect( removed ).to.equal( false );
      }
    );
  } );

  describe( 'setStorage', function() {
    beforeEach( function() {
      setStorage( window.localStorage );
    } );

    it(
      'should default to storage set in setStorage ' +
      'if storage arg is omitted in setItem',
      function() {
        setItem( 'foo', 'bar' );
        expect( window.localStorage.getItem( 'foo' ) ).to.equal( 'bar' );
        expect( window.sessionStorage.getItem( 'foo' ) ).to.be.undefined;
      }
    );

    it(
      'should default to storage set in setStorage ' +
      'if storage arg is omitted in getItem',
      function() {
        window.localStorage.setItem( 'foo', 'bar' );
        window.sessionStorage.setItem( 'foo', 'baz' );

        var item = getItem( 'foo' );

        expect( item ).to.equal( 'bar' );
        expect( item ).to.not.equal( 'baz' );
      }
    );

    it(
      'should default to storage set in setStorage' +
      'if storage arg is omitted in removeItem',
      function() {
        window.localStorage.setItem( 'foo', 'bar' );
        window.sessionStorage.setItem( 'foo', 'baz' );

        removeItem( 'foo', window.localStorage );
        expect( window.localStorage.getItem( 'foo' ) ).to.be.undefined;
        expect( window.sessionStorage.getItem( 'foo' ) ).to.equal( 'baz' );
      }
    );

    it( 'should throw an error if passed arg is empty',
      function() {
        function storageError() {
          setStorage();
        }
        expect( storageError, Error ).to.throw( Error );
      }
    );

    it( 'should throw an error if passed arg is a string',
      function() {
        function storageError() {
          setStorage( 'string' );
        }
        expect( storageError, Error ).to.throw( Error );
      }
    );

    it( 'should throw an error if passed arg is a boolean',
      function() {
        function storageError() {
          setStorage( true );
        }
        expect( storageError, Error ).to.throw( Error );
      }
    );
  } );

} );
