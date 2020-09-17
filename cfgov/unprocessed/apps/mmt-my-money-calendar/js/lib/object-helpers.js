export function transform( obj, callback, initialValue = {} ) {
  return [ ...Object.entries( obj ) ].reduce( callback, initialValue );
}

export function pluck( obj, props = [] ) {
  const output = {};

  for ( const prop of props ) {
    if ( typeof obj[prop] === 'undefined' ) continue;
    output[prop] = obj[prop];
  }

  return output;
}

export const filterProps = ( obj, props = [] ) => Object.keys( obj )
  .filter( key => !props.includes( key ) )
  .reduce( ( result, key ) => {
    result[key] = obj[key];
    return result;
  }, {} );

export const isEmpty = obj => Object.keys( obj ).length < 1;
