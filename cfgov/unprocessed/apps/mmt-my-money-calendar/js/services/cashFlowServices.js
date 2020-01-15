/**
 * Generates savings total for use with 'Totals Summary'
 * @param {Object} expenseObj Number of options to generate in addition to current month
 */

export const savingsTotal = expenseObj =>
  expenseObj
    .filter(item => item.type.value === "savings")
    .map(entry => entry.amount)
    .reduce((total, current) => total + current, 0);

/**
 * Generates expense total for use with 'Totals Summary'
 * @param {Object} expenseObj Number of options to generate in addition to current month
 */
export const expenseTotal = expenseObj =>
  expenseObj
    .filter(item => item.type.value !== "savings")
    .map(entry => entry.amount)
    .reduce((total, current) => total + current, 0);
