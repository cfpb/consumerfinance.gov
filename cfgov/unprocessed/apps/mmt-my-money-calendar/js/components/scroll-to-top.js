import { useEffect } from 'react';
import { useLocation } from 'react-router-dom';

export default function ScrollToTop() {
  /* istanbul ignore next */
  useScrollToTop();
  return null;
}

export function useScrollToTop() {
  /* istanbul ignore next */
  const { pathname } = useLocation();

  useEffect( () => {
    window.scrollTo( 0, 0 );
  }, [ pathname ] );
}

export function useScrollToTopOnMount() {
  /* istanbul ignore next */
  useEffect( () => {
    window.scrollTo( 0, 0 );
  }, [] );
}
