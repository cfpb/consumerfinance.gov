import { useEffect } from 'react';
import { useLocation } from 'react-router-dom';
import { useStore } from '../stores';

export function useWizardStep({
  pageTitle,
  subtitle,
  description,
  progress,
  nextStepPath,
  prevStepPath
}) {
  const { uiStore } = useStore();
  const location = useLocation();

  useEffect(() => {
    uiStore.updateWizardStep({
      pageTitle,
      subtitle,
      description,
      progress,
      nextStepPath,
      prevStepPath,
    });
  }, [location]);
}
