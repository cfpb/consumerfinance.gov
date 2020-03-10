const DEFAULT_FORMATTER = new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD' });

export function formatCurrency(num, formatter = DEFAULT_FORMATTER) {
  if (!Number.isInteger(num)) {
    num = 0;
  }

  return formatter.format(num);
}

export function toCents(cash) {
  const replaced = cash.replace(/[\$,\.]/g, '');
  const parsed = Number.parseInt(replaced, 10);
  if (Number.isNaN(parsed)) return 0;
  return parsed;
}
