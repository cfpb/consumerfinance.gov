import
Slider
  // eslint-disable-next-line max-len
  from '../../../../../../cfgov/unprocessed/apps/owning-a-home/js/explore-rates/Slider';
let sliderDom;
let slider;

const HTML_SNIPPET = `
<div class="a-range">
  <div class="a-range_labels">
    <span class="a-range_labels-min"></span>
    <span class="a-range_labels-max"></span>
  </div>
  <input type="range"
         class="a-range_input">
  <div class="a-range_text"></div>
</div>
`;

describe( 'explore-rates/Slider', () => {
  beforeEach( () => {
    document.body.innerHTML = HTML_SNIPPET;
    sliderDom = document.querySelector( '.a-range' );
    slider = new Slider( sliderDom );
    slider.init( {
      min: 0,
      max: 100,
      value: 60
    } );
  } );

  describe( 'init()', () => {
    it( 'should return instance when initialized', () => {
      expect( slider ).toBeInstanceOf( Slider );
      expect( slider.init() ).toBeInstanceOf( Slider );
    } );

    it( 'should initialize rangeslider class', () => {
      const rangeSliderDom = sliderDom.querySelector( '.rangeslider' );
      expect( rangeSliderDom.classList.contains( 'rangeslider' ) )
        .toBe( true );
    } );
  } );

  describe( 'min()', () => {
    it( 'should return minimum value of the range slider', () => {
      expect( slider.min() ).toBe( 0 );
    } );
  } );

  describe( 'max()', () => {
    it( 'should return maximum value of the range slider', () => {
      expect( slider.max() ).toBe( 100 );
    } );
  } );

  describe( 'valMin()', () => {
    it( 'should return the minimum value of the range slider label', () => {
      expect( slider.valMin() ).toBe( 60 );
    } );
  } );

  describe( 'valMax()', () => {
    it( 'should return 19 units above the minimum ' +
        'value of the range slider label', () => {
      expect( slider.valMax() ).toBe( 79 );
    } );

    it( 'should return the maximum value when minimum value of ' +
        'the range slider is less than 20 units from maximum', () => {
      document.body.innerHTML = HTML_SNIPPET;
      sliderDom = document.querySelector( '.a-range' );
      slider = new Slider( sliderDom );
      slider.init( {
        min: 0,
        max: 100,
        value: 90
      } );
      expect( slider.valMax() ).toBe( 100 );
    } );
  } );

  describe( 'currentState()', () => {
    it( 'should return the warning state of the range slider label', () => {
      slider.setState( Slider.STATUS_WARNING );
      expect( slider.currentState() ).toBe( Slider.STATUS_WARNING );
      slider.setState( Slider.STATUS_OKAY );
      expect( slider.currentState() ).toBe( Slider.STATUS_OKAY );
    } );
  } );

  describe( 'setState()', () => {
    it( 'should set the warning state of the range slider label', () => {
      slider.setState( Slider.STATUS_WARNING );
      const handleDom = sliderDom.querySelector( '.rangeslider__handle' );
      expect( handleDom.classList.contains( 'warning' ) ).toBe( true );
      slider.setState( Slider.STATUS_OKAY );
      expect( handleDom.classList.contains( 'warning' ) ).toBe( false );
    } );

    it( 'should throw error when incorrect state is passed', () => {
      function incorrectState() {
        slider.setState();
      }
      expect( incorrectState )
        .toThrowError( 'State set in range slider is not supported!' );
    } );
  } );
} );
