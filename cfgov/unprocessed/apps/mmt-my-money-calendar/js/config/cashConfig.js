import cashInIcon from "../assets/cash-in-icon.png";
import cashOutIcon from "../assets/cash-out-icon.png";

export const cashConfig = {
  incomes: {
    type: "income",
    title: "Cash in",
    addButtonText: "Add income",
    icon: cashInIcon,
    namePlaceholder: "Acme Inc. paycheck",
    typeOptions: [
      { value: "job", label: "Job" },
      { value: "child", label: "Child support" },
      { value: "disability", label: "Disability benefits" },
      { value: "government", label: "Government program" },
      { value: "retirement", label: "Retirement benefits" },
      { value: "other", label: "Other" }
    ]
  },
  expenses: {
    type: "expense",
    title: "Cash out",
    addButtonText: "Add expense",
    icon: cashOutIcon,
    namePlaceholder: "Mortgage payment",
    typeOptions: [
      { value: "bill", label: "Bill payment" },
      { value: "credit", label: "Credit card payment" },
      { value: "rent", label: "Rent or mortgage" },
      { value: "savings", label: "Savings" },
      { value: "other", label: "Other" }
    ]
  }
};
