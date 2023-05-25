import { email as validateEmail } from '../../../../../cfgov/unprocessed/js/modules/util/validators.js';

let testField;
let returnedObject;
const ERROR_MSG = 'You have entered an invalid email address.';

describe('Validators', () => {
  describe('email field', () => {
    beforeEach(() => {
      testField = document.createElement('input');
    });

    it('should return an empty object for a valid email', () => {
      testField.value = 'test@demo.com';
      returnedObject = validateEmail(testField);

      expect(returnedObject).toStrictEqual({});
    });

    it('should return an error object for a missing domain', () => {
      testField.value = 'test';
      returnedObject = validateEmail(testField);

      expect(returnedObject['email']).toBe(false);
      expect(returnedObject['msg']).toBe(ERROR_MSG);
    });

    it('should return an error object for a missing user', () => {
      testField.value = '@demo.com';
      returnedObject = validateEmail(testField);

      expect(returnedObject['email']).toBe(false);
      expect(returnedObject['msg']).toBe(ERROR_MSG);
    });
  });
});
