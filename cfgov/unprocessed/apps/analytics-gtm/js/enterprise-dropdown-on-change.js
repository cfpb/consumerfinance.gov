function addListener( element, type, callback ) {
  if ( element.addEventListener ) element.addEventListener( type, callback );
  else if ( element.attachEvent ) element.attachEvent( 'on' + type, callback );
}

const mySelects = document.getElementsByTagName( 'select' );
let selectIndex = mySelects.length;
while ( --selectIndex >= 0 ) {
  addListener( mySelects[selectIndex], 'change', onChangeHandler );
}

function onChangeHandler() {
  const customEvent = {
    'event': 'gtm.change',
    'gtm.element': this,
    'gtm.elementClasses': this.className,
    'gtm.elementId': this.id,
    'gtm.elementTarget': this.target
  };
  window.dataLayer.push( customEvent );
}
