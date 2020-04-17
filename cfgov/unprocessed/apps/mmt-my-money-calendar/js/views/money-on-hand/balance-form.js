import { useMemo } from 'react';
import { observer } from 'mobx-react';
import { useParams, useHistory, Redirect } from 'react-router-dom';
import { Formik } from 'formik';
import { useStore } from '../../stores';
import { useBEM } from '../../lib/hooks';
import { CurrencyField } from '../../components/forms';
import { BackButton, NextButton } from '../../components/button';
import { useScrollToTop } from '../../components/scroll-to-top';

import iconPlaceholder from '../../../img/icon-placeholder.png';

function BalanceForm() {
  const { wizardStore } = useStore();
  const bem = useBEM('wizard');
  const { source } = useParams();
  const history = useHistory();

  useScrollToTop();

  if (!wizardStore.fundingSources.length) return <Redirect to="/money-on-hand" />;

  const currentIndex = wizardStore.fundingSources.indexOf(source);
  const prevSource = currentIndex > 0 ? wizardStore.fundingSources[currentIndex - 1] : null;
  const prevStep = prevSource ? `/money-on-hand/balances/${prevSource}` : '/money-on-hand/sources';
  const nextSource =
    wizardStore.fundingSources.length >= currentIndex + 1 ? wizardStore.fundingSources[currentIndex + 1] : null;
  const nextStep = nextSource ? `/money-on-hand/balances/${nextSource}` : '/money-on-hand/summary';

  const initialValues = useMemo(
    () =>
      wizardStore.fundingSources.reduce((values, source) => {
        values[source] = wizardStore.fundingSourceBalances[source] || 0;
        return values;
      }, {}),
    [wizardStore.fundingSources]
  );

  return (
    <>
      <header className={bem('header')}>
        <h2 className={bem('section-title')}>Money on Hand</h2>
      </header>

      <main className={bem('main')}>
        <figure className={bem('step-image')}>
          <img src={iconPlaceholder} alt="placeholder" />
        </figure>

        <Formik
          initialValues={initialValues}
          onSubmit={(values) => {
            wizardStore.setFundingSourceBalance(source, Number(values[source]));
            history.push(nextStep);
          }}
        >
          {(formik) => (
            <form onSubmit={formik.handleSubmit}>
              <CurrencyField
                id={source}
                name={source}
                label={wizardStore.fundingSourceOptions[source].label}
                value={formik.values[source]}
                onChange={formik.handleChange}
                onBlur={formik.handleBlur}
              />

              <div className={bem('buttons')}>
                <BackButton onClick={() => history.push(prevStep)}>Back</BackButton>
                <NextButton type="submit">Next</NextButton>
              </div>
            </form>
          )}
        </Formik>
      </main>
    </>
  );
}

export default observer(BalanceForm);
