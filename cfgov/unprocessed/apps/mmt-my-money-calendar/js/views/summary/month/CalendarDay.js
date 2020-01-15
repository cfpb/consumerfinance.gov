import React from "react";
import { joinClasses } from "../../../services/stringServices";
import { ReactComponent as DollarIcon } from "../../../assets/dollar-icon.svg";
import { ReactComponent as MinusIcon } from "../../../assets/minus-icon.svg";

/**
 * CalendarDay
 * @param {Number} number Day in the month
 * @param {Number} date Timestamp (ms since epoch)
 * @param {Function} setState Update function for global state
 * @param {Boolean} hasEntries Flag to display dots
 * @param {Boolean} hasCash Flag to display red/green stylings
 * @param {Boolean} showCashStyling Flag to avoid styling days for which we don't have enough info
 */
export const CalendarDay = ({
  number,
  date,
  setState,
  hasEntries,
  hasCash,
  showCashStyling,
  startingBalanceDay
}) => {
  // Dynamically determine styling for the day
  const classHasEntries = hasEntries ? "hasEntries" : "noEntries";
  const classHasCash = showCashStyling
    ? hasCash
      ? "hasCash"
      : "noCash"
    : null;

  const classes = joinClasses(["day", classHasEntries, classHasCash]);

  const Icon = hasCash ? DollarIcon : MinusIcon;

  const handleClick = () => {
    setState({
      selectedDay: date,
      selectedDayStartBalance: startingBalanceDay,
      selectedDayIsStyled: showCashStyling
    });
  };

  return (
    <div id={`day${number}`} className={classes} onClick={handleClick}>
      <div className="number">{number}</div>
      {showCashStyling && <div className="dots">•••••</div>}
      {showCashStyling && (
        <div className="symbol">
          <Icon />
        </div>
      )}
    </div>
  );
};

/**
 * CalendarDayPlaceholder
 * Dummy component for non-month days
 */
export const CalendarDayPlaceholder = () => (
  <div className="day placeholder"></div>
);
