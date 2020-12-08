import { ObtenerRespuestasBuscar } from '../../pages/obtener-respuestas/buscar';

const buscar = new ObtenerRespuestasBuscar();

describe( 'obtener-respuestas', () => {
  describe( 'Buscar', () => {
    it( 'should autocomplete results', () => {
      buscar.open();
      buscar.enter( 'divulgación de cierre' );
      buscar.autocomplete().should( 'be.visible' );
    } );

    it( 'should return results', () => {
      buscar.open();
      buscar.enter( 'divulgación de cierre' );
      buscar.search();
      buscar.resultsSection().should( 'be.visible' );
    } );

    it( 'should correct spelling', () => {
      buscar.open();
      buscar.enter( 'vehíclo' );
      buscar.search();
      buscar.resultsHeader().contains( 'results for “vehículo”' );
      buscar.resultsHeader().siblings( 'p' ).first().contains( 'Search instead for' );
    } );
  } );
} );
