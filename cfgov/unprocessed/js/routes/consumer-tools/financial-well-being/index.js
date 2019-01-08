import * as fwbQuestions from '../../../../apps/financial-well-being/js/fwb-questions';

/* TODO: This eventlistener may not be necessary and should probably be removed
after it fires. */
window.addEventListener( 'load', function() {
  fwbQuestions.init();
} );
