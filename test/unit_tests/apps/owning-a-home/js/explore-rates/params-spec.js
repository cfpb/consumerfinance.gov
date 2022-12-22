import {
  getAllParams,
  getVal,
  setVal,
  update,
} from '../../../../../../cfgov/unprocessed/apps/owning-a-home/js/explore-rates/params.js';

const HTML_SNIPPET = `
  <input id="credit-score"
         type="range" min="600" max="840" step="20" value="700">
  <input id="down-payment" type="text" placeholder="20,000">
  <input id="house-price" type="text" placeholder="200,000">
  <input id="loan-amount" type="text" placeholder="200,000">
  <select id="location">
      <option value="VT">Vermont</option>
  </select>
  <select id="rate-structure">
    <option value="fixed">Fixed</option>
    <option value="arm">Adjustable</option>
  </select>
  <select id="loan-term">
      <option value="30">30 Years</option>
      <option value="15">15 Years</option>
  </select>
  <select id="loan-type">
      <option value="conf">Conventional</option>
      <option value="fha">FHA</option>
      <option value="va">VA</option>
  </select>
  <select id="arm-type">
      <option value="3-1">3/1</option>
      <option value="5-1">5/1</option>
      <option value="7-1">7/1</option>
      <option value="10-1">10/1</option>
  </select>
`;

describe('explore-rates/params', () => {
  beforeEach(() => {
    document.body.innerHTML = HTML_SNIPPET;
  });

  it('should be able to get a value', () => {
    expect(getVal('credit-score')).toBe(700);
    expect(getVal('down-payment')).toBe('20,000');
    expect(getVal('dp-constant')).toBe('');
    expect(getVal('house-price')).toBe('200,000');
    expect(getVal('loan-amount')).toBeUndefined();
    expect(getVal('location')).toBe('AL');
    expect(getVal('rate-structure')).toBe('fixed');
    expect(getVal('loan-term')).toBe(30);
    expect(getVal('loan-type')).toBe('conf');
    expect(getVal('arm-type')).toBe('5-1');
    expect(getVal('edited')).toBe(false);
    expect(getVal('isJumbo')).toBe(false);
    expect(getVal('prevLoanType')).toBe('');
    expect(getVal('prevLocation')).toBe('');
    expect(getVal('request')).toBeUndefined();
  });

  it('should be able to set a value', () => {
    setVal('credit-score', 800);
    expect(getVal('credit-score')).toBe(800);
  });

  it('should be able to return all stored values', () => {
    let UNDEFINED;
    const mockData = {
      'credit-score': 800,
      'down-payment': '20,000',
      'dp-constant': '',
      'house-price': '200,000',
      location: 'AL',
      'loan-amount': UNDEFINED,
      'rate-structure': 'fixed',
      'loan-term': 30,
      'loan-type': 'conf',
      'arm-type': '5-1',
      edited: false,
      isJumbo: false,
      prevLoanType: '',
      prevLocation: '',
      request: UNDEFINED,
    };
    const storedValues = getAllParams();
    expect(storedValues).toStrictEqual(mockData);
  });

  it('should be able to update a value from the HTML', () => {
    expect(getVal('prevLoanType')).toBe('');
    expect(getVal('prevLocation')).toBe('');
    update();
    expect(getVal('prevLoanType')).toBe('conf');
    expect(getVal('prevLocation')).toBe('AL');

    const sliderElement = document.querySelector('#credit-score');
    expect(getVal('credit-score')).toBe(700);
    sliderElement.value = 800;
    update();
    expect(getVal('credit-score')).toBe(800);
  });
});
