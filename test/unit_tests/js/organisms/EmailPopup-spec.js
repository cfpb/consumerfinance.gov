import EmailPopup from '../../../../cfgov/unprocessed/js/organisms/EmailPopup.js';
import HTML_SNIPPET from '../../mocks/emailPopupSnippet.js';

let emailPopup;

describe('EmailPopup', () => {
  beforeEach(() => {
    document.body.innerHTML = HTML_SNIPPET;
    emailPopup = new EmailPopup(document.querySelector('.o-email-popup'));
    emailPopup.init();
  });

  describe('init()', () => {
    it('should return the instance when initialized', () => {
      expect(emailPopup.init()).toBeInstanceOf(EmailPopup);
    });
  });

  describe('getDom()', () => {
    it('should return the base element', () => {
      const baseElement = document.querySelector('.o-email-popup');
      expect(baseElement).toStrictEqual(emailPopup.getDom());
    });
  });

  describe('hidePopup()', () => {
    it('should remove CSS class that sets organism as hidden', () => {
      emailPopup.hidePopup();
      const baseElement = emailPopup.getDom();
      const containsClass = baseElement.classList.contains(
        'o-email-popup__visible'
      );
      expect(containsClass).toBe(false);
    });
  });

  describe('showPopup()', () => {
    it(
      'should not add CSS class that sets organism as visible ' +
        'if date is not set in local storage',
      () => {
        const isShown = emailPopup.showPopup();
        const baseElement = emailPopup.getDom();
        const containsClass = baseElement.classList.contains(
          'o-email-popup__visible'
        );
        expect(containsClass).toBe(false);
        expect(isShown).toBe(false);
      }
    );

    it(
      'should add CSS class that sets organism as visible ' +
        'if date is set in local storage',
      () => {
        const days = 1;
        const date = new Date();
        const last = new Date(date.getTime() - days * 24 * 60 * 60 * 1000);
        localStorage.setItem('testPopupPopupShowNext', last);
        const isShown = emailPopup.showPopup();
        const baseElement = emailPopup.getDom();
        const containsClass = baseElement.classList.contains(
          'o-email-popup__visible'
        );
        expect(containsClass).toBe(true);
        expect(isShown).toBe(true);
      }
    );
  });
});
