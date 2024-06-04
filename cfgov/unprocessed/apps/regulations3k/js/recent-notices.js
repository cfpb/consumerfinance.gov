const NOTICES_URL = './recent-notices-json';
const CFPB_NOTICES =
  'https://www.federalregister.gov/agencies/consumer-financial-protection-bureau';

const processNotice = (notice) => {
  const a = document.createElement('a');
  const li = document.createElement('li');
  a.href = encodeURI(notice.html_url);
  a.textContent = notice.title;
  li.className = 'm-list__item';
  li.appendChild(a);
  return li;
};

const processNotices = (notices) => {
  const html = document.createDocumentFragment();
  const lastNotice = {
    html_url: CFPB_NOTICES,
    title: 'More Bureau notices',
  };
  notices.forEach((notice) => {
    html.appendChild(processNotice(notice));
  });
  html.appendChild(processNotice(lastNotice));
  return html;
};

const init = () => {
  const noticesContainer = document.querySelector('#regs3k-notices');
  fetch(NOTICES_URL)
    .then((response) => response.json())
    .then((notices) => {
      notices = notices.results;
      const html = processNotices(notices);
      noticesContainer.innerHTML = '';
      noticesContainer.appendChild(html);
    })
    .catch((err) => {
      // No need to handle the error, the default HTML is a graceful fallback.
      console.error(err);
    });
};

window.addEventListener('load', init);

export { processNotice, processNotices };
