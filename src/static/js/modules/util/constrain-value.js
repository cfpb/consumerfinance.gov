'use strict';

function constrainValue( min, max, duration ) {
  if ( duration > max ) {
    return max;
  } else if ( duration < min ) {
    return min;
  }

  return duration;
}

module.exports = constrainValue;
