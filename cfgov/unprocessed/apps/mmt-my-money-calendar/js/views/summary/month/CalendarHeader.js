import React from "react";
import { CALENDAR_LABELS } from "../../../services/calendarServices";

/**
 * Displays the Calendar column labels
 */
export const CalendarHeader = () => (
  <div className="header row">
    {CALENDAR_LABELS.map((label, idx) => (
      <div key={`${label}${idx}`} className="day label">
        {label}
      </div>
    ))}
  </div>
);
