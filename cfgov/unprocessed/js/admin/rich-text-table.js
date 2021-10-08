/* eslint-disable max-lines-per-function, complexity, max-statements, require-jsdoc, func-style */

import { stateToHTML } from 'draft-js-export-html';

const body = document.querySelector( 'body' );
function _handleModalClicks( event ) {
  if ( document.querySelector( '.modal-open' ) ) {
    event.stopImmediatePropagation();
  }
}

// https://handsontable.com/docs/7.2.2/tutorial-cell-editor.html
( function( Handsontable ) {
  // We're extending the base TextEditor, https://github.com/handsontable/handsontable/blob/master/src/editors/textEditor/textEditor.js
  const RichTextEditor = Handsontable.editors.TextEditor.prototype.extend();

  const draftail_options = {
    entityTypes: [
      {
        type: 'LINK',
        icon: 'link',
        description: 'Link',
        attributes: [ 'url', 'id', 'parentId' ],
        whitelist: { href: '^(http:|https:|undefined$)' }
      },
      {
        type: 'DOCUMENT',
        icon: 'doc-full',
        description: 'Document'
      }
    ],
    enableHorizontalRule: false,
    enableLineBreak: true,
    inlineStyles: [
      {
        type: 'BOLD',
        icon: 'bold',
        description: 'Bold'
      },
      {
        type: 'ITALIC',
        icon: 'italic',
        description: 'Italic'
      }
    ],
    blockTypes: [
      {
        label: 'H3',
        type: 'header-three',
        description: 'Heading 3'
      },
      {
        label: 'H4',
        type: 'header-four',
        description: 'Heading 4'
      },
      {
        label: 'H5',
        type: 'header-five',
        description: 'Heading 5'
      },
      {
        type: 'ordered-list-item',
        icon: 'list-ol',
        description: 'Numbered list'
      },
      {
        type: 'unordered-list-item',
        icon: 'list-ul',
        description: 'Bulleted list'
      }
    ]
  };

  /* Do some light modification to the TextEditor's TEXTAREA element to
     prepare it for Draftail. */
  RichTextEditor.prototype.createElements = function() {
    Handsontable.editors.TextEditor.prototype.createElements.call( this );

    /* TextEditor's TEXTAREA will hold our data for Draftail, and we'll use
       its style when we open the editor. */
    this.TEXTAREA.id = 'rich-text-table-cell-editor';
    this.TEXTAREA.style.display = 'none';
  };

  // Get the Draftail value from the input and convert it back to HTML
  RichTextEditor.prototype.getValue = function() {
    const options = {
      entityStyleFn: entity => {
        const entityType = entity.get( 'type' ).toLowerCase();
        if ( entityType === 'document' ) {
          const data = entity.getData();
          return {
            element: 'a',
            attributes: {
              'href': data.url,
              'data-linktype': 'DOCUMENT',
              'data-id': data.id,
              'type': 'DOCUMENT'
            },
            style: {
            }
          };
        }
        return null;
      }
    };
    const editorValue = this.TEXTAREA.value;

    const raw = JSON.parse( editorValue );
    if ( raw === null ) return '';

    const state = window.DraftJS.convertFromRaw( raw );
    return stateToHTML( state, options );
  };

  /* Convert the given value to what Draftail expects, and store it on the
     input element from which we'll initialize Draftail */
  RichTextEditor.prototype.setValue = function( value ) {
    let contentState;

    const blocksFromHTML = value ? window.DraftJS.convertFromHTML( value ) : null;
    if ( blocksFromHTML && blocksFromHTML.contentBlocks ) {
      contentState = window.DraftJS.ContentState.createFromBlockArray( blocksFromHTML.contentBlocks, blocksFromHTML.entityMap );
    } else {
      contentState = window.DraftJS.ContentState.createFromText( '' );
    }

    const cellValue = window.DraftJS.convertToRaw( contentState );
    if ( cellValue.entityMap ) {
      for ( const entity in cellValue.entityMap ) {
        if ( cellValue.entityMap[entity] && cellValue.entityMap[entity].data ) {
          cellValue.entityMap[entity].data.url = cellValue.entityMap[entity].data.href;
          if ( cellValue.entityMap[entity].data.url.startsWith( '/documents/' ) ) {
            cellValue.entityMap[entity].type = 'DOCUMENT';
          }
        }
      }
    }

    this.TEXTAREA.value = JSON.stringify( cellValue );
  };

  RichTextEditor.prototype.open = function() {
    /* Initialize the Draftail editor for this cell
       We seem to have to initialize a new Draftail editor for every cell,
       because there doesn't seem to be a way to update the data after
       initialization. */
    window.draftail.initEditor(
      '#' + this.TEXTAREA.id,
      draftail_options,
      document.currentScript
    );

    // Call TextEditor's open
    Handsontable.editors.TextEditor.prototype.open.call( this );

    // Style the Draftail editor with the TextEditor's TEXTAREA's style
    const draftailWrapper = this.TEXTAREA_PARENT.querySelector( '.Draftail-Editor__wrapper' );
    draftailWrapper.style.cssText = this.TEXTAREA.style.cssText;
    draftailWrapper.style.display = 'block';

    /* This is default style for input elements.
       TODO: Specify this in a stylesheet somewhere */
    draftailWrapper.style.backgroundColor = '#fafafa';
    draftailWrapper.style.border = '1px solid var(--color-input-focus-border)';

    // Clear the TEXTAREA's style and hide it
    this.TEXTAREA.style.cssText = null;
    this.TEXTAREA.style.display = 'none';

    body.addEventListener( 'mousedown', _handleModalClicks );
  };

  RichTextEditor.prototype.close = function() {
    Handsontable.editors.TextEditor.prototype.close.call( this );
    // Remove the Draftail editor for this cell
    this.TEXTAREA_PARENT.querySelector( '.Draftail-Editor__wrapper' ).remove();
    body.removeEventListener( 'mousedown', _handleModalClicks );
  };

  // Register the rich text editor
  Handsontable.editors.RichTextEditor = RichTextEditor;
  Handsontable.editors.registerEditor( 'RichTextEditor', RichTextEditor );
} )( window.Handsontable );


