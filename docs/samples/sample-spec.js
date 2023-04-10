import sample from '../../../../cfgov/unprocessed/js/modules/sample.js';

describe('sample', () => {
  it.skip('should return a string with expected value', () => {
    const sampleString = 'Shredder';
    expect(sample.init()).toBe(sampleString);
  });
});
