const simpleTableRowLinks = require(
  '../../../../cfgov/unprocessed/js/modules/o-table-row-links'
);

import { simulateEvent } from '../../../util/simulate-event';

let tableDom;
let linkDom;
let linkRowCellDom;
let nonLinkRowCellDom;
let locationSpy;

const HTML_SNIPPET = `
  <table class="o-table__row-links">
      <tbody>
          <tr>
              <th>cell1</th>
              <th class="nonLinkRowCell">cell2</th>
              <th>cell3</th>
              <th>cell4</th>
          </tr>
          <tr>
              <td><a href="https://www.example.com">linkCell5</a></td>
              <td class="linkRowCell">cell6</td>
              <td>cell7</td>
              <td>cell8</td>
          </tr>
      </tbody>
  </table>
`;

describe( 'o-table-row-links', () => {
  beforeEach( () => {
    window.location.assign = jest.fn();
    locationSpy = jest.spyOn( window.location, 'assign' );

    document.body.innerHTML = HTML_SNIPPET;
    tableDom = document.querySelector( '.o-table__row-links' );
    linkDom = tableDom.querySelector( 'a' );
    linkRowCellDom = tableDom.querySelector( '.linkRowCell' );
    nonLinkRowCellDom = tableDom.querySelector( '.nonLinkRowCell' );

    simpleTableRowLinks.init();
  } );

  it( 'should navigate to new location when link row cell clicked', () => {
    simulateEvent( 'click', linkRowCellDom );
    expect( locationSpy ).toBeCalledWith( 'https://www.example.com' );
  } );

  it( 'should not set window location when link is clicked', () => {
    simulateEvent( 'click', linkDom );
    expect( locationSpy ).toHaveBeenCalledTimes( 0 );
  } );

  it( 'should not navigate to new location when non link row cell clicked',
    () => {
      simulateEvent( 'click', nonLinkRowCellDom );
      expect( locationSpy ).toHaveBeenCalledTimes( 0 );
    }
  );
} );
