import { observer } from 'mobx-react';
import { useMemo } from 'react';
import { useFormik } from 'formik';
import { useParams, useHistory, Redirect, withRouter } from 'react-router-dom';
import * as yup from 'yup';
import { DateTime } from 'luxon';
import dotProp from 'dot-prop';
import { useStore } from '../../../stores';
import { Categories } from '../../../stores/models/cash-flow-event';
import Button, { ButtonLink } from '../../../components/button';
import { TextField, DateField, Checkbox, CurrencyField, RadioButton, SelectField } from '../../../components/forms';
import { recurrenceRules, numberWithOrdinal } from '../../../lib/calendar-helpers';
import { range } from '../../../lib/array-helpers';
import Logger from '../../../lib/logger';

function Form() {
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
  const { categories = '' } = useParams();
  const categoryPath = categories.replace(/\//g, '.');
  const category = Categories.get(categoryPath);
  const eventType = categoryPath.split('.')[0];

  const formik = useFormik({
    initialValues: {
      name: '',
      totalCents: 0,
      dateTime: uiStore.selectedDate ? uiStore.selectedDate.toFormat('yyyy-MM-dd') : '',
      recurs: false,
      recurrenceRule: undefined,
      payday1: 15,
      payday2: 30,
    },
    validationSchema: yup.object({
      name: yup.string(),
      totalCents: yup.number().integer().required(),
      dateTime: yup.date().required(),
      recurs: yup.boolean(),
      recurrenceRule: yup.string(),
      payday1: yup.number().when(['recurs', 'recurrenceRule'], {
        is: (recurs, recurrenceRule) => recurs && recurrenceRule === 'semimonthly',
        then: yup.number().integer().required().cast(),
        otherwise: yup.number(),
      }),
      payday2: yup.number().when(['recurs', 'recurrenceRule'], {
        is: (recurs, recurrenceRule) => recurs && recurrenceRule === 'semimonthly',
        then: yup.number().integer().required().cast(),
        otherwise: yup.number(),
      }),
    }),
    onSubmit: (values) => {
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
        eventStore.createEvent({
          ...values,
          category: categoryPath,
        });
        history.push('/calendar');
      } catch (err) {
        logger.error(err);
        uiStore.setError(err);
      }
    },
  });

  /*
  if (!uiStore.selectedCategory)
    return <Redirect to="/calendar/add" />;
    */

  return (
    <section className="add-event">
      <h2 className="add-event__title">{category.name}</h2>
      <p className="add-event__intro">Enter your {category.name.toLowerCase()} details.</p>

      <form onSubmit={formik.handleSubmit}>
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
          value={formik.values.dateTime}
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
            id="recurrenceRule"
            name="recurrenceRule"
            label="Frequency"
            options={recurrenceOptions}
            value={formik.values.recurrenceRule}
            onChange={formik.handleChange}
            onBlur={formik.handleBlur}
          />
        )}

        {formik.values.recurs && formik.values.recurrenceRule === 'semimonthly' && (
          <SelectField
            id="payday1"
            name="payday1"
            label="First Payday"
            options={monthDayOptions}
            onChange={formik.handleChange}
            onBlur={formik.handleBlur}
            value={formik.values.payday1}
          />
        )}

        {formik.values.recurs && formik.values.recurrenceRule === 'semimonthly' && (
          <SelectField
            id="payday2"
            name="payday2"
            label="Second Payday"
            options={monthDayOptions}
            onChange={formik.handleChange}
            onBlur={formik.handleBlur}
            value={formik.values.payday2}
          />
        )}

        <Button type="submit">Save</Button>
      </form>
    </section>
  );
}

export default withRouter(observer(Form));
