const richTextEditor = require(
  '../../shared_objects/wagtail-admin-rich-text-editor.js'
);
const linkChooser = require(
  '../../shared_objects/wagtail-admin-link-chooser.js'
);
const { defineSupportCode } = require( 'cucumber' );
const { expect } = require( 'chai' );

defineSupportCode( function( { Then, When, After, setDefaultTimeout } ) {

  setDefaultTimeout( 10800 );

  After( function() {

    /* browser.manage().logs().get( 'browser' )
       .then( function( browserLog ) {
       console.log( browserLog );
       } ); */

  } );

  When( /I click the (.*) button in the rich text editor/,
    function( buttonName ) {

      return richTextEditor.clickButton( buttonName );
    }
  );

  When( /I insert (.*) into the rich text editor/, function( text ) {

    return richTextEditor.insertText( text );
  } );

  When( /I select the text in the rich text editor/, function() {

    return richTextEditor.selectText();
  } );

  When( /I clear the rich text editor/, function() {


    return richTextEditor.clearText();
  } );

  Then( /(.*) should be wrapped in a (.*) tag/, function( text, tag ) {
    let tagText = `<${ tag }>${ text }</${ tag }>`;

    if ( tag === 'ol' || tag === 'ul' ) {
      tagText = `<${ tag }><li>${ text }<br></li></${ tag }>`;
    }

    return richTextEditor.getTextAreaValue().then( function( textAreaValue ) {

      expect( textAreaValue ).to.contain( tagText );
    } );
  } );

  Then( /the rich text editor should contain (?:a\s)?(.*?)(?:\s?element)?/,
    function( content ) {
      if ( content === 'hr' ) {
        content = '<hr>';
      }

      return richTextEditor.getTextAreaValue().then( function( textAreaValue ) {
        expect( textAreaValue ).to.contain( content );
      } );
    }
  );

  Then( /the rich text editor should only contain (.*)/, function( content ) {

    return richTextEditor.getTextAreaValue().then( function( textAreaValue ) {
      const tagText = `<p>${ content }</p>`;

      expect( textAreaValue ).to.equal( tagText );
    } );
  } );

  Then( /the inserted link should have the correct format/, function() {

    return richTextEditor.getTextAreaValue().then( function( textAreaValue ) {

      expect( textAreaValue ).to.contain( linkChooser.selectedLink.HTML );
    } );
  } );

} );
