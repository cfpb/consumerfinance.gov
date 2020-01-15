import { isEmpty } from "lodash";
import React, { useContext } from "react";
import { AppContext } from "../../../App";
import { range } from "../../../services/arrayServices";
import {
  createWeekRows,
  getMonthInfo
} from "../../../services/calendarServices";
import { totalAmount } from "../../../services/currencyServices";
import {
  convertToDateString,
  MAX_DAYS_IN_MONTH
} from "../../../services/dateServices";
import { filterByDate } from "../../../services/objectServices";
import "../../../styles/Calendar.scss";
import { DayModal } from "./DayModal";
import { CalendarBody } from "./CalendarBody";
import { CalendarDay, CalendarDayPlaceholder } from "./CalendarDay";
import { CalendarHeader } from "./CalendarHeader";
import { CalendarKey } from "./CalendarKey";

/**
 * Calendar - Pulls data from AppContext and displays a calendar for the selectedMonth
 */
export const Calendar = () => {
  const {
    monthlyData,
    selectedDay,
    selectedMonth,
    setState,
    selectedDayStartBalance
  } = useContext(AppContext);

  // Get info needed to draw the calendar
  const { firstWeekday, daysInMonth } = getMonthInfo(selectedMonth.label);

  // Initialize an array with placeholders for non-month days
  const days = range(firstWeekday).map((_, idx) => (
    <CalendarDayPlaceholder key={`placeholder${idx}`} />
  ));

  // Get the info needed to derive the daily styles
  const { startingBalance, incomes, expenses } = monthlyData[
    selectedMonth.label
  ];

  let todaysDate,
    todaysIncomes,
    todaysExpenses,
    todayHasEntries,
    todayIsStyled,
    currentBalance = 0,
    prevBalance = 0,
    firstDayWithEntries = MAX_DAYS_IN_MONTH + 1;

  // Create an entry for each day of month
  range(1, daysInMonth + 1).forEach(dayNumber => {
    todaysDate = convertToDateString(dayNumber, selectedMonth.label);
    todaysIncomes = filterByDate(incomes, todaysDate);
    todaysExpenses = filterByDate(expenses, todaysDate);
    todayHasEntries = !isEmpty(todaysIncomes) || !isEmpty(todaysExpenses);

    // Start styling, at the latest, from the first day with entries
    if (todayHasEntries && firstDayWithEntries > MAX_DAYS_IN_MONTH) {
      firstDayWithEntries = dayNumber;
      todayIsStyled = true;
    }

    // Only include the month's starting balance in calculations that fall on or after the start day
    if (startingBalance.startDay && startingBalance.startDay === dayNumber) {
      todayIsStyled = true;
      prevBalance = currentBalance + startingBalance.total;
      currentBalance +=
        startingBalance.total +
        totalAmount(todaysIncomes) -
        totalAmount(todaysExpenses);
    } else {
      prevBalance = todayIsStyled ? currentBalance : null;
      currentBalance +=
        totalAmount(todaysIncomes) - totalAmount(todaysExpenses);
    }

    days.push(
      <CalendarDay
        key={dayNumber}
        number={dayNumber}
        date={todaysDate}
        setState={setState}
        hasCash={currentBalance > 0}
        hasEntries={todayHasEntries}
        showCashStyling={todayIsStyled}
        startingBalanceDay={prevBalance}
      />
    );
  });

  return (
    <>
      {selectedDay && (
        <DayModal
          selectedDate={selectedDay}
          startingDayStartingBalance={selectedDayStartBalance}
          closeModal={() =>
            setState({ selectedDay: null, selectedDayStartBalance: null })
          }
        />
      )}
      <div className="calendar">
        <CalendarHeader />
        <CalendarBody rows={createWeekRows(days)} />
        <CalendarKey show={startingBalance} />
      </div>
    </>
  );
};

export default Calendar;
