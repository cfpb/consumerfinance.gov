const DEFAULT_FORMATTER = new Intl.NumberFormat( 'en-US', { style: 'currency', currency: 'USD' } );

export function formatCurrency( num, options = {} ) {
  const {
    symbol = true,
    formatter = DEFAULT_FORMATTER
  } = options;
  const result = formatter.format( num );

  if ( symbol ) return result;
  return result.slice( 1 );
}

export function toCents( cash ) {
  const replaced = cash.replace( /[\$,\.]/g, '' );
  const parsed = Number.parseInt( replaced, 10 );
  if ( Number.isNaN( parsed ) ) return 0;
  return parsed;
}
