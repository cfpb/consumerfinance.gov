import { computed, action, observable } from 'mobx';
import { compact } from '../lib/array-helpers';
import logger from '../lib/logger';
import { Categories } from './models/categories';
import icons from '../lib/category-icons';

class StrategiesStore {
  negativeStrategies = {
    'expense.personal.coronavirus': {
      id: 'coronaVirus',
      icon1: icons.veteranBenefits1,
      title: 'Protect Your Finances from COVID-19',
      body:
        'Get information about protecting your financial health.',
      link: {
        href: ' https://www.consumerfinance.gov/coronavirus/',
        text: 'Tools and Resources',
      },
    },
    'expense.personal.emergencySavings': {
      id: 'saveForEmergencies',
      title: 'Save for Emergencies',
      icon1: icons.veteranBenefits1,
      body: 'Saving helps reduce stress when the unexpected happens.',
      link: {
        href: 'https://www.consumerfinance.gov/about-us/blog/how-save-emergencies-and-future/',
        text: 'How to save for emergencies and the future',
      },
    },
    'expense.personal.tightWeek': {
      id: 'tightWeek',
      title: 'Tips for a tight week',
      icon1: icons.veteranBenefits1,
      body: 'See how to add more money to your cash flow.',
      link: {
        href: '',
        text: 'Increase Income and Benefits',
      },
    },
  };

  fixItStrategies = {
    largestHousingExpense: [
      {
        categories: ['expense.housing.mortgage'],
        title: 'Split Mortgage',
        text: 'Ask your mortgage company to find out if you could split your payment into smaller amounts.',
      },
      {
        categories: ['expense.housing.rent'],
        title: 'Rent',
        text: 'If possible, ask your landlord to let you make multiple payments toward rent.  If not, contact a local organization that helps with rental assistance.',
      },
    ],
    largestBillableExpense: [
      {
        categories: ['expense.transportation.carPayment'],
        title: 'Car Payment Date',
        text:
          'Ask car loan company if you could move the due date to a week with more money.',
      },
      {
        categories: ['expense.transportation.carInsurance'],
        title: 'Car Insurance Date',
        text:
          'Ask your insurance company if you could move the due date to a week with more money.',
      },
      {
        categories: ['expense.debt.medicalBill'],
        title: 'Medical Bill',
        text:
          'Ask your creditor if you could move the due date to a week with more money.',
      },
      {
        categories: ['expense.debt.personalLoan'],
        title: 'Loan Due Date',
        text:
          'Ask your lender if you could move the due date to a week with more money.',
      },
      {
        categories: ['expense.debt.creditCard'],
        title: 'Credit Card Due Date',
        text:
          'Contact your credit card company to find out if you could move the due date to a week where you have more money.',
      },
      {
        categories: ['expense.debt.studentLoan'],
        title: 'Student Loan Due Date',
        text:
          'Contact your student loan company to find out if you could move the due date of this bill to a week where you have more money.',
      },
    ],
    largestAdHocExpense: [
      {
        categories: [
          'expense.transportation.publicTransportation',
          'expense.transportation.gas',
          'expense.food.eatingOut',
          'expense.personal.clothing',
          'expense.personal.personalCare',
          'expense.personal.funMoney',
        ],
        title: (categoryName) =>`Adjust ${categoryName.toLowerCase()} Spending`,
        template: (categoryName) =>
          `You control how much you spend on ${categoryName.toLowerCase()}.  Consider buying less this week until you have more money.`,
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
