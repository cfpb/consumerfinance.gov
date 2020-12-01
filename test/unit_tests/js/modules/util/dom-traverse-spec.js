const BASE_JS_PATH = '../../../../../cfgov/unprocessed/js/';
const domTraverse = require( BASE_JS_PATH + 'modules/util/dom-traverse' );

describe( 'Dom Traverse', () => {
  describe( 'queryOne()', () => {
    beforeAll( () => {
      document.body.innerHTML =
        '<div class="div-1"></div><div class="div-2"></div>';
    } );

    it( 'should return the first elem if the expr is a string', () => {
      const query = domTraverse.queryOne( 'div' );

      expect( query.className ).toBe( 'div-1' );
    } );

    it( 'should return the passed expr if it’s an object', () => {
      const obj = document.createElement( 'div' );
      obj.className = 'div-3';
      const query = domTraverse.queryOne( obj );

      expect( query.className ).toBe( 'div-3' );
    } );

    it( 'should return null if the elem doesn’t exist', () => {
      const query = document.querySelector( '.div-4' );

      expect( query ).toBeNull();
    } );
  } );

  describe( 'closest()', () => {
    beforeAll( () => {
      document.body.innerHTML =
        '<div class="grandparent"><div class="parent"><div class="child">' +
        '</div></div></div>';
    } );

    it( 'should return the immediate parent HTMLNode with a passed selector',
      () => {
        const child = document.querySelector( '.child' );
        const parent = domTraverse.closest( child, 'div' );

        expect( parent.className ).toBe( 'parent' );
      }
    );

    it( 'should return the grandparent HTMLNode with a passed selector', () => {
      const child = document.querySelector( '.child' );
      const parent = domTraverse.closest( child, '.grandparent' );

      expect( parent.className ).toBe( 'grandparent' );
    } );

    it( 'should return null without a passed selector', () => {
      const child = document.querySelector( '.child' );
      const parent = domTraverse.closest( child );

      expect( parent ).toBeNull();
    } );

    it( 'should return null if the selector wasn’t found',
      () => {
        const child = document.querySelector( '.child' );
        const parent = domTraverse.closest( child, 'greatgrandparent' );

        expect( parent ).toBeNull();
      }
    );
  } );
} );
