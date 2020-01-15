import React from "react";

import { Month } from "./Month";

export default function Summary() {
  return (
    <section id="summary-view">
      <p className="page-title">Here is your summary</p>
      <p className="description">
        Start by updating your starting balance or select any date to enter your
        income and expenses.
      </p>
      <Month title="January" />
      <div className="strategy">Strategy List Link</div>
    </section>
  );
}
