import drivingCostEstimate from '../../../../../../cfgov/unprocessed/apps/youth-employment-success/js/views/driving-cost-estimate';

const CLASSES = drivingCostEstimate.CLASSES;

const HTML = `
  <div class="${ CLASSES.CONTAINER } u-hidden">
    <p>$<span class="${ CLASSES.COST_PER_MILE }"></span></p>
  </div>
`;

describe( 'drivingCostEstimateView', () => {
  let el;
  let view;

  beforeEach( () => {
    document.body.innerHTML = HTML;
    el = document.querySelector( `.${ CLASSES.CONTAINER }` );
    view = drivingCostEstimate( el );
  } );

  it( 'hides itself on init', () => {
    expect( el.classList.contains( 'u-hidden' ) ).toBeTruthy();
  } );

  it( 'reveals itself on render when transportation type is drive', () => {
    view.render( { transportation: 'Drive' } );

    expect( el.classList.contains( 'u-hidden' ) ).toBeFalsy();
    expect( el.querySelector( `.${ CLASSES.COST_PER_MILE }` ).textContent ).toBe( '$1.80' );
  } );

  it( 'hide itself again when transportation type is not drive', () => {
    view.render( { transportation: 'Drive' } );
    view.render( { transportation: 'Walk' } );

    expect( el.classList.contains( 'u-hidden' ) ).toBeTruthy();
    expect( el.querySelector( `.${ CLASSES.COST_PER_MILE }` ).textContent ).toBe( '' );
  } );
} );
