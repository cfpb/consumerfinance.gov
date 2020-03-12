import { render } from 'react-dom';
import { configure as configureMobX } from 'mobx';
import { Workbox } from 'workbox-window';
import { StoreProvider } from './stores';
import Routes from './routes';

configureMobX({ enforceActions: 'observed' });

if (process.env.SERVICE_WORKER_ENABLED && 'serviceWorker' in navigator) {
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

// In development mode, expose global functions to seed and clear the local IDB database:
if (process.env.NODE_ENV === 'development') {
  async function loadSeeders() {
    window.seed = await import(/* webpackChunkName: "seeds.js" */ './seed-data.js');
  }

  window.seedTestData = async function seedTestData() {
    if (!window.seed) await loadSeeders();

    console.info('Imported seed data script');
    const results = await window.seed.seedData();
    console.info('Seeding complete %O', results);
  };

  window.clearTestData = async function clearTestData() {
    if (!window.seed) await loadSeeders();

    await window.seed.clearData();
    console.info('Cleared all data');
  };
}

const App = () => (
  <StoreProvider>
    <section className="my-money-calendar">
      <Routes />
    </section>
  </StoreProvider>
);

render(<App />, document.querySelector('#mmt-my-money-calendar'));
