import { formatTimestamp } from '../../../../../cfgov/unprocessed/js/modules/util/strings.js';

describe('Strings formatTimestamp()', () => {
  it('should convert 23 seconds into 00:23 timestamp', () => {
    const seconds = 23;
    expect(formatTimestamp(seconds)).toBe('00:23');
  });

  it('should convert 160 seconds into 02:40 timestamp', () => {
    const seconds = 160;
    expect(formatTimestamp(seconds)).toBe('02:40');
  });

  it('should convert 16001 seconds into 04:26:41 timestamp', () => {
    const seconds = 16001;
    expect(formatTimestamp(seconds)).toBe('04:26:41');
  });
});
