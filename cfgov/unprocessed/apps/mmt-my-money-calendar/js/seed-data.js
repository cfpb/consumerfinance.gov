import CashFlowEvent from './stores/models/cash-flow-event';
import { DateTime } from 'luxon';
import { RRule } from 'rrule';

const now = DateTime.local();
const randDay = (max = 30) => now.plus(Math.floor(Math.random() * max) + 1).toJSDate();

export async function seedData() {
  await seedCashFlowEvents();
}

function seedCashFlowEvents() {
  let currentDate;

  const events = [
    {
      name: 'Starting Balance',
      date: now.toJSDate(),
      totalCents: 50000,
      category: 'startingBalance',
    },
    {
      name: 'Paycheck',
      date: currentDate = randDay(),
      category: 'Job',
      totalCents: 30000,
      recurs: true,
      recurrence: new RRule({
        freq: RRule.WEEKLY,
        byweekday: RRule.FR,
        dtstart: currentDate,
        count: 12,
      }).toString(),
    },
    {
      name: 'Rent',
      date: currentDate = randDay(),
      category: 'Housing',
      subcategory: 'Rent',
      totalCents: 80000,
      recurs: true,
      recurrence: new RRule({
        freq: RRule.MONTHLY,
        count: 3,
        dtstart: currentDate,
      }).toString(),
    },
  ];

  return Promise.all(events.map((event) => {
    const cfe = new CashFlowEvent(event);
    return cfe.save();
  }));
}
