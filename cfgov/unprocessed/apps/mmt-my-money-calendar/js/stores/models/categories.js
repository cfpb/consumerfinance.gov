import { computed, observable } from 'mobx';
import dotProp from 'dot-prop';
import { isEmpty, filterProps } from '../../lib/object-helpers';
import icons from '../../lib/category-icons';

export class CategoryTree {
  static internalProps = [
    'name',
    'icon',
    'description',
    'restricted',
    'recurrenceTypes',
    'strategy',
    'hasBill',
    'hasRestrictions',
    'allowableExpenses'
  ];

  @observable categories = {};

  constructor(categories = {}) {
    this.categories = categories;
  }

  get all() {
    return this.categories;
  }

  get(path = '') {
    if (!path) return this.all;
    const normalizedPath = path.replace(/\//g, '.');
    return dotProp.get(this.categories, normalizedPath);
  }

  childrenOf(path = '') {
    const category = typeof path === 'string' ? this.get(path) : path;
    const children = filterProps(category, this.constructor.internalProps);
    return isEmpty(children) ? null : children;
  }

  hasSubcategories(category = {}) {
    return Object.keys(category).filter( key => !this.constructor.internalProps.includes(key)).length > 0;
  }

  isChildOf(childName, parentName) {
    let result = false;
    const childKey = childName.match(/\.([^\.]+)$/)[1];
    const parent = this.get(parentName);

    if (!this.hasSubcategories(parent)) return false;
    /* eslint-disable-next-line */
    this.recurseSubcategories(parentName, key => {
      if (key === childKey) {
        result = true;
        return false;
      }
    });

    return result;
  }

  recurseSubcategories(category, cb) {
    const children = this.childrenOf(category);

    if (!children) return;

    for (const [key, child] of Object.entries(children)) {
      /* eslint-disable-next-line */
      const retVal = cb(key, child);
      if (retVal === false) return;
      if (this.hasSubcategories(child)) this.recurseSubcategories(child, cb);
    }
  }
}

export const Categories = new CategoryTree({
  income: {
    name: 'Income',
    startingBalance: {
      name: 'Starting Balance',
      restricted: true,
      recurrenceTypes: []
    },
    salary: {
      name: 'Job',
      icon: icons.job,
      recurrenceTypes: ['weekly', 'biweekly', 'monthly', 'semimonthly'],
      strategy: {
        id: 'directDeposit',
        icon1: icons.paycheck1,
        title: 'Direct Deposit',
        body: 'Sign up for direct deposit as a safer and faster option for your paycheck.',
        link: {
          href: 'https://www.consumerfinance.gov/ask-cfpb/should-i-enroll-in-direct-deposit-en-1027/',
          text: 'See more'
        }
      }
    },
    benefits: {
      name: 'Benefits',
      icon: icons.benefits,
      va: {
        name: 'Veterans Benefits',
        icon: icons.veteransBenefits,
        recurrenceTypes: ['monthly'],
        strategy: {
          id: 'vetBenefits',
          icon1: icons.veteransBenefits1,
          title: 'Explore Military Financial Resources',
          body:
            'Manage financial challenges at every step of your military career.',
          link: {
            href: 'https://www.consumerfinance.gov/consumer-tools/military-financial-lifecycle/',
            text: 'Navigating the Military Financial Lifecycle'
          }
        }
      },
      disability: {
        name: 'Disability Benefits',
        icon: icons.disabilityBenefits,
        recurrenceTypes: ['monthly'],
        strategy: {
          id: 'disabilityBenefits',
          icon1: icons.disabilityBenefits1,
          title: 'Tools for People With Disabilities',
          body:
            'Find tips and skill-building resources for people with disabilities.',
          link: {
            href: 'https://www.consumerfinance.gov/about-us/blog/new-financial-empowerment-tools-people-disabilities/',
            text: 'Focus on People with Disabilities Guide'
          }
        }
      },
      socialSecurity: {
        name: 'Social Security Benefits',
        icon: icons.socialSecurity,
        recurrenceTypes: ['monthly']
      },
      unemployment: {
        name: 'Unemployment',
        icon: icons.unemployment,
        recurrenceTypes: ['monthly'],
        strategy: {
          id: 'jobTraining',
          icon1: icons.unemployment1,
          title: 'Build Your Skills',
          body:
            'Find job training opportunities at your local Career One-Stop.',
          link: {
            href: 'https://www.careeronestop.org/localhelp/americanjobcenters/find-american-job-centers.aspx',
            text: 'Locate an American Job Center'
          }
        }
      },
      tanf: {
        name: 'TANF',
        icon: icons.tanf,
        recurrenceTypes: ['monthly']
      },
      snap: {
        name: 'SNAP',
        icon: icons.snap,
        recurrenceTypes: ['monthly'],
        hasRestrictions: true,
        allowableExpenses: ['expense.food.groceries']
      }
    },
    other: {
      name: 'Other',
      icon: icons.other,
      description: 'Includes child support payments, etc.',
      recurrenceTypes: ['weekly', 'biweekly', 'monthly', 'semimonthly']
    }
  },
  expense: {
    name: 'Expense',
    housing: {
      name: 'Housing',
      icon: icons.housing,
      mortgage: {
        name: 'Mortgage',
        icon: icons.mortgage,
        recurrenceTypes: ['monthly'],
        hasBill: true,
        strategy: {
          id: 'refinanceMortgage',
          icon1: icons.mortgage1,
          title: 'Refinance Your Mortgage',
          body:
            'Check with your mortgage lender to see if you qualify for a lower interest rate.  Then enter the new payment amount into the calendar.',
          link: {
            href: 'https://www.consumerfinance.gov/mortgage/',
            text: 'Answers to Your Mortgage Questions'
          }
        }
      },
      rent: {
        name: 'Rent',
        icon: icons.rent,
        recurrenceTypes: ['weekly', 'monthly', 'biweekly'],
        hasBill: true
      },
      propertyTaxes: {
        name: 'Property Tax',
        icon: icons.propertyTaxes,
        recurrenceTypes: ['monthly'],
        hasBill: true
      },
      rentersInsurance: {
        name: 'Renters Insurance',
        icon: icons.rentersInsurance,
        recurrenceTypes: ['monthly'],
        hasBill: true
      },
      homeownersInsurance: {
        name: 'Homeowners Insurance',
        icon: icons.homeownersInsurance,
        recurrenceTypes: ['monthly'],
        hasBill: true
      }
    },
    utilities: {
      name: 'Utilities',
      icon: icons.utilities,
      fuel: {
        name: 'Natural Gas',
        icon: icons.naturalgas,
        recurrenceTypes: ['monthly', 'biweekly'],
        hasBill: true,
        strategy: {
          id: 'utilityPaymentPlansGas',
          icon1: icons.naturalGas1,
          title: 'Payment Plans for Utilities',
          body:
            'Check with your gas company to see if you qualify.  Then enter the new bill amount into the calendar to see your cash flow.'
        }
      },
      waterSewage: {
        name: 'Water/Sewage',
        icon: icons.water,
        recurrenceTypes: ['monthly', 'biweekly'],
        hasBill: true
      },
      electricity: {
        name: 'Electricity',
        icon: icons.electricity,
        recurrenceTypes: ['monthly', 'biweekly'],
        hasBill: true,
        strategy: {
          id: 'utilityPaymentPlansElectric',
          icon1: icons.electricity1,
          title: 'Payment Plans for Utilities',
          body:
            'Check with your electric company to see if you qualify.  Then enter the new monthly amount into the calendar.'
        }
      },
      trash: {
        name: 'Trash',
        icon: icons.trash,
        recurrenceTypes: ['monthly', 'biweekly'],
        hasBill: true
      },
      cable: {
        name: 'Cable/Satellite',
        icon: icons.cable,
        recurrenceTypes: ['monthly', 'biweekly'],
        hasBill: true,
        strategy: {
          id: 'cablePlans',
          icon1: icons.cable1,
          title: 'Entertainment Options',
          body:
            'Contact your cable company to ask about lower-cost plans or consider a cheaper streaming service.'
        }
      },
      internet: {
        name: 'Internet',
        icon: icons.internet,
        recurrenceTypes: ['monthly', 'biweekly'],
        hasBill: true,
        strategy: {
          id: 'lifelineInternet',
          icon1: icons.internet1,
          title: 'Low Cost Internet Services',
          body:
            'If you qualify for the "Lifeline" program, you could lower the monthly cost of internet service.',
          link: {
            href: 'https://www.fcc.gov/consumers/guides/lifeline-support-affordable-communications',
            text: 'Explore Lifeline'
          }
        }
      },
      phone: {
        name: 'Phone/Cell',
        icon: icons.phone,
        recurrenceTypes: ['monthly', 'biweekly'],
        hasBill: true,
        strategy: {
          id: 'lifelinePhone',
          icon1: icons.phone1,
          title: 'Low Cost Phone Service',
          body:
            'If you qualify for the "Lifeline" program, you could lower the monthly cost of phone service.',
          link: {
            href: 'https://www.fcc.gov/consumers/guides/lifeline-support-affordable-communications',
            text: 'Explore Lifeline'
          }
        }
      }
    },
    transportation: {
      name: 'Transportation',
      icon: icons.transportation,
      carPayment: {
        name: 'Car Payment',
        icon: icons.carPayment,
        recurrenceTypes: ['monthly'],
        hasBill: true,
        strategy: {
          id: 'refinanceCarLoan',
          icon1: icons.carPayment1,
          title: 'Refinance Your Car Loan',
          body:
            'Check with local car loan companies to see if you qualify for a lower interest rate.  Then enter the new expense into the calendar to see how it affects your cash flow.',
          link: {
            href: 'https://www.consumerfinance.gov/consumer-tools/auto-loans/',
            text: 'Car Loans'
          }
        }
      },
      carMaintenance: {
        name: 'Car Maintenance',
        icon: icons.carMaintenance,
        hasBill: false,
        strategy: {
          id: 'carMaintenance',
          icon1: icons.carMaintenance1,
          title: 'Maintain Your Car',
          body:
            'Regularly change your oil and maintain proper tire pressure to avoid some car repair expenses.'
        }
      },
      carInsurance: {
        name: 'Car Insurance',
        icon: icons.carInsurance,
        recurrenceTypes: ['monthly'],
        hasBill: true,
        strategy: {
          id: 'compareInsuranceRates',
          icon1: icons.carInsurance1,
          title: 'Shop Around for Car Insurance',
          body:
            'Get free quotes from other insurance companies to see if you qualify for a lower rate.'
        }
      },
      gas: {
        name: 'Gas',
        icon: icons.gas,
        recurrenceTypes: ['weekly'],
        hasBill: false
      },
      publicTransportation: {
        name: 'Public Transportation Fare',
        icon: icons.publicTransportationFare,
        recurrenceTypes: ['weekly', 'monthly'],
        hasBill: false,
        strategy: {
          id: 'compareTransportationOptions',
          icon1: icons.publicTransportation1,
          title: 'Compare Fare Options',
          body:
            'If you often use public transportation, a monthly pass may be a cheaper option than paying for each ride.'
        }
      }
    },
    food: {
      name: 'Food',
      icon: icons.food,
      eatingOut: {
        name: 'Eating Out',
        icon: icons.eatingOut,
        recurrenceTypes: ['weekly', 'monthly'],
        hasBill: false,
        strategy: {
          id: 'reduceFoodExpenses',
          icon1: icons.eatingOut1,
          title: 'Reduce Eating Out Costs',
          body:
            'Making your lunch, avoiding fountain drinks and even finding local restaurants with "Kids Eat Free" specials can help reduce costs.'
        }
      },
      groceries: {
        name: 'Groceries',
        icon: icons.groceries,
        recurrenceTypes: ['weekly', 'monthly'],
        hasBill: false
      }
    },
    emergencySavings: {
      name: 'Savings',
      icon: icons.emergencySavings,
      recurrenceTypes: ['weekly', 'monthly'],
      hasBill: false
    },
    personal: {
      name: 'Personal',
      icon: icons.personal,
      healthcare: {
        name: 'Health Care',
        icon: icons.healthcare,
        recurrenceTypes: ['weekly', 'monthly'],
        hasBill: false,
        strategy: {
          id: 'healthCare',
          icon1: icons.healthCare1,
          title: 'Health Insurance',
          body:
            'Health insurance can drastically reduce the costs of unforeseen medical bills.  Find a plan that fits your budget.',
          link: {
            href: 'https://www.healthcare.gov',
            text: 'HealthCare.gov'
          }
        }
      },
      subscriptions: {
        name: 'Subscription',
        icon: icons.subscriptions,
        recurrenceTypes: ['weekly', 'monthly'],
        hasBill: true,
        strategy: {
          id: 'cancelSubscriptions',
          icon1: icons.subscriptions1,
          title: 'Subscriptions',
          body: 'Remove auto-renew for subscriptions and cancel those you no longer use or need.'
        }
      },
      clothing: {
        name: 'Clothing',
        icon: icons.clothing,
        hasBill: false,
        strategy: {
          id: 'secondHandClothing',
          icon1: icons.clothing1,
          title: 'Consider Second-hand Shops',
          body:
            'Thrift shops and consignment stores are more cost-effective alternatives to retail.'
        }
      },
      giving: {
        name: 'Giving',
        icon: icons.giving,
        recurrenceTypes: ['weekly', 'monthly'],
        hasBill: false,
        strategy: {
          id: 'trackDonations',
          icon1: icons.giving1,
          title: 'Donations',
          body:
            'Your charitable donations may be tax deductible. Keep records and receipts to lower the cost of your annual taxes.'
        }
      },
      education: {
        name: 'Education',
        icon: icons.education,
        recurrenceTypes: ['weekly', 'monthly'],
        hasBill: true
      },
      childCare: {
        name: 'Child Care',
        icon: icons.childCare,
        recurrenceTypes: ['weekly', 'monthly'],
        hasBill: true,
        strategy: {
          id: 'childCareAssistance',
          icon1: icons.childCare1,
          title: 'Get Childcare Assistance',
          body:
            'See if you qualify for free or reduced rate childcare.',
          link: {
            href: 'https://www.childcare.gov/consumer-education/get-help-paying-for-child-care',
            text: 'Get Help Paying for Childcare'
          }
        }
      },
      personalCare: {
        name: 'Personal Care/Cosmetics',
        icon: icons.personalCareCosmetics,
        recurrenceTypes: ['weekly', 'monthly'],
        hasBill: false
      },
      pets: {
        name: 'Pet',
        icon: icons.pets,
        recurrenceTypes: ['weekly', 'monthly'],
        hasBill: false
      },
      householdSupplies: {
        name: 'Household Supplies',
        icon: icons.householdSupplies,
        recurrenceTypes: ['weekly', 'monthly'],
        hasBill: false
      },
      funMoney: {
        name: 'Fun Money',
        icon: icons.funMoney,
        recurrenceTypes: ['weekly', 'monthly'],
        hasBill: false
      }
    },
    debt: {
      name: 'Debt',
      icon: icons.debt,
      strategy: {
        id: 'dealWithDebt',
        icon1: icons.debt,
        title: "Explore CFPB's Resources for Dealing With Debt",
        body:
          "Whether you're about to receive a medical procedure or are having trouble paying your medical bills, there are things you can do to help keep medical debt in check.",
        link: {
          href:
            'https://www.consumerfinance.gov/practitioner-resources/your-money-your-goals/toolkit/#dealing-with-debt',
          text: 'Dealing with Debt'
        }
      },
      medicalBill: {
        name: 'Medical Bill',
        icon: icons.medicalBill,
        recurrenceTypes: ['weekly', 'monthly'],
        hasBill: true,
        strategy: {
          id: 'medicaidCHIP',
          icon1: icons.medicalBill1,
          title: 'Health Care',
          body:
            'Health insurance can drastically reduce the costs of unforeseen medical bills.  Find a plan that fits your budget.',
          link: {
            href:
              'https://www.healthcare.gov',
            text: 'HealthCare.gov'
          }
        }
      },
      courtOrderedExpenses: {
        name: 'Court-Ordered Fee',
        icon: icons.courtOrderedExpenses,
        recurrenceTypes: ['weekly', 'monthly'],
        hasBill: true
      },
      personalLoan: {
        name: 'Personal Loan',
        icon: icons.personalLoan,
        recurrenceTypes: ['monthly'],
        hasBill: true
      },
      creditCard: {
        name: 'Credit Card',
        icon: icons.creditCard,
        recurrenceTypes: ['monthly'],
        hasBill: true
      },
      studentLoan: {
        name: 'Student Loan',
        icon: icons.studentLoan,
        recurrenceTypes: ['monthly'],
        hasBill: true,
        strategy: {
          id: 'studentLoanRepayment',
          icon1: icons.studentLoan1,
          title: 'Explore Repayment Options',
          body:
            'You have choices when repaying student loans. Make sure your plan works for you.',
          link: {
            href: 'https://www.consumerfinance.gov/paying-for-college/repay-student-debt/',
            text: 'Repay student debt'
          }
        }
      }
    },
    other: {
      name: 'Other',
      icon: icons.other,
      recurrenceTypes: ['monthly', 'weekly'],
      hasBill: false
    }
  }
});
