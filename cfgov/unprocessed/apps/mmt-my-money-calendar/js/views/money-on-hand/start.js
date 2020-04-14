import { Link } from 'react-router-dom';
import { useBEM } from '../../lib/hooks';

export default function Start() {
  const bem = useBEM('wizard');

  return (
    <section className={bem()}>
      <header className={bem('header')}>
        <h1 className={bem('header-app-title')}>MyMoneyCalendar</h1>

        <p className={bem('header-intro')}>
          See how your money flows from week to week and learn how to avoid coming up short.
        </p>
      </header>

      <main className={bem('main')}>
        <p>
          Enter your income, expenses, and cash-on-hand to build your calendar.
        </p>
        <p>
          It's okay to estimate.
        </p>

        <Link className="a-btn" to="/money-on-hand/sources">Begin</Link>
      </main>
    </section>
  );
}
