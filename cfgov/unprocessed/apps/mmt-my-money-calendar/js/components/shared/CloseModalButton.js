import React from "react";
import closeIcon from "../../../img/close-icon.png";

export const CloseModalButton = ({ closeModal }) => (
  <div className="text-button close-modal" onClick={closeModal}>
    <span>Close</span>
    <img src={closeIcon} alt="circled x" />
  </div>
);
