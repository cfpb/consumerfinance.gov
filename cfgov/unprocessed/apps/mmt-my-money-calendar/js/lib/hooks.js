import { useEffect, useCallback } from 'react';
import { useLocation } from 'react-router-dom';
import { useStore } from '../stores';

export const useClickHandler = (cb, deps) => useCallback((evt) => {
  evt.preventDefault();
  cb(evt);
}, deps);

export const useClickConfirm = (message, cb, deps, confirm = window.confirm) => useClickHandler((evt) => {
  if (!confirm(message)) return;
  cb(evt);
}, deps);

export const useBEM = (baseClass) => useCallback((module, modifier) => {
  let klass = baseClass;

  if (module) klass += `__${module}`;
  if (modifier) klass += `--${modifier}`;

  return klass;
}, [baseClass]);
