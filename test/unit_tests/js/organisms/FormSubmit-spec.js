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
});
