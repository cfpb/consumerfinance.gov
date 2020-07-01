import { computed, action, observable } from 'mobx';
import { compact } from '../lib/array-helpers';
import logger from '../lib/logger';
import { Categories } from './models/categories';

class StrategiesStore {
  negativeStrategies = {
    'expense.personal.coronavirus': {
      id: 'coronaVirus',
      title: 'Protect Your Finances During the Coronavirus Pandemic',
      body:
        'The CFPB is committed to providing consumers with up-to-date information and resources to protect and manage their finances during this difficult time.',
      link: {
        href: ' https://www.consumerfinance.gov/coronavirus/',
        text: 'Tools and Resources',
      },
    },
    'expense.personal.emergencySavings': {
      id: 'saveForEmergencies',
      title: 'Save for Emergencies',
      body: 'Saving helps reduce stress when the unexpected happens.',
      link: {
        href: 'https://www.consumerfinance.gov/about-us/blog/how-save-emergencies-and-future/',
        text: 'How to save for emergencies and the future',
      },
    },
  };

  fixItStrategies = {
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
        categories: ['expense.utilities.fuel', 'expense.utilities.waterSewage', 'expense.utilities.electricity'],
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
        template: (categoryName) =>
          `Your ${categoryName.toLowerCase()} expense was your largest expense this week not tied to a bill you are obligated to pay. Consider spending a little less this week and a little more in weeks where you have fewer expenses or more income.`,
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
    return this.analyzeFixItEvents(this.eventsForWeek);
  }

  @computed get fixItResults() {
    const results = compact(
      Object.entries(this.fixItWeekAnalysis).map(([type, event]) => {
        if (!event || event.hideFixItStrategy) return;

        const strategy = this.fixItStrategies[type].find((sgy) => sgy.categories.includes(event.category));

        if (!strategy) return;

        strategy.event = event;

        if (strategy.template && typeof strategy.template === 'function') {
          strategy.text = strategy.template(event.categoryDetails.name);
        }

        return strategy;
      })
    );

    if (results.length) return results;

    return [
      {
        title: 'Explore Your General Strategies',
        text:
          "Based upon your weekly transactions we can't recommend any Fix-It Strategies. Make sure that you've entered in all of your expenses and income for the week then check back here later.  Otherwise, review the generic strategies below.",
      },
    ];
  }

  @computed get strategyResults() {
    const strategyIDs = new Set();
    const list = this.eventStore.eventCategories.map((catPath) => {
      const { strategy } = Categories.get(catPath) || {};
      return strategy;
    });
    for (const [catPath, strategy] of Object.entries(this.negativeStrategies)) {
      if (!this.eventStore.eventCategories.includes(catPath)) {
        list.push(strategy);
      }
    }

    let reversedList = [...list].reverse();

    return compact(reversedList).filter((item) => {
      if (strategyIDs.has(item.id)) return false;
      strategyIDs.add(item.id);
      this.logger.debug('Strategy IDs set: %O', strategyIDs);
      return true;
    });
  }

  analyzeFixItEvents(events) {
    return events.reduce(
      (results, event) => {
        if (event.totalCents < 0 && !event.categoryDetails.hasBill) {
          if (this.fixItStrategies['largestAdHocExpense'].find((sgy) => sgy.categories.includes(event.category))) {
            if (!results.largestAdHocExpense || results.largestAdHocExpense.isLessThan(event)) {
              results.largestAdHocExpense = event;
            }
          }
        }

        if (event.categoryDetails.hasBill) {
          if (!event.category.includes('expense.housing')) {
            if (this.fixItStrategies['largestBillableExpense'].find((sgy) => sgy.categories.includes(event.category))) {
              if (!results.largestBillableExpense || results.largestBillableExpense.isLessThan(event)) {
                results.largestBillableExpense = event;
              }
            }
          }
        }

        if (/^expense\.housing/.test(event.category)) {
          if (!results.largestHousingExpense || results.largestHousingExpense.isLessThan(event)) {
            results.largestHousingExpense = event;
          }
        }

        return results;
      },
      {
        largestAdHocExpense: undefined,
        largestBillableExpense: undefined,
        largestHousingExpense: undefined,
      }
    );
  }
}

export default StrategiesStore;
