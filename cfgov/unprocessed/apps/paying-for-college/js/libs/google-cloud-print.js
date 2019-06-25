( function() {
  var h,
      k = this,
      aa = function( a, b ) {
        let c = a.split( '.' ),
            d = k; c[0] in d || !d.execScript || d.execScript( 'var ' + c[0] ); for ( var e; c.length && ( e = c.shift() ); )c.length || void 0 === b ? d = d[e] ? d[e] : d[e] = {} : d[e] = b;
      },
      ba = function() {},
      ca = function( a ) {
        const b = typeof a; if ( b == 'object' ) {
          if ( a ) {
            if ( a instanceof Array ) return 'array'; if ( a instanceof Object ) return b; const c = Object.prototype.toString.call( a ); if ( c == '[object Window]' ) return 'object'; if ( c == '[object Array]' || typeof a.length == 'number' && typeof a.splice != 'undefined' && typeof a.propertyIsEnumerable != 'undefined' &&
!a.propertyIsEnumerable( 'splice' ) ) return 'array'; if ( c == '[object Function]' || typeof a.call != 'undefined' && typeof a.propertyIsEnumerable != 'undefined' && !a.propertyIsEnumerable( 'call' ) ) return 'function';
          } else { return 'null'; }
        } else if ( b == 'function' && typeof a.call == 'undefined' ) { return 'object'; } return b;
      },
      l = function( a ) { return ca( a ) == 'array'; },
      m = function( a ) { return typeof a == 'string'; },
      n = function( a ) { return typeof a == 'number'; },
      da = function( a ) { const b = typeof a; return b == 'object' && a != null || b == 'function'; },
      ea = function( a, b, c ) {
        return a.call.apply( a.bind,
          arguments );
      },
      fa = function( a, b, c ) { if ( !a ) throw Error(); if ( arguments.length > 2 ) { const d = Array.prototype.slice.call( arguments, 2 ); return function() { const c = Array.prototype.slice.call( arguments ); Array.prototype.unshift.apply( c, d ); return a.apply( b, c ); }; } return function() { return a.apply( b, arguments ); }; },
      q = function( a, b, c ) { q = Function.prototype.bind && Function.prototype.bind.toString().indexOf( 'native code' ) != -1 ? ea : fa; return q.apply( null, arguments ); },
      r = function( a, b ) {
        function c() {}c.prototype = b.prototype; a.Aa = b.prototype;
        a.prototype = new c(); a.prototype.constructor = a; a.Za = function( a, c, f ) { for ( var g = Array( arguments.length - 2 ), p = 2; p < arguments.length; p++ )g[p - 2] = arguments[p]; return b.prototype[c].apply( a, g ); };
      }; var ga = function() { this.V = void 0; },
      t = function( a ) { const b = []; ha( new ga(), a, b ); return b.join( '' ); },
      ha = function( a, b, c ) {
        if ( b == null ) { c.push( 'null' ); } else {
          if ( typeof b == 'object' ) {
            if ( l( b ) ) { var d = b; b = d.length; c.push( '[' ); for ( var e = '', f = 0; f < b; f++ )c.push( e ), e = d[f], ha( a, a.V ? a.V.call( d, String( f ), e ) : e, c ), e = ','; c.push( ']' ); return; } if ( b instanceof String || b instanceof Number || b instanceof Boolean ) { b = b.valueOf(); } else {
              c.push( '{' ); f = ''; for ( d in b ) {
                Object.prototype.hasOwnProperty.call( b, d ) && ( e = b[d], typeof e != 'function' && ( c.push( f ),
                ia( d, c ), c.push( ':' ), ha( a, a.V ? a.V.call( b, d, e ) : e, c ), f = ',' ) );
              }c.push( '}' ); return;
            }
          } switch ( typeof b ) { case 'string': ia( b, c ); break; case 'number': c.push( isFinite( b ) && !isNaN( b ) ? String( b ) : 'null' ); break; case 'boolean': c.push( String( b ) ); break; case 'function': c.push( 'null' ); break; default: throw Error( 'Unknown type: ' + typeof b ); }
        }
      },
      ja = { '"': '\\"', '\\': '\\\\', '/': '\\/', '\b': '\\b', '\f': '\\f', '\n': '\\n', '\r': '\\r', '\t': '\\t', '\x0B': '\\u000b' },
      ka = ( /\uffff/ ).test( '\uffff' ) ? /[\\\"\x00-\x1f\x7f-\uffff]/g : /[\\\"\x00-\x1f\x7f-\xff]/g,
      ia = function( a, b ) { b.push( '"', a.replace( ka, function( a ) { let b = ja[a]; b || ( b = '\\u' + ( a.charCodeAt( 0 ) | 65536 ).toString( 16 ).substr( 1 ), ja[a] = b ); return b; } ), '"' ); }; const u = function() { this.ha = 'print-document'; this.ja = 0; this.za = !1; },
        la = { Xa: 'print-document', Ya: 'print-file' }; u.prototype.Ra = function( a ) { this.ha = a; return this; }; u.prototype.Ta = function( a ) { this.ja = a; return this; }; u.prototype.Ua = function( a ) { this.za = a; return this; }; aa( 'cloudprint.Configuration', u ); u.prototype.setMode = u.prototype.Ra; u.prototype.setSelectedUser = u.prototype.Ta; u.prototype.setShowPrintLocally = u.prototype.Ua; aa( 'cloudprint.Configuration.Mode', la ); la.PRINT_DOCUMENT = 'print-document';
  la.PRINT_FILE = 'print-file'; const ma = function( a, b, c, d ) { this.Wa = a; this.Va = b; this.na = c; this.Fa = d || ''; }; ma.prototype.ca = function() { return this.na; }; var v = function( a ) { if ( Error.captureStackTrace ) { Error.captureStackTrace( this, v ); } else { const b = Error().stack; b && ( this.stack = b ); }a && ( this.message = String( a ) ); }; r( v, Error ); v.prototype.name = 'CustomError'; let w; var na = function( a, b ) { for ( var c = a.split( '%s' ), d = '', e = Array.prototype.slice.call( arguments, 1 ); e.length && c.length > 1; )d += c.shift() + e.shift(); return d + c.join( '%s' ); },
      oa = String.prototype.trim ? function( a ) { return a.trim(); } : function( a ) { return a.replace( /^[\s\xa0]+|[\s\xa0]+$/g, '' ); },
      pa = /&/g,
      qa = /</g,
      ra = />/g,
      sa = /"/g,
      ta = /'/g,
      ua = /\x00/g,
      va = /[\x00&<>"']/,
      ya = function( a ) {
        let b = 0,
            c = oa( String( wa ) ).split( '.' ); a = oa( String( a ) ).split( '.' ); for ( let d = Math.max( c.length, a.length ), e = 0; b == 0 && e < d; e++ ) {
          const f = c[e] || '',
                g = a[e] || '',
                p = RegExp( '(\\d*)(\\D*)', 'g' ),
                z = RegExp( '(\\d*)(\\D*)', 'g' ); do {
            const Q = p.exec( f ) || [ '', '', '' ],
                  R = z.exec( g ) || [ '', '', '' ]; if ( Q[0].length == 0 && R[0].length == 0 ) break; b = xa( Q[1].length == 0 ? 0 : parseInt( Q[1], 10 ), R[1].length == 0 ? 0 : parseInt( R[1], 10 ) ) || xa( Q[2].length == 0, R[2].length == 0 ) || xa( Q[2], R[2] );
          } while ( b == 0 );
        } return b;
      },
      xa = function( a, b ) { return a < b ? -1 : a > b ? 1 : 0; }; const x = function( a, b ) { b.unshift( a ); v.call( this, na.apply( null, b ) ); b.shift(); }; r( x, v ); x.prototype.name = 'AssertionError';
  var za = function( a, b, c, d ) {
        var e = 'Assertion failed'; if ( c ) {
          var e = e + ( ': ' + c ),
              f = d;
        } else { a && ( e += ': ' + a, f = b ); } throw new x( String( e ), f || [] );
      },
      y = function( a, b, c ) { a || za( '', null, b, Array.prototype.slice.call( arguments, 2 ) ); },
      Aa = function( a, b ) { throw new x( 'Failure' + ( a ? ': ' + a : '' ), Array.prototype.slice.call( arguments, 1 ) ); },
      Ba = function( a, b, c ) { m( a ) || za( 'Expected string but got %s: %s.', [ ca( a ), a ], b, Array.prototype.slice.call( arguments, 2 ) ); return a; },
      Da = function( a, b, c, d ) {
        a instanceof b || za( 'Expected instanceof %s but got %s.', [ Ca( b ),
          Ca( a ) ], c, Array.prototype.slice.call( arguments, 3 ) );
      },
      Ca = function( a ) { return a instanceof Function ? a.displayName || a.name || 'unknown type name' : a instanceof Object ? a.constructor.displayName || a.constructor.name || Object.prototype.toString.call( a ) : a === null ? 'null' : typeof a; }; const Ea = Array.prototype.indexOf ? function( a, b, c ) { y( a.length != null ); return Array.prototype.indexOf.call( a, b, c ); } : function( a, b, c ) { c = c == null ? 0 : c < 0 ? Math.max( 0, a.length + c ) : c; if ( m( a ) ) return m( b ) && b.length == 1 ? a.indexOf( b, c ) : -1; for ( ;c < a.length; c++ ) if ( c in a && a[c] === b ) return c; return -1; }; const Fa = function( a, b, c ) { for ( const d in a )b.call( c, a[d], d, a ); },
        Ga = 'constructor hasOwnProperty isPrototypeOf propertyIsEnumerable toLocaleString toString valueOf'.split( ' ' ),
        Ha = function( a, b ) { for ( var c, d, e = 1; e < arguments.length; e++ ) { d = arguments[e]; for ( c in d )a[c] = d[c]; for ( let f = 0; f < Ga.length; f++ )c = Ga[f], Object.prototype.hasOwnProperty.call( d, c ) && ( a[c] = d[c] ); } }; let A; a: { const Ia = k.navigator; if ( Ia ) { const Ja = Ia.userAgent; if ( Ja ) { A = Ja; break a; } }A = ''; } const B = function( a ) { return A.indexOf( a ) != -1; }; let Ka = B( 'Opera' ) || B( 'OPR' ),
      C = B( 'Trident' ) || B( 'MSIE' ),
      D = B( 'Edge' ),
      E = B( 'Gecko' ) && !( A.toLowerCase().indexOf( 'webkit' ) != -1 && !B( 'Edge' ) ) && !( B( 'Trident' ) || B( 'MSIE' ) ) && !B( 'Edge' ),
      F = A.toLowerCase().indexOf( 'webkit' ) != -1 && !B( 'Edge' ),
      La = F && B( 'Mobile' ),
      G = B( 'Macintosh' ),
      Ma = B( 'Windows' ),
      Na = B( 'Linux' ) || B( 'CrOS' ),
      Oa = function() { const a = k.document; return a ? a.documentMode : void 0; },
      Pa;
  a: {
    let Qa = '',
        Ra = ( function() { const a = A; if ( E ) return ( /rv\:([^\);]+)(\)|;)/ ).exec( a ); if ( D ) return ( /Edge\/([\d\.]+)/ ).exec( a ); if ( C ) return ( /\b(?:MSIE|rv)[: ]([^\);]+)(\)|;)/ ).exec( a ); if ( F ) return ( /WebKit\/(\S+)/ ).exec( a ); if ( Ka ) return ( /(?:Version)[ \/]?(\S+)/ ).exec( a ); } )(); Ra && ( Qa = Ra ? Ra[1] : '' ); if ( C ) { const Sa = Oa(); if ( Sa != null && Sa > parseFloat( Qa ) ) { Pa = String( Sa ); break a; } }Pa = Qa;
  } var wa = Pa,
      Ta = {},
      H = function( a ) { return Ta[a] || ( Ta[a] = ya( a ) >= 0 ); },
      Ua = k.document,
      Va = Ua && C ? Oa() || ( Ua.compatMode == 'CSS1Compat' ? parseInt( wa, 10 ) : 5 ) : void 0; !E && !C || C && Number( Va ) >= 9 || E && H( '1.9.1' ); C && H( '9' ); var Xa = function( a, b ) {
        let c = b || document,
            d = null; return ( d = c.getElementsByClassName ? c.getElementsByClassName( a )[0] : c.querySelectorAll && c.querySelector ? c.querySelector( '.' + a ) : Wa( a, b )[0] ) || null;
      },
      Wa = function( a, b ) {
        let c, d, e, f; c = document; c = b || c; if ( c.querySelectorAll && c.querySelector && a ) return c.querySelectorAll( String( a ? '.' + a : '' ) ); if ( a && c.getElementsByClassName ) { var g = c.getElementsByClassName( a ); return g; }g = c.getElementsByTagName( '*' ); if ( a ) {
          f = {}; for ( d = e = 0; c = g[d]; d++ ) {
            var p = c.className,
                z; if ( z = typeof p.split == 'function' ) {
              z =
Ea( p.split( /\s+/ ), a ) >= 0;
            }z && ( f[e++] = c );
          }f.length = e; return f;
        } return g;
      },
      I = function( a ) { this.Ea = a || k.document || document; }; I.prototype.createElement = function( a ) { return this.Ea.createElement( a ); }; I.prototype.appendChild = function( a, b ) { a.appendChild( b ); }; const Ya = { ab: !0 },
        Za = { bb: !0 },
        J = function() { throw Error( 'Do not instantiate directly' ); }; J.prototype.ba = null; J.prototype.ca = function() { return this.content; }; J.prototype.toString = function() { return this.content; }; const $a = function() { J.call( this ); }; r( $a, J ); const ab = function( a ) { if ( !da( a ) ) return String( a ); if ( a instanceof J ) { if ( a.L === Ya ) return Ba( a.ca() ); if ( a.L === Za ) return a = a.ca(), va.test( a ) && ( a.indexOf( '&' ) != -1 && ( a = a.replace( pa, '&amp;' ) ), a.indexOf( '<' ) != -1 && ( a = a.replace( qa, '&lt;' ) ), a.indexOf( '>' ) != -1 && ( a = a.replace( ra, '&gt;' ) ), a.indexOf( '"' ) != -1 && ( a = a.replace( sa, '&quot;' ) ), a.indexOf( "'" ) != -1 && ( a = a.replace( ta, '&#39;' ) ), a.indexOf( '\x00' ) != -1 && ( a = a.replace( ua, '&#0;' ) ) ), a; }Aa( 'Soy template output is unsafe for use as HTML: ' + a ); return 'zSoyz'; },
        bb = /^<(body|caption|col|colgroup|head|html|tr|td|th|tbody|thead|tfoot)>/i,
        cb = {}; const db = function( a, b ) { b || w || ( w = new I() ); this.Ba = a || null; this.Qa = []; }; db.prototype.Ka = ba; const fb = function() { const a = eb; return a.Ba ? a.Ba.getData() : {}; }; var eb = new db(); const K = function() { this.oa = this.oa; this.Na = this.Na; }; K.prototype.oa = !1; var gb = function( a ) { gb[' ']( a ); return a; }; gb[' '] = ba; const hb = !C || Number( Va ) >= 9,
        ib = C && !H( '9' ); !F || H( '528' ); E && H( '1.9b' ) || C && H( '8' ) || Ka && H( '9.5' ) || F && H( '528' ); E && !H( '8' ) || C && H( '9' ); const L = function( a, b ) { this.type = a; this.currentTarget = this.target = b; this.defaultPrevented = this.A = !1; this.ya = !0; }; L.prototype.preventDefault = function() { this.defaultPrevented = !0; this.ya = !1; }; const M = function( a, b ) {
    L.call( this, a ? a.type : '' ); this.relatedTarget = this.currentTarget = this.target = null; this.charCode = this.keyCode = this.button = this.screenY = this.screenX = this.clientY = this.clientX = this.offsetY = this.offsetX = 0; this.metaKey = this.shiftKey = this.altKey = this.ctrlKey = !1; this.M = this.state = null; if ( a ) {
      const c = this.type = a.type,
            d = a.changedTouches ? a.changedTouches[0] : null; this.target = a.target || a.srcElement; this.currentTarget = b; let e = a.relatedTarget; if ( e ) {
        if ( E ) {
          let f; a: {
            try { gb( e.nodeName ); f = !0; break a; } catch ( g ) {}f =
!1;
          }f || ( e = null );
        }
      } else { c == 'mouseover' ? e = a.fromElement : c == 'mouseout' && ( e = a.toElement ); } this.relatedTarget = e; d === null ? ( this.offsetX = F || void 0 !== a.offsetX ? a.offsetX : a.layerX, this.offsetY = F || void 0 !== a.offsetY ? a.offsetY : a.layerY, this.clientX = void 0 !== a.clientX ? a.clientX : a.pageX, this.clientY = void 0 !== a.clientY ? a.clientY : a.pageY, this.screenX = a.screenX || 0, this.screenY = a.screenY || 0 ) : ( this.clientX = void 0 !== d.clientX ? d.clientX : d.pageX, this.clientY = void 0 !== d.clientY ? d.clientY : d.pageY, this.screenX = d.screenX || 0,
      this.screenY = d.screenY || 0 ); this.button = a.button; this.keyCode = a.keyCode || 0; this.charCode = a.charCode || ( c == 'keypress' ? a.keyCode : 0 ); this.ctrlKey = a.ctrlKey; this.altKey = a.altKey; this.shiftKey = a.shiftKey; this.metaKey = a.metaKey; this.state = a.state; this.M = a; a.defaultPrevented && this.preventDefault();
    }
  }; r( M, L );
  M.prototype.preventDefault = function() { M.Aa.preventDefault.call( this ); const a = this.M; if ( a.preventDefault )a.preventDefault(); else if ( a.returnValue = !1, ib ) try { if ( a.ctrlKey || a.keyCode >= 112 && a.keyCode <= 123 )a.keyCode = -1; } catch ( b ) {} }; let N = 'closure_listenable_' + ( 1E6 * Math.random() | 0 ),
      jb = 0; const kb = function( a, b, c, d, e ) { this.listener = a; this.T = null; this.src = b; this.type = c; this.K = Boolean( d ); this.N = e; this.key = ++jb; this.B = this.J = !1; },
        lb = function( a ) { a.B = !0; a.listener = null; a.T = null; a.src = null; a.N = null; }; const O = function( a ) { this.src = a; this.b = {}; this.I = 0; }; O.prototype.add = function( a, b, c, d, e ) { const f = a.toString(); a = this.b[f]; a || ( a = this.b[f] = [], this.I++ ); const g = mb( a, b, d, e ); g > -1 ? ( b = a[g], c || ( b.J = !1 ) ) : ( b = new kb( b, this.src, f, Boolean( d ), e ), b.J = c, a.push( b ) ); return b; }; O.prototype.remove = function( a, b, c, d ) { a = a.toString(); if ( !( a in this.b ) ) return !1; const e = this.b[a]; b = mb( e, b, c, d ); return b > -1 ? ( lb( e[b] ), y( e.length != null ), Array.prototype.splice.call( e, b, 1 ), e.length == 0 && ( delete this.b[a], this.I-- ), !0 ) : !1; };
  const nb = function( a, b ) {
    const c = b.type; if ( c in a.b ) {
      let d = a.b[c],
          e = Ea( d, b ),
          f; if ( f = e >= 0 )y( d.length != null ), Array.prototype.splice.call( d, e, 1 ); f && ( lb( b ), a.b[c].length == 0 && ( delete a.b[c], a.I-- ) );
    }
  }; O.prototype.U = function( a ) {
    a = a && a.toString(); let b = 0,
        c; for ( c in this.b ) if ( !a || c == a ) { for ( let d = this.b[c], e = 0; e < d.length; e++ )++b, lb( d[e] ); delete this.b[c]; this.I--; } return b;
  }; O.prototype.F = function( a, b, c, d ) { a = this.b[a.toString()]; let e = -1; a && ( e = mb( a, b, c, d ) ); return e > -1 ? a[e] : null; };
  var mb = function( a, b, c, d ) { for ( let e = 0; e < a.length; ++e ) { const f = a[e]; if ( !f.B && f.listener == b && f.K == Boolean( c ) && f.N == d ) return e; } return -1; }; var ob = 'closure_lm_' + ( 1E6 * Math.random() | 0 ),
      pb = {},
      qb = 0,
      P = function( a, b, c, d, e ) {
        if ( l( b ) ) { for ( var f = 0; f < b.length; f++ )P( a, b[f], c, d, e ); return null; }c = rb( c ); if ( a && a[N] ) { a = a.w( b, c, d, e ); } else {
          if ( !b ) throw Error( 'Invalid event type' ); var f = Boolean( d ),
              g = S( a ); g || ( a[ob] = g = new O( a ) ); c = g.add( b, c, !1, d, e ); if ( !c.T ) {
            d = sb(); c.T = d; d.src = a; d.listener = c; if ( a.addEventListener )a.addEventListener( b.toString(), d, f ); else if ( a.attachEvent )a.attachEvent( tb( b.toString() ), d ); else throw Error( 'addEventListener and attachEvent are unavailable.' );
            qb++;
          }a = c;
        } return a;
      },
      sb = function() {
        var a = ub,
            b = hb ? function( c ) { return a.call( b.src, b.listener, c ); } : function( c ) { c = a.call( b.src, b.listener, c ); if ( !c ) return c; }; return b;
      },
      vb = function( a, b, c, d, e ) { if ( l( b ) ) for ( let f = 0; f < b.length; f++ )vb( a, b[f], c, d, e ); else c = rb( c ), a && a[N] ? a.la( b, c, d, e ) : a && ( a = S( a ) ) && ( b = a.F( b, c, Boolean( d ), e ) ) && T( b ); },
      T = function( a ) {
        if ( !n( a ) && a && !a.B ) {
          const b = a.src; if ( b && b[N] ) { nb( b.g, a ); } else {
            let c = a.type,
                d = a.T; b.removeEventListener ? b.removeEventListener( c, d, a.K ) : b.detachEvent && b.detachEvent( tb( c ), d ); qb--; ( c = S( b ) ) ?
              ( nb( c, a ), c.I == 0 && ( c.src = null, b[ob] = null ) ) : lb( a );
          }
        }
      },
      tb = function( a ) { return a in pb ? pb[a] : pb[a] = 'on' + a; },
      xb = function( a, b, c, d ) { let e = !0; if ( a = S( a ) ) if ( b = a.b[b.toString()] ) for ( b = b.concat(), a = 0; a < b.length; a++ ) { let f = b[a]; f && f.K == c && !f.B && ( f = wb( f, d ), e = e && !1 !== f ); } return e; },
      wb = function( a, b ) {
        const c = a.listener,
              d = a.N || a.src; a.J && T( a ); return c.call( d, b );
      },
      ub = function( a, b ) {
        if ( a.B ) return !0; if ( !hb ) {
          let c; if ( !( c = b ) )a: { c = [ 'window', 'event' ]; for ( var d = k, e; e = c.shift(); ) if ( d[e] != null ) { d = d[e]; } else { c = null; break a; }c = d; }e = c; c = new M( e,
            this ); d = !0; if ( !( e.keyCode < 0 || void 0 != e.returnValue ) ) {
            a: { var f = !1; if ( e.keyCode == 0 ) try { e.keyCode = -1; break a; } catch ( z ) { f = !0; } if ( f || void 0 == e.returnValue )e.returnValue = !0; }e = []; for ( f = c.currentTarget; f; f = f.parentNode )e.push( f ); for ( var f = a.type, g = e.length - 1; !c.A && g >= 0; g-- ) {
              c.currentTarget = e[g]; var p = xb( e[g], f, !0, c ),
                  d = d && p;
            } for ( g = 0; !c.A && g < e.length; g++ )c.currentTarget = e[g], p = xb( e[g], f, !1, c ), d = d && p;
          } return d;
        } return wb( a, new M( b, this ) );
      },
      S = function( a ) { a = a[ob]; return a instanceof O ? a : null; },
      yb = '__closure_events_fn_' +
