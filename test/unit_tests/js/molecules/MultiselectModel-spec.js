import MultiselectModel from '../../../../unprocessed/js/molecules/MultiselectModel';

const HTML_SNIPPET = `
<select class="o-multiselect" multiple>
  <option value="mortgages">
    Mortgages
  </option>
  <option value="financial-education" selected>
    Financial education
  </option>
  <option value="financial-well-being">
    Financial well-being
  </option>
  <option value="student-loans">
    Student loans
  </option>
  <option value="rulemaking">
    Rulemaking
  </option>
  <option value="banking">
    Banking
  </option>
</select>
`;

let multiselectModel;
let selectDom;

describe( 'MultiselectModel', () => {
  beforeEach( () => {
    document.body.innerHTML = HTML_SNIPPET;

    selectDom = document.querySelector( 'select[multiple]' );
    multiselectModel = new MultiselectModel( selectDom.options ).init();
  } );

  describe( 'init()', () => {
    it( 'should correctly initialize when given valid options', () => {
      multiselectModel = new MultiselectModel( selectDom.options ).init();
      expect( multiselectModel.constructor ).toBe( MultiselectModel );
    } );
  } );

  describe( 'toggleOption()', () => {
    it( 'should toggle checked value of option', () => {
      expect( multiselectModel.getOption( 0 ).checked ).toBe( false );
      expect( multiselectModel.toggleOption( 0 ) ).toBe( true );
      expect( multiselectModel.getOption( 0 ).checked ).toBe( true );

      expect( multiselectModel.getOption( 1 ).checked ).toBe( true );
      expect( multiselectModel.toggleOption( 1 ) ).toBe( false );
      expect( multiselectModel.getOption( 1 ).checked ).toBe( false );

      expect( multiselectModel.getOption( 2 ).checked ).toBe( false );
      expect( multiselectModel.toggleOption( 2 ) ).toBe( true );
      expect( multiselectModel.getOption( 2 ).checked ).toBe( true );

      expect( multiselectModel.getOption( 3 ).checked ).toBe( false );
      expect( multiselectModel.toggleOption( 3 ) ).toBe( true );
      expect( multiselectModel.getOption( 3 ).checked ).toBe( true );

      expect( multiselectModel.getOption( 4 ).checked ).toBe( false );
      expect( multiselectModel.toggleOption( 4 ) ).toBe( true );
      expect( multiselectModel.getOption( 4 ).checked ).toBe( true );

      expect( multiselectModel.getOption( 5 ).checked ).toBe( false );
      expect( multiselectModel.toggleOption( 5 ) ).toBe( true );
      expect( multiselectModel.getOption( 5 ).checked ).toBe( true );

      // Try to push beyond maximum selections.
      expect( multiselectModel.toggleOption( 1 ) ).toBe( false );
      expect( multiselectModel.getOption( 1 ).checked ).toBe( false );
      expect( multiselectModel.toggleOption( 2 ) ).toBe( false );
      expect( multiselectModel.getOption( 2 ).checked ).toBe( false );
      expect( multiselectModel.toggleOption( 1 ) ).toBe( true );
      expect( multiselectModel.getOption( 1 ).checked ).toBe( true );
    } );
  } );

  describe( 'getSelectedIndices()', () => {
    it( 'should get the indices of the checked options', () => {
      expect( multiselectModel.getSelectedIndices()[0] ).toBe( 1 );
      multiselectModel.toggleOption( 0 );
      expect( multiselectModel.getSelectedIndices()[0] ).toBe( 0 );
      expect( multiselectModel.getSelectedIndices()[1] ).toBe( 1 );
    } );
  } );

  describe( 'isAtMaxSelections()', () => {
    it( 'should toggle checked value of option', () => {
      expect( multiselectModel.isAtMaxSelections() ).toBe( false );

      multiselectModel.toggleOption( 0 );
      expect( multiselectModel.isAtMaxSelections() ).toBe( false );

      // No need to toggle the second option because it's already checked.

      multiselectModel.toggleOption( 2 );
      expect( multiselectModel.isAtMaxSelections() ).toBe( false );

      multiselectModel.toggleOption( 3 );
      expect( multiselectModel.isAtMaxSelections() ).toBe( false );

      multiselectModel.toggleOption( 4 );
      expect( multiselectModel.isAtMaxSelections() ).toBe( true );

      multiselectModel.toggleOption( 5 );
      expect( multiselectModel.isAtMaxSelections() ).toBe( true );

      multiselectModel.toggleOption( 5 );
      expect( multiselectModel.isAtMaxSelections() ).toBe( true );

      expect( multiselectModel.toggleOption( 4 ) ).toBe( false );
      expect( multiselectModel.isAtMaxSelections() ).toBe( false );
    } );
  } );

  describe( 'filterIndices()', () => {
    it( 'should return indices of matched options in a search', () => {
      expect( multiselectModel.filterIndices( 'mo' ).length ).toBe( 1 );
      expect( multiselectModel.filterIndices( 'mort' ).length ).toBe( 1 );
      expect( multiselectModel.filterIndices( 'mort' )[0] ).toBe( 0 );
      expect( multiselectModel.filterIndices( 'fin' ).length ).toBe( 2 );
      expect( multiselectModel.filterIndices( 'fin' )[0] ).toBe( 1 );
      expect( multiselectModel.filterIndices( 'fin' )[1] ).toBe( 2 );
      expect( multiselectModel.filterIndices( 'being' ).length ).toBe( 1 );
      expect( multiselectModel.filterIndices( 'being' )[0] ).toBe( 2 );
    } );
  } );

  describe( 'clearFilter()', () => {
    it( 'should clear current and last matched options in a search', () => {
      multiselectModel.filterIndices( 'fin' );
      expect( multiselectModel.getLastFilterIndices().length ).toBe( 0 );
      expect( multiselectModel.getFilterIndices().length ).toBe( 2 );
      multiselectModel.filterIndices( 'mo' );
      expect( multiselectModel.getLastFilterIndices().length ).toBe( 2 );
      expect( multiselectModel.getFilterIndices().length ).toBe( 1 );
      multiselectModel.clearFilter();
      expect( multiselectModel.getLastFilterIndices().length ).toBe( 0 );
      expect( multiselectModel.getFilterIndices().length ).toBe( 0 );
    } );
  } );

  describe( 'getFilterIndices()', () => {
    it( 'should return current indices of matched options in a search', () => {
      expect( multiselectModel.getFilterIndices().length ).toBe( 0 );
      multiselectModel.filterIndices( 'fin' );
      expect( multiselectModel.getFilterIndices().length ).toBe( 2 );
      expect( multiselectModel.getFilterIndices()[0] ).toBe( 1 );
      expect( multiselectModel.getFilterIndices()[1] ).toBe( 2 );
    } );
  } );

  describe( 'getLastFilterIndices()', () => {
    it( 'should return indices of the last matched options in a search', () => {
      expect( multiselectModel.getLastFilterIndices().length ).toBe( 0 );
      multiselectModel.filterIndices( 'fin' );
      expect( multiselectModel.getLastFilterIndices().length ).toBe( 0 );
      multiselectModel.filterIndices( 'mo' );
      expect( multiselectModel.getLastFilterIndices().length ).toBe( 2 );
      expect( multiselectModel.getLastFilterIndices()[0] ).toBe( 1 );
      expect( multiselectModel.getLastFilterIndices()[1] ).toBe( 2 );
      multiselectModel.filterIndices( 'being' );
      expect( multiselectModel.getLastFilterIndices().length ).toBe( 1 );
      expect( multiselectModel.getLastFilterIndices()[0] ).toBe( 0 );
    } );
  } );

  describe( 'getIndex()', () => {
    it( 'should get correct index when no filter results', () => {
      expect( multiselectModel.getIndex() ).toBe( -1 );
      multiselectModel.setIndex( 2 );
      expect( multiselectModel.getIndex() ).toBe( 2 );
      multiselectModel.filterIndices( 'asdf' );
      expect( multiselectModel.getIndex() ).toBe( -1 );
    } );

    it( 'should get reset index when options are filtered', () => {
      expect( multiselectModel.getIndex() ).toBe( -1 );
      multiselectModel.setIndex( 2 );
      expect( multiselectModel.getIndex() ).toBe( 2 );
      multiselectModel.filterIndices( 'mo' );
      expect( multiselectModel.getIndex() ).toBe( -1 );
    } );
  } );

  describe( 'setIndex()', () => {
    it( 'should set index within available option range', () => {
      expect( multiselectModel.getIndex() ).toBe( -1 );
      multiselectModel.setIndex( 0 );
      expect( multiselectModel.getIndex() ).toBe( 0 );
      multiselectModel.setIndex( 1 );
      expect( multiselectModel.getIndex() ).toBe( 1 );
      multiselectModel.setIndex( 2 );
      expect( multiselectModel.getIndex() ).toBe( 2 );
      multiselectModel.setIndex( 10 );
      expect( multiselectModel.getIndex() ).toBe( 5 );
      multiselectModel.setIndex( -2 );
      expect( multiselectModel.getIndex() ).toBe( -1 );
    } );

    it( 'should set index within filtered option range', () => {
      expect( multiselectModel.getIndex() ).toBe( -1 );
      multiselectModel.filterIndices( 'fin' );
      multiselectModel.setIndex( 0 );
      expect( multiselectModel.getIndex() ).toBe( 0 );
      expect( multiselectModel.getFilterIndices()[multiselectModel.getIndex()] )
        .toBe( 1 );
      multiselectModel.setIndex( 1 );
      expect( multiselectModel.getIndex() ).toBe( 1 );
      multiselectModel.setIndex( 2 );
      expect( multiselectModel.getIndex() ).toBe( 1 );
    } );
  } );

  describe( 'resetIndex()', () => {
    it( 'should return -1 for index when called', () => {
      expect( multiselectModel.resetIndex() ).toBe( -1 );
    } );
  } );

  describe( 'getOption()', () => {
    it( 'should return the correct option when requested', () => {
      expect( multiselectModel.getOption( 2 ).text ).toBe( 'Financial well-being' );
      expect( multiselectModel.getOption( 2 ).value ).toBe( 'financial-well-being' );
      expect( multiselectModel.getOption( 2 ).checked ).toBe( false );
      expect( multiselectModel.getOption( 1 ).checked ).toBe( true );
    } );
  } );

  describe( 'getOptions()', () => {
    it( 'should return the full options list', () => {
      expect( multiselectModel.getOptions().length ).toBe( 6 );
      multiselectModel.filterIndices( 'asdf' );
      expect( multiselectModel.getOptions().length ).toBe( 6 );
    } );
  } );

} );
