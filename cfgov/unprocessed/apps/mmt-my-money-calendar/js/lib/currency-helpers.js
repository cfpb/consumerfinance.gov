const DEFAULT_FORMATTER = new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD' });

export function formatCurrency(num, formatter = DEFAULT_FORMATTER) {
  return formatter.format(num);
}
