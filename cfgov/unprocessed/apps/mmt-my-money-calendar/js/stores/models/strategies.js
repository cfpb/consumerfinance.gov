export class StrategyAnalyzer {
  constructor(strategies = []) {
    this.strategies = strategies;
  }

  analyzeExpenses(expenses) {

  }
}

export const Strategies = new StrategyAnalyzer([
  {
    weekHasCategory: 'expense.housing.mortgage',
    text: 'Contact your mortgage company to find out if you could split your payment into two payments per month',
  },
  {
    weekHasCategory: 'expense.housing.rent',
    text: 'Contact your landlord to find out if you could split your payment into two payments per month',
  },
  {
    weekHasCategory: ['expense.utilities.fuel', 'expense.utilities.waterSewage'],
    isLargestBillableExpense: true,
    text: 'Contact your utility company to find out about budget billing',
  },
  {
    weekHasCategory: ['expense.transportation.carPayment', 'expense.transportation.carInsurance'],
    isLargestBillableExpense: true,
    text: 'Contact your car loan company to find out if you could move the due date of this bill to a week where you have more income or fewer expenses.',
  },
  {
    weekHasCategory: [
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
    weekHasCategory: [
      'expense.debt.medicalBill',
      'expense.debt.personalLoan',
    ],
    isLargestBillableExpense: true,
    text: 'Contact your creditor to find out if you could move the due date of this bill to a week where you have more income or fewer expenses.',
  },
  {
    weekHasCategory: 'expense.debt.creditCard',
    isLargestBillableExpense: true,
    text: 'Contact your credit card company to find out if you could move the due date of this bill to a week where you have more income or fewer expenses.',
  },
  {
    weekHasCategory: 'expense.debt.studentLoan',
    isLargestBillableExpense: true,
    text: 'Contact your student loan company to find out if you could move the due date of this bill to a week where you have more income or fewer expenses.',
  }
]);

export default Strategies;