/* Based on Wagtail's initTable. We have to override Wagtail's to add more
   fields to the table block, and Wagtail's implementation does not provide
   hooks with which to do that.
   https://github.com/wagtail/wagtail/blob/773da59107b7cd0e072d3f8c3d5bb7287d47b9b8/client/src/entrypoints/contrib/table_block/table.js */
function initAtomicTable( id, tableOptions ) {
  // Definitions from Wagtail's initTable
  const containerId = id + '-handsontable-container';
  let hot = null;

  // Wagtail's built-in field elements
  const tableHeaderCheckbox = window.jQuery( '#' + id + '-handsontable-header' );
  const colHeaderCheckbox = window.jQuery( '#' + id + '-handsontable-col-header' );
  const tableCaption = window.jQuery( '#' + id + '-handsontable-col-caption' );

  // Out custom field elements
  const headingText = window.jQuery( '#' + id + '-handsontable-heading-text' );
  const headingLevel = window.jQuery( '#' + id + '-handsontable-heading-level' );
  const headingIcon = window.jQuery( '#' + id + '-handsontable-heading-icon' );
  const stripedRows = window.jQuery( '#' + id + '-handsontable-striped-rows' );
  const stackOnMobile = window.jQuery( '#' + id + '-handsontable-stack-on-mobile' );
  const tableFullWidth = window.jQuery( '#' + id + '-handsontable-full-width' );
  const tableColFixed = window.jQuery( '#' + id + '-handsontable-col-fixed' );
  const tableIsSortable = window.jQuery( '#' + id + '-handsontable-sortable' );
  const colWidthInput = window.jQuery( '#' + id + '-fixed-width-column-input' );
  const colSortTypeInput = window.jQuery( '#' + id + '-sortable-input' );
  const colWidthSelector = window.jQuery( `
    <td>
      <select class="column-width-input">
        <option value="">Flexible width</option>
        <option value="u-w10pct">10%</option>
        <option value="u-w20pct">20%</option>
        <option value="u-w25pct">25%</option>
        <option value="u-w30pct">30%</option>
        <option value="u-w33pct">33%</option>
        <option value="u-w40pct">40%</option>
        <option value="u-w50pct">50%</option>
        <option value="u-w60pct">60%</option>
        <option value="u-w66pct">66%</option>
        <option value="u-w70pct">70%</option>
        <option value="u-w75pct">75%</option>
        <option value="u-w80pct">80%</option>
        <option value="u-w90pct">90%</option>
      </select>
    </td>
  ` );
  const colSortSelector = window.jQuery( `
    <td>
      <select class="sortable-type-input">
        <option value="">None</option>
        <option value="string">Alphabetical</option>
        <option value="number">Numerical</option>
        <option value="string-default">Alphabetical and sort initially</option>
        <option value="number-default">Numerical and sort initially</option>
      </select>
    </td>
  ` );

  /* Initialize the field values based on the JSON data in this table
     block's hidden field. */
  const hiddenStreamInput = window.jQuery( '#' + id );
  let columnWidths;
  let colSortTypes;
  let dataForForm = null;
  try {
    console.log( 'Loaded', hiddenStreamInput.val() );
    dataForForm = JSON.parse( hiddenStreamInput.val() );
  } catch ( e ) {
    // do nothing
  }
  if ( dataForForm !== null ) {
    // Wagtail's built-in fields
    if ( dataForForm.hasOwnProperty( 'first_row_is_table_header' ) ) {
      tableHeaderCheckbox.prop( 'checked', dataForForm.first_row_is_table_header );
    }
    if ( dataForForm.hasOwnProperty( 'first_col_is_header' ) ) {
      colHeaderCheckbox.prop( 'checked', dataForForm.first_col_is_header );
    }
    if ( dataForForm.hasOwnProperty( 'table_caption' ) ) {
      tableCaption.prop( 'value', dataForForm.table_caption );
    }

    // Custom fields
    if ( dataForForm.hasOwnProperty( 'heading_text' ) ) {
      headingText.prop( 'value', dataForForm.heading_text );
    }
    if ( dataForForm.hasOwnProperty( 'heading_level' ) ) {
      headingLevel.prop( 'value', dataForForm.heading_level );
    }
    if ( dataForForm.hasOwnProperty( 'heading_icon' ) ) {
      headingIcon.prop( 'value', dataForForm.heading_icon );
    }
    if ( dataForForm.hasOwnProperty( 'is_striped' ) ) {
      stripedRows.prop( 'checked', dataForForm.is_striped );
    }
    if ( dataForForm.hasOwnProperty( 'is_stacked' ) ) {
      stackOnMobile.prop( 'checked', dataForForm.is_stacked );
    }
    if ( dataForForm.hasOwnProperty( 'is_full_width' ) ) {
      tableFullWidth.prop( 'checked', dataForForm.is_full_width );
    }
    if ( dataForForm.hasOwnProperty( 'fixed_col_widths' ) ) {
      tableColFixed.prop( 'checked', dataForForm.fixed_col_widths );
    }
    if ( dataForForm.hasOwnProperty( 'is_sortable' ) ) {
      tableIsSortable.prop( 'checked', dataForForm.is_sortable );
    }
    if ( dataForForm.hasOwnProperty( 'column_widths' ) ) {
      columnWidths = dataForForm.column_widths;
    }
    if ( dataForForm.hasOwnProperty( 'sortable_types' ) ) {
      colSortTypes = dataForForm.sortable_types;
    }
  }

  /* Function from Wagtail's initTable used below in the customized persist
     function */
  const getCellsClassnames = function() {
    const meta = hot.getCellsMeta();
    const cellsClassnames = [];
    for ( let i = 0; i < meta.length; i++ ) {
      if ( meta[i].hasOwnProperty( 'className' ) ) {
        cellsClassnames.push( {
          row: meta[i].row,
          col: meta[i].col,
          className: meta[i].className
        } );
      }
    }
    return cellsClassnames;
  };

  /* Custom function to get column widths and sort types for all columns */
  const getColAttributes = function( colAttributeTable ) {
    let colAttributes = [];
    const selectedAttributes = colAttributeTable.find( 'option:selected' );
    selectedAttributes.each( index => {
      const selectedAttribute = selectedAttributes[index].value;
      colAttributes.push( selectedAttribute );
    } );
    return colAttributes;
  };

  /* Persist field values back to the JSON data in this table block's hidden
     field's JSON. This function is then called by event handling functions
     defined below. */
  const persist = function() {
    console.log( 'Persisting' );
    hiddenStreamInput.val( JSON.stringify( {
      // Wagtail's built-in fields
      data: hot.getData(),
      cell: getCellsClassnames(),
      first_row_is_table_header: tableHeaderCheckbox.prop( 'checked' ),
      first_col_is_header: colHeaderCheckbox.prop( 'checked' ),
      table_caption: tableCaption.val(),

      // Custom fields
      heading_text: headingText.val(),
      heading_level: headingLevel.val(),
      heading_icon: headingIcon.val(),
      is_striped: stripedRows.prop( 'checked' ),
      is_stacked: stackOnMobile.prop( 'checked' ),
      is_full_width: tableFullWidth.prop( 'checked' ),
      fixed_col_widths: tableColFixed.prop( 'checked' ),
      is_sortable: tableIsSortable.prop( 'checked' ),
      column_widths: getColAttributes( colWidthInput ),
      sortable_types: getColAttributes( colSortTypeInput )

    } ) );
    console.log( 'Persisted', hiddenStreamInput.val() );
  };

  const toggleAttributeInputTable = function( attributeInputTable, isAttributeEnabled ) {
    if ( isAttributeEnabled ) {
      attributeInputTable.show();
    } else {
      attributeInputTable.hide();
    }
  };

  const populateColumnAttributeInputs = function() {
    const colCount = columnWidths ? columnWidths.length : hot.countCols();
    for ( let index = 0; index < colCount; index++ ) {
      const colWidthValue = columnWidths ? columnWidths[index] : '';
      const colSortType = colSortTypes ? colSortTypes[index] : '';
      const colWidthSelectorClone =
        colWidthSelector
          .clone()
          .on( 'change', () => { persist(); } );
      const colSortSelectorClone =
        colSortSelector
          .clone()
          .on( 'change', () => { persist(); } );
      colWidthSelectorClone
        .find( 'select option[value="' + colWidthValue + '"]' )
        .prop('selected', true);
      colSortSelectorClone
        .find( 'select option[value="' + colSortType + '"]' )
        .prop('selected', true);
      colWidthInput
        .find( 'tr' )
        .append( colWidthSelectorClone );
      colSortTypeInput
        .find( 'tr' )
        .append( colSortSelectorClone );
    }
  };

  const handleColumnAttributeChange = function( event ) {
    const attributeName = event.target.getAttribute( 'name' );
    const isAttributeEnabled = event.target.checked;
    let attributeInputTable;
    if ( attributeName === 'handsontable-col-fixed' ) {
      attributeInputTable = colWidthInput;
    } else if ( attributeName === 'handsontable-sortable' ) {
      attributeInputTable = colSortTypeInput;
    }
    toggleAttributeInputTable( attributeInputTable, isAttributeEnabled );
    persist();
  };

  /* Ensure each form field persists when changed.
     Wagtail's built-in fields */
  tableHeaderCheckbox.on( 'change', () => { persist(); } );
  colHeaderCheckbox.on( 'change', () => { persist(); } );
  tableCaption.on( 'change', () => { persist(); } );
  // Custom fields
  headingText.on( 'change', () => { persist(); } );
  headingLevel.on( 'change', () => { persist(); } );
  headingIcon.on( 'change', () => { persist(); } );
  stripedRows.on( 'change', () => { persist(); } );
  stackOnMobile.on( 'change', () => { persist(); } );
  tableFullWidth.on( 'change', () => { persist(); } );
  tableColFixed.on( 'change', () => { handleColumnAttributeChange( event ); } );
  tableIsSortable.on( 'change', () => { handleColumnAttributeChange( event ); } );
  // Change handlers for column widths and sort types are in populateColumnAttributeInputs

  /* The rest of this function is duplicated from Wagtail's initTable
     implementation in order to extend it to add extra fields. Those fields
     are persisted via event handling functions passed in via tableOptions,
     but the defaults for those call the resizeHeight function. It's only
     available in the inner scope of the initTable function, so we have to
     redefine it here. */
  const getWidth = function() {
    return window.jQuery( '.widget-table_input' ).closest( '.sequence-member-inner' ).width();
  };
  const getHeight = function() {
    const tableParent = window.jQuery( '#' + id ).parent();
    return tableParent.find( '.htCore' ).height() + ( tableParent.find( '.input' ).height() * 2 );
  };
  const resizeTargets = [ '.input > .handsontable', '.wtHider', '.wtHolder' ];
  const resizeHeight = function( height ) {
    const currTable = window.jQuery( '#' + id );
    window.jQuery.each( resizeTargets, function() {
      currTable.closest( '.field-content' ).find( this ).height( height );
    } );
  };

  /* Ensure that we persist the table block's data on each of the event types
     that Wagtail registers with HandsonTable */
  let isInitialized = false;
  const cellEvent = function( change, source ) {
    if ( source === 'loadData' ) {
      return; // don't save this change
    }
    persist();
  };
  const metaEvent = function( row, column, key, value ) {
    if ( isInitialized && key === 'className' ) {
      persist();
    }
  };
  const initEvent = function() {
    isInitialized = true;
  };
  const structureEvent = function( index, amount ) {
    resizeHeight( getHeight() );
    persist();
  };

  /* Custom handlers for adding and removing columns that also add and remove
     column attributes for the new or removed column */
  const handleCreateCol = function(index, amount ) {
    const newColIndex = index - 1 < 0 ? 0 : index - 1;
    const colWidthInputCell = colWidthInput.find( 'td:eq(' + newColIndex + ')' );
    const colSortTypeCell = colSortTypeInput.find( 'td:eq(' + newColIndex + ')' );
    const colWidthSelectorClone =
      colWidthSelector
        .clone()
        .on( 'change', () => { persist(); } );
    const colSortSelectorClone =
      colSortSelector
        .clone()
        .on( 'change', () => { persist(); } );
    if ( newColIndex === 0 ) {
      colWidthInputCell.before( colWidthSelectorClone );
      colSortTypeCell.before( colSortSelectorClone );
    } else {
      colWidthInputCell.after( colWidthSelectorClone );
      colSortTypeCell.after( colSortSelectorClone );
    }
    structureEvent( index, amount );
  };
  const handleRemoveCol = function(index, amount ) {
    colWidthInput.find( 'td:eq(' + index + ')' ).remove();
    colSortTypeInput.find( 'td:eq(' + index + ')' ).remove();
    structureEvent( index, amount );
  };

  const finalOptions = {};
  const defaultOptions = {
    afterChange: cellEvent,
    afterCreateCol: handleCreateCol,
    afterCreateRow: structureEvent,
    afterRemoveCol: handleRemoveCol,
    afterRemoveRow: structureEvent,
    afterSetCellMeta: metaEvent,
    afterInit: initEvent
  };
  if ( dataForForm !== null ) {
    if ( dataForForm.hasOwnProperty( 'data' ) ) {
      defaultOptions.data = dataForForm.data;
    }
    if ( dataForForm.hasOwnProperty( 'cell' ) ) {
      defaultOptions.cell = dataForForm.cell;
    }
  }

  Object.keys( defaultOptions ).forEach( key => {
    finalOptions[key] = defaultOptions[key];
  } );
  Object.keys( tableOptions ).forEach( key => {
    finalOptions[key] = tableOptions[key];
  } );

  hot = new window.Handsontable( document.getElementById( containerId ), finalOptions );
  hot.render();

  populateColumnAttributeInputs();
  if ( tableColFixed.prop( 'checked' ) ) {
    toggleAttributeInputTable( colWidthInput, true );
  }
  if ( tableIsSortable.prop( 'checked' ) ) {
    toggleAttributeInputTable( colSortTypeInput, true );
  }


  if ( 'resize' in window.jQuery( window ) ) {
    resizeHeight( getHeight() );
    window.jQuery( window ).on( 'load', () => {
      window.jQuery( window ).trigger( 'resize' );
    } );
  }
}
window.initAtomicTable = initAtomicTable;


