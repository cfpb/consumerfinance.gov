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

    if (normalizedPath.length && !(/\./).test(normalizedPath) && this.categories[normalizedPath])
      return this.categories[normalizedPath].subcategories;

    return dotProp.get(this.categories, normalizedPath.replace(/\./g, '.subcategories.'));
  }
}

export const Categories = new CategoryTree({
  income: {
    name: 'Income',
    subcategories: {
      salary: {
        name: 'Job',
        description: 'Income from employment',
      },
      benefits: {
        name: 'Benefits',
        subcategories: {
          va: {
            name: 'Veterans Benefits',
          },
          disability: {
            name: 'Disability Benefits',
          },
          ss: {
            name: 'Social Security Benefits',
          },
          unemployment: {
            name: 'Unemployment',
          },
          tanf: {
            name: 'TANF',
          },
          snap: {
            name: 'SNAP',
          },
        },
      },
      other: {
        name: 'Other',
        description: 'Includes child support payments, etc.',
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
          },
          rent: {
            name: 'Rent',
          },
          propertyTaxes: {
            name: 'Property Taxes',
          },
          rentersInsurance: {
            name: 'Renters Insurance',
          },
          homeownersInsurance: {
            name: 'Homeowners Insurance',
          },
        },
      },
      utilities: {
        name: 'Utilities',
        subcategories: {
          fuel: {
            name: 'Natural Gas, Oil, Propane',
          },
          waterSewage: {
            name: 'Water/Sewage',
          },
          electricity: {
            name: 'Electricity',
          },
          trash: {
            name: 'Trash',
          },
          cable: {
            name: 'Cable/Satellite',
          },
          internet: {
            name: 'Internet',
          },
          phone: {
            name: 'Phone/Cell',
          },
        },
      },
      transportation: {
        name: 'Transportation',
        subcategories: {
          carPayment: {
            name: 'Car Payment',
          },
          carMaintenance: {
            name: 'Car Maintenance',
          },
          carInsurance: {
            name: 'Car Insurance',
          },
          gas: {
            name: 'Gas',
          },
          publicTransportation: {
            name: 'Public Transportation Fare',
          },
        },
      },
      food: {
        name: 'Food',
        subcategories: {
          eatingOut: {
            name: 'Eating Out',
          },
          groceries: {
            name: 'Groceries',
          },
        },
      },
      personal: {
        name: 'Personal',
        subcategories: {
          emergencySavings: {
            name: 'Emergency Savings',
          },
          healthcare: {
            name: 'Health Care',
          },
          subscriptions: {
            name: 'Subscriptions',
          },
          clothing: {
            name: 'Clothing',
          },
          giving: {
            name: 'Giving',
          },
          education: {
            name: 'Education',
          },
          childCare: {
            name: 'Child Care',
          },
          personalCare: {
            name: 'Personal Care/Cosmetics',
          },
          pets: {
            name: 'Pets',
          },
          householdSupplies: {
            name: 'Household Supplies',
          },
          funMoney: {
            name: 'Fun Money',
          },
        },
      },
      debt: {
        name: 'Debt',
        subcategories: {
          medicalBill: {
            name: 'Medical Bill',
          },
          courtOrderedExpenses: {
            name: 'Court-Ordered Expenses',
          },
          personalLoan: {
            name: 'Personal Loan',
          },
          creditCard: {
            name: 'Credit Card',
          },
          studentLoan: {
            name: 'Student Loan',
          },
        },
      },
    },
  },
});
