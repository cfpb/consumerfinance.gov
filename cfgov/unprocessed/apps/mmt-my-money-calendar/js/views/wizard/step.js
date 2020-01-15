import { Link, useRouteMatch } from 'react-router-dom';

export default function Step() {
  const match = useRouteMatch('/step/:step');

  return (
    <div className="wizard-step">
      <h2>Step {match.params.step}</h2>
    </div>
  );
}
