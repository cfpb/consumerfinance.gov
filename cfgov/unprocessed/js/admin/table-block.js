/* eslint-env jquery */
import { stateToHTML } from 'draft-js-export-html';

/*  TableBlock HandsonTable bridge

    Code copied from
    https://github.com/wagtail/wagtail/blob/master/wagtail/contrib/table_block/static/table_block/js/table.js

    Modifications were made to add new form fields to the TableBlock in Wagtail admin and support the rich text editor within table cells */
( function( win ) {


  function initRichTextTable( id, options ) {
    id = '#' + id;

    const utilities = {

      assign: function( target, source ) {
        target = target || {};

        for ( const key in source ) {
          if ( source.hasOwnProperty( key ) ) {
            target[key] = source[key];
          }
        }

        return target;
      },

      DIMENSIONS: {
        WIDTH:  0,
        HEIGHT: 1
      },

      $colWidthSelect: {},
      $sortableSelect: {}
    };

    let HandsonTableWagtailBridge = {};

    const HandsonTable = {

      initialize: function initialize( element, initializeOptions ) {
        if ( 'Handsontable' in win === false ) {
          return null;
        }

        const onTableChange = $.proxy( this.onTableChange, this );
        const onCreateCol = $.proxy( this.onCreateCol, this );
        const onRemoveCol = $.proxy( this.onRemoveCol, this );

        initializeOptions.afterChange = onTableChange;
        initializeOptions.afterCreateCol = onCreateCol;
        initializeOptions.afterCreateRow = onTableChange;
        initializeOptions.afterRemoveCol = onRemoveCol;
        initializeOptions.afterRemoveRow = onTableChange;
        initializeOptions.contextMenu = [
          'row_above',
          'row_below',
          '---------',
          'col_left',
          'col_right',
          '---------',
          'remove_row',
          'remove_col',
          '---------',
          'undo',
          'redo'
        ];

        this.$element = $( element );
        this.$element.addClass( 'richText' );
        initializeOptions = this.modify( initializeOptions );

        // Call to render removes 'null' literals from empty cells
        this.create( element, initializeOptions ).render();

        return this;
      },

      create: function create( element, createOptions ) {
        this.instance = new window.Handsontable( element, createOptions || {} );

        return this.instance;
      },

      modify: function modify( modifyOptions ) {
        const RichTextEditor = window.Handsontable.editors.BaseEditor.prototype.extend();

        RichTextEditor.prototype.beginEditing = function() {
          const initialCellValue = this.instance.getValue();
          let contentState;
          const blocksFromHTML = initialCellValue ? window.DraftJS.convertFromHTML( initialCellValue ) : null;
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
          const cellProperties = this.cellProperties;
          const instance = this.instance;

          instance.deselectCell();
          const modalDom = showModal();
          const editorHtml = _createRichTextEditor( cellValue );

          modalDom.on( 'save-btn:clicked', function() {
            const editorValue = editorHtml.value;
            let html;

            /* If editor is empty then set html to null becasue some 3rd parrty helper
               functions don't play nicely with empty valu cells */
            if ( !editorValue || editorValue === 'null' ) {
              html = null;
            } else {
              const raw = JSON.parse( editorValue );
              const state = window.DraftJS.convertFromRaw( raw );
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
              html = stateToHTML( state, options );
            }

            instance.setDataAtCell( cellProperties.row, cellProperties.col, html );
            instance.render();
            $( win ).resize();
          } );

        };

        modifyOptions.editor = RichTextEditor;

        return modifyOptions;
      },

      onTableChange: function onTableChange( index, change ) {
        if ( change === 'loadData' ) {
          return null;
        }

        this.$element.trigger( 'table:change', [ this.instance.getData() ] );

        return this;
      },

      onCreateCol: function onCreateCol( index ) {
        HandsonTableWagtailBridge.ui.$fixedWidthColInput
          .find( 'td' ).eq( index - 1 )
          .after( '<td>' + utilities.$colWidthSelect + '</td>' );

        HandsonTableWagtailBridge.ui.$sortableInput
          .find( 'td' ).eq( index - 1 )
          .after( '<td>' + utilities.$sortableSelect + '</td>' );

        this.$element.trigger( 'table:change', [ this.instance.getData() ] );

        return this;
      },

      onRemoveCol: function onRemoveCol( index ) {
        HandsonTableWagtailBridge.ui.$fixedWidthColInput
          .find( 'td' ).eq( index )
          .remove();

        this.$element.trigger( 'table:change', [ this.instance.getData() ] );

        return this;
      }
    };

    HandsonTableWagtailBridge = {

      initialize: function initialize( id, initializeOptions ) {
        const _this = this;
        let hiddenFieldData;

        utilities.$colWidthSelect = $( this.ui.$inputContainer + ' .column-width-input' ).prop( 'outerHTML' );
        utilities.$sortableSelect = $( this.ui.$inputContainer + ' .sortable-type-input' ).prop( 'outerHTML' );

        this.options = utilities.assign( {}, initializeOptions );
        this.element = document.querySelector( this.ui.$inputContainer );
        this.setCachedElements();

        hiddenFieldData = this.getHiddenFieldData();
        if ( hiddenFieldData && hiddenFieldData.hasOwnProperty( 'data' ) ) {

          // Overrides default value from options (if given) with value from database
          this.options.data = hiddenFieldData.data;
        }

        this.handsonTable = HandsonTable.initialize( this.ui.$container[0], this.options );
        this.handsonTable.$element.on( 'table:change', function( event, data ) {
          _this.saveDataToHiddenField( data );
        } );

        this.initializeEvents();
        this.initializeForm( hiddenFieldData );
      },


      initializeEvents: function initializeEvents() {
        const _this = this;
        const $window = $( win );

        $( this.element ).find( 'input' ).change( $.proxy( this.saveDataToHiddenField, this ) );

        // Apply resize after document is finished loading (parent .sequence-member-inner width is set)
        if ( !options.hasOwnProperty( 'width' ) ||
                     !options.hasOwnProperty( 'height' ) ) {
          // Size to parent .sequence-member-inner width if width is not given in options
          $window.resize( function() {
            _this.handsonTable.instance.updateSettings( {
              width: _this.getWidth(),
              height: _this.getHeight()
            } );
            _this.resize( utilities.DIMENSIONS.WIDTH, '100%' );
          } );
        }

        if ( 'resize' in $window ) {
          this.resize( utilities.DIMENSIONS.HEIGHT, this.getHeight() );
          $window.on( 'load', function() {
            $window.resize();
          } );
        }

        // On click, toggle visibility of fixed width inputs
        $( id + '-handsontable-col-fixed' ).click( function() {
          if ( $( this ).is( ':checked' ) ) {
            _this.toggleInputTable( _this.ui.$fixedWidthColInput, true );
          } else {
            _this.toggleInputTable( _this.ui.$fixedWidthColInput, false );
          }
        } );

        // On click, toggle visibility of sortable inputs
        $( id + '-handsontable-sortable' ).click( function() {
          if ( $( this ).is( ':checked' ) ) {
            _this.toggleInputTable( _this.ui.$sortableInput, true );
          } else {
            _this.toggleInputTable( _this.ui.$sortableInput, false );
          }
        } );

        // On change to Heading level, save data
        $( id + '-handsontable-heading-level' ).on( 'change', function() {
          _this.saveDataToHiddenField( 'no data' );
        } );

        // On change of fixed width values, save data
        $( id + '-fixed-width-column-input' ).on( 'change', '.column-width-input', function() {
          _this.saveDataToHiddenField( 'no data' );
        } );

        // On change of sortable values, save data
        $( id + '-sortable-input' ).on( 'change', '.sortable-type-input', function() {
          _this.saveDataToHiddenField( 'no data' );
        } );
      },

      ui: {
        $container:                 id + '-handsontable-container',
        $inputContainer:            id + '-handsontable-input-container',
        $headingText:               id + '-handsontable-heading-text',
        $headingLevel:              id + '-handsontable-heading-level',
        $headingIcon:               id + '-handsontable-heading-icon',
        $hasColHeaderCheckbox:      id + '-handsontable-col-header',
        $hasRowHeaderCheckbox:      id + '-handsontable-header',
        $hiddenField:               id,
        $isFullWidthCheckbox:       id + '-handsontable-full-width',
        $isStackedOnMobileCheckbox: id + '-handsontable-stack-on-mobile',
        $isTableStripedCheckbox:    id + '-handsontable-striped-rows',
        $fixedWidthColsCheckbox:    id + '-handsontable-col-fixed',
        $fixedWidthColInput:        id + '-fixed-width-column-input',
        $widthWarning:              id + '-width_warning',
        $isSortableCheckbox:        id + '-handsontable-sortable',
        $sortableInput:             id + '-sortable-input',
        $resizeTargets:             '.input > .handsontable, .wtHider, .wtHolder'
      },

      initializeForm: function initializeForm( hiddenFieldData ) {
        const ui = this.ui;
        let uiMap;
        let elem;
        let value;

        if ( hiddenFieldData !== null ) {
          uiMap = {
            heading_text:                ui.$headingText,
            heading_level:               ui.$headingLevel,
            heading_icon:                ui.$headingIcon,
            first_row_is_table_header:   ui.$hasRowHeaderCheckbox,
            first_col_is_header:         ui.$hasColHeaderCheckbox,
            is_full_width:               ui.$isFullWidthCheckbox,
            is_striped:                  ui.$isTableStripedCheckbox,
            is_stacked:                  ui.$isStackedOnMobileCheckbox,
            fixed_col_widths:            ui.$fixedWidthColsCheckbox,
            is_sortable:                 ui.$isSortableCheckbox
          };

          Object.keys( uiMap ).forEach( function( key ) {
            elem = uiMap[key][0];
            value = hiddenFieldData[key];

            if ( elem.tagName === 'INPUT' && elem.type === 'checkbox' && value ) {
              uiMap[key].prop( 'checked', value );
            } else if ( elem.tagName === 'INPUT' && elem.type === 'text' && value ) {
              uiMap[key].prop( 'value', value );
            } else if ( elem.tagName === 'SELECT' && value ) {
              uiMap[key].prop( 'value', value );
            }
          } );
        }

        // update fixed width input to match table
        const count = this.handsonTable.instance.countCols();
        const fixedWidthRow = this.ui.$fixedWidthColInput.find( 'tr' );
        fixedWidthRow.empty();
        for ( let y = 0; y < count; y++ ) {
          fixedWidthRow.append( '<td>' + utilities.$colWidthSelect + '</td>' );
        }

        // update sortable input to match table
        const sortableRow = this.ui.$sortableInput.find( 'tr' );
        sortableRow.empty();
        for ( let z = 0; z < count; z++ ) {
          sortableRow.append( '<td>' + utilities.$sortableSelect + '</td>' );
        }

        if ( ui.$fixedWidthColsCheckbox.is( ':checked' ) ) {
          this.toggleInputTable( this.ui.$fixedWidthColInput, true );
          ui.$fixedWidthColInput.find( 'td' ).each( function( index, value ) {
            $( this ).find( 'select' ).val( hiddenFieldData.column_widths[index] );
          } );
          this.getColumnWidths();
        }

        if ( ui.$isSortableCheckbox.is( ':checked' ) ) {
          this.toggleInputTable( this.ui.$sortableInput, true );
          ui.$sortableInput.find( 'td' ).each( function( index, value ) {
            $( this ).find( 'select' ).val( hiddenFieldData.sortable_types[index] );
          } );
        }
      },

      displayWidthWarning: function displayWidthWarning( totalWidth ) {
        // Display warning for width > 100%
        if ( totalWidth > 100 && this.ui.$fixedWidthColsCheckbox.is( ':checked' ) ) {
          this.ui.$widthWarning.show();
        } else {
          this.ui.$widthWarning.hide();
        }
      },

      getColumnWidths: function getColumnWidths() {
        const colCount = this.ui.$fixedWidthColInput.find( 'tr td' ).length;
        const array = [];
        let totalWidth = 0;

        for ( let x = 0; x < colCount; x++ ) {
          const i = x + 1;
          const widthClass = this.ui.$fixedWidthColInput
            .find( 'tr td:nth-child( ' + i + ' ) select option:selected' )
            .val();
          if ( widthClass ) {
            totalWidth += Number( widthClass.substring( 3, 5 ) );
          } else {
            totalWidth += 1;
          }

          array[x] = widthClass;
        }

        this.displayWidthWarning( totalWidth );

        return array;
      },

      getWidth: function getWidth() {
        return $( '.widget-table_input' ).closest( '.sequence-member-inner' ).width();
      },

      getHeight: function getHeight() {
        const tableParent = this.ui.$container.parent();

        return tableParent.find( '.htCore' ).height() +
                       ( tableParent.find( '.input' ).height() * 2 );
      },

      getSortableTypes: function getSortableTypes() {
        const colCount = this.ui.$sortableInput.find( 'tr td' ).length,
              array = [];

        for ( let x = 0; x < colCount; x++ ) {
          const i = x + 1;

          array[x] = this.ui.$sortableInput
            .find( 'tr td:nth-child( ' + i + ' ) select option:selected' )
            .val();
        }

        return array;
      },

      getHiddenFieldData: function getHiddenFieldData() {
        try {
          return $.parseJSON( this.ui.$hiddenField.val() );
        } catch ( error ) {
          // do nothing
          return null;
        }
      },

      setCachedElements: function setCachedElements() {
        let key;
        const ui = $.extend( {}, this.ui );
        const $element = $( this.element );
        let element;

        for ( key in ui ) {
          if ( ui.hasOwnProperty( key ) ) {
            element = $element.find( ui[key] );
            if ( element.length ) {
              ui[key] = element;
            } else {
              ui[key] = null;
            }
          }
        }

        this.ui = ui;

        return ui;
      },

      saveDataToHiddenField: function saveDataToHiddenField( data ) {
        const ui = this.ui;

        if ( !data ) {
          return;
        }

        ui.$hiddenField.val( JSON.stringify( {
          data:                      this.handsonTable.instance.getData(),
          column_widths:             this.getColumnWidths(),
          sortable_types:            this.getSortableTypes(),
          heading_text:              ui.$headingText.prop( 'value' ),
          heading_level:             ui.$headingLevel.prop( 'value' ),
          heading_icon:              ui.$headingIcon.prop( 'value' ),
          first_row_is_table_header: ui.$hasRowHeaderCheckbox.prop( 'checked' ),
          first_col_is_header:       ui.$hasColHeaderCheckbox.prop( 'checked' ),
          is_full_width:             ui.$isFullWidthCheckbox.prop( 'checked' ),
          is_striped:                ui.$isTableStripedCheckbox.prop( 'checked' ),
          is_stacked:                ui.$isStackedOnMobileCheckbox.prop( 'checked' ),
          fixed_col_widths:          ui.$fixedWidthColsCheckbox.prop( 'checked' ),
          is_sortable:               ui.$isSortableCheckbox.prop( 'checked' )
        } ) );
      },

      resize: function resize( dimension, amount ) {
        if ( dimension === utilities.DIMENSIONS.WIDTH ) {
          $.each( this.ui.$resizeTargets, function() {
            $( this ).width( amount );
          } );
          const parentDiv = $( '.widget-table_input' ).parent();
          parentDiv.find( '.field-content' ).width( amount );
          parentDiv.find( '.fieldname-table .field-content .field-content' ).width( '80%' );

        } else if ( dimension === utilities.DIMENSIONS.HEIGHT ) {
          const _this = this;
          $.each( this.ui.$resizeTargets, function() {
            _this.ui.$container.closest( '.field-content' ).find( this ).height( amount );
          } );
        }
      },

      onTableChange: function onTableChange( index ) {
        this.resize( utilities.DIMENSIONS.HEIGHT, this.getHeight() );
        this.saveDataToHiddenField();
      },

      toggleInputTable: function toggleInputTable( inputTable, state ) {
        state = state || true;

        if ( state === true ) {
          inputTable.show();
        } else {
          inputTable.hide();
        }
      }
    };

    return HandsonTableWagtailBridge.initialize( id, options );
  }


  /*  showModal

      Code copied from
      https://github.com/wagtail/wagtail/blob/master/wagtail/admin/
      static_src/wagtailadmin/js/hallo-bootstrap.js

      Create a Wagtail modal using Javascript. */
  function showModal( ) {
    let modalDom;
    let modalBodyDom;
    let bodyDom = null;
    let saveBtnDom;

    // Set header template.
    const MODAL_BODY_TEMPLATE = [
      '<header class="nice-padding hasform">',
      '<div class="row">',
      '<div class="left">',
      '<div class="col">',
      '<h1 class="icon icon-table">Edit Table Cell</h1>',
      '</div>',
      '</div>',
      '</div>',
      '</header>',
      '<div class="row active nice-padding struct-block object">',
      '<label class="hidden" for="table-block-editor">Table Cell Input</label>',
      '<input class="hidden" id="table-block-editor" maxlength="255" name="title" type="text" value="" class="data-draftail-input">',
      '</div><br>',
      '<div class="row active nice-padding m-t-10">',
      '<label class="hidden" for="table-block-save-btn">Save</label>',
      '<button id="table-block-save-btn" type="button" data-dismiss="modal" class="button">Save Button</button>',
      '</div>'
    ].join( '' );

    // Set body template.
    const MODAL_TEMPLATE = [
      '<div class="table-block-modal fade"',
      'tabindex="-1" role="dialog" aria-hidden="true">',
      '<div class="modal-dialog">',
      '<div class="modal-content">',
      '<label class="hidden" for="close-table-block-modal-btn">Close Modal Button</label>',
      '<button id="close-table-block-modal-btn" type="button" class="button close icon text-replace icon-cross"',
      'data-dismiss="modal" aria-hidden="true">×</button>',
      '<div class="modal-body"></div>',
      '</div>',
      '</div>'
    ].join( '' );

    modalDom = $( MODAL_TEMPLATE );
    modalBodyDom = modalDom.find( '.modal-body' );
    modalBodyDom.html( MODAL_BODY_TEMPLATE );
    bodyDom = $( 'body' );
    bodyDom.find( '.table-block-modal' ).remove();
    bodyDom.append( modalDom );
    modalDom.modal( 'show' );
    saveBtnDom = modalDom.find( '#table-block-save-btn' );
    saveBtnDom.on( 'click', function( event ) {
      modalDom.trigger( 'save-btn:clicked', event );
    } );

    return modalDom;
  }

  /*  createRichTextEditor

      Code copied from
      https://github.com/wagtail/wagtail/blob/master/wagtail/admin/
      static_src/wagtailadmin/js/hallo-bootstrap.js

      Modifications were made to add new form fields to the TableBlock in Wagtail admin and support the rich text editor within table cells.
      TODO: Refactor this code and submit PR to Wagtail repo. */
  function _createRichTextEditor( initialValue ) {
    const id = 'table-block-editor';
    const editor = $( '#' + id ).attr( 'value', JSON.stringify( initialValue ) );

    window.draftail.initEditor(
      '#' + id,
      {
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
        enableLineBreak: false,
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
      },
      document.currentScript
    );

    const html = editor[0];

    return html;
  }

  function insertRichTextDeleteControl( element ) {
    const link = $( '<a class="icon icon-cross text-replace delete-control">Delete</a>' );
    $( element ).addClass( 'rich-text-deletable' ).prepend( link );
    link.on( 'click', function() {
      const widget = $( element ).parent( '.richtext' ).data( 'IKS-hallo' );
      $( element ).fadeOut( function() {
        $( element ).remove();
        if ( widget && widget.options.editable ) {
          widget.element.trigger( 'change' );
        }
      } );
    } );
  }

  $( function() {
    $( '.richtext [contenteditable="false"]' ).each( function() {
      insertRichTextDeleteControl( this );
    } );
  } );

  win.initRichTextTable = initRichTextTable;

} )( window );

