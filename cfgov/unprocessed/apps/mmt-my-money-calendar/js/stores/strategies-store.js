import { computed, action, observable } from 'mobx';
import { compact } from '../lib/array-helpers';
import logger from '../lib/logger';

class StrategiesStore {
  strategies = {
    largestHousingExpense: [
      {
        categories: ['expense.housing.mortgage'],
        text: 'Contact your mortgage company to find out if you could split your payment into two payments per month',
      },
      {
        categories: ['expense.housing.rent'],
        text: 'Contact your landlord to find out if you could split your payment into two payments per month',
      },
    ],
    largestBillableExpense: [
      {
        categories: ['expense.utilities.fuel', 'expense.utilities.waterSewage'],
        text: 'Contact your utility company to find out about budget billing',
      },
      {
        categories: ['expense.transportation.carPayment', 'expense.transportation.carInsurance'],
        text:
          'Contact your car loan company to find out if you could move the due date of this bill to a week where you have more income or fewer expenses.',
      },
      {
        categories: ['expense.debt.medicalBill', 'expense.debt.personalLoan'],
        text:
          'Contact your creditor to find out if you could move the due date of this bill to a week where you have more income or fewer expenses.',
      },
      {
        categories: ['expense.debt.creditCard'],
        text:
          'Contact your credit card company to find out if you could move the due date of this bill to a week where you have more income or fewer expenses.',
      },
      {
        categories: ['expense.debt.studentLoan'],
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
        text: (categoryName) =>
          `${categoryName} was your largest expense this week not tied to a bill you are obligated to pay. Consider spending a little less this week and a little more in weeks where you have fewer expenses or more income.`,
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
    return this.eventStore.getEventsForWeek(this.uiStore.currentWeek);
  }

  @computed get weekAnalysis() {
    return this.analyzeEvents(this.eventsForWeek);
  }

  @computed get strategyResults() {
    return compact(
      Object.entries(this.weekAnalysis).map(([type, event]) => {
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
