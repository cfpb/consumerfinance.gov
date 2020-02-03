import * as idb from 'idb';
import { render } from 'react-dom';
import { configure as configureMobX } from 'mobx';
import { Workbox } from 'workbox-window';
import { DateTime, Info } from 'luxon';
import { RRule } from 'rrule';
import { StoreProvider } from './stores';
import Routes from './routes';
import CashFlowEvent from './stores/models/cash-flow-event';

configureMobX({ enforceActions: 'observed' });

const App = () => (
  <StoreProvider>
    <section className="my-money-calendar">
      <Routes />
    </section>
  </StoreProvider>
);

render(<App />, document.querySelector('#mmt-my-money-calendar'));

if (process.env.NODE_ENV === 'production' && 'serviceWorker' in navigator) {
  const wb = new Workbox('/mmt-my-money-calendar/service-worker.js', { scope: '/mmt-my-money-calendar' });

  wb.addEventListener('activated', (evt) => {
    if (!evt.isUpdate) {
      console.info('MMC service worker activated for the first time');
    } else {
      console.info('MMC service worker updated');
    }
  });

  wb.register();
}

if (process.env.NODE_ENV === 'development') {
  window.idb = idb;
  window.CashFlowEvent = CashFlowEvent;
  window.DateTime = DateTime;
  window.Info = Info;
  window.RRule = RRule;

  async function loadSeeders() {
    window.seed = await import(/* webpackChunkName: "seeds.js" */ './seed-data.js');
  };

  window.seedTestData = async function seedTestData() {
    if (!window.seed) await loadSeeders();

    console.info('Imported seed data script');
    const results = await window.seed.seedData();
    console.info('Seeding complete %O', results);
  };

  window.clearTestData = async function clearTestData() {
    if (!window.seed) await loadSeeders();

    await clearData();
    console.info('Cleared all data');
  }
}