/* AtomicTableBlock's Telepath widget.
   This handles the rendering of the entire table block form in the Wagtail
   admin. It is based on the Wagtail TableInput class:
   https://github.com/wagtail/wagtail/blob/773da59107b7cd0e072d3f8c3d5bb7287d47b9b8/client/src/entrypoints/contrib/table_block/table.js#L176-L243 */
class RichTextTableInput {
  constructor( options ) {
    this.options = options;
  }

  render( placeholder, name, id, initialState ) {
    const container = document.createElement( 'div' );
    container.innerHTML = `
      <div class="field">
        <label for="${ id }-handsontable-heading">Heading</label>
        <div class="field-content">
          <div class="heading-text-block">
            <label for="${ id }-handsontable-heading-text">Text:</label>
            <div class="input">
              <input type="text" id="${ id }-handsontable-heading-text" name="handsontable-heading-text">
            </div>
          </div>
          <div class="heading-level-block">
            <label for="${ id }-handsontable-heading-level">Level:</label>
            <div class="input">
              <select id="${ id }-handsontable-heading-level" name="handsontable-heading-level" placeholder="Level">
                <option value="h2">H2</option>
                <option value="h3">H3</option>
                <option value="h4">H4</option>
              </select>
            </div>
          </div>
          <div class="heading-icon-block">
            <label for="${ id }-handsontable-heading-icon">Icon:</label>
            <div class="input">
              <input type="text" id="${ id }-handsontable-heading-icon" name="handsontable-heading-icon">
              <span class="help">Input the name of an icon to appear to the left of the heading. E.g., approved, help-round, etc. <a href="https://cfpb.github.io/design-system/foundation/iconography">See full list of icons</a></span>
            </div>
          </div>
        </div>
      </div>
      <br/>

      <div class="field boolean_field widget-checkbox_input">
        <label for="${ id }-handsontable-striped-rows">Striped rows</label>
        <div class="field-content">
          <div class="input">
            <input type="checkbox" id="${ id }-handsontable-striped-rows" name="handsontable-striped-rows">
            <span class="help">Display the Table with striped rows</span>
          </div>
        </div>
      </div>
      <br/>

      <div class="field boolean_field widget-checkbox_input">
        <label for="${ id }-handsontable-stack-on-mobile">Stacked on mobile</label>
        <div class="field-content">
          <div class="input">
            <input type="checkbox" id="${ id }-handsontable-stack-on-mobile" name="handsontable-stack-on-mobile">
            <span class="help">Stack the table columns on mobile</span>
          </div>
        </div>
      </div>

      <div class="field boolean_field widget-checkbox_input">
        <label for="${ id }-handsontable-full-width">Full-width</label>
        <div class="field-content">
          <div class="input">
            <input type="checkbox" id="${ id }-handsontable-full-width" name="handsontable-full-width">
            <span class="help">Display the table at full-width</span>
         </div>
      </div>
      </div>
      <br/>

      <div class="field boolean_field widget-checkbox_input">
        <label for="${ id }-handsontable-header">Row header</label>
        <div class="field-content">
          <div class="input">
            <input type="checkbox" id="${ id }-handsontable-header" name="handsontable-header" />
          </div>
          <span class="help">Display the first row as a header.</span>
        </div>
      </div>
      <br/>

      <div class="field boolean_field widget-checkbox_input">
        <label for="${ id }-handsontable-col-header">Column header</label>
        <div class="field-content">
          <div class="input">
            <input type="checkbox" id="${ id }-handsontable-col-header" name="handsontable-col-header" />
          </div>
          <span class="help">Display the first column as a header.</span>
        </div>
      </div>
      <br/>

      <div class="field boolean_field widget-checkbox_input">
        <label for="${ id }-handsontable-col-fixed">Fixed-width columns</label>
        <div class="field-content">
          <div class="input">
            <input type="checkbox" id="${ id }-handsontable-col-fixed" name="handsontable-col-fixed">
            <span class="help">Enable fixed width columns</span>
          </div>
        </div>
      </div>
      <br/>

      <div class="field boolean_field widget-checkbox_input">
        <label for="${ id }-handsontable-sortable">Sortable table</label>
        <div class="field-content">
          <div class="input">
            <input type="checkbox" id="${ id }-handsontable-sortable" name="handsontable-sortable">
            <span class="help">Enable sortable table functionality</span>
          </div>
        </div>
      </div>
      <br/>

      <table id="${ id }-fixed-width-column-input">
        <tbody>
          <tr></tr>
        </tbody>
      </table>

      <table id="${ id }-sortable-input">
        <tbody>
          <tr></tr>
        </tbody>
      </table>

      <div id="${ id }-handsontable-container"></div>
      <input type="hidden" name="${ name }" id="${ id }" placeholder="Table">
    `;
    placeholder.replaceWith( container );

    const input = container.querySelector( `input[name="${ name }"]` );
    const options = this.options;

    const widget = {
      getValue() {
        return JSON.parse( input.value );
      },
      getState() {
        return JSON.parse( input.value );
      },
      setState( state ) {
        input.value = JSON.stringify( state );
        initAtomicTable( id, options );
      },
      focus() {}
    };
    widget.setState( initialState );
    return widget;
  }
}
window.telepath.register( 'v1.widgets.RichTextTableInput', RichTextTableInput );

