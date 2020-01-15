import React, { useContext, useState } from "react";
import { Redirect } from "react-router-dom";
import { AppContext } from "../../../App";
import { dayString } from "../../services/dateServices";
import { filterByDate } from "../../services/objectServices";
import Cash from "../../Cash/Cash";
import { CashAvailableToday } from "../../cash/CashAvailableToday";
import { CloseModalButton } from "../../components/shared/CloseModalButton";
import { Divider } from "../../components/shared/Divider";

export const DayModal = ({ closeModal, selectedDate }) => {
  const {
    monthlyData,
    selectedDayIsStyled,
    selectedDayStartBalance,
    selectedMonth,
    setState
  } = useContext(AppContext);

  const [incomes, setIncomes] = useState(
    filterByDate(monthlyData[selectedMonth.label].incomes, selectedDate)
  );
  const [expenses, setExpenses] = useState(
    filterByDate(monthlyData[selectedMonth.label].expenses, selectedDate)
  );

  // User needs to select a month before we can show day-level data
  if (!selectedMonth) return <Redirect to="/month" />;

  const saveEntries = e => {
    e.preventDefault();
    setState(prevState => {
      const thisMonthsData = prevState.monthlyData[selectedMonth.label];
      return {
        monthlyData: {
          ...prevState.monthlyData,
          // Update the selected Month
          [selectedMonth.label]: {
            ...thisMonthsData,
            incomes: [
              // Update today's incomes without overwriting incomes for other days in the month
              ...deleteEnteriesByDay(thisMonthsData, "incomes", selectedDate),
              ...incomes
            ],
            expenses: [
              // Update today's expenses without overwriting expenses for other days in the month
              ...deleteEnteriesByDay(thisMonthsData, "expenses", selectedDate),
              ...expenses
            ]
          }
        }
      };
    });
    closeModal();
  };

  return (
    <div className="modal-wrapper">
      <div className="day modal">
        <div className="header section ">
          <CloseModalButton closeModal={closeModal} />
          <div className="title">You've selected:</div>
          <div className="date">{dayString(selectedDate)}</div>
        </div>
        <Divider color="dark" />
        <Cash
          section="incomes"
          data={incomes}
          date={selectedDate}
          setState={setIncomes}
          selectedMonth={selectedMonth}
        />
        <Divider color="dark" />
        <Cash
          section="expenses"
          data={expenses}
          date={selectedDate}
          setState={setExpenses}
          selectedMonth={selectedMonth}
        />
        <CashAvailableToday
          incomes={incomes}
          expenses={expenses}
          startBalance={selectedDayStartBalance}
          date={selectedDate}
          isStyled={selectedDayIsStyled}
        />
        <div className="actions section">
          <button className="primary" onClick={saveEntries}>
            Done
          </button>
          {/* vvv I think we should have a more easily accessible "Don't save changes" button vvv */}
          {/* <button className="secondary" onClick={closeModal}>
          Cancel
        </button> */}
        </div>
      </div>
    </div>
  );
};

// Filters out enteries for a given date
const deleteEnteriesByDay = (dataObject, section, date) =>
  Object.keys(dataObject[section])
    .map(key => dataObject[section][key])
    .filter(item => item.date !== date);
