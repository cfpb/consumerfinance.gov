import CashFlowEvent from './stores/models/cash-flow-event';
import { DateTime } from 'luxon';
import { RRule } from 'rrule';

let currentDate;
const now = DateTime.local().startOf('day');
const randDay = (max = 30) => {
  const date = now.plus({ days: Math.floor(Math.random() * max) + 1 }).toJSDate();
  currentDate = date;
  return date;
};

export async function seedData() {
  await seedCashFlowEvents();
}

export async function clearData() {
  await clearCashFlowEvents();
}

export async function clearCashFlowEvents() {
  const { store, tx } = await CashFlowEvent.transaction('readwrite');
  await store.clear();
  return tx.complete;
}

function seedCashFlowEvents() {
  const events = [
    {
      name: 'Starting Balance',
      date: now.toJSDate(),
      totalCents: 50000,
      category: 'startingBalance',
    },
    {
      name: 'Paycheck',
      date: randDay(),
      category: 'Job',
      totalCents: 30000,
      recurs: true,
      recurrenceRule: new RRule({
        freq: RRule.WEEKLY,
        dtstart: currentDate,
        count: 12,
      }),
    },
    {
      name: 'Rent',
      date: randDay(),
      category: 'Housing',
      subcategory: 'Rent',
      totalCents: -80000,
      recurs: true,
      recurrenceRule: new RRule({
        freq: RRule.MONTHLY,
        count: 3,
        dtstart: currentDate,
      }),
    },
    {
      name: 'Groceries',
      date: randDay(),
      category: 'Groceries',
      totalCents: -20000,
      recurs: true,
      recurrenceRule: new RRule({
        freq: RRule.WEEKLY,
        dtstart: currentDate,
        count: 12,
      }),
    },
  ];

  return Promise.all(events.map((event) => {
    const cfe = new CashFlowEvent(event);
    console.log('Add event: %O', cfe.asObject);
    return cfe.save();
  }));
}
