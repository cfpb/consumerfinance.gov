
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

    function initAtomicTable(id, tableOptions) {
        var containerId = id + '-handsontable-container';
        var tableHeaderCheckboxId = id + '-handsontable-header';
        var colHeaderCheckboxId = id + '-handsontable-col-header';
        var isFullWidthCheckboxId = id + '-handsontable-full-width';
        var isTableStripedCheckboxId = id + '-handsontable-striped-rows';
        var isStackedOnMobileCheckboxId = id + '-handsontable-stack-on-mobile';
        var hiddenStreamInput = $('#' + id);
        var tableContainer = $('#' + containerId);
        var tableHeaderCheckbox = $('#' + tableHeaderCheckboxId);
        var colHeaderCheckbox = $('#' + colHeaderCheckboxId);
        var isFullWidthCheckbox = $('#' + isFullWidthCheckboxId);
        var isTableStripedCheckbox = $('#' + isTableStripedCheckboxId);
        var isStackedOnMobileCheckbox = $('#' + isStackedOnMobileCheckboxId);

        var hansonTable;
        var finalOptions = {};
        var persist;
        var cellEvent;
        var editor;
        var structureEvent;
        var dataForForm = null;
        var getWidth = function() {
            return $('.widget-table_input').closest('.sequence-member-inner').width();
        };
        var getHeight = function() {
            var tableParent = $('#' + id).parent();
            return tableParent.find('.htCore').height() + (tableParent.find('.input').height() * 2);
        };
        var height = getHeight();
        var resizeTargets = ['.input > .handsontable', '.wtHider', '.wtHolder'];
        var resizeHeight = function(height) {
            var currTable = $('#' + id);
            $.each(resizeTargets, function() {
                currTable.closest('.field-content').find(this).height(height);
            });
        };

        function resizeWidth(width) {
            $.each(resizeTargets, function() {
                $(this).width(width);
            });
            var parentDiv = $('.widget-table_input').parent();
            parentDiv.find('.field-content').width(width);
            parentDiv.find('.fieldname-table .field-content .field-content').width('80%');
        }

        try {
            dataForForm = $.parseJSON(hiddenStreamInput.val());
        } catch (e) {
            // do nothing
        }

        for (var key in tableOptions) {
            if (tableOptions.hasOwnProperty(key)) {
                finalOptions[key] = tableOptions[key];
            }
        }

        if (dataForForm !== null) {
            if (dataForForm.hasOwnProperty('data')) {
                // Overrides default value from tableOptions (if given) with value from database
                finalOptions.data = dataForForm.data;
            }

            if (dataForForm.hasOwnProperty('first_row_is_table_header')) {
                tableHeaderCheckbox.prop('checked', dataForForm.first_row_is_table_header);
            }
            if (dataForForm.hasOwnProperty('first_col_is_header')) {
                colHeaderCheckbox.prop('checked', dataForForm.first_col_is_header);
            }
            if (dataForForm.hasOwnProperty('is_full_width')) {
                isFullWidthCheckbox.prop('checked', dataForForm.is_full_width);
            }
            if (dataForForm.hasOwnProperty('is_striped')) {
                isTableStripedCheckbox.prop('checked', dataForForm.is_striped);
            }
            if (dataForForm.hasOwnProperty('is_stacked')) {
                isStackedOnMobileCheckbox.prop('checked', dataForForm.is_stacked);
            }
        }

        if (!tableOptions.hasOwnProperty('width') || !tableOptions.hasOwnProperty('height')) {
            // Size to parent .sequence-member-inner width if width is not given in tableOptions
            $(window).resize(function() {
                hansonTable.updateSettings({
                    width: getWidth(),
                    height: getHeight()
                });
                resizeWidth('100%');
            });
        }

        persist = function() {
            hiddenStreamInput.val(JSON.stringify({
                data: hansonTable.getData(),
                first_row_is_table_header: tableHeaderCheckbox.prop('checked'),
                first_col_is_header: colHeaderCheckbox.prop('checked'),
                is_full_width: isFullWidthCheckbox.prop('checked'),
                is_striped: isTableStripedCheckbox.prop('checked'),
                is_stacked: isStackedOnMobileCheckbox.prop('checked')
            }));
        };

        cellEvent = function(change, source) {
            if (source === 'loadData') {
                return; //don't save this change
            }

            persist();
        };

        structureEvent = function(index, amount) {
            resizeHeight(getHeight());
            persist();
        };

        tableHeaderCheckbox.change(function() {
            persist();
        });

        colHeaderCheckbox.change(function() {
            persist();
        });

        isFullWidthCheckbox.change(function(){
            persist();
        });

        isTableStripedCheckbox.change(function(){
            persist();
        });

        isStackedOnMobileCheckbox.change(function(){
            persist();
        });

        finalOptions.afterChange = cellEvent;
        finalOptions.afterCreateCol = structureEvent;
        finalOptions.afterCreateRow = structureEvent;
        finalOptions.afterRemoveCol = structureEvent;
        finalOptions.afterRemoveRow = structureEvent;
        finalOptions.contextMenu = [ 'row_above',
                                     'row_below',
                                     '---------',
                                     'col_left',
                                     'col_right',
                                     '---------',
                                     'remove_row',
                                     'remove_col',
                                     '---------',
                                     'undo', 'redo'];

        if( finalOptions ) {
            var RichTextEditor = Handsontable.editors.BaseEditor.prototype.extend();
            tableContainer.addClass( 'richtext' );

            RichTextEditor.prototype.beginEditing = function( event, tableCellIndex, tableCell ) {
                var initialCellValue = this.instance.getValue();
                var editorValue = initialCellValue;
                var cellProperties = this.cellProperties;
                var modalDom;
                var richTextEditor;

                this.instance.deselectCell();
                modalDom = _showModal();
                richTextEditor = _createRichTextEditor( initialCellValue );
                modalDom.on( 'save-btn:clicked', function() {
                    hansonTable.setDataAtCell(cellProperties.row, cellProperties.col, richTextEditor.html());
                    hansonTable.render();
                    $(window).resize();
                } );
            }

            finalOptions.editor = RichTextEditor;
        }

        hansonTable = new Handsontable(document.getElementById(containerId), finalOptions);
        hansonTable.render(); // Call to render removes 'null' literals from empty cells

        // Apply resize after document is finished loading (parent .sequence-member-inner width is set)
        if ('resize' in $(window)) {
            resizeHeight(getHeight());
            $(window).load(function() {
                $(window).resize();
            });
        }
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
    function _showModal( ) {
        var _modalDom;
        var _modalBodyDom;
        var _bodyDom = null;
        var _saveBtnDom;

        // Set header template.
        var MODAL_BODY_TEMPLATE = [ '<style>.hallotoolbar { z-index: 1000 }</style>',
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
                                        '<input id="table-block-editor" maxlength="255" name="title" type="text">',
                                    '</div></br>',
                                    '<div class="row active nice-padding m-t-10">',
                                        '<button id="table-block-save-btn" type="button" data-dismiss="modal" class="button" >',
                                            '<span class="icon"></span><em>Save</em>',
                                        '</button>',
                                    '</div>' ].join( '' );

        // Set body template.
        var MODAL_TEMPLATE = [ '<div id="table-block-modal" class="modal fade"',
                               'tabindex="-1" role="dialog" aria-hidden="true">',
                                    '<div class="modal-dialog">',
                                        '<div class="modal-content">',
                                            '<button type="button" class="button close icon text-replace icon-cross"',
                                            'data-dismiss="modal" aria-hidden="true">×</button>',
                                        '<div class="modal-body"></div>',
                                    '</div>',
                                '</div>' ].join( '' );

        _modalDom = $( MODAL_TEMPLATE );
        _modalBodyDom = _modalDom.find( '.modal-body' );
        _modalBodyDom.html( MODAL_BODY_TEMPLATE );
        _bodyDom = $( 'body' );
        _bodyDom.find( '> .modal' ).remove();
        _bodyDom.append( _modalDom );
        _modalDom.modal( 'show' );
        _saveBtnDom = _modalDom.find( '#table-block-save-btn' );

        _saveBtnDom.on( 'click', function( event ) {
            _modalDom.trigger( 'save-btn:clicked', event );
        } );

        return _modalDom;
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
        'use strict';

        var id = 'table-block-editor'
        var input = $('#' + id );
        var richText = $('<div class="richtext"></div>').html(initialValue);

        richText.insertBefore(input);
        input.hide();

        var removeStylingPending = false;
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
            var hallo = richText.data('IKS-hallo');

            if (hallo) {
                hallo.setModified();
            }
        }

        var closestObj = input.closest('.object');

        richText.hallo({
            toolbar: 'halloToolbarFixed',
            toolbarCssClass: (closestObj.hasClass('full')) ? 'full' : (closestObj.hasClass('stream-field')) ? 'stream-field' : '',
            plugins: halloPlugins,
            editable: true,
        }).bind('hallomodified', function(event, data) {
            input.val( data.content );
            if (!removeStylingPending) {
                setTimeout(removeStyling, 100);
                removeStylingPending = true;
            }
        }).bind('paste drop', function(event, data) {
            setTimeout(function() {
                removeStyling();
                setModified();
            }, 1);
        /* Animate the fields open when you click into them. */
        }).bind('halloactivated', function(event, data) {
            $(event.target).addClass('expanded', 200, function(e) {
                /* Hallo's toolbar will reposition itself on the scroll event.
                This is useful since animating the fields can cause it to be
                positioned badly initially. */
                $(window).trigger('scroll');
            });
        }).bind('hallodeactivated', function(event, data) {
            $(window).trigger('scroll');
        });

        window.setTimeout( function() {
            richText.focus();
        }, 500 );

        setupLinkTooltips(richText);

        return richText;
    }

    function setupLinkTooltips(elem) {
        elem.tooltip({
            animation: false,
            title: function() {
                return $(this).attr('href');
            },
            trigger: 'hover',
            placement: 'bottom',
            selector: 'a'
        });
    }

    function insertRichTextDeleteControl(elem) {
        var a = $('<a class="icon icon-cross text-replace delete-control">Delete</a>');
        $(elem).addClass('rich-text-deletable').prepend(a);
        a.click(function() {
            var widget = $(elem).parent('.richtext').data('IKS-hallo');
            $(elem).fadeOut(function() {
                $(elem).remove();
                if (widget != undefined && widget.options.editable) {
                    widget.element.trigger('change');
                }
            });
        });
    }

    $(function() {
        $('.richtext [contenteditable="false"]').each(function() {
            insertRichTextDeleteControl(this);
        });
    });

    win.initAtomicTable = initAtomicTable;

} ) ( window );

