const customEvent = require('customevent');

class ProgressBar {
  constructor( totalNum, numDone ) {
    this.totalNum = totalNum;
    this.numDone = numDone;

    const event = new customEvent( ProgressBar.UPDATE_EVT, {
      detail: { progressBar: this }
    } );
    document.dispatchEvent( event );
  }

  getPercentage() {
    return Math.round( 100 * this.numDone / this.totalNum );
  }

  update( numDone ) {
    this.numDone = numDone;

    const event = new customEvent( ProgressBar.UPDATE_EVT, {
      detail: { progressBar: this }
    } );
    document.dispatchEvent( event );
  }
}

ProgressBar.UPDATE_EVT = 'ProgressBar:update';

module.exports = ProgressBar;
