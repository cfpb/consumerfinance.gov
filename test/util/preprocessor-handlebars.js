// Preprocess Handlebars templates for tests.
module.exports = {
  process( src ) {
    return `
    const Handlebars = require( 'handlebars' );
    module.exports = Handlebars.compile( \`${ src }\` );
    `;
  }
};
