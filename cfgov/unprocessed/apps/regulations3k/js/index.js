/* This is some sample JS to confirm webpack is working as expected.
   Its contents are meaningless and will change. */

const module1 = require( './module1.js' );
const module2 = require( './module2.js' );
const Turbolinks = require( 'turbolinks' );

const Expandable = require( '../../../js/organisms/Expandable.js' );

const expandableDom = document.querySelectorAll( '.block .o-expandable' );
let expandable;

if ( expandableDom ) {
  for ( let i = 0, len = expandableDom.length; i < len; i++ ) {
    expandable = new Expandable( expandableDom[i] );
    expandable.init();
  }
}

Turbolinks.start();

const app = {
  init: () => {
    module1.init();
    module2.init();
    const payment = module1.getMonthlyPayment( 180000, 4.25, 360, 60 );
    console.log( `Your monthly payment is $${ payment }.` );
  }
};

app.init();
