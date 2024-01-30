import FormSubmit from '../../../../cfgov/unprocessed/js/organisms/FormSubmit.js';
import HTML_SNIPPET from '../../mocks/emailSignupSnippet.js';

const BASE_CLASS = 'o-email-signup';

describe('FormSubmit', () => {
  let signupForm;
  let formSubmit;
  let thisFormSubmit;

  beforeEach(() => {
    document.body.innerHTML = HTML_SNIPPET;
    signupForm = document.querySelector(`.${BASE_CLASS}`);
    formSubmit = new FormSubmit(signupForm, BASE_CLASS, {});
    thisFormSubmit = formSubmit.init();
  });

  describe('init()', () => {
    it('should return the FormSubmit instance when initialized', () => {
      expect(typeof thisFormSubmit).toStrictEqual('object');
      expect(signupForm.dataset.jsHook).toStrictEqual('state_atomic_init');
      expect(formSubmit.init()).toBeInstanceOf(FormSubmit);
    });
  });

  describe('getMessage()', () => {
    it('should return the correct messages based on the state', () => {
      // Return generic error message if wrong state was passed.
      expect(thisFormSubmit.getMessage('TYPO', 'en')).toEqual('Error.');

      // Return error message.
      expect(thisFormSubmit.getMessage('ERROR', 'es')).toEqual(
        'Había un error en su presentación. Por favor, inténtelo más tarde.',
      );

      // Return success message.
      expect(thisFormSubmit.getMessage('SUCCESS', 'en')).toEqual(
        'Your submission was successfully received.',
      );
      expect(thisFormSubmit.getMessage('SUCCESS', 'ar')).toEqual(
        'تم استلام طلبك  بنجاح.',
      );
      expect(thisFormSubmit.getMessage('SUCCESS', 'zh-Hant')).toEqual(
        '您提交的資料已被成功接收。',
      );

      // Return english message by default if the language isn't found.
      expect(thisFormSubmit.getMessage('SUCCESS', 'de')).toEqual(
        'Your submission was successfully received.',
      );
    });
  });
});
