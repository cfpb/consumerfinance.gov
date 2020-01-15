import React from "react";

import { Icon } from "../shared/Icon";

// import "../../styles/CalendarView.scss";

export const SectionTip = ({ text }) => (
  <div className="section-tip-wrapper">
    <Icon type="light-bulb" />
    <div className="text">
      <strong>Tip:</strong> {text}
    </div>
  </div>
);
