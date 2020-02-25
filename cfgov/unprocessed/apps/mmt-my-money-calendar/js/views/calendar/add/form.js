import { observer } from 'mobx-react';
import { useMemo } from 'react';
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
import { useScrollToTop } from '../../../components/scroll-to-top';
import Logger from '../../../lib/logger';
import CashFlowEvent from '../../../stores/models/cash-flow-event';

function Form() {
  useScrollToTop();

  const { uiStore, eventStore } = useStore();
  const history = useHistory();
  const logger = useMemo(() => Logger.addGroup('eventForm'), []);
  const recurrenceOptions = useMemo(
    () => Object.entries(recurrenceRules).map(([value, { label }]) => ({ label, value })),
    []
  );
  const monthDayOptions = useMemo(
    () => [...range(1, 30)].map((num) => ({ label: numberWithOrdinal(num), value: num })),
    []
  );
  const paydaySchema = useMemo(() => yup.number().when(['recurs', 'recurrenceType'], {
    is: (recurs, recurrenceType) => recurs && recurrenceType === 'semimonthly',
    then: yup.number().integer().required().cast(),
    otherwise: yup.number(),
  }), []);

  let { id, categories = '' } = useParams();
  const isNew = !id;
  let categoryPath = categories.replace(/\//g, '.');
  let pathSegments = categoryPath.split('.');
  let category = Categories.get(categoryPath);
  let eventType = pathSegments[0];

  const event = id ? eventStore.getEvent(id) : new CashFlowEvent({
    category: categoryPath,
    dateTime: uiStore.selectedDate,
  });

  if (id && !eventStore.eventsLoaded) return null;

  if (isNew && !category)
    return <Redirect to="/calendar/add" />;

  if (id && event) {
    categoryPath = event.category;
    category = Categories.get(categoryPath);
    pathSegments = categoryPath.split('.');
    eventType = pathSegments[0];
    logger.log('Editing existing event: %O', event);
  }

  return (
    <section className="add-event">
      <BackButton variant="secondary" onClick={() => history.goBack()}>Back</BackButton>
      <h2 className="add-event__title">{category.name}</h2>
      <p className="add-event__intro">Enter your {category.name.toLowerCase()} details.</p>

      <Formik
        initialValues={event.toFormValues()}
        validationSchema={yup.object({
          name: yup.string(),
          totalCents: yup.number().integer().positive().required(),
          dateTime: yup.date().required(),
          recurrenceType: yup.string().when('recurs', {
            is: true,
            then: yup.string().required(),
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
            const { handler } = recurrenceRules[values.recurrenceRule];
            values.recurrenceRule = values.recurrenceRule === 'semimonthly'
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
              onBlur={formik.handleBlur}
              value={formik.values.name}
              errors={formik.errors.name}
              touched={formik.touched.name}
            />

            <CurrencyField
              id="totalCents"
              name="totalCents"
              label="Pay Amount"
              onChange={formik.handleChange}
              onBlur={formik.handleBlur}
              value={formik.values.totalCents}
              errors={formik.errors.totalCents}
              touched={formik.touched.totalCents}
            />

            <DateField
              id="dateTime"
              name="dateTime"
              label={eventType === 'expense' ? 'Due Date' : 'Pay Date'}
              onChange={formik.handleChange}
              onBlur={formik.handleBlur}
              value={formik.values.dateTime || ''}
              errors={formik.errors.dateTime}
              touched={formik.touched.dateTime}
            />

            <Checkbox
              id="recurs"
              name="recurs"
              label="Recurring?"
              checked={formik.values.recurs}
              onChange={formik.handleChange}
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
                />
                <SelectField
                  id="payday2"
                  name="payday2"
                  label="Second Payday"
                  options={monthDayOptions}
                  onChange={formik.handleChange}
                  onBlur={formik.handleBlur}
                  value={formik.values.payday2}
                />
              </>
            )}

            <Button fullWidth disabled={!formik.dirty && !formik.isValid} type="submit">Save</Button>
          </form>
        )}
      </Formik>
    </section>
  );
}

export default withRouter(observer(Form));
