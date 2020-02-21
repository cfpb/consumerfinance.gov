import { observer } from 'mobx-react';
import { useStore } from '../../../stores';
import { useMemo } from 'react';
import { useFormik } from 'formik';
import { useHistory } from 'react-router-dom';
import * as yup from 'yup';
import { DateTime } from 'luxon';
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
  const formik = useFormik({
    initialValues: {},
    validationSchema: {},
    onSubmit: (values) => {
      logger.debug('Event form submission: %O', values);
    },
  });

  return (
    <section className="add-event">
      <h2>Add some Stuff</h2>
    </section>
  );
}

export default observer(Form);
