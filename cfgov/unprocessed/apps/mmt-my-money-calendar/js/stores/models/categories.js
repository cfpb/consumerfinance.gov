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
        strategy: {
          title: 'Sign Up for Direct Deposit',
          body: 'Direct deposit may help you to avoid fees and interest associated with Check Cashing.',
          link: 'https://www.consumerfinance.gov/ask-cfpb/should-i-enroll-in-direct-deposit-en-1027/',
        },
      },
      benefits: {
        name: 'Benefits',
        subcategories: {
          va: {
            name: 'Veterans Benefits',
            recurrenceTypes: ['monthly'],
            strategy: {
              title: 'Explore CFPB\'s Military Financial Resources',
              body: 'These tools, designed specifically for servicemembers, can help you manage financial challenges at every step of your military career.',
              link: 'https://www.consumerfinance.gov/consumer-tools/military-financial-lifecycle/',
            },
          },
          disability: {
            name: 'Disability Benefits',
            recurrenceTypes: ['monthly'],
            strategy: {
              title: 'Explore the Focus on People with Disabilities Companion Guides',
              body: 'These guides contains tips, information, tools, and skill-building resources for people with disabilities and from organizations that serve the disability community.',
              link: 'https://www.consumerfinance.gov/about-us/blog/new-financial-empowerment-tools-people-disabilities/',
            },
          },
          socialSecurity: {
            name: 'Social Security Benefits',
            recurrenceTypes: ['monthly'],
          },
          unemployment: {
            name: 'Unemployment',
            recurrenceTypes: ['monthly'],
            strategy: {
              title: 'Explore CareerOneStop Job Training Opportunities',
              link: 'https://www.careeronestop.org/localhelp/americanjobcenters/find-american-job-centers.aspx',
            },
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
            strategy: {
              title: 'Refinance your mortgage',
              body: 'Check with your mortgage lender to see if you qualify, then enter the new expense into the calendar to see how it affects your cash flow.',
              link: 'https://www.consumerfinance.gov/owning-a-home/',
            },
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
            strategy: {
              title: 'Explore Level Payment Plans for Utilities',
              body: 'Also known as budget billing, these plans average your bills out over the year. Check with your utility providers to see if you qualify, then enter the new monthly average into the calendar to see how it affects your cash flow.',
            },
          },
          waterSewage: {
            name: 'Water/Sewage',
            recurrenceTypes: ['monthly'],
            hasBill: true,
            strategy: {
              title: 'Explore Level Payment Plans for Utilities',
              body: 'Also known as budget billing, these plans average your bills out over the year. Check with your utility providers to see if you qualify, then enter the new monthly average into the calendar to see how it affects your cash flow.',
            },
          },
          electricity: {
            name: 'Electricity',
            recurrenceTypes: ['monthly'],
            hasBill: true,
            strategy: {
              title: 'Explore Level Payment Plans for Utilities',
              body: 'Also known as budget billing, these plans average your bills out over the year. Check with your utility providers to see if you qualify, then enter the new monthly average into the calendar to see how it affects your cash flow.',
            },
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
            strategy: {
              title: 'Explore Low Cost Phone and Internet Services',
              body: 'If you qualify for the FCC\'s "Lifeline" phone rate you could lower the monthly cost of phone and internet service.',
            },
          },
          phone: {
            name: 'Phone/Cell',
            recurrenceTypes: ['monthly'],
            hasBill: true,
            strategy: {
              title: 'Explore Low Cost Phone and Internet Services',
              body: 'If you qualify for the FCC\'s "Lifeline" phone rate you could lower the monthly cost of phone and internet service.',
            },
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
            strategy: {
              title: 'Refinance your car loan',
              body: 'Check with your auto lender to see if you qualify, then enter the new expense into the calendar to see how it affects your cash flow.',
              link: 'https://www.consumerfinance.gov/consumer-tools/auto-loans/',
            },
          },
          carMaintenance: {
            name: 'Car Maintenance',
            hasBill: false,
            strategy: {
              title: 'Regularly maintain your car to cut repair costs',
              body: 'Preventive measures (e.g., regularly changing your oil, maintaining proper tire pressure) can help you avoid car repair expenses.',
            },
          },
          carInsurance: {
            name: 'Car Insurance',
            recurrenceTypes: ['monthly'],
            hasBill: true,
            strategy: {
              title: 'Compare the Rates of Other Insurance Companies',
              body: 'Most car Insurance providers offer quote over the phone or online. Research other providers and reenter their quotes into the calendar to see how much you could save.',
            },
          },
          gas: {
            name: 'Gas',
            recurrenceTypes: ['weekly'],
            hasBill: false,
            strategy: {
              title: 'Carpool or Ride Share',
              body: 'Carpooling or ridesharing can save a lot on fuel costs as well as allow you access to HOV lanes, freeing up money for your budget and shortening your commute.',
            },
          },
          publicTransportation: {
            name: 'Public Transportation Fare',
            recurrenceTypes: ['weekly', 'monthly'],
            hasBill: false,
            strategy: {
              title: 'Compare Transportation Options',
              body: 'Evaluate your avaliable modes of transportation to discover cheaper alternatives that can put more money in your budget.',
            },
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
            strategy: {
              title: 'Reduce your Expenses while eating out',
              body: 'Preparing your lunch, avoiding fountain drinks and even finding local restaurants with specials, like "kids eat free" nights, can help reduce this expense.',
            },
          },
          groceries: {
            name: 'Groceries',
            recurrenceTypes: ['weekly', 'monthly'],
            hasBill: false,
            strategy: {
              title: 'Reduce your Grocery Expenses',
              body: 'Using coupons and buying groceries and supplies in bulk with other family or friends can help reduce your grocery costs and put more money in your budget.',
            },
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
            strategyIfMissing: {
              title: 'Save for Emergencies',
              body: 'Saving helps reduce stress when the unexpected happens.',
              link: 'https://www.consumerfinance.gov/about-us/blog/how-save-emergencies-and-future/',
            }
          },
          healthcare: {
            name: 'Health Care',
            recurrenceTypes: ['weekly', 'monthly'],
            hasBill: false,
            strategyIfMissing: {
              title: 'Choose a Health Care Plan That Fits Your Budget',
              body: 'Health insurance can drastically reduce the costs of unforeseen medical bills.',
              link: 'https://www.healthcare.gov/',
            },
          },
          subscriptions: {
            name: 'Subscriptions',
            recurrencetypes: ['weekly', 'monthly'],
            hasBill: true,
            strategy: {
              title: 'Cancel Unnecessary Subscriptions',
              body: 'Remove auto-renew for subscriptions and cancel those you no longer use or need.',
            },
          },
          clothing: {
            name: 'Clothing',
            hasBill: false,
            strategy: {
              title: 'Consider Second-hand Shops',
              body: 'Buying clothes and accessorits through classifieds ads, thrift shops, and consignment stores are much more cost effective alternatives to retail.',
              link: 'https://www.consumerfinance.gov/about-us/blog/track-your-spending-with-this-easy-tool/',
            },
          },
          giving: {
            name: 'Giving',
            recurrencetypes: ['weekly', 'monthly'],
            hasBill: false,
            strategy: {
              title: 'Keep track of Your Donations',
              body: 'Your charitable donations my be tax deductible. Keep records and receipts of these exchanges to lower the cost of your annual taxes.',
              link: 'https://www.irs.gov/charities-non-profits/charitable-contributions',
            },
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
            strategy: {
              title: 'Get Child Care assistance',
              body: 'There are a number of financial aid programs designed to help parents struggling with childcare costs. Enrolling in these programs could free more money in your budget.',
              link: 'https://www.childcare.gov/consumer-education/get-help-paying-for-child-care'
            }
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
        strategy: {
          title: 'Explore CFPB\'s Resources for Dealing With Debt',
          body: 'Whether you\'re about to receive a medical procedure or are having trouble paying your medical bills, there are things you can do to help keep medical debt in check.',
          link: 'https://www.consumerfinance.gov/practitioner-resources/your-money-your-goals/toolkit/#dealing-with-debt',
        },
        subcategories: {
          medicalBill: {
            name: 'Medical Bill',
            recurrencetypes: ['weekly', 'monthly'],
            hasBill: true,
            strategy: {
              title: 'Sign up for Medicaid and CHIP',
              body: 'Seek help with paying medical bills, because receiving timely medical care can help you maintain your earning potential.',
              link: 'https://www.consumerfinance.gov/practitioner-resources/your-money-your-goals/toolkit/#dealing-with-debt',
            },
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
            strategy: {
              title: 'Explore Repayment Options',
              body: 'You have choices when it comes to repaying student loans. Make sure you have the repayment plan that works best for you.',
              link: 'https://www.consumerfinance.gov/paying-for-college/repay-student-debt/',
            }
          },
        },
      },
    },
  },
});
