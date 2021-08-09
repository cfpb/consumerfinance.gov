import { stateToHTML } from 'draft-js-export-html';

// https://handsontable.com/docs/7.2.2/tutorial-cell-editor.html
(function(Handsontable){
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
  }

  RichTextEditor.prototype.init = function() {
    Handsontable.editors.TextEditor.prototype.init.call(this);
    this.EDITOR = null;
    this.TEXTAREA = document.createElement('input');
    this.TEXTAREA.id = 'rich-text-table-cell-editor';
    this.TEXTAREA.style.visibility = 'hidden';
    this.textareaStyle = this.TEXTAREA.style;
    Handsontable.dom.empty(this.TEXTAREA_PARENT);
    this.TEXTAREA_PARENT.appendChild(this.TEXTAREA);
    this.TEXTAREA_PARENT.style.backgroundColor = 'white';
  }

  RichTextEditor.prototype.getValue = function() {
    console.log("get value");
    const options = {};
    const editorValue = this.TEXTAREA.value;
    const raw = JSON.parse(editorValue);
    const state = window.DraftJS.convertFromRaw( raw );
    return stateToHTML(state, options);
  }

  RichTextEditor.prototype.setValue = function(value) {
    console.log("set value", value);
    let contentState;
    const blocksFromHTML = value ? window.DraftJS.convertFromHTML(value) : null;
    if (blocksFromHTML && blocksFromHTML.contentBlocks) {
      contentState = window.DraftJS.ContentState.createFromBlockArray(blocksFromHTML.contentBlocks, blocksFromHTML.entityMap);
    } else {
      contentState = window.DraftJS.ContentState.createFromText('');
    }
    const cellValue = window.DraftJS.convertToRaw(contentState);
    this.TEXTAREA.value = JSON.stringify(cellValue);
    console.log(cellValue);
  }

  RichTextEditor.prototype.open = function() {
    console.log("open", this.TEXTAREA);
    // Initialize Draftail
    window.draftail.initEditor(
      '#' + this.TEXTAREA.id,
      draftail_options,
      document.currentScript
    );
    Handsontable.editors.TextEditor.prototype.open.call(this);
  }

  RichTextEditor.prototype.close = function() {
    Handsontable.editors.TextEditor.prototype.close.call(this);
    // Remove Draftail for this cell
    this.TEXTAREA_PARENT.querySelector('.Draftail-Editor__wrapper').remove();
  }

  // Register the rich text editor
  Handsontable.editors.RichTextEditor = RichTextEditor;
  Handsontable.editors.registerEditor('RichTextEditor', RichTextEditor);
})(Handsontable);
