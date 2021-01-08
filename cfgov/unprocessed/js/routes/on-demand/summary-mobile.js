import SummaryMobile from '../../organisms/SummaryMobile.js';

const summaryMobileDoms = document.querySelectorAll( `.${ SummaryMobile.BASE_CLASS }` );
let summaryMobile;
for ( let i = 0, len = summaryMobileDoms.length; i < len; i++ ) {
  summaryMobile = new SummaryMobile( summaryMobileDoms[i] );
  summaryMobile.init();
}
