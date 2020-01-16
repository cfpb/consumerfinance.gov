import { useEffect } from 'react';
import { Link, useRouteMatch } from 'react-router-dom';

export default function Step() {
  const match = useRouteMatch('/wizard/step/:step');

  return (
    <div className="wizard-step">
      <h2>Step {match.params.step}</h2>
    </div>
  );
}
