import { ObtenerRespuestasBuscar } from './obtener-respuestas-helpers';

const buscar = new AskCfpbSearch();

describe( 'Obtener Respuestas', () => {
  beforeEach( () => {
    buscar.open( 'es' );
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
      buscar.resultsHeader().should( 'contain', 'resultados para “vehículo”' );
      buscar.resultsHeader().siblings( 'p' ).first().should( 'contain', 'Busca de vehíclo' );
    } );

    it( 'should limit queries to a maximum length', () => {
      buscar.enter( buscar.longTerm() );
      buscar.input().should( 'contain.class', 'a-text-input__error' )
        .and( 'have.attr', 'maxlength' );
      buscar.maxLengthErrorMessage().should( 'be.visible' );
      buscar.submitButton().should( 'be.disabled' );
    } );
  } );
} );
