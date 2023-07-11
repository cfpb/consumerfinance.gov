import addEmailPopup from '../../../../../cfgov/unprocessed/js/modules/util/add-email-popup.js';
import HTML_SNIPPET from '../../../mocks/emailPopupSnippet.js';

describe('add-email-popup', () => {
  beforeEach(() => {
    document.body.innerHTML = HTML_SNIPPET;
  });

  it('should hide the email popup initially', () => {
    addEmailPopup.init();
    const emailPopupDom = document.querySelector('.o-email-popup');
    expect(emailPopupDom.classList.contains('o-email-popup__visible')).toBe(
      false,
    );
  });
});
