import { Route, Redirect, Switch, Link, useRouteMatch } from "react-router-dom";
import StartingBalance from "./steps/starting-balance";
import Income from "./steps/income";
import Expenses from "./steps/expenses";
import { useStore } from '../../stores';
import { observer } from 'mobx-react';

function Wizard() {

  const { uiStore } = useStore();

  return (
    <section className="wizard">
      <header className="wizard__header">
        <h1 className="wizard__title">{uiStore.pageTitle}</h1>
        <h2 className="wizard__subtitle">{uiStore.subtitle}</h2>

        <div className="wizard__description">
          {uiStore.description}
        </div>
      </header>

      <Link to="/">Back Home</Link>

      <Switch>
        <Route path="/wizard/starting-balance">
          <StartingBalance />
        </Route>
        <Route path="/wizard/income">
          <Income />
        </Route>
        <Route path="/wizard/expenses">
          <Expenses />
        </Route>
      </Switch>

      <Link to="/summary">Go to Summary</Link>
    </section>
  );
}

export default observer(Wizard);
