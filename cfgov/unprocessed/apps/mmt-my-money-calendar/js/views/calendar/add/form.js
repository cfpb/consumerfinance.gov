import { observer } from 'mobx-react';
import { useMemo, useCallback } from 'react';
import { Formik } from 'formik';
import { useParams, useHistory, Redirect, withRouter } from 'react-router-dom';
import * as yup from 'yup';
import { DateTime } from 'luxon';
import dotProp from 'dot-prop';
import { useStore } from '../../../stores';
import { Categories } from '../../../stores/models/categories';
import Button, { ButtonLink, BackButton } from '../../../components/button';
import { TextField, DateField, Checkbox, CurrencyField, RadioButton, SelectField } from '../../../components/forms';
import { recurrenceRules, numberWithOrdinal } from '../../../lib/calendar-helpers';
import { range } from '../../../lib/array-helpers';
import { pluck } from '../../../lib/object-helpers';
import { useScrollToTop } from '../../../components/scroll-to-top';
import Logger from '../../../lib/logger';
import CashFlowEvent from '../../../stores/models/cash-flow-event';

function Form() {
  useScrollToTop();

  const { uiStore, eventStore } = useStore();
  const history = useHistory();
  const logger = useMemo(() => Logger.addGroup('eventForm'), []);
  const monthDayOptions = useMemo(
    () => [...range(1, 30)].map((num) => ({ label: numberWithOrdinal(num), value: num })),
    []
  );
  const paydaySchema = useMemo(
    () =>
      yup.number().when(['recurs', 'recurrenceType'], {
        is: (recurs, recurrenceType) => recurs && recurrenceType === 'semimonthly',
        then: yup
          .number()
          .integer()
          .required('Day of month is required for semimonthly recurrences')
          .cast(),
        otherwise: yup.number(),
      }),
    []
  );

  // Toggle bottom nav bar when inputs are focused, to prevent it from obscuring text on mobile screens:
  const focusHandler = useCallback(
    (evt) => {
      uiStore.toggleBottomNav(false);
    },
    [uiStore]
  );
  const blurHandler = useCallback(
    (cb) => (evt) => {
      uiStore.toggleBottomNav(true);
      cb(evt);
    },
    [uiStore]
  );

  let { id, categories = '' } = useParams();
  const isNew = !id;
  let categoryPath = categories.replace(/\//g, '.');
  let pathSegments = categoryPath.split('.');
  let category = Categories.get(categoryPath);
  let eventType = pathSegments[0];

  const event = id
    ? eventStore.getEvent(id)
    : new CashFlowEvent({
        category: categoryPath,
        dateTime: uiStore.selectedDate,
      });

  if (id && event) {
    categoryPath = event.category;
    category = Categories.get(categoryPath);
    pathSegments = categoryPath.split('.');
    eventType = pathSegments[0];
    logger.log('Editing existing event: %O', event);
  }

  const recurrenceOptions = useMemo(() => {
    const rules = category.recurrenceTypes ? pluck(recurrenceRules, category.recurrenceTypes) : recurrenceRules;
    return Object.entries(rules).map(([value, { label }]) => ({ label, value }));
  }, [category]);

  if (id && !eventStore.eventsLoaded) return null;

  if (isNew && !category) return <Redirect to="/calendar/add" />;

  return (
    <section className="add-event">
      <BackButton variant="secondary" onClick={() => history.goBack()}>
        Back
      </BackButton>

      <h2 className="add-event__title">{category.name}</h2>
      <p className="add-event__intro">Enter your {category.name.toLowerCase()} details.</p>

      <Formik
        initialValues={event.toFormValues()}
        validationSchema={yup.object({
          name: yup.string(),
          totalCents: yup
            .number('Total must be a number')
            .integer()
            .positive('Total must be greater than $0.00')
            .required('Total is required'),
          dateTime: yup.date('Must be a valid date').required('Date is required'),
          recurrenceType: yup.string().when('recurs', {
            is: true,
            then: yup.string().required('Frequency is required for recurring transactions'),
            otherwise: yup.string(),
          }),
          payday1: paydaySchema,
          payday2: paydaySchema,
        })}
        onSubmit={(values) => {
          if (!values.name) values.name = category.name;

          logger.debug('Event form submission: %O', values);
          logger.debug('Category %s', categoryPath);

          values.totalCents = Number.parseInt(values.totalCents, 10);
          values.dateTime = DateTime.fromFormat(values.dateTime, 'yyyy-MM-dd');

          if (eventType === 'expense') values.totalCents = -values.totalCents;

          if (values.recurs) {
            const { handler } = recurrenceRules[values.recurrenceType];
            values.recurrenceRule =
              values.recurrenceType === 'semimonthly'
                ? handler(values.dateTime.toJSDate(), values.payday1, values.payday2)
                : handler(values.dateTime.toJSDate());
          }

          try {
            eventStore.createEvent(values);
            history.push('/calendar');
          } catch (err) {
            logger.error(err);
            uiStore.setError(err);
          }
        }}
      >
        {(formik) => (
          <form onSubmit={formik.handleSubmit}>
            <TextField
              name="name"
              id="name"
              label="Description"
              onChange={formik.handleChange}
              onFocus={focusHandler}
              onBlur={blurHandler(formik.handleBlur)}
              value={formik.values.name}
              errors={formik.errors.name}
              touched={formik.touched.name}
              tabIndex="0"
              placeholder={category.name}
            />

            <CurrencyField
              id="totalCents"
              name="totalCents"
              label="Pay Amount"
              onChange={formik.handleChange}
              onFocus={focusHandler}
              onBlur={blurHandler(formik.handleBlur)}
              value={formik.values.totalCents}
              errors={formik.errors.totalCents}
              touched={formik.touched.totalCents}
              tabIndex="0"
              required
            />

            <DateField
              id="dateTime"
              name="dateTime"
              label={eventType === 'expense' ? 'Due Date' : 'Pay Date'}
              onChange={formik.handleChange}
              onFocus={focusHandler}
              onBlur={blurHandler(formik.handleBlur)}
              value={formik.values.dateTime || ''}
              errors={formik.errors.dateTime}
              touched={formik.touched.dateTime}
              tabIndex="0"
              required
            />

            <Checkbox
              id="recurs"
              name="recurs"
              label="Recurring?"
              checked={formik.values.recurs}
              onChange={formik.handleChange}
              tabIndex="0"
            />

            {formik.values.recurs && (
              <SelectField
                id="recurrenceType"
                name="recurrenceType"
                label="Frequency"
                options={recurrenceOptions}
                value={formik.values.recurrenceType}
                onChange={formik.handleChange}
                onBlur={formik.handleBlur}
                errors={formik.errors.recurrenceType}
                touched={formik.touched.recurrenceType}
                required={formik.values.recurs}
                tabIndex="0"
              />
            )}

            {formik.values.recurs && formik.values.recurrenceType === 'semimonthly' && (
              <>
                <SelectField
                  id="payday1"
                  name="payday1"
                  label="First Payday"
                  options={monthDayOptions}
                  onChange={formik.handleChange}
                  onBlur={formik.handleBlur}
                  value={formik.values.payday1}
                  required={formik.values.recurrenceType === 'semimonthly'}
                  tabIndex="0"
                />
                <SelectField
                  id="payday2"
                  name="payday2"
                  label="Second Payday"
                  options={monthDayOptions}
                  onChange={formik.handleChange}
                  onBlur={formik.handleBlur}
                  value={formik.values.payday2}
                  required={formik.values.recurrenceType === 'semimonthly'}
                  tabIndex="0"
                />
              </>
            )}

            <Button fullWidth disabled={!formik.dirty && !formik.isValid} type="submit" tabIndex="0">
              Save
            </Button>
          </form>
        )}
      </Formik>
    </section>
  );
}

export default withRouter(observer(Form));
