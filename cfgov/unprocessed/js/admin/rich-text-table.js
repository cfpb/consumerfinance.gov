import { stateToHTML } from 'draft-js-export-html';

// https://handsontable.com/docs/7.2.2/tutorial-cell-editor.html
( function( Handsontable ) {
  console.log( 'INIT 2' );
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
  };

  RichTextEditor.prototype.close = function() {
    Handsontable.editors.TextEditor.prototype.close.call( this );
    // Remove the Draftail editor for this cell
    this.TEXTAREA_PARENT.querySelector( '.Draftail-Editor__wrapper' ).remove();
  };

  // Register the rich text editor
  Handsontable.editors.RichTextEditor = RichTextEditor;
  Handsontable.editors.registerEditor( 'RichTextEditor', RichTextEditor );
} )( window.Handsontable );
