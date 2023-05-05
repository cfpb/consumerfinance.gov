const fetchApiData = (birthdate, salary, dataLang) => {
  let url = `../retirement-api/estimator/${birthdate}/${Number(salary)}/`;

  if (dataLang === 'es') {
    url = `../${url}es/`;
  }

  return fetch(url).then((v) => v.json());
};

export default fetchApiData;
