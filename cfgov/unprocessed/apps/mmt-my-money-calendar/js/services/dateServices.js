import { getMonthNumber } from "./calendarServices";

export const MONTH_NAMES = [
  "January",
  "February",
  "March",
  "April",
  "May",
  "June",
  "July",
  "August",
  "September",
  "October",
  "November",
  "December"
];

export const DAY_NAMES = [
  "Sunday",
  "Monday",
  "Tuesday",
  "Wednesday",
  "Thursday",
  "Friday",
  "Saturday"
];

export const MAX_DAYS_IN_MONTH = 31;

/**
 * Returns a string for the day
 * @param {String} dateString YYYY-MM-DD
 * @returns {String} ex. 'Thursday, October 31'
 */
export const dayString = dateString => {
  let date = new Date(dateString + "T00:00:00");
  let day = DAY_NAMES[date.getDay()];
  let month = MONTH_NAMES[date.getMonth()];
  let dayNumber = date.getDate();

  let validDate = true;
  [day, month, dayNumber].forEach(part => {
    if ([undefined, NaN].includes(part)) {
      validDate = false;
    }
  });

  if (!validDate) return "Invalid Date";
  return `${day}, ${month} ${dayNumber}`;
};

/**
 *
 * @param {Number} day Day of month
 * @param {String} monthYear ex. "October 2019"
 */
export const convertToDateString = (day, monthYear) => {
  let [month, year] = monthYear.split(" ");
  month = getMonthNumber(month) + 1;
  const dayString = day < 10 ? `0${day}` : day;

  return `${year}-${month}-${dayString}`;
};

/**
 * Generates select options for MonthSelect dropdown menu
 * @param {Number} monthsAhead Number of options to generate in addition to current month
 */
export const generateMonthOptions = (monthsAhead = 6) =>
  [...Array(monthsAhead + 1).keys()].map(add => {
    const today = new Date();
    today.setDate(1);
    today.setMonth(today.getMonth() + add);

    const thisMonth = today.getMonth();
    const year = today.getFullYear();

    return {
      value: `${MONTH_NAMES[thisMonth].toLowerCase()}-${year}`,
      label: `${MONTH_NAMES[thisMonth]} ${year}`
    };
  });
