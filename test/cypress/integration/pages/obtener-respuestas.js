import { ObtenerRespuestasBuscar } from '../../pages/obtener-respuestas/buscar';

const buscar = new ObtenerRespuestasBuscar();

describe( 'Obtener Respuestas', () => {
  beforeEach( () => {
    buscar.open();
  } );
  describe( 'Buscar', () => {
    it( 'should autocomplete results', () => {
      buscar.enter( 'divulgación de cierre' );
      buscar.autocomplete().should( 'be.visible' );
    } );

    it( 'should return results', () => {
      buscar.enter( 'divulgación de cierre' );
      buscar.search();
      buscar.resultsSection().should( 'be.visible' );
    } );

    it( 'should correct spelling', () => {
      buscar.enter( 'vehíclo' );
      buscar.search();
      buscar.resultsHeader()
        .should( 'contain', 'resultados para “vehículo”' );
      buscar.resultsHeader().siblings( 'p' ).first()
        .should( 'contain', 'Busca de vehíclo' );
    } );
  } );
} );
