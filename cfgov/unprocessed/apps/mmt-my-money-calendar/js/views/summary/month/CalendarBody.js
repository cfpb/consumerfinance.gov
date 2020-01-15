import React from "react";

/**
 * Displays the Days of the calendar
 * @param {Array} props.rows A group of 7 CalendarDay/Placeholder components
 */
export const CalendarBody = ({ rows }) => {
  return rows.map((daysofWeek, idx) => (
    <div key={"row" + idx} className="row">
      {daysofWeek}
    </div>
  ));
};

CalendarBody.defaultProps = {
  rows: []
};
