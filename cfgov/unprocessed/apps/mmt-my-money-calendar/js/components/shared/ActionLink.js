import React from "react";

import { Icon } from "./Icon";

import "../../styles/ActionLink.scss";

export const ActionLink = ({ text, icon }) => {
  return (
    <div className="action-link">
      <div className="underline">{text}</div>
      <div>
        <Icon type={icon} />
      </div>
    </div>
  );
};
