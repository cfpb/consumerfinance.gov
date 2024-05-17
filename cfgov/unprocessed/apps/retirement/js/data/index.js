export const benefits = {
  fullAge: 67,
  age62: 1515,
  age63: 1635,
  age64: 1744,
  age65: 1889,
  age66: 2035,
  age67: 2180,
  age68: 2354,
  age69: 2529,
  age70: 2719,
  earlyAge: 62,
  currentAge: 37,
  earlyRetirementAge: '62 and 1 month',
  fullRetirementAge: 67,
};

export let lifetime = {};

/**
 * @param {string} birthdate - Birthday in MM-DD-YYYY format
 * @param {number} salary - Entered salary as a number
 * @returns {Promise} A promise that resolved to the parsed response
 */
export function fetchApiData(birthdate, salary) {
  if (typeof birthdate !== 'string' || typeof salary !== 'number')
    throw new Error('Invalid API call');
  const url = `../retirement-api/estimator/${birthdate}/${salary}/`;

  return fetch(url).then((v) => v.json());
}

/**
 * @param {object} resp - The API response object;
 */
export function updateDataFromApi(resp) {
  const data = resp.data;
  let fullAge = Number(data['full retirement age'].slice(0, 2));
  if (resp.current_age > fullAge) {
    fullAge = resp.current_age;
  }

  Object.keys(resp.data.benefits).forEach((key) => {
    const prop = key.replace(' ', '');
    benefits[prop] = resp.data.benefits[key];
  });

  lifetime = resp.data.lifetime;

  benefits['currentAge'] = resp.current_age;
  benefits['past_fra'] = resp.past_fra;
  benefits['fullRetirementAge'] = data['full retirement age'];
  benefits['earlyRetirementAge'] = data['early retirement age'];
  benefits['fullAge'] = Number(fullAge);
  benefits['earlyAge'] = Number(data['early retirement age'].slice(0, 2));
  benefits['monthsPastBirthday'] = Number(data.months_past_birthday);
}
