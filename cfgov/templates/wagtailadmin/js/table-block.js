
'use strict';

/*
 *  TableBlock HansonTable bridge
 *
 *  Code copied from
 *  https://github.com/torchbox/wagtail/blob/master/wagtail/contrib/table_block/static/table_block/js/table.js
 *
 *  Modifications were made to add new form fields to the TableBlock in Wagtail admin.
 */
( function( win ) {

    function initRichTextTable( id, options ) {
        id = '#' + id;

        var utilities = {

            assign: function( target, source ) {
                target = target || {};

                for ( var key in source ) {
                    if (source.hasOwnProperty(key)) {
                        target[key] = source[key];
                    }
                }

                return target
            },

            DIMENSIONS: {
                WIDTH:  0,
                HEIGHT: 1
            },

            $colWidthSelect: {}
        };

        var HandsonTable = {

            initialize: function initialize( element, options ) {
                if ( 'Handsontable' in win === false ) {
                    return;
                }

                var onTableChange = $.proxy( this.onTableChange, this );
                var onCreateCol = $.proxy( this.onCreateCol, this );
                var onRemoveCol = $.proxy( this.onRemoveCol, this );

                options.afterChange = onTableChange;
                options.afterCreateCol = onCreateCol;
                options.afterCreateRow = onTableChange;
                options.afterRemoveCol = onRemoveCol;
                options.afterRemoveRow = onTableChange;
                options.contextMenu = [ 'row_above',
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
                options = this.modify( options );

                // Call to render removes 'null' literals from empty cells
                this.create( element, options ).render();

                return this;
            },

            create: function create( element, options ) {
                this.instance = new Handsontable( element , options || {} );

                return this.instance;
            },

            modify: function modify( options ) {
                var RichTextEditor = Handsontable.editors.BaseEditor.prototype.extend();

                RichTextEditor.prototype.beginEditing = function( event, tableCellIndex, tableCell ) {
                    var initialCellValue = this.instance.getValue();
                    var cellProperties = this.cellProperties;
                    var modalDom;
                    var richTextEditor;
                    var instance = this.instance;

                    instance.deselectCell();
                    modalDom = showModal();
                    richTextEditor = _createRichTextEditor( initialCellValue );
                    modalDom.on( 'save-btn:clicked', function() {
                        instance.setDataAtCell( cellProperties.row, cellProperties.col, richTextEditor.html() );
                        instance.render();
                        $( win ).resize();
                    } );
                }

                options.editor = RichTextEditor;

                return options;
            },

            onTableChange: function onTableChange( index, change ) {
                if ( change === 'loadData' ) {
                    return
                }

                this.$element.trigger( 'table:change', [this.instance.getData()] );

                return this;
            },

            onCreateCol: function onCreateCol( index, change ) {
              HandsonTableWagtailBridge.ui.$fixedWidthColInput
                .find( 'td' ).eq( index - 1 )
                .after( '<td>' + utilities.$colWidthSelect + '</td>' );

              this.$element.trigger( 'table:change', [this.instance.getData()] );

              return this;
            },

            onRemoveCol: function onRemoveCol( index, change ) {
              HandsonTableWagtailBridge.ui.$fixedWidthColInput
                .find( 'td' ).eq( index )
                .remove();

              this.$element.trigger( 'table:change', [this.instance.getData()] );

              return this;
            }
        };

        var HandsonTableWagtailBridge = {

            initialize: function initialize( id , options ) {
                var _this = this;
                var hiddenFieldData;

                utilities.$colWidthSelect = $( this.ui.$inputContainer + ' .column-width-input' ).prop( 'outerHTML' );

                this.options = utilities.assign( {} , options );
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
                var _this = this;
                var $window = $( win );

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
                    $window.load( function() {
                        $window.resize();
                    } );
                }

                // On click, toggle visibility of fixed width inputs
                $( id + '-handsontable-col-fixed' ).click( function() {
                  if ( $( this ).is( ':checked' ) ) {
                    _this.toggleInputTable( true );
                  } else {
                    _this.toggleInputTable( false );
                  }
                } );

                // On change of fixed width values, save data
                $( id + '-fixed-width-column-input' ).on( 'change', '.column-width-input', function() {
                  _this.saveDataToHiddenField( 'no data' );
                } )

            },

            ui: {
                $container:                 id + '-handsontable-container',
                $inputContainer:            id + '-handsontable-input-container',
                $hasColHeaderCheckbox:      id + '-handsontable-col-header',
                $hasRowHeaderCheckbox:      id + '-handsontable-header',
                $hiddenField:               id,
                $isFullWidthCheckbox:       id + '-handsontable-full-width',
                $isStackedOnMobileCheckbox: id + '-handsontable-stack-on-mobile',
                $isTableStripedCheckbox:    id + '-handsontable-striped-rows',
                $fixedWidthColsCheckbox:    id + '-handsontable-col-fixed',
                $fixedWidthColInput:        id + '-fixed-width-column-input',
                $widthWarning:             id + '-width_warning',
                $resizeTargets:             '.input > .handsontable, .wtHider, .wtHolder'
            },

            initializeForm: function initializeForm( hiddenFieldData ) {
                var ui = this.ui;
                var uiMap;
                var value;

                if ( hiddenFieldData !== null ) {
                    uiMap = { first_row_is_table_header:   ui.$hasRowHeaderCheckbox,
                              first_col_is_header:         ui.$hasColHeaderCheckbox,
                              is_full_width:               ui.$isFullWidthCheckbox,
                              is_striped:                  ui.$isTableStripedCheckbox,
                              is_stacked:                  ui.$isStackedOnMobileCheckbox,
                              fixed_col_widths:            ui.$fixedWidthColsCheckbox
                          };

                    Object.keys( uiMap ).forEach( function( key ) {
                        if ( value = hiddenFieldData[key] ) {
                            uiMap[key].prop( 'checked', value );
                        }
                    } );
                }

                // update fixed width input to match table
                var count = this.handsonTable.instance.countCols();
                var row = this.ui.$fixedWidthColInput.find( 'tr' );
                row.empty();
                for ( var x = 0; x < count; x++ ) {
                  row.append( '<td>' + utilities.$colWidthSelect + '</td>' );
                }

                if ( ui.$fixedWidthColsCheckbox.is( ':checked' ) ) {
                  this.toggleInputTable( true );
                  ui.$fixedWidthColInput.find( 'td' ).each( function( index, value) {
                    $( this ).find( 'select' ).val( hiddenFieldData.column_widths[index] );
                  } )
                  this.getColumnWidths();
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
              var colCount = this.ui.$fixedWidthColInput.find( 'tr td' ).length,
                  array = [],
                  totalWidth = 0;

              for ( var x = 0; x <  colCount; x++ ) {
                var i = x + 1;
                var widthClass = this.ui.$fixedWidthColInput.find( 'tr td:nth-child( ' + i + ') select option:selected' ).val()
                if ( widthClass !== '' ) {
                  totalWidth += Number( widthClass.substring(3, 5) );
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
                var tableParent = this.ui.$container.parent();

                return tableParent.find( '.htCore' ).height() +
                       ( tableParent.find( '.input' ).height() * 2 );
            },

            getHiddenFieldData: function getHiddenFieldData() {
                try {
                    return $.parseJSON( this.ui.$hiddenField.val() );
                } catch ( e ) {
                    // do nothing
                }
            },

            setCachedElements: function setCachedElements() {
                var key;
                var ui = $.extend( {}, this.ui );
                var $element = $( this.element );
                var element;

                for ( key in ui ) {
                  if ( ui.hasOwnProperty( key ) ) {
                    element = $element.find( ui[key] );
                    if ( element.length) {
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
                var ui = this.ui;

                if ( !data ) {
                    return;
                }

                ui.$hiddenField.val( JSON.stringify( {
                    data:                      this.handsonTable.instance.getData(),
                    column_widths:             this.getColumnWidths(),
                    first_row_is_table_header: ui.$hasRowHeaderCheckbox.prop( 'checked' ),
                    first_col_is_header:       ui.$hasColHeaderCheckbox.prop( 'checked' ),
                    is_full_width:             ui.$isFullWidthCheckbox.prop( 'checked' ),
                    is_striped:                ui.$isTableStripedCheckbox.prop( 'checked' ),
                    is_stacked:                ui.$isStackedOnMobileCheckbox.prop( 'checked' ),
                    fixed_col_widths:          ui.$fixedWidthColsCheckbox.prop( 'checked' )
                } ) );
            },

            resize: function resize( dimension, amount ) {
                if( dimension === utilities.DIMENSIONS.WIDTH ) {
                    $.each( this.ui.$resizeTargets, function() {
                        $( this ).width( amount );
                    } );
                    var parentDiv = $('.widget-table_input').parent();
                    parentDiv.find('.field-content').width( amount );
                    parentDiv.find('.fieldname-table .field-content .field-content').width('80%');

                } else if( dimension === utilities.DIMENSIONS.HEIGHT ) {
                    var _this = this;
                    $.each( this.ui.$resizeTargets, function() {
                        _this.ui.$container.closest('.field-content').find(this).height( amount );
                    } );
                }
            },

            onTableChange: function onTableChange( index ) {
                this.resize( utilities.DIMENSIONS.HEIGHT, this.getHeight() );
                this.saveDataToHiddenField();
            },

            toggleInputTable: function toggleInputTable( visible ) {
              if ( visible === true ) {
                this.ui.$fixedWidthColInput.show();
              } else {
                this.ui.$fixedWidthColInput.hide();
              }
            }
        };

        return HandsonTableWagtailBridge.initialize( id, options );
    }


    /*
     *  showModal
     *
     *  Code copied from
     *  https://github.com/torchbox/wagtail/blob/master/wagtail/wagtailadmin/
     *  static_src/wagtailadmin/js/hallo-bootstrap.js
     *
     *  Create a Wagtail modal using Javascript.
     */
    function showModal( ) {
        var modalDom;
        var modalBodyDom;
        var bodyDom = null;
        var saveBtnDom;

        // Set header template.
        var MODAL_BODY_TEMPLATE = [ '<header class="nice-padding hasform">',
                                        '<div class="row">',
                                            '<div class="left">',
                                                '<div class="col">',
                                                    '<h1 class="icon icon-table">Edit Table Cell</h1>',
                                                '</div>',
                                            '</div>',
                                        '</div>',
                                    '</header>',
                                    '<div class="row active nice-padding struct-block object">',
                                        '<input id="table-block-editor" maxlength="255" name="title" type="text">',
                                    '</div></br>',
                                    '<div class="row active nice-padding m-t-10">',
                                        '<button id="table-block-save-btn" type="button" data-dismiss="modal" class="button" >',
                                            '<span class="icon"></span><em>Save</em>',
                                        '</button>',
                                    '</div>' ].join( '' );

        // Set body template.
        var MODAL_TEMPLATE = [ '<div class="table-block-modal fade"',
                               'tabindex="-1" role="dialog" aria-hidden="true">',
                                    '<div class="modal-dialog">',
                                        '<div class="modal-content">',
                                            '<button type="button" class="button close icon text-replace icon-cross"',
                                            'data-dismiss="modal" aria-hidden="true">×</button>',
                                        '<div class="modal-body"></div>',
                                    '</div>',
                                '</div>' ].join( '' );

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

    /*
     *  createRichTextEditor
     *
     *  Code copied from
     *  https://github.com/torchbox/wagtail/blob/master/wagtail/wagtailadmin/
     *  static_src/wagtailadmin/js/hallo-bootstrap.js
     *
     *  Modifications were made to add new form fields to the TableBlock in Wagtail admin.
     *  TODO: Refactor this code and submit PR to Wagtail repo.
     */
    function _createRichTextEditor( initialValue ) {
        var id = 'table-block-editor'
        var input = $( '#' + id );
        var richText = $( '<div class="richtext"></div>' ).html( initialValue );
        var removeStylingPending = false;

        richText.insertBefore( input );
        input.hide();

        function removeStyling() {
            /* Strip the 'style' attribute from spans that have no other attributes.
            (we don't remove the span entirely as that messes with the cursor position,
            and spans will be removed anyway by our whitelisting)
            */
            $('span[style]', richText).filter(function() {
                return this.attributes.length === 1;
            }).removeAttr('style');
            removeStylingPending = false;
        }

        /* Workaround for faulty change-detection in hallo */
        function setModified() {
            var hallo = richText.data( 'IKS-hallo' );
            if ( hallo ) {
                hallo.setModified();
            }
        }

        var closestObj = input.closest( '.object' );


        richText.hallo({
            toolbar: 'halloToolbarFixed',
            toolbarCssClass: ( closestObj.hasClass( 'full' ) ) ? 'full' : (closestObj.hasClass( 'stream-field' )) ? 'stream-field' : '',
            plugins: halloPlugins,
            editable: true,
        } ).bind( 'hallomodified', function( event, data ) {
            input.val( data.content );
            if ( !removeStylingPending ) {
                setTimeout( removeStyling, 100 );
                removeStylingPending = true;
            }
        } ).bind( 'paste drop', function( event, data ) {
            setTimeout(function() {
                removeStyling();
                setModified();
            }, 1);
        /* Animate the fields open when you click into them. */
        } ).bind( 'halloactivated', function( event, data ) {
            $( event.target ).addClass( 'expanded', 200, function(e) {
                /* Hallo's toolbar will reposition itself on the scroll event.
                This is useful since animating the fields can cause it to be
                positioned badly initially. */
                $( window ).trigger( 'scroll' );
            } );
        } ).bind( 'hallodeactivated', function( event, data ) {
            $( window ).trigger( 'scroll' );
        } );

        window.setTimeout( function() {
            richText.focus();
        }, 500 );

        setupLinkTooltips( richText );

        return richText;
    }

    function setupLinkTooltips( element ) {
        element.tooltip( {
            animation: false,
            title: function() {
                return $( this ).attr( 'href' );
            },
            trigger: 'hover',
            placement: 'bottom',
            selector: 'a'
        } );
    }

    function insertRichTextDeleteControl( element ) {
        var link = $( '<a class="icon icon-cross text-replace delete-control">Delete</a>' );
        $ ( element ).addClass( 'rich-text-deletable' ).prepend( link );
        link.click( function() {
            var widget = $( element ).parent( '.richtext' ).data( 'IKS-hallo' );
            $( element ).fadeOut( function() {
                $( element ).remove();
                if ( widget != undefined && widget.options.editable ) {
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

} ) ( window );
