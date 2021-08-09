// https://handsontable.com/docs/7.2.2/tutorial-cell-editor.html
(function(Handsontable){
  var RichTextEditor = Handsontable.editors.TextEditor.prototype.extend();

  RichTextEditor.prototype.createElements = function() {
    Handsontable.editors.TextEditor.prototype.createElements.call(this)

    this.TEXTAREA = document.createElement('input');
    this.TEXTAREA.setAttribute('placeholder', 'Custom placeholder');
    this.TEXTAREA.className = 'handsontableInput';
    this.textareaStyle = this.TEXTAREA.style;
    Handsontable.dom.empty(this.TEXTAREA_PARENT);
    this.TEXTAREA_PARENT.appendChild(this.TEXTAREA);
  }

  Handsontable.editors.RichTextEditor = RichTextEditor;

  Handsontable.editors.registerEditor('RichTextEditor', RichTextEditor);
})(Handsontable);
