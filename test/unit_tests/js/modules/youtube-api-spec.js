import youTubeAPI from '../../../../cfgov/unprocessed/js/modules/youtube-api.js';

describe( 'youtube-api', () => {

  describe( '.fetchImageURL()', () => {
    it( 'should return an image URL with the video ID included', () => {
      const testID = 'thisTestID';
      expect( youTubeAPI.fetchImageURL( testID ) )
        .toBe( 'https://img.youtube.com/vi/thisTestID/maxresdefault.jpg' );
    } );

    it( 'should throw an error when video ID is not supplied', () => {
      expect( () => { youTubeAPI.fetchImageURL(); } )
        .toThrow( 'No Video ID provided!' );
    } );
  } );

  describe( '.instantiatePlayer()', () => {
    it( 'should throw an error when YouTube IFrame API is not loaded', () => {
      expect( () => { youTubeAPI.instantiatePlayer(); } )
        .toThrow( 'YouTube IFrame API is not loaded!' );
    } );
  } );

} );
