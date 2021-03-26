import tableRow from '../templates/table-row';

const TBODY_SELECTOR = 'tbody';

function buildTableBody() {
  const table = document.createElement( 'table' );
  const body = document.createElement( 'tbody' );

  table.appendChild( body );

  return body;
}

function populateTableRows( contents ) {
  const fragment = document.createDocumentFragment();
  const body = buildTableBody();

  const rows = contents.reduce( ( rows, rowContent ) => `${ rows }${ tableRow( rowContent ) }`, '' );

  body.innerHTML = rows;

  const rowEls = Array.prototype.slice.call( body.querySelectorAll( 'tr' ) );

  rowEls.forEach( rowEl => fragment.appendChild( rowEl ) );

  return fragment;
}

function printTable( element ) {
  const _dom = element;

  return {
    render( content ) {
      const elementToUpdate = _dom.querySelector( TBODY_SELECTOR );
      const nextHTML = populateTableRows( content );

      elementToUpdate.innerHTML = '';
      elementToUpdate.appendChild( nextHTML );
    }
  };
}

export default printTable;
