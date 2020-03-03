import dotProp from 'dot-prop';

export class CategoryTree {
  constructor(categories = {}) {
    this.categories = categories;
  }

  get all() {
    return this.categories;
  }

  get(path = '') {
    const normalizedPath = path.replace(/\//g, '.');

    if (normalizedPath.length && !/\./.test(normalizedPath) && this.categories[normalizedPath])
      return dotProp.get(this.categories[normalizedPath], 'subcategories', this.categories[normalizedPath]);

    return dotProp.get(this.categories, normalizedPath.replace(/\./g, '.subcategories.'));
  }
}

export const Categories = new CategoryTree({
  startingBalance: {
    name: 'Starting Balance',
    restricted: true,
    recurrenceTypes: [],
  },
  income: {
    name: 'Income',
    subcategories: {
      salary: {
        name: 'Job',
        description: 'Income from employment',
        recurrenceTypes: ['weekly', 'biweekly', 'monthly', 'semimonthly'],
      },
      benefits: {
        name: 'Benefits',
        subcategories: {
          va: {
            name: 'Veterans Benefits',
            recurrenceTypes: ['monthly'],
          },
          disability: {
            name: 'Disability Benefits',
            recurrenceTypes: ['monthly'],
          },
          ss: {
            name: 'Social Security Benefits',
            recurrenceTypes: ['monthly'],
          },
          unemployment: {
            name: 'Unemployment',
            recurrenceTypes: ['monthly'],
          },
          tanf: {
            name: 'TANF',
            recurrenceTypes: ['monthly'],
          },
          snap: {
            name: 'SNAP',
            recurrenceTypes: ['monthly'],
          },
        },
      },
      other: {
        name: 'Other',
        description: 'Includes child support payments, etc.',
        recurrenceTypes: ['weekly', 'biweekly', 'monthly', 'semimonthly'],
      },
    },
  },
  expense: {
    name: 'Expense',
    subcategories: {
      housing: {
        name: 'Housing',
        subcategories: {
          mortgage: {
            name: 'Mortgage',
            recurrenceTypes: ['monthly'],
          },
          rent: {
            name: 'Rent',
            recurrenceTypes: ['weekly', 'monthly'],
          },
          propertyTaxes: {
            name: 'Property Taxes',
            recurrenceTypes: ['monthly'],
          },
          rentersInsurance: {
            name: 'Renters Insurance',
            recurrenceTypes: ['monthly'],
          },
          homeownersInsurance: {
            name: 'Homeowners Insurance',
            recurrenceTypes: ['monthly'],
          },
        },
      },
      utilities: {
        name: 'Utilities',
        subcategories: {
          fuel: {
            name: 'Natural Gas, Oil, Propane',
            recurrenceTypes: ['monthly'],
          },
          waterSewage: {
            name: 'Water/Sewage',
            recurrenceTypes: ['monthly'],
          },
          electricity: {
            name: 'Electricity',
            recurrenceTypes: ['monthly'],
          },
          trash: {
            name: 'Trash',
            recurrenceTypes: ['monthly'],
          },
          cable: {
            name: 'Cable/Satellite',
            recurrenceTypes: ['monthly'],
          },
          internet: {
            name: 'Internet',
            recurrenceTypes: ['monthly'],
          },
          phone: {
            name: 'Phone/Cell',
            recurrenceTypes: ['monthly'],
          },
        },
      },
      transportation: {
        name: 'Transportation',
        subcategories: {
          carPayment: {
            name: 'Car Payment',
            recurrenceTypes: ['monthly'],
          },
          carMaintenance: {
            name: 'Car Maintenance',
          },
          carInsurance: {
            name: 'Car Insurance',
            recurrenceTypes: ['monthly'],
          },
          gas: {
            name: 'Gas',
            recurrenceTypes: ['weekly'],
          },
          publicTransportation: {
            name: 'Public Transportation Fare',
            recurrenceTypes: ['weekly', 'monthly'],
          },
        },
      },
      food: {
        name: 'Food',
        subcategories: {
          eatingOut: {
            name: 'Eating Out',
            recurrenceTypes: ['weekly', 'monthly'],
          },
          groceries: {
            name: 'Groceries',
            recurrenceTypes: ['weekly', 'monthly'],
          },
        },
      },
      personal: {
        name: 'Personal',
        subcategories: {
          emergencySavings: {
            name: 'Emergency Savings',
            recurrenceTypes: ['weekly', 'monthly'],
          },
          healthcare: {
            name: 'Health Care',
            recurrenceTypes: ['weekly', 'monthly'],
          },
          subscriptions: {
            name: 'Subscriptions',
            recurrencetypes: ['weekly', 'monthly'],
          },
          clothing: {
            name: 'Clothing',
          },
          giving: {
            name: 'Giving',
            recurrencetypes: ['weekly', 'monthly'],
          },
          education: {
            name: 'Education',
            recurrencetypes: ['weekly', 'monthly'],
          },
          childCare: {
            name: 'Child Care',
            recurrencetypes: ['weekly', 'monthly'],
          },
          personalCare: {
            name: 'Personal Care/Cosmetics',
            recurrencetypes: ['weekly', 'monthly'],
          },
          pets: {
            name: 'Pets',
            recurrencetypes: ['weekly', 'monthly'],
          },
          householdSupplies: {
            name: 'Household Supplies',
            recurrencetypes: ['weekly', 'monthly'],
          },
          funMoney: {
            name: 'Fun Money',
            recurrencetypes: ['weekly', 'monthly'],
          },
        },
      },
      debt: {
        name: 'Debt',
        subcategories: {
          medicalBill: {
            name: 'Medical Bill',
            recurrencetypes: ['weekly', 'monthly'],
          },
          courtOrderedExpenses: {
            name: 'Court-Ordered Expenses',
            recurrencetypes: ['weekly', 'monthly'],
          },
          personalLoan: {
            name: 'Personal Loan',
            recurrencetypes: ['monthly'],
          },
          creditCard: {
            name: 'Credit Card',
            recurrencetypes: ['monthly'],
          },
          studentLoan: {
            name: 'Student Loan',
            recurrencetypes: ['monthly'],
          },
        },
      },
    },
  },
});
