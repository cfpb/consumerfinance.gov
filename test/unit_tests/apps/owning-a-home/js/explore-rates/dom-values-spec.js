import { getSelection } from '../../../../../../cfgov/unprocessed/apps/owning-a-home/js/explore-rates/dom-values.js';

const HTML_SNIPPET = `
  <input id="credit-score"
         type="range" min="600" max="840" step="20" value="700">
  <select id="arm-type">
      <option value="3-1">3/1</option>
      <option value="5-1">5/1</option>
      <option value="7-1">7/1</option>
      <option value="10-1">10/1</option>
  </select>
  <input id="location" type="text" value="AL">
  <input id="test-price" type="text" value="$300,000">
  <input id="house-price" type="text" placeholder="200,000">
`;

describe('explore-rates/dom-values', () => {
  beforeEach(() => {
    document.body.innerHTML = HTML_SNIPPET;
  });

  it('should be able to get a value', () => {
    expect(getSelection('not-found-elm')).toBeUndefined();
    expect(getSelection('location')).toStrictEqual('AL');
    expect(getSelection('credit-score')).toStrictEqual(700);
    expect(getSelection('arm-type')).toStrictEqual('3-1');
    expect(getSelection('test-price')).toStrictEqual(300000);
    expect(getSelection('house-price')).toStrictEqual(200000);
  });
});
