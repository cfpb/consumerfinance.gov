import {
  convertStringToNumber,
  commaSeparate,
  formatUSD,
} from '../../../../../cfgov/unprocessed/js/modules/util/format.js';

describe('convertStringToNumber', () => {
  it('Parse number strings with non-numeric characters', () => {
    expect(convertStringToNumber('9a99')).toBe(999);
    expect(convertStringToNumber('u123456')).toBe(123456);
    expect(convertStringToNumber('01234')).toBe(1234);
    expect(convertStringToNumber('$1,234,567')).toBe(1234567);
    expect(convertStringToNumber('Ilikethenumber5')).toBe(5);
    expect(
      convertStringToNumber('function somefunction() { do badstuff; }'),
    ).toBe(0);
  });

  it('Parse the first period as a decimal point', () => {
    expect(convertStringToNumber('4.22')).toBe(4.22);
    expect(convertStringToNumber('I.like.the.number.5')).toBe(0.5);
    expect(convertStringToNumber('1.2.3.4.5.6.7')).toBe(1.234567);
  });

  it('Handle things that are not strings', () => {
    expect(convertStringToNumber(1234)).toBe(1234);
    expect(convertStringToNumber(undefined)).toBe(0);
  });

  it('Strip dollar sign', () => {
    expect(convertStringToNumber('$0.00')).toBe(0);
    expect(convertStringToNumber('$123')).toBe(123);
    expect(convertStringToNumber('$123.4')).toBe(123.4);
    expect(convertStringToNumber('$123.45')).toBe(123.45);
    expect(convertStringToNumber('$123.456')).toBe(123.456);
  });

  it('Deal with extraneous characters', () => {
    expect(convertStringToNumber('$%123')).toBe(123);
    expect(convertStringToNumber('123.45.67')).toBe(123.4567);
    expect(convertStringToNumber('79aaasdfa69s89')).toBe(796989);
  });

  it('Ignore non-parseable strings', () => {
    const obj = { foo: 'bar' };
    const func = function (a) {
      return a;
    };

    expect(convertStringToNumber('blah')).toBe(0);
    expect(convertStringToNumber(obj)).toBe(0);
    expect(convertStringToNumber(func)).toBe(0);
    expect(convertStringToNumber(Date)).toBe(0);
  });
});

describe('commaSeparate', () => {
  it('Comma separate a numeric string', () => {
    expect(commaSeparate('1234567')).toBe('1,234,567');
    expect(commaSeparate('1234')).toBe('1,234');
    expect(commaSeparate('5')).toBe('5');
    expect(commaSeparate('199')).toBe('199');
  });

  it('Handle numeric strings with >3 decimal places', () => {
    expect(commaSeparate('9.1234')).toBe('9.1234');
    expect(commaSeparate('12345678.999999')).toBe('12,345,678.999999');
  });
});

describe('formatUSD', () => {
  it('Format numbers w/o decimal places', () => {
    expect(formatUSD({ amount: 1, decimalPlaces: 0 })).toBe('$1');
    expect(formatUSD({ amount: 1.25, decimalPlaces: 0 })).toBe('$1');
    expect(formatUSD({ amount: 1.258, decimalPlaces: 0 })).toBe('$1');
    expect(formatUSD({ amount: 1.25889349857, decimalPlaces: 0 })).toBe('$1');
    expect(formatUSD({ amount: 798127394873, decimalPlaces: 0 })).toBe(
      '$798,127,394,873',
    );
    expect(formatUSD({ amount: 0o00423, decimalPlaces: 0 })).toBe('$275');
  });

  it('Format numbers w/ one decimal places', () => {
    expect(formatUSD({ amount: 1, decimalPlaces: 1 })).toBe('$1.0');
    expect(formatUSD({ amount: 1.25, decimalPlaces: 1 })).toBe('$1.3');
    expect(formatUSD({ amount: 1.258, decimalPlaces: 1 })).toBe('$1.3');
    expect(formatUSD({ amount: 1.25889349857, decimalPlaces: 1 })).toBe('$1.3');
    expect(formatUSD({ amount: 798127394873, decimalPlaces: 1 })).toBe(
      '$798,127,394,873.0',
    );
    expect(formatUSD({ amount: 0o00423, decimalPlaces: 1 })).toBe('$275.0');
  });

  it('Format numbers w/ two decimal places', () => {
    expect(formatUSD({ amount: 1 })).toBe('$1.00');
    expect(formatUSD({ amount: 1.25 })).toBe('$1.25');
    expect(formatUSD({ amount: 1.258 })).toBe('$1.26');
    expect(formatUSD({ amount: 1.25889349857 })).toBe('$1.26');
    expect(formatUSD({ amount: 798127394873 })).toBe('$798,127,394,873.00');
    expect(formatUSD({ amount: 0o00423 })).toBe('$275.00');
  });

  it('Format numbers w/ three decimal places', () => {
    expect(formatUSD({ amount: 1, decimalPlaces: 3 })).toBe('$1.000');
    expect(formatUSD({ amount: 1.25, decimalPlaces: 3 })).toBe('$1.250');
    expect(formatUSD({ amount: 1.258, decimalPlaces: 3 })).toBe('$1.258');
    expect(formatUSD({ amount: 1.25889349857, decimalPlaces: 3 })).toBe(
      '$1.259',
    );
    expect(formatUSD({ amount: 798127394873, decimalPlaces: 3 })).toBe(
      '$798,127,394,873.000',
    );
    expect(formatUSD({ amount: 0o00423, decimalPlaces: 3 })).toBe('$275.000');
  });

  it('Format strings by removing non-numeric characters', () => {
    expect(formatUSD({ amount: 'foo99', decimalPlaces: 0 })).toBe('$99');
    expect(formatUSD({ amount: '--??!!1,2,3,4,5,6,7', decimalPlaces: 0 })).toBe(
      '-$1,234,567',
    );
    expect(formatUSD({ amount: 'zero', decimalPlaces: 0 })).toBe('$0');
  });

  it('Preserve negative numbers as negative dollars', () => {
    expect(formatUSD({ amount: -99, decimalPlaces: 0 })).toBe('-$99');
    expect(formatUSD({ amount: -1234, decimalPlaces: 0 })).toBe('-$1,234');
    expect(formatUSD({ amount: -5.55, decimalPlaces: 2 })).toBe('-$5.55');
  });
});
