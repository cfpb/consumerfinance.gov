import FormModel from '../../../../../cfgov/unprocessed/js/modules/util/FormModel.js';

const HTML_SNIPPET = `
<form method="get" action=".">
  <input type="text">

  <!-- Ignored input -->
  <input type="hidden">

  <!-- Disabled inputs -->
  <input type="text" disabled>
  <input type="text" disabled="">
  <input type="text" disabled="disabled">

  <!-- Required inputs -->
  <input type="text" required>
  <input type="text" required="">
  <input type="text" required="required">


  <!-- Required radio buttons -->
  <input type="checkbox" value="blog" id="filter_categories_blog" name="categories" required>
  <label for="filter_categories_blog">
      Blog
  </label>
  <input type="checkbox" value="op-ed" id="filter_categories_op-ed" name="categories" required>
  <label for="filter_categories_op-ed">
      Op-ed
  </label>
  <input type="checkbox" value="press-release" id="filter_categories_press-release" name="categories" required>
  <label for="filter_categories_press-release">
      Press release
  </label>

  <!-- Not required radio buttons -->
  <input type="checkbox" value="blog" id="filter_categories_blog" name="categories" required>
  <label for="filter_categories_blog">
      Blog
  </label>
  <input type="checkbox" value="op-ed" id="filter_categories_op-ed" name="categories" required>
  <label for="filter_categories_op-ed">
      Op-ed
  </label>
  <input type="checkbox" value="press-release" id="filter_categories_press-release" name="categories" required>
  <label for="filter_categories_press-release">
      Press release
  </label>

  <input type="submit" value="Apply filters">
</form>
`;

describe( 'FormModel', () => {
  beforeAll( () => {
    document.body.innerHTML = HTML_SNIPPET;
  } );

  describe( '.getModel()', () => {
    it( 'should return an object with properties of the form', () => {
      const modelInst = new FormModel( document.forms[0] ).init();
      const model = modelInst.getModel();

      expect( model.get( 'elements' ).length ).toBe( 15 );
      expect( model.get( 'validateableElements' ).length ).toBe( 13 );
    } );

  } );

} );
