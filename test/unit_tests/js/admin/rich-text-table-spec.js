import tableWrapper from '../../../../cfgov/unprocessed/js/admin/rich-text-table.js';

describe( 'Initializes RichTextEditor', () => {
  it( 'should build and register an editor', () => {
    const TextEditor = jest.fn();
    const registerEditor = jest.fn();
    const extend = jest.fn().mockImplementation( () => jest.fn() );

    const tableMock = {
      editors: {
        TextEditor,
        registerEditor
      }
    };
    TextEditor.prototype.extend = extend;

    tableWrapper.richTextTable( tableMock );
    expect( extend ).toBeCalled();
    expect( registerEditor ).toBeCalled();
  } );
} );

describe( 'Initializes the AtomicTable', () => {
  it( 'hook up a Handsontable', () => {
    const render = jest.fn();
    const countCols = jest.fn();

    const hot = jest.fn().mockImplementation( function() {
      this.render = render;
      this.countCols = countCols;
    } );

    const on = jest.fn();
    const prop = jest.fn();
    const jq = jest.fn().mockImplementation( () => ( {
      on,
      prop
    } ) );

    window.Handsontable = hot;
    window.jQuery = jq;

    tableWrapper.initAtomicTable( '', {} );
    expect( hot ).toBeCalled();
    expect( jq ).toHaveBeenCalledTimes( 17 );
    expect( on ).toHaveBeenCalledTimes( 11 );
    expect( render ).toBeCalled();
    expect( prop ).toHaveBeenCalledTimes( 2 );
  } );
} );

describe( 'RichTextTableInput', () => {
  it( 'Builds a RichTextTableInput', () => {
    const rep = jest.fn();
    const rtti = new tableWrapper.RichTextTableInput( {} );

    rtti.render( { replaceWith: rep }, 'test', 'test' );
    expect( rep ).toBeCalled();
  } );
} );
