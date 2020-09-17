import dotProp from 'dot-prop';

export const compact = arr => arr.filter( Boolean );
export const unique = arr => [ ...new Set( arr ) ];
export const pluck = ( arrOfObjects, propPath, defaultValue ) => arrOfObjects.map( obj => dotProp.get( obj, propPath, defaultValue ) );
export const toMap = ( arrOfObjects, keyProp ) => new Map( arrOfObjects.map( item => [ item[keyProp], item ] ) );

export function *range( start, stop, step = 1 ) {
  for ( let i = start; i <= stop; i += step ) {
    yield i;
  }
}
