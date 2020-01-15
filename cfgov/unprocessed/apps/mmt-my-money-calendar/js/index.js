import * as idb from 'idb';
import { render } from 'react-dom';
import Greeting from './components/greeting';
import Counter from './components/counter';
import { configure as configureMobX } from 'mobx';
import Routes from './routes';

configureMobX({ enforceActions: 'observed' });

const App = () => (
  <section className="my-money-calendar">
    <Routes />
  </section>
);

window.idb = idb;

render(<App />, document.querySelector('#mmt-my-money-calendar'));
