
'use strict';

let EC = protractor.ExpectedConditions;

let buttons = {
  bold:          '.halloformat button[title="bold"]',
  H2:            '.halloheadings button[title="h2"]',
  H3:            '.halloheadings button[title="h3"]',
  H4:            '.halloheadings button[title="h4"]',
  H5:            '.halloheadings button[title="h5"]',
  italic:        '.halloformat button[title="italic"]',
  link:          '.hallowagtaillink button[title="Add/Edit Link"]',
  media:         '.hallowagtailembeds title["Images"]',
  ol:            '.hallolists button[title="OL"]',
  p:             '.halloheadings button[title="p"]',
  redo:          '.halloreundo button[title="Redo"]',
  hr:            '.hallohr button[title="Horizontal rule"]',
  undo:          '.halloreundo button[title="Undo"]',
  unlink:        '.hallowagtaillink button[title="Remove Link"]',
  ul:            '.hallolists button[title="UL"]',
  video:         '.hallowagtailembeds buttom[title="Embed"]'
};

let containerSelector = '.widget-hallo_rich_text_area';
let textAreaSelector = containerSelector + ' .richtext';
let container = element( by.css( containerSelector ) );
let textArea = element( by.css( textAreaSelector ) );

function clickButton( buttonName ) {
  let normalizedButtonName = buttonName
                             .replace( /\s/g, '' );
  let btn = element( by.css( buttons[normalizedButtonName] ) );

  return browser
         .wait( EC.elementToBeClickable( btn ), 500 )
         .then( btn.click );
}

function insertText( text ) {
  browser.wait( EC.elementToBeClickable( textArea ), 500 )

  return textArea.sendKeys( text );
}

function clearText( text ) {

  return textArea.clear();
}

function selectText( ) {
  function _selectText( className ) {
    let range = document.createRange();
    let element = document.body.querySelector( className ).firstChild;
    range.selectNode( element );
    let windowSelection = window.getSelection();
    windowSelection.removeAllRanges();
    windowSelection.addRange(range);

    return windowSelection;
  }

  return browser.executeScript( _selectText, textAreaSelector );
}

function getTextAreaValue() {

  return textArea.getAttribute( 'innerHTML' );
}

let richTextEditor = {
  buttons:          buttons,
  clickButton:      clickButton,
  getTextAreaValue: getTextAreaValue,
  insertText:       insertText,
  textArea:         textArea,
  clearText:        clearText,
  selectText:       selectText
};

module.exports = richTextEditor;
