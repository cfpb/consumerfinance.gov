import { computed, action, observable } from 'mobx';
import { compact } from '../lib/array-helpers';
import logger from '../lib/logger';
import { Categories } from './models/categories';
import icons from '../lib/category-icons';

class StrategiesStore {
  negativeStrategies = {
    'expense.personal.coronavirus': {
      id: 'coronaVirus',
      icon1: icons.coronaVirus1,
      title: 'COVID-19',
      body:
        'Get information about protecting your financial health.',
      link: {
        href: 'https://www.consumerfinance.gov/coronavirus/',
        text: 'Tools and Resources'
      }
    },
    'expense.personal.tightWeek': {
      id: 'tightWeek',
      icon1: icons.paycheck1,
      title: 'Tips for a Tight Week',
      body: 'See how to add more money to your cash flow.',
      link: {
        href: 'https://files.consumerfinance.gov/f/documents/cfpb_your-money-your-goals_increase-inc-benefits_tool_2018-11.pdf',
        text: 'Increase Income and Benefits'
      }
    }
  };

  fixItStrategies = {
    largestHousingExpense: [
      {
        categories: ['expense.housing.mortgage'],
        icon1: icons.mortgage1,
        title: 'Split Mortgage',
        text: 'Ask your mortgage company to find out if you could split your payment into smaller amounts.'
      },
      {
        categories: ['expense.housing.rent'],
        icon1: icons.mortgage1,
        title: 'Rent',
        text: 'If possible, ask your landlord to let you make multiple payments toward rent.  If not, contact a local organization that helps with rental assistance.'
      }
    ],
    largestBillableExpense: [
      {
        categories: ['expense.transportation.carPayment'],
        icon1: icons.carPayment1,
        title: 'Car Payment Date',
        text:
          'Ask your car loan company if you could move the due date to a week with more money.'
      },
      {
        categories: ['expense.transportation.carInsurance'],
        icon1: icons.carInsurance1,
        title: 'Car Insurance Date',
        text:
          'Ask your insurance company if you could move the due date to a week with more money.'
      },
      {
        categories: ['expense.debt.medicalBill'],
        icon1: icons.medicalBill1,
        title: 'Medical Bill',
        text:
          'Ask your creditor if you could move the due date to a week with more money.'
      },
      {
        categories: ['expense.debt.personalLoan'],
        icon1: icons.personalLoan,
        title: 'Loan Due Date',
        text:
          'Ask your lender if you could move the due date to a week with more money.'
      },
      {
        categories: ['expense.debt.creditCard'],
        icon1: icons.creditCard,
        title: 'Credit Card Due Date',
        text:
          'Contact your credit card company to find out if you could move the due date to a week where you have more money.'
      },
      {
        categories: ['expense.debt.studentLoan'],
        icon1: icons.studentLoan1,
        title: 'Student Loan Due Date',
        text:
          'Contact your student loan company to find out if you could move the due date of this bill to a week where you have more money.'
      }
    ],
    largestAdHocExpense: [
      {
        categories: ['expense.transportation.publicTransportation'],
        icon1: icons.studentLoan1,
        title: 'Adjust Transportation Spending',
        text:
          'You control how much you spend on public transportation.  Consider spending less this week until you have more money.'
      },
      {
        categories: ['expense.transportation.gas'],
        icon1: icons.gas1,
        title: 'Adjust Gas Spending',
        text:
          'You control how much you spend on gas.  Consider buying less this week until you have more money.'
      },
      {
        categories: ['expense.food.eatingOut'],
        icon1: icons.eatingOut1,
        title: 'Adjust Spending on Eating Out',
        text:
          'You control how much you spend on in this category.  Consider eating out less this week until you have more money.'
      },
      {
        categories: ['expense.personal.clothing'],
        icon1: icons.clothing1,
        title: 'Adjust Spending on Clothing',
        text:
          'You control how much you spend on clothing.  Consider buying less this week until you have more money.'
      },
      {
        categories: ['expense.personal.personalCare'],
        icon1: icons.personal,
        title: 'Adjust Spending on Personal Care items',
        text:
          'You control how much you spend on personal care.  Consider buying less this week until you have more money.'
      },
      {
        categories: ['expense.personal.funMoney'],
        icon1: icons.funMoney,
        title: 'Adjust Spending with Fun Money',
        text:
          'You control how much you use fun money.  Consider buying less this week until you have more money.'
      }
    ]
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

        const strategy = this.fixItStrategies[type].find( sgy => sgy.categories.includes(event.category));

        if (!strategy) return;

        strategy.event = event;

        if (strategy.template && typeof strategy.template === 'function') {
          strategy.text = strategy.template(event.categoryDetails.name);
        }

        return strategy;
      })
    );

    return results;
  }

  @computed get strategyResults() {
    const strategyIDs = new Set();
    const list = this.eventStore.eventCategories.map( catPath => {
      const { strategy } = Categories.get(catPath) || {};
      return strategy;
    });
    for (const [catPath, strategy] of Object.entries(this.negativeStrategies)) {
      if (!this.eventStore.eventCategories.includes(catPath)) {
        list.push(strategy);
      }
    }

    return compact(list).filter( item => {
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
            /*eslint dot-notation: ["error", { "allowPattern": "^[a-z]+(_[a-z]+)+$" }]*/
            if (this.fixItStrategies["largestBillableExpense"].find( sgy => sgy.categories.includes(event.category))) {
              if (!results.largestBillableExpense || results.largestBillableExpense.isLessThan(event)) {
                results.largestBillableExpense = event;
              }
            }
          }
        }

        if ('/^expense\.housing/'.test(event.category)) {
          if (!results.largestHousingExpense || results.largestHousingExpense.isLessThan(event)) {
            results.largestHousingExpense = event;
          }
        }
        return results;
      },
      {
        largestAdHocExpense: null,
        largestBillableExpense: null,
        largestHousingExpense: null
      }
    );
  }
}

export default StrategiesStore;
