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
            hasBill: true,
          },
          rent: {
            name: 'Rent',
            recurrenceTypes: ['weekly', 'monthly'],
            hasBill: true,
          },
          propertyTaxes: {
            name: 'Property Taxes',
            recurrenceTypes: ['monthly'],
            hasBill: true,
          },
          rentersInsurance: {
            name: 'Renters Insurance',
            recurrenceTypes: ['monthly'],
            hasBill: true,
          },
          homeownersInsurance: {
            name: 'Homeowners Insurance',
            recurrenceTypes: ['monthly'],
            hasBill: true,
          },
        },
      },
      utilities: {
        name: 'Utilities',
        subcategories: {
          fuel: {
            name: 'Natural Gas, Oil, Propane',
            recurrenceTypes: ['monthly'],
            hasBill: true,
          },
          waterSewage: {
            name: 'Water/Sewage',
            recurrenceTypes: ['monthly'],
            hasBill: true,
          },
          electricity: {
            name: 'Electricity',
            recurrenceTypes: ['monthly'],
            hasBill: true,
          },
          trash: {
            name: 'Trash',
            recurrenceTypes: ['monthly'],
            hasBill: true,
          },
          cable: {
            name: 'Cable/Satellite',
            recurrenceTypes: ['monthly'],
            hasBill: true,
          },
          internet: {
            name: 'Internet',
            recurrenceTypes: ['monthly'],
            hasBill: true,
          },
          phone: {
            name: 'Phone/Cell',
            recurrenceTypes: ['monthly'],
            hasBill: true,
          },
        },
      },
      transportation: {
        name: 'Transportation',
        subcategories: {
          carPayment: {
            name: 'Car Payment',
            recurrenceTypes: ['monthly'],
            hasBill: true,
          },
          carMaintenance: {
            name: 'Car Maintenance',
            hasBill: false,
          },
          carInsurance: {
            name: 'Car Insurance',
            recurrenceTypes: ['monthly'],
            hasBill: true,
          },
          gas: {
            name: 'Gas',
            recurrenceTypes: ['weekly'],
            hasBill: false,
          },
          publicTransportation: {
            name: 'Public Transportation Fare',
            recurrenceTypes: ['weekly', 'monthly'],
            hasBill: false,
          },
        },
      },
      food: {
        name: 'Food',
        subcategories: {
          eatingOut: {
            name: 'Eating Out',
            recurrenceTypes: ['weekly', 'monthly'],
            hasBill: false,
          },
          groceries: {
            name: 'Groceries',
            recurrenceTypes: ['weekly', 'monthly'],
            hasBill: false,
          },
        },
      },
      personal: {
        name: 'Personal',
        subcategories: {
          emergencySavings: {
            name: 'Emergency Savings',
            recurrenceTypes: ['weekly', 'monthly'],
            hasBill: false,
          },
          healthcare: {
            name: 'Health Care',
            recurrenceTypes: ['weekly', 'monthly'],
            hasBill: false,
          },
          subscriptions: {
            name: 'Subscriptions',
            recurrencetypes: ['weekly', 'monthly'],
            hasBill: true,
          },
          clothing: {
            name: 'Clothing',
            hasBill: false,
          },
          giving: {
            name: 'Giving',
            recurrencetypes: ['weekly', 'monthly'],
            hasBill: false,
          },
          education: {
            name: 'Education',
            recurrencetypes: ['weekly', 'monthly'],
            hasBill: true,
          },
          childCare: {
            name: 'Child Care',
            recurrencetypes: ['weekly', 'monthly'],
            hasBill: true,
          },
          personalCare: {
            name: 'Personal Care/Cosmetics',
            recurrencetypes: ['weekly', 'monthly'],
            hasBill: false,
          },
          pets: {
            name: 'Pets',
            recurrencetypes: ['weekly', 'monthly'],
            hasBill: false,
          },
          householdSupplies: {
            name: 'Household Supplies',
            recurrencetypes: ['weekly', 'monthly'],
            hasBill: false,
          },
          funMoney: {
            name: 'Fun Money',
            recurrencetypes: ['weekly', 'monthly'],
            hasBill: false,
          },
        },
      },
      debt: {
        name: 'Debt',
        subcategories: {
          medicalBill: {
            name: 'Medical Bill',
            recurrencetypes: ['weekly', 'monthly'],
            hasBill: true,
          },
          courtOrderedExpenses: {
            name: 'Court-Ordered Expenses',
            recurrencetypes: ['weekly', 'monthly'],
            hasBill: true,
          },
          personalLoan: {
            name: 'Personal Loan',
            recurrencetypes: ['monthly'],
            hasBill: true,
          },
          creditCard: {
            name: 'Credit Card',
            recurrencetypes: ['monthly'],
            hasBill: true,
          },
          studentLoan: {
            name: 'Student Loan',
            recurrencetypes: ['monthly'],
            hasBill: true,
          },
        },
      },
    },
  },
});
