import { fetch } from './regs3k-utils';
import { queryOne as find } from '@cfpb/cfpb-atomic-component/src/utilities/dom-traverse.js';

const NOTICES_URL = './recent-notices-json';
const CFPB_NOTICES = 'https://www.federalregister.gov/agencies/consumer-financial-protection-bureau';

const processNotice = notice => {
  const a = document.createElement( 'a' );
  const li = document.createElement( 'li' );
  a.href = encodeURI( notice.html_url );
  a.textContent = notice.title;
  li.className = 'm-list_link';
  li.appendChild( a );
  return li;
};

const processNotices = notices => {
  const html = document.createDocumentFragment();
  const lastNotice = {
    html_url: CFPB_NOTICES,
    title: 'More Bureau notices'
  };
  notices.forEach( notice => {
    html.appendChild( processNotice( notice ) );
  } );
  html.appendChild( processNotice( lastNotice ) );
  return html;
};

const init = () => {
  const noticesContainer = find( '#regs3k-notices' );
  fetch( NOTICES_URL, ( err, notices ) => {
    if ( err !== null ) {
      // No need to handle the error, the default HTML is a graceful fallback.
      return console.error( err );
    }
    notices = JSON.parse( notices ).results;
    const html = processNotices( notices );
    noticesContainer.innerHTML = '';
    return noticesContainer.appendChild( html );
  } );
};

window.addEventListener( 'load', init );

export {
  processNotice,
  processNotices
};
