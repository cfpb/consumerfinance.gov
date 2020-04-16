import { observer } from 'mobx-react';
import { useParams, useHistory } from 'react-router-dom';
import { useStore } from '../../stores';
import { useBEM } from '../../lib/hooks';
import { CurrencyField } from '../../components/forms';
import { BackButton, NextButton } from '../../components/button';
import { useScrollToTop } from '../../components/scroll-to-top';

import iconPlaceholder from '../../../img/icon-placeholder.png';
import { Formik } from 'formik';

function BalanceForm() {
  const { wizardStore } = useStore();
  const bem = useBEM('wizard');
  const { source } = useParams();
  const history = useHistory();

  useScrollToTop();

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
          initialValues={{
            [source]: 0,
          }}
          onSubmit={(values) => {

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
                <BackButton onClick={(e) => e.preventDefault()}>Back</BackButton>
                <NextButton type="submit">
                  Next
                </NextButton>
              </div>
            </form>
          )}
        </Formik>
      </main>
    </>
  )
}

export default observer(BalanceForm);
