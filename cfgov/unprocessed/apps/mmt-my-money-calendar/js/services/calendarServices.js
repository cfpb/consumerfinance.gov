import React from "react";
import { CalendarDayPlaceholder } from "../components/CalendarView/Calendar/CalendarDay";
import { MONTH_NAMES } from "./dateServices";

export const CALENDAR_LABELS = ["S", "M", "T", "W", "T", "F", "S"];

/**
 * Creates groups of 7
 * @param {Array} days a list of CalendarDay/Placeholder components
 */
export const createWeekRows = days => {
  const result = [];
  let startIdx = 0;
  let endIdx = 7;

  while (startIdx < days.length) {
    const rowArray = days.slice(startIdx, endIdx);

    // Pad end of row with placeholders to ensure consistent display
    while (7 - rowArray.length > 0) {
      rowArray.push(
        <CalendarDayPlaceholder key={`placeholder${rowArray.length + 7}`} />
      );
    }

    result.push(rowArray);
    startIdx += 7;
    endIdx += 7;
  }

  return result;
};

/**
 * Derive some info about the month for Calendar display
 * @param {String} str i.e. 'October 2019
 */
export const getMonthInfo = str => {
  let [month, year] = str.split(" ");
  month = getMonthNumber(month);
  year = Number.parseInt(year);

  // Do some voodoo to get the last day of the month
  const daysInMonth = new Date(year, month + 1, 0).getDate();

  // Get the weekday number of the 1st of the month [0-Sun 6-Sat]
  const firstWeekday = new Date(year, month, 1).getDay();

  return { daysInMonth, firstWeekday };
};

/**
 * Returns the month number
 * @example getMonthNumber("January") => 0
 * @param {String} monthName
 */
export const getMonthNumber = monthName => MONTH_NAMES.indexOf(monthName);

/**
 *  Default values for an entry in state.monthlyData
 */
export const defaultMonthlyDataEntry = {
  startingBalance: {
    checking: 0,
    prepaid: 0,
    other: 0,
    total: 0,
    startDay: 1
  },
  incomes: {},
  expenses: {}
};

/**
 * Creates a new entry in state.monthlyData
 * @param {String} month ex. "October 2019"
 * @param {Function} setState
 */
export const initializeMonthlyData = (month, setState) => {
  setState(prev => ({
    monthlyData: {
      ...prev.monthlyData,
      [month]: { ...defaultMonthlyDataEntry }
    }
  }));
};
