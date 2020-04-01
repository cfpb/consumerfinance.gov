import { computed, action, observable } from 'mobx';
import logger from '../lib/logger';

class StrategiesStore {
  strategies = [
    {
      hasCategory: 'expense.housing.mortgage',
      text: 'Contact your mortgage company to find out if you could split your payment into two payments per month',
    },
    {
      hasCategory: 'expense.housing.rent',
      text: 'Contact your landlord to find out if you could split your payment into two payments per month',
    },
    {
      hasCategory: ['expense.utilities.fuel', 'expense.utilities.waterSewage'],
      isLargestBillableExpense: true,
      text: 'Contact your utility company to find out about budget billing',
    },
    {
      hasCategory: ['expense.transportation.carPayment', 'expense.transportation.carInsurance'],
      isLargestBillableExpense: true,
      text: 'Contact your car loan company to find out if you could move the due date of this bill to a week where you have more income or fewer expenses.',
    },
    {
      hasCategory: [
        'expense.transportation.publicTransportation',
        'expense.transportation.gas',
        'expense.food.eatingOut',
        'expense.food.groceries',
        'expense.personal.clothing',
        'expense.personal.personalCare',
        'expense.personal.funMoney',
      ],
      isLargestAdHocExpense: true,
      text: (categoryName) => `${categoryName} was your largest expense this week not tied to a bill you are obligated to pay. Consider spending a little less this week and a little more in weeks where you have fewer expenses or more income.`
    },
    {
      hasCategory: [
        'expense.debt.medicalBill',
        'expense.debt.personalLoan',
      ],
      isLargestBillableExpense: true,
      text: 'Contact your creditor to find out if you could move the due date of this bill to a week where you have more income or fewer expenses.',
    },
    {
      hasCategory: 'expense.debt.creditCard',
      isLargestBillableExpense: true,
      text: 'Contact your credit card company to find out if you could move the due date of this bill to a week where you have more income or fewer expenses.',
    },
    {
      hasCategory: 'expense.debt.studentLoan',
      isLargestBillableExpense: true,
      text: 'Contact your student loan company to find out if you could move the due date of this bill to a week where you have more income or fewer expenses.',
    }
  ];

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

  analyzeEvents(events) {
    return events.reduce((results, event) => {
      if ((/^expense\.housing/).test(event.category)) {
        if (!results.largestHousingExpense || results.largestHousingExpense.isLessThan(event)) {
          results.largestHousingExpense = event;
        }
      }

      if (event.categoryDetails.hasBill) {
        if (!results.largestBillableExpense || results.largestBillableExpense.isLessThan(event)) {
          results.largestBillableExpense = event;
        }
      } else {
        if (!results.largestAdHocExpense || results.largestAdHocExpense.isLessThan(event)) {
          results.largestAdHocExpense = event;
        }
      }

      return results;
    }, {
      largestHousingExpense: undefined,
      largestBillableExpense: undefined,
      largestAdHocExpense: undefined,
    });
  }
}

export default StrategiesStore;
