const green50 = '#bae0a2';
const green20 = '#e2efd8';
const gray80 = '#75787b';
const gray5 = '#f7f8f9';
const pacific20 = '#d6e8fa';
const pacific50 = '#96c4ed';

/**
 * Returns color given a data value.
 * @param   {number} value A numerical data value.
 * @returns {string}       A color hex string.
 */
function getColorByValue( value ) {

  if ( value < -15 ) {
    return pacific50;
  }
  if ( value < -5 ) {
    return pacific20;
  }
  if ( value < 6 ) {
    return gray5;
  }
  if ( value < 16 ) {
    return green20;
  }
  return green50;
}

export default {
  getColorByValue: getColorByValue,
  green50: green50,
  green20: green20,
  gray80: gray80,
  gray5: gray5,
  pacific20: pacific20,
  pacific50: pacific50
};
