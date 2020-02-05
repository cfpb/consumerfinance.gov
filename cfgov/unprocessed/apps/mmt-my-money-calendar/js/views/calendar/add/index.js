import clsx from 'clsx';
import { observer } from 'mobx-react';
import { useFormik } from 'formik';
import { useStore } from '../../../stores';
import Button from '../../../components/button';
import { TextField, Checkbox, CurrencyField, RadioButton } from '../../../components/forms';
import * as Yup from 'yup';

function Add() {
  const { uiStore, eventStore } = useStore();
  const formik = useFormik({
    initialValues: {
      name: '',
      total: 0,
    },
    validationSchema: Yup.object({
      name: Yup.string().required(),
      totalCents: Yup.number().integer().required(),
    }),
    onSubmit: (values) => {

    }
  });

  return (
    <section className="add-event">
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

        <TextField
          id="name"
          name="name"
          label="Description"
          onChange={formik.handleChange}
          value={formik.values.name}
          onBlur={formik.handleBlur}
        />

        <TextField
          id="category"
          name="category"
          label="Category"
          onChange={formik.handleChange}
          onBlur={formik.handleBlur}
          value={formik.values.category}
        />

        <TextField
          id="subcategory"
          name="subcategory"
          label="Subcategory"
          onChange={formik.handleChange}
          onBlur={formik.handleBlur}
          value={formik.values.subcategory}
        />

        <CurrencyField
          id="totalCents"
          name="totalCents"
          label="Amount"
          onChange={formik.handleChange}
          onBlur={formik.handleBlur}
          value={formik.values.total}
        />


        {formik.touched.name && formik.errors.name ? (
          <strong>{formik.errors.name}</strong>
        ) : null}

        <pre>
          Form State:
          {JSON.stringify(formik.values, null, 2)}

          Errors:
          {JSON.stringify(formik.errors, null, 2)}
        </pre>

        <Button type="submit">Save</Button>
      </form>
    </section>
  );
}

export default observer(Add);