( 1E9 * Math.random() >>> 0 ),
      rb = function( a ) { y( a, 'Listener can not be null.' ); if ( ca( a ) == 'function' ) return a; y( a.handleEvent, 'An object listener must have handleEvent method.' ); a[yb] || ( a[yb] = function( b ) { return a.handleEvent( b ); } ); return a[yb]; }; const U = function( a ) { K.call( this ); this.qa = a; this.G = {}; }; r( U, K ); const zb = []; U.prototype.w = function( a, b, c, d ) { l( b ) || ( b && ( zb[0] = b.toString() ), b = zb ); for ( let e = 0; e < b.length; e++ ) { const f = P( a, b[e], c || this.handleEvent, d || !1, this.qa || this ); if ( !f ) break; this.G[f.key] = f; } return this; };
  U.prototype.la = function( a, b, c, d, e ) { if ( l( b ) ) for ( let f = 0; f < b.length; f++ ) this.la( a, b[f], c, d, e ); else c = c || this.handleEvent, e = e || this.qa || this, c = rb( c ), d = Boolean( d ), b = a && a[N] ? a.F( b, c, d, e ) : a ? ( a = S( a ) ) ? a.F( b, c, d, e ) : null : null, b && ( T( b ), delete this.G[b.key] ); return this; }; U.prototype.U = function() { Fa( this.G, function( a, b ) { this.G.hasOwnProperty( b ) && T( a ); }, this ); this.G = {}; }; U.prototype.handleEvent = function() { throw Error( 'EventHandler.handleEvent not implemented' ); }; C && H( 8 ); const Ab = function() { J.call( this ); }; r( Ab, J ); Ab.prototype.L = Ya; const Bb = function( a, b ) { this.content = String( a ); this.ba = b != null ? b : null; }; r( Bb, $a ); Bb.prototype.L = Za;
  const Cb = ( function( a ) { function b( a ) { this.content = a; }b.prototype = a.prototype; return function( a, d ) { const e = new b( String( a ) ); void 0 !== d && ( e.ba = d ); return e; }; } )( Ab ),
        Db = function( a ) {
          let b = new I( void 0 ); y( a, 'Soy template may not be null.' ); a: {
            a = a( cb, void 0, void 0 ); b = ( b || w || ( w = new I() ) ).createElement( 'DIV' ); a = ab( a ); const c = a.match( bb ); y( !c, 'This template starts with a %s, which cannot be a child of a <div>, as required by soy internals. Consider using goog.soy.renderElement instead.\nTemplate output: %s', c && c[0], a ); b.innerHTML =
a; if ( b.childNodes.length == 1 && ( a = b.firstChild, a.nodeType == 1 ) ) { b = a; break a; }
          } return b;
        }; ( function( a ) { function b( a ) { this.content = a; }b.prototype = a.prototype; return function( a, d ) { let e = String( a ); if ( !e ) return ''; e = new b( e ); void 0 !== d && ( e.ba = d ); return e; }; } )( Ab ); const Eb = function( a, b, c ) {
    c = c || {}; a = String( '<style type="text/css"' + ( c.C ? ' nonce="' + c.C + '"' : '' ) + '>.__gcp_button_cls {display: block; background: url(data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAAoCAYAAAA/tpB3AAAAAXNSR0IArs4c6QAAAAZiS0dEAP8A/wD/oL2nkwAAAAlwSFlzAAAK6wAACusBgosNWgAAAAd0SU1FB9sEFhYNCw4IkMgAAAA1SURBVAjXvcexCQAxDATB5aT+C1UNEufEYOzPP1lmsW1VFepuNDNbzx4B/yQzUUR8dC+2vQAZOSMDprhidAAAAABJRU5ErkJggg==) repeat-x; border: 1px solid #ccc; height: 20px; text-decoration: none; font: bold 14px/20px "Droid Sans", "Helvetica Neue", Arial, Helvetica, Geneva, sans-serif; color: #666; position: relative; padding: 0 5px 0 25px; float: left; text-shadow: #fff 0 1px 1px; cursor: pointer; -webkit-border-radius: 3px; -moz-border-radius: 3px; border-radius: 3px; -webkit-transition: background-position .2s ease-out, color .2s ease-out;}.__gcp_button_cls:hover {background-position: 0 -20px; color: #111;}.__gcp_button_img_cls {height: 18px; width: 17px; position: absolute; left: 5px; top: 2px; background: url(data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABEAAAASBAMAAABP1yhnAAAAA3NCSVQICAjb4U/gAAAAFVBMVEX///+RkZH///+RkZEAmQDLPDwAVKrOcjT8AAAAB3RSTlMA7v//////bfV3xQAAAAlwSFlzAAALEgAACxIB0t1+/AAAABx0RVh0U29mdHdhcmUAQWRvYmUgRmlyZXdvcmtzIENTNXG14zYAAAAVdEVYdENyZWF0aW9uIFRpbWUANC8xOS8xMcNUYbQAAABuSURBVAiZXY7BCcAwCEVFQxboAmLoPegCoTv0HnrI/iNUDb3Ug3588r8AQGYGWYdI6yFIATCXxN5aqmyBEwSOs42NLVwcK2m4YIdO512u7rtmKGWYMWCrswyVsKoP8k6ra82/0u8XDGfOIPHy8QKJ2w71g2IHXgAAAABJRU5ErkJggg==) no-repeat center;}</style><div class="__gcp_button_cls"><div class="__gcp_button_img_cls"></div><div>Print</div></div>' );
    return Cb( a );
  }; Eb.ka = 'cp.gadget.tpl.printButton'; const Fb = function() { return new Bb( 'You are using an outdated browser. For better performance and more advanced features such as Google Cloud Print - please upgrade to a modern browser such as Google Chrome, Firefox 3 or IE9 (if using IE9, ensure that compatibility mode is turned off).', void 0 ); }; Fb.ka = 'cp.gadget.tpl.browserIsNotSupported'; const Gb = function( a, b, c, d ) { this.name = a; this.data = b; this.source = c; this.origin = d; },
        Hb = function() { this.R = {}; const a = this.S = q( this.Ja, this ); window.addEventListener ? window.addEventListener( 'message', a, !1 ) : window.attachEvent( 'onmessage', a ); }; Hb.prototype.addListener = function( a, b, c, d ) { const e = this.R[a] || []; b = new Ib( b, c, d ); Ea( e, b ) >= 0 || e.push( b ); this.R[a] = e; return this; }; Hb.prototype.xa = function() { this.R = {}; return this; };
  Hb.prototype.Ja = function( a ) { if ( a.data ) { var b = a.data.indexOf( '::' ); if ( !( b <= 0 ) ) for ( var c = a.data.substr( 0, b ), b = new Gb( c, a.data.substr( b + 2 ), a.source, a.origin ), c = this.R[c] || [], d, e = 0; d = c[e]; e++ )d.source && d.source != a.source || d.origin != '*' && d.origin != a.origin || d.Ga( b ); } }; var Ib = function( a, b, c ) { this.Ga = a; this.source = b || null; this.origin = c || '*'; }; const V = function( a ) { this.S = new Hb(); this.fa = this.ea = !1; this.m = this.l = this.o = this.i = null; this.u = []; this.v = a; }; h = V.prototype; h.open = function() { this.fa && this.close(); this.fa = !0; this.ua(); const a = this.da(); a && this.S.addListener( 'cp-dialog-on-init', q( this.ia, this ), a ).addListener( 'cp-dialog-on-close', q( this.close, this ), a ).addListener( 'cp-dialog-on-print-locally', q( this.Pa, this ), a ); }; h.close = function() { this.ma(); this.S.xa(); this.fa = this.ea = !1; this.l && this.l(); }; h.W = function( a ) { this.i = a; this.a && this.a.W( this.i ); };
  h.Z = function( a ) { this.o = a; Jb( this, this.o ); }; h.X = function( a ) { this.l = a; }; h.Y = function( a ) { this.m = a; }; h.$ = function( a ) { this.u = a; Kb( this, 'cp-dialog-set-tags', t( this.u ) ); }; const Lb = function( a ) { return ( a.i || 'https://www.google.com/' ) + a.pa() + '?user=' + a.v.ja + '&hl=en'; }; V.prototype.ia = function() { this.ea = !0; Jb( this, this.o ); Kb( this, 'cp-dialog-set-tags', t( this.u ) ); let a; a = this.v; a = t( { 'mode': a.ha, 'selected_user': a.ja, 'show-print-locally': a.za } ); Kb( this, 'cp-dialog-set-configuration', a ); };
  var Jb = function( a, b ) { if ( b ) { let c; c = {}; c.type = b.Wa; c.title = b.Va; c.content = b.na; c.encoding = b.Fa; c = t( c ); Kb( a, 'cp-dialog-set-print-document', c ); } },
      Kb = function( a, b, c ) { const d = a.da(); d && a.ea && d.postMessage && d.postMessage( b + '::' + c, '*' ); }; V.prototype.Pa = function() { this.close(); this.m ? this.m() : window.print(); }; var Ob = function( a, b, c, d, e ) { if ( !( C || D || F && H( '525' ) ) ) return !0; if ( G && e ) return Mb( a ); if ( e && !d ) return !1; n( b ) && ( b = Nb( b ) ); if ( !c && ( b == 17 || b == 18 || G && b == 91 ) ) return !1; if ( ( F || D ) && d && c ) switch ( a ) { case 220: case 219: case 221: case 192: case 186: case 189: case 187: case 188: case 190: case 191: case 192: case 222: return !1; } if ( C && d && b == a ) return !1; switch ( a ) { case 13: return !0; case 27: return !( F || D ); } return Mb( a ); },
      Mb = function( a ) {
        if ( a >= 48 && a <= 57 || a >= 96 && a <= 106 || a >= 65 && a <= 90 || ( F || D ) && a == 0 ) return !0; switch ( a ) {
          case 32: case 43: case 63: case 64: case 107: case 109: case 110: case 111: case 186: case 59: case 189: case 187: case 61: case 188: case 190: case 191: case 192: case 222: case 219: case 220: case 221: return !0;
          default: return !1;
        }
      },
      Nb = function( a ) { if ( E )a = Pb( a ); else if ( G && F ) switch ( a ) { case 93: a = 91; break; } return a; },
      Pb = function( a ) { switch ( a ) { case 61: return 187; case 59: return 186; case 173: return 189; case 224: return 91; case 0: return 224; default: return a; } }; const W = function() { K.call( this ); this.g = new O( this ); this.Ca = this; this.wa = null; }; r( W, K ); W.prototype[N] = !0; h = W.prototype; h.addEventListener = function( a, b, c, d ) { P( this, a, b, c, d ); }; h.removeEventListener = function( a, b, c, d ) { vb( this, a, b, c, d ); };
  h.dispatchEvent = function( a ) {
    Qb( this ); let b,
        c = this.wa; if ( c ) { b = []; for ( var d = 1; c; c = c.wa )b.push( c ), y( ++d < 1E3, 'infinite loop' ); }c = this.Ca; d = a.type || a; if ( m( a ) ) { a = new L( a, c ); } else if ( a instanceof L ) { a.target = a.target || c; } else { var e = a; a = new L( d, c ); Ha( a, e ); } var e = !0,
        f; if ( b ) for ( var g = b.length - 1; !a.A && g >= 0; g-- )f = a.currentTarget = b[g], e = Rb( f, d, !0, a ) && e; a.A || ( f = a.currentTarget = c, e = Rb( f, d, !0, a ) && e, a.A || ( e = Rb( f, d, !1, a ) && e ) ); if ( b ) for ( g = 0; !a.A && g < b.length; g++ )f = a.currentTarget = b[g], e = Rb( f, d, !1, a ) && e; return e;
  };
  h.w = function( a, b, c, d ) { Qb( this ); return this.g.add( String( a ), b, !1, c, d ); }; h.la = function( a, b, c, d ) { return this.g.remove( String( a ), b, c, d ); }; h.xa = function( a ) { return this.g ? this.g.U( a ) : 0; }; var Rb = function( a, b, c, d ) {
    b = a.g.b[String( b )]; if ( !b ) return !0; b = b.concat(); for ( var e = !0, f = 0; f < b.length; ++f ) {
      const g = b[f]; if ( g && !g.B && g.K == c ) {
        const p = g.listener,
              z = g.N || g.src; g.J && nb( a.g, g ); e = !1 !== p.call( z, d ) && e;
      }
    } return e && d.ya != 0;
  }; W.prototype.F = function( a, b, c, d ) { return this.g.F( String( a ), b, c, d ); }; var Qb = function( a ) { y( a.g, 'Event target is not initialized. Did you call the superclass (goog.events.EventTarget) constructor?' ); }; const X = function( a, b ) { W.call( this ); a && ( this.P && this.detach(), this.f = a, this.O = P( this.f, 'keypress', this, b ), this.ga = P( this.f, 'keydown', this.Ha, b, this ), this.P = P( this.f, 'keyup', this.Ia, b, this ) ); }; r( X, W ); h = X.prototype; h.f = null; h.O = null; h.ga = null; h.P = null; h.c = -1; h.h = -1; h.aa = !1;
  const Sb = { 3: 13, 12: 144, 63232: 38, 63233: 40, 63234: 37, 63235: 39, 63236: 112, 63237: 113, 63238: 114, 63239: 115, 63240: 116, 63241: 117, 63242: 118, 63243: 119, 63244: 120, 63245: 121, 63246: 122, 63247: 123, 63248: 44, 63272: 46, 63273: 36, 63275: 35, 63276: 33, 63277: 34, 63289: 144, 63302: 45 },
        Tb = { 'Up': 38, 'Down': 40, 'Left': 37, 'Right': 39, 'Enter': 13, 'F1': 112, 'F2': 113, 'F3': 114, 'F4': 115, 'F5': 116, 'F6': 117, 'F7': 118, 'F8': 119, 'F9': 120, 'F10': 121, 'F11': 122, 'F12': 123, 'U+007F': 46, 'Home': 36, 'End': 35, 'PageUp': 33, 'PageDown': 34, 'Insert': 45 },
        Ub = C || D || F && H( '525' ),
        Vb = G && E;
  X.prototype.Ha = function( a ) { if ( F || D ) if ( this.c == 17 && !a.ctrlKey || this.c == 18 && !a.altKey || G && this.c == 91 && !a.metaKey ) this.h = this.c = -1; this.c == -1 && ( a.ctrlKey && a.keyCode != 17 ? this.c = 17 : a.altKey && a.keyCode != 18 ? this.c = 18 : a.metaKey && a.keyCode != 91 && ( this.c = 91 ) ); Ub && !Ob( a.keyCode, this.c, a.shiftKey, a.ctrlKey, a.altKey ) ? this.handleEvent( a ) : ( this.h = Nb( a.keyCode ), Vb && ( this.aa = a.altKey ) ); }; X.prototype.Ia = function( a ) { this.h = this.c = -1; this.aa = a.altKey; };
  X.prototype.handleEvent = function( a ) {
    let b = a.M,
        c, d,
        e = b.altKey; C && a.type == 'keypress' ? ( c = this.h, d = c != 13 && c != 27 ? b.keyCode : 0 ) : ( F || D ) && a.type == 'keypress' ? ( c = this.h, d = b.charCode >= 0 && b.charCode < 63232 && Mb( c ) ? b.charCode : 0 ) : Ka && !F ? ( c = this.h, d = Mb( c ) ? b.keyCode : 0 ) : ( c = b.keyCode || this.h, d = b.charCode || 0, Vb && ( e = this.aa ), G && d == 63 && c == 224 && ( c = 191 ) ); let f = c = Nb( c ),
        g = b.keyIdentifier; c ? c >= 63232 && c in Sb ? f = Sb[c] : c == 25 && a.shiftKey && ( f = 9 ) : g && g in Tb && ( f = Tb[g] ); a = f == this.c; this.c = f; b = new Wb( f, d, a, b ); b.altKey = e; this.dispatchEvent( b );
  };
  X.prototype.detach = function() { this.O && ( T( this.O ), T( this.ga ), T( this.P ), this.P = this.ga = this.O = null ); this.f = null; this.h = this.c = -1; }; var Wb = function( a, b, c, d ) { M.call( this, d ); this.type = 'key'; this.keyCode = a; this.charCode = b; this.repeat = c; }; r( Wb, M ); const Xb = function( a, b ) {
    W.call( this ); var c = this.f = a,
        c = da( c ) && c.nodeType == 1 ? this.f : this.f ? this.f.body : null,
        d; if ( d = Boolean( c ) ) { a: { y( c, 'Node cannot be null or undefined.' ); d = c.nodeType == 9 ? c : c.ownerDocument || c.document; if ( d.defaultView && d.defaultView.getComputedStyle && ( d = d.defaultView.getComputedStyle( c, null ) ) ) { d = d.direction || d.getPropertyValue( 'direction' ) || ''; break a; }d = ''; }d = ( d || ( c.currentStyle ? c.currentStyle.direction : null ) || c.style && c.style.direction ) == 'rtl'; } this.La = d; P( this.f, E ? 'DOMMouseScroll' : 'mousewheel',
      this, b );
  }; r( Xb, W ); Xb.prototype.handleEvent = function( a ) {
    let b = 0,
        c = 0,
        d = 0; a = a.M; if ( a.type == 'mousewheel' ) { c = 1; if ( C || F && ( Ma || H( '532.0' ) ) )c = 40; d = Yb( -a.wheelDelta, c ); void 0 !== a.wheelDeltaX ? ( b = Yb( -a.wheelDeltaX, c ), c = Yb( -a.wheelDeltaY, c ) ) : c = d; } else { d = a.detail, d > 100 ? d = 3 : d < -100 && ( d = -3 ), void 0 !== a.axis && a.axis === a.HORIZONTAL_AXIS ? b = d : c = d; }n( this.sa ) && ( b = Math.min( Math.max( b, -this.sa ), this.sa ) ); n( this.ta ) && ( c = Math.min( Math.max( c, -this.ta ), this.ta ) ); this.La && ( b = -b ); b = new Zb( d, a, b, c ); this.dispatchEvent( b );
  };
  var Yb = function( a, b ) { return F && ( G || Na ) && a % b != 0 ? a : a / b; },
      Zb = function( a, b, c, d ) { M.call( this, b ); this.type = 'mousewheel'; this.detail = a; this.deltaX = c; this.deltaY = d; }; r( Zb, M ); const $b = function( a, b, c ) {
    c = c || {}; return Cb( '<style type="text/css"' + ( c.C ? ' nonce="' + c.C + '"' : '' ) + '>.__gcp_dialog_background_cls {position: fixed; top: 0; bottom: 0; left: 0; right: 0; z-index: 1002; background: white; opacity: 0.75;}.__gcp_dialog_container_cls {height: 385px; width: 600px; top: 50%; margin-top: -190px; left: 50%; margin-left: -325px; padding: 15px 25px; -webkit-box-shadow: 0 4px 16px rgba(0,0,0,.2); -moz-box-shadow: 0 4px 16px rgba(0,0,0,.2); box-shadow: 0 4px 16px rgba(0,0,0,.2); background: white; background-clip: padding-box; border: 1px solid #ACACAC; border: 1px solid rgba(0, 0, 0, .333); outline: 0; position: fixed; background: white; z-index: 2147483646;}.__gcp_dialog_close_cls {height: 15px; width: 15px; top: 21px; right: 31px; position: absolute; background: url(data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAA8AAAAPCAYAAAA71pVKAAAAAXNSR0IArs4c6QAAAAZiS0dEAP8A/wD/oL2nkwAAAAlwSFlzAAALEwAACxMBAJqcGAAAAAd0SU1FB9sEGRcrKtgeedMAAAAZdEVYdENvbW1lbnQAQ3JlYXRlZCB3aXRoIEdJTVBXgQ4XAAAAWklEQVQoz8WTuQ0AMQgEDc1S01Zrp77TgPwEJoQdtCAwSb2dxiksqXu7CF91QnknwV+Y5T9wRFgFzHW0TQ0IRJiEBKZwNvPWtrMRym3PYNlg1SLqnp2n3XzVAKIEULf6A6q/AAAAAElFTkSuQmCC) no-repeat center; cursor: pointer; z-index: 2147483647;}</style><div class="__gcp_dialog_background_cls"></div><div class="__gcp_dialog_container_cls"><div class="__gcp_dialog_close_cls"></div><iframe class="__gcp_dialog_iframe_cls" style="' +
( c.C ? '/*' + c.C + '*/' : '' ) + 'height: 100%; width: 100%; border: 0;"></iframe></div>' );
  }; $b.ka = 'cp.gadget.tpl.printDialogDesktop'; const ac = function( a ) { V.call( this, a ); this.D = new U( this ); this.Ma = new Xb( document ); this.j = Db( $b ); this.ra = this.s = null; }; r( ac, V ); h = ac.prototype; h.ua = function() { document.body.appendChild( this.j ); this.s = Xa( '__gcp_dialog_iframe_cls', this.j ); const a = Xa( '__gcp_dialog_close_cls', this.j ); this.j.style.display = ''; this.ra = new X( this.j.ownerDocument.body ); this.D.w( a, 'click', q( this.close, this ) ).w( this.ra, 'key', q( this.Oa, this ) ).w( this.Ma, 'mousewheel', function( a ) { a.preventDefault(); } ); this.s.src = Lb( this ); this.s.focus(); };
  h.ma = function() { this.j.style.display = 'none'; this.s && ( this.s.src = '' ); this.D.U(); }; h.da = function() { return this.s && this.s.contentWindow; }; h.pa = function() { return 'cloudprint/gadget.html'; }; h.ia = function() { ac.Aa.ia.call( this ); Xa( '__gcp_dialog_close_cls', this.j ).style.display = 'none'; }; h.Oa = function( a ) { a.keyCode == 27 && ( a.preventDefault(), this.close() ); }; const Y = function( a ) { V.call( this, a ); this.H = null; }; r( Y, V ); Y.prototype.da = function() { return this.H; }; Y.prototype.pa = function() { return 'cloudprint/dialog.html'; }; Y.prototype.ua = function() { this.H = window.open( Lb( this ) ); }; Y.prototype.ma = function() { this.H && !this.H.closed && this.H.close(); }; const Z = function( a ) { this.D = new U( this ); this.m = this.l = this.o = this.a = this.i = null; this.u = []; this.v = a || new u(); }; h = Z.prototype; h.Sa = function( a ) { this.D.U(); a && this.D.w( a, 'click', q( this.va, this ) ); }; h.W = function( a ) { this.i = a; this.a && this.a.W( this.i ); }; h.Z = function( a, b, c, d ) { if ( this.v.ha != 'print-document' ) throw Error( 'Cannot set print document on gadget which is not in PRINT_DOCUMENT mode.' ); this.o = new ma( a, b, c, d ); this.a && this.a.Z( this.o ); }; h.X = function( a ) { this.l = a || null; this.a && this.a.X( this.l ); };
  h.Y = function( a ) { this.m = a || null; this.a && this.a.Y( this.m ); }; h.$ = function( a ) { this.u = a; this.a && this.a.$( this.u ); };
  h.va = function() {
    if ( C ? ya( '9' ) >= 0 : E ? ya( '1.9.0' ) >= 0 : 1 ) { if ( !this.a ) { var a; La ? a = !0 : ( a = A, a = a.indexOf( 'Android' ) != -1 || a.indexOf( 'iPad' ) != -1 || a.indexOf( 'iPod' ) != -1 || a.indexOf( 'iPhone' ) != -1 ); this.a = a ? new Y( this.v ) : new ac( this.v ); this.a.W( this.i ); this.a.Z( this.o ); this.a.X( this.l ); this.a.Y( this.m ); this.a.$( this.u ); } this.a.open(); } else {
      a = alert; const b = Fb( fb() ); Da( b, J, 'renderText cannot be called on a non-strict soy template' ); y( b.L === Za, 'renderText was called with a template of kind other than "text"' ); eb.Qa.push( { cb: Fb.ka,
        data: null,
        $a: fb() } ); eb.Ka(); a( String( b ) );
    }
  }; h.Da = function() { this.a && this.a.close(); }; aa( 'cloudprint.Gadget', Z ); Z.createDefaultPrintButton = function( a ) { const b = Db( Eb ); ( a = m( a ) ? document.getElementById( a ) : a ) && a.appendChild( b ); return b; }; Z.prototype.setPrintButton = Z.prototype.Sa; Z.prototype.setPrintDocument = Z.prototype.Z; Z.prototype.setOnCloseCallback = Z.prototype.X; Z.prototype.setOnPrintLocallyCallback = Z.prototype.Y; Z.prototype.setPrintTags = Z.prototype.$; Z.prototype.openPrintDialog = Z.prototype.va;
  Z.prototype.closePrintDialog = Z.prototype.Da;
} )();
