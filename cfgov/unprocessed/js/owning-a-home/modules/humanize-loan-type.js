'use strict';

module.exports = function( loanType ) {
  loanType = loanType === 'conf' ? 'conventional' : loanType.toUpperCase();
  return loanType;
};
