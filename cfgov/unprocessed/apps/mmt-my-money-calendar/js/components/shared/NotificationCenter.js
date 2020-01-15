import React from "react";

import { Icon } from "./Icon";

// import "../../styles/NotificationCenter.scss";

export const NotificationCenter = () => (
  <div className="notification-center-wrapper">
    <Icon type="star-icon" />
    <div className="text">
      Nice! Your calendar updated to reflect your positive starting balance.
      Learn more about your spending by adding a few income and expenses on the
      days you expect to receive or pay them.
    </div>
  </div>
);
