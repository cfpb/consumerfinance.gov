/**
 * Convert cents to a currency formatted string
 * @param {Number} cents
 * @param {String} currency
 */
export const formatCurrency = (cents, currency = "USD") => {
  const dollars = cents / 100;
  return dollars.toLocaleString("en-US", {
    style: "currency",
    currency
  });
};

/**
 * Convert a string to a Number representing cents
 * @param {String} str a string
 */
export const toCents = str => {
  const replaced = str.replace(/[$,.]/g, "");
  const parsed = Number.parseInt(replaced);
  if (isNaN(parsed)) return 0;
  return parsed;
};

/**
 * Returns the total value of the data set
 * @param {[Object]} data Incomes or Expenses
 * @returns {Number} Total value
 */
export const totalAmount = data =>
  data.reduce((prev, curr) => prev + Number(curr.amount), 0);

/**
 * Returns the percentage of a subtotal of a grandtotal
 * @param {Number} subtotal
 * @param {Number} grandtotal
 * @returns {Integer}
 */
export const findPercentage = (subtotal, grandtotal) => {
  if (!grandtotal) return 0;
  return Math.floor((subtotal / grandtotal) * 100);
};
