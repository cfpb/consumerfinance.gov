import { computed, action, observable } from 'mobx';
import { compact } from '../lib/array-helpers';
import logger from '../lib/logger';

const isPlural = (word) => word.endsWith('s');

class StrategiesStore {
  strategies = {
    largestHousingExpense: [
      {
        categories: ['expense.housing.mortgage'],
        title: 'Split Mortgage Payments',
        text: 'Contact your mortgage company to find out if you could split your payment into two payments per month',
      },
      {
        categories: ['expense.housing.rent'],
        title: 'Split Rent Payments',
        text: 'Contact your landlord to find out if you could split your payment into two payments per month',
      },
    ],
    largestBillableExpense: [
      {
        categories: ['expense.utilities.fuel', 'expense.utilities.waterSewage'],
        title: 'Budget Utility Billing',
        text: 'Contact your utility company to find out about budget billing',
      },
      {
        categories: ['expense.transportation.carPayment', 'expense.transportation.carInsurance'],
        title: 'Move Due Date',
        text:
          'Contact your car loan company to find out if you could move the due date of this bill to a week where you have more income or fewer expenses.',
      },
      {
        categories: ['expense.debt.medicalBill', 'expense.debt.personalLoan'],
        title: 'Move Due Date',
        text:
          'Contact your creditor to find out if you could move the due date of this bill to a week where you have more income or fewer expenses.',
      },
      {
        categories: ['expense.debt.creditCard'],
        title: 'Move Due Date',
        text:
          'Contact your credit card company to find out if you could move the due date of this bill to a week where you have more income or fewer expenses.',
      },
      {
        categories: ['expense.debt.studentLoan'],
        title: 'Move Due Date',
        text:
          'Contact your student loan company to find out if you could move the due date of this bill to a week where you have more income or fewer expenses.',
      },
    ],
    largestAdHocExpense: [
      {
        categories: [
          'expense.transportation.publicTransportation',
          'expense.transportation.gas',
          'expense.food.eatingOut',
          'expense.food.groceries',
          'expense.personal.clothing',
          'expense.personal.personalCare',
          'expense.personal.funMoney',
        ],
        title: 'Adjust Spending this Week',
        text: (categoryName) =>
          `${categoryName} ${isPlural(categoryName) ? 'were' : 'was'} your largest expense this week not tied to a bill you are obligated to pay. Consider spending a little less this week and a little more in weeks where you have fewer expenses or more income.`,
      },
    ],
  };

  constructor(rootStore) {
    this.rootStore = rootStore;
    this.logger = logger.addGroup('strategiesStore');
    this.uiStore = this.rootStore.uiStore;
    this.eventStore = this.rootStore.eventStore;

    this.logger.debug('Initialize strategies store %O', this);
  }

  @computed get eventsForWeek() {
    return this.eventStore.getEventsForWeek(this.uiStore.currentWeek) || [];
  }

  @computed get fixItWeekAnalysis() {
    if (this.eventStore.getBalanceForDate(this.uiStore.currentWeek.endOf('week')) > 0) return {};
    return this.analyzeEvents(this.eventsForWeek);
  }

  @computed get fixItResults() {
    return compact(
      Object.entries(this.fixItWeekAnalysis).map(([type, event]) => {
        if (!event) return;

        const strategy = this.strategies[type].find((sgy) => sgy.categories.includes(event.category));

        if (!strategy) return;

        strategy.event = event;

        if (typeof strategy.text === 'function') {
          strategy.text = strategy.text(event.categoryDetails.name);
        }

        return strategy;
      })
    );
  }

  analyzeEvents(events) {
    return events.reduce(
      (results, event) => {
        if (/^expense\.housing/.test(event.category)) {
          if (!results.largestHousingExpense || results.largestHousingExpense.isLessThan(event)) {
            results.largestHousingExpense = event;
          }
        }

        if (event.categoryDetails.hasBill) {
          if (!results.largestBillableExpense || results.largestBillableExpense.isLessThan(event)) {
            results.largestBillableExpense = event;
          }
        } else if (event.totalCents < 0 && !event.categoryDetails.hasBill) {
          if (!results.largestAdHocExpense || results.largestAdHocExpense.isLessThan(event)) {
            results.largestAdHocExpense = event;
          }
        }

        return results;
      },
      {
        largestHousingExpense: undefined,
        largestBillableExpense: undefined,
        largestAdHocExpense: undefined,
      }
    );
  }
}

export default StrategiesStore;
