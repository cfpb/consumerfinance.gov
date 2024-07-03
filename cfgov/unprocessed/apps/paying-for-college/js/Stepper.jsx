import React from 'react';

function Step({ active }) {
  return <li className={active ? 'active' : ''}></li>;
}

function CurrentStep({ step }) {
  return <span className="current-step">{step}</span>;
}

export default function Stepper({ steps, step, headings }) {
  return (
    <div className="m-stepper block block--sub block--flush-top ">
      <ol>
        {[...Array(steps)].map((v, i) => {
          return <Step key={i} active={i < step} />;
        })}
      </ol>
      <div>
        <span>
          <CurrentStep step={step} /> of {steps}
        </span>
        {headings ? <span class="h4">{headings[step - 1]}</span> : null}
      </div>
    </div>
  );
}
