import {
  getNewHash,
  isOldHash,
} from '../../../../../cfgov/unprocessed/apps/regulations3k/js/regs3k-utils.js';

describe('The Regs3K search utils', () => {
  describe('Hash utils', () => {
    it('should convert a hash', () => {
      expect(getNewHash('1010-Interp-1')).toEqual('Interp-1');
      expect(getNewHash('#1010-Interp-1')).toEqual('Interp-1');

      expect(getNewHash('1011-4-a')).toEqual('a');
      expect(getNewHash('#1011-4-a')).toEqual('a');

      expect(getNewHash('1003-2-f-Interp-3')).toEqual('2-f-Interp-3');
      expect(getNewHash('#1003-2-f-Interp-3')).toEqual('2-f-Interp-3');

      expect(getNewHash('1003-4-a-9-ii-C')).toEqual('a-9-ii-C');
      expect(getNewHash('#1003-4-a-9-ii-C')).toEqual('a-9-ii-C');
    });

    it('should check if a hash needs to be converted', () => {
      expect(isOldHash('1010-Interp-1')).toBeTrue;
      expect(isOldHash('#1010-Interp-1')).toBeTrue;

      expect(isOldHash('101-Interp-1')).toBeFalse;
      expect(isOldHash('#101-Interp-1')).toBeFalse;

      expect(isOldHash('1003-2-f-Interp-3')).toBeTrue;
      expect(isOldHash('#1003-2-f-Interp-3')).toBeTrue;

      expect(isOldHash('003-2-f-Interp-3')).toBeFalse;
      expect(isOldHash('#003-2-f-Interp-3')).toBeFalse;

      expect(isOldHash('bloop')).toBeFalse;
      expect(isOldHash('#bloop')).toBeFalse;

      expect(isOldHash('asdf-2-f-Interp-3')).toBeFalse;
      expect(isOldHash('#asdf-2-f-Interp-3')).toBeFalse;
    });
  });
});
