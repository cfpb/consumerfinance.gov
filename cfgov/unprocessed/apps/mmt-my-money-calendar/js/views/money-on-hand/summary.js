import { useCallback } from 'react';
import { observer } from 'mobx-react';
import { Redirect, useHistory } from 'react-router-dom';
import { useStore } from '../../stores';
import { useBEM } from '../../lib/hooks';
import { useScrollToTop } from '../../components/scroll-to-top';
import { formatCurrency } from '../../lib/currency-helpers';
import { BackButton, NextButton } from '../../components/button';

import categoryIcons from '../../lib/category-icons';
import SvgImage from '../../components/svg-image';

function Summary() {
  const { eventStore, wizardStore } = useStore();
  const bem = useBEM('wizard');
  const history = useHistory();
  const saveAndRedirect = useCallback(
    async (evt) => {
      evt.preventDefault();

      await eventStore.saveEvent({
        name: 'Starting Balance',
        category: 'income.startingBalance',
        totalCents: wizardStore.totalStartingFundsCents,
        date: new Date(),
      });

      wizardStore.reset();

      history.push('/calendar');
    },
    [wizardStore.totalStartingFundsCents]
  );

  useScrollToTop();

  if (!wizardStore.fundingSources.length && !wizardStore.noStartingFunds) return <Redirect to='/money-on-hand' />;

  return (
    <>
      <header className={bem('header')}>
        <h2 className={bem('section-title')}>Money on Hand</h2>
      </header>

      <main className={bem('main')}>
        <figure className={bem('step-image')}>
          <SvgImage src={categoryIcons.moneyOnHand} alt='Money on Hand icon' />
        </figure>

        <h3>Starting Balance Summary</h3>

        <p>You have money in the following places:</p>

        <ul>
          {Boolean(wizardStore.fundingSources.length) && wizardStore.fundingSources.map((source, idx) => {
            const { name } = wizardStore.fundingSourceOptions[source];
            const balance = wizardStore.fundingSourceBalances[source];

            return (
              <li key={`funding-src-${idx}`} className='funding-source'>
                <span className='funding-source__name'>{name}:</span>
                <span className='funding-source__balance'>{formatCurrency(balance / 100)}</span>
              </li>
            );
          })}

          {wizardStore.noStartingFunds && (
            <li className='funding-source'>
              <em>No starting funds</em>
            </li>
          )}
        </ul>

        <p>
          <strong>Total Starting Balance:</strong> {formatCurrency(wizardStore.totalStartingFunds)}
        </p>

        <div className={bem('buttons')}>
          <BackButton onClick={history.goBack}>Back</BackButton>
          <NextButton onClick={saveAndRedirect}>Go to Calendar</NextButton>
        </div>
      </main>
    </>
  );
}

export default observer(Summary);
