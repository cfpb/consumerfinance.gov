import clsx from 'clsx';
import { observer } from 'mobx-react';
import { useHistory } from 'react-router-dom';
import { Formik, FieldArray } from 'formik';
import * as yup from 'yup';
import { Link } from 'react-router-dom';
import { useScrollToTop } from '../../components/scroll-to-top';
import { useBEM } from '../../lib/hooks';
import { useStore } from '../../stores';
import { BackButton, NextButton } from '../../components/button';
import { Checkbox } from '../../components/forms';

import iconPlaceholder from '../../../img/icon-placeholder.png';

function Sources() {
  const bem = useBEM('wizard');
  const { wizardStore } = useStore();
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
            fundingSources: [],
            noFunds: false,
          }}
          onSubmit={(values) => {
            if (values.noFunds) {
              history.push('/money-on-hand/summary');
              return;
            }

            wizardStore.setFundingSources(values.fundingSources);
            history.push(`/money-on-hand/balances/${values.fundingSources[0]}`);
          }}
        >
          {(formik) => (
            <form onSubmit={formik.handleSubmit}>
              <p className="checkbox-group-label">Where do you have money?</p>

              <div className={bem('field')}>
                <FieldArray
                  name="fundingSources"
                  render={(arrayHelpers) => (
                    <div>
                      {Object.entries(wizardStore.fundingSourceOptions).map(([key, { name }], idx) => (
                        <Checkbox
                          largeTarget
                          disabled={formik.values.noFunds}
                          key={`funding-source-opt-${idx}`}
                          name="fundingSources"
                          id={`fundingSources-opt-${idx}`}
                          value={key}
                          checked={formik.values.fundingSources.includes(key)}
                          onChange={(e) => {
                            if (e.target.checked) {
                              arrayHelpers.push(key);
                            } else {
                              const i = formik.values.fundingSources.indexOf(key);
                              arrayHelpers.remove(i);
                            }
                          }}
                          label={name}
                          castToBoolean={false}
                        />
                      ))}
                    </div>
                  )}
                />
              </div>

              <div className={clsx(bem('field'), 'last')}>
                <Checkbox
                  largeTarget
                  id="funding-source-none"
                  name="noFunds"
                  checked={Boolean(formik.values.noFunds)}
                  onChange={formik.handleChange}
                  label="None"
                  disabled={formik.values.fundingSources.length > 0}
                />
              </div>

              <div className={bem('buttons')}>
                <BackButton onClick={(e) => e.preventDefault()}>Back</BackButton>
                <NextButton type="submit" disabled={!formik.values.fundingSources.length}>
                  Next
                </NextButton>
              </div>
            </form>
          )}
        </Formik>
      </main>
    </>
  );
}

export default observer(Sources);
