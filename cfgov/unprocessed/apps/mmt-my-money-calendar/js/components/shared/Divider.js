import React from "react";
// import "../../styles/Divider.scss";
import { joinClasses } from "../../services/stringServices";

export const Divider = ({ color = "light" }) => (
  <div className={joinClasses(["divider", color])}></div>
);
