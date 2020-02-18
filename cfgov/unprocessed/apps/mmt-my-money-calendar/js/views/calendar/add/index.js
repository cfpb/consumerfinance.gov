import clsx from 'clsx';
import { useMemo } from 'react';
import { observer } from 'mobx-react';
import { useFormik } from 'formik';
import { useHistory } from 'react-router-dom';
import * as Yup from 'yup';
import { DateTime } from 'luxon';
import { useStore } from '../../../stores';
import { Categories } from '../../../stores/models/cash-flow-event';
import Button, { ButtonLink } from '../../../components/button';
import { TextField, DateField, Checkbox, CurrencyField, RadioButton, SelectField } from '../../../components/forms';
import { recurrenceRules, numberWithOrdinal } from '../../../lib/calendar-helpers';
import { range } from '../../../lib/array-helpers';

import arrowLeft from '@cfpb/cfpb-icons/src/icons/arrow-left.svg';

function Add() {
  const { uiStore, eventStore } = useStore();
  const history = useHistory();
  const recurrenceOptions = useMemo(
    () => Object.entries(recurrenceRules).map(([value, { label }]) => ({ label, value })),
    []
  );
  const monthDayOptions = useMemo(
    () => [...range(1, 30)].map((num) => ({ label: numberWithOrdinal(num), value: num })),
    []
  );
  const formik = useFormik({
    initialValues: {
      name: '',
      totalCents: 0,
      category: undefined,
      eventType: undefined,
      dateTime: uiStore.selectedDate ? uiStore.selectedDate.toFormat('yyyy-MM-dd') : '',
      recurs: false,
      recurrenceRule: undefined,
      payday1: 15,
      payday2: 30,
    },
    validationSchema: Yup.object({
      name: Yup.string().required(),
      totalCents: Yup.number()
        .integer()
        .required(),
      eventType: Yup.string().required(),
      category: Yup.string().required(),
      dateTime: Yup.date().required(),
    }),
    onSubmit: (values) => {
      console.log('Form submit: %O', values);
      if (values.eventType === 'expense') values.totalCents = -values.totalCents;

      values.totalCents = parseInt(values.totalCents, 10);
      values.dateTime = DateTime.fromFormat(values.dateTime, 'yyyy-MM-dd');

      try {
        eventStore.createEvent(values);
        history.push('/calendar');
      } catch (err) {
        console.error(err);
        uiStore.setError(err);
      }
    },
  });

  const categoryOptions = useMemo(() => {
    if (!formik.values.eventType || !Categories[formik.values.eventType]) return [];

    return Object.entries(Categories[formik.values.eventType]).reduce((output, [slug, category]) => {
      if (!category.subcategories) {
        output = [...output, { value: `${formik.values.eventType}.${slug}`, label: category.name }];
        return output;
      }

      const options = Object.entries(category.subcategories).map(([id, subcategory]) => ({
        label: `${category.name} > ${subcategory.name}`,
        value: `${formik.values.eventType}.${slug}.${id}`,
      }));

      output = [...output, ...options];

      return output;
    }, []);
  }, [formik.values.eventType]);

  return (
    <section className="add-event">
      <ButtonLink variant="secondary" to="/calendar" icon={arrowLeft}>
        Back
      </ButtonLink>
      <h1>Add Income and Expenses</h1>

      <form onSubmit={formik.handleSubmit}>
        <label className="a-label">Transaction Type:</label>
        <RadioButton
          id="radio-income"
          name="eventType"
          value="income"
          label="Income"
          onChange={formik.handleChange}
          checked={formik.values.eventType === 'income'}
          largeTarget
        />

        <RadioButton
          id="radio-expense"
          name="eventType"
          value="expense"
          label="Expense"
          onChange={formik.handleChange}
          checked={formik.values.eventType === 'expense'}
          largeTarget
        />

        {formik.errors.eventType && formik.touched.eventType && <div className="error">{formik.errors.eventType}</div>}

        <DateField
          id="dateTime"
          name="dateTime"
          label="Date"
          value={formik.values.dateTime}
          onChange={formik.handleChange}
          onBlur={formik.handleBlur}
        />

        {formik.errors.dateTime && formik.touched.dateTime && <div className="error">{formik.errors.dateTime}</div>}

        <SelectField
          id="category"
          name="category"
          label="Category"
          value={formik.values.category}
          onChange={formik.handleChange}
          onBlur={formik.handleBlur}
          options={categoryOptions}
        />

        {formik.errors.category && formik.touched.category && <div className="error">{formik.errors.category}</div>}

        <TextField
          id="name"
          name="name"
          label="Description"
          onChange={formik.handleChange}
          value={formik.values.name}
          onBlur={formik.handleBlur}
        />

        {formik.errors.description && formik.touched.description && (
          <div className="error">{formik.errors.description}</div>
        )}

        <CurrencyField
          id="totalCents"
          name="totalCents"
          label="Amount"
          onChange={formik.handleChange}
          onBlur={formik.handleBlur}
          value={formik.values.totalCents}
        />

        {formik.errors.totalCents && formik.touched.totalCents && (
          <div className="error">{formik.errors.totalCents}</div>
        )}

        <Checkbox
          id="recurs"
          name="recurs"
          label="Is this a recurring event?"
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
            label="First Payday of the Month"
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
            label="Second Payday of the Month"
            options={monthDayOptions}
            onChange={formik.handleChange}
            onBlur={formik.handleBlur}
            value={formik.values.payday2}
          />
        )}

        <h3>Form State</h3>
        <pre>{JSON.stringify(formik.values, null, 2)}</pre>

        <Button type="submit">Save</Button>
      </form>
    </section>
  );
}

export default observer(Add);
