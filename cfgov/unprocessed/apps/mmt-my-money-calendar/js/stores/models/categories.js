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
    'allowableExpenses',
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
    return Object.keys(category).filter((key) => !this.constructor.internalProps.includes(key)).length > 0;
  }

  isChildOf(childName, parentName) {
    let result = false;
    const childKey = childName.match(/\.([^\.]+)$/)[1];
    const parent = this.get(parentName);

    if (!this.hasSubcategories(parent)) return false;

    this.recurseSubcategories(parentName, (key) => {
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
      recurrenceTypes: [],
    },
    salary: {
      name: 'Job',
      icon: icons.job,
      recurrenceTypes: ['weekly', 'biweekly', 'monthly', 'semimonthly'],
      strategy: {
        id: 'directDeposit',
        title: 'Sign Up for Direct Deposit',
        body: 'Direct deposit may help you to avoid fees and interest associated with Check Cashing.',
        link: {
          href: 'https://www.consumerfinance.gov/ask-cfpb/should-i-enroll-in-direct-deposit-en-1027/',
          text: 'Should I enroll in direct deposit?',
        },
      },
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
          title: "Explore CFPB's Military Financial Resources",
          body:
            'These tools, designed specifically for service members, can help you manage financial challenges at every step of your military career.',
          link: {
            href: 'https://www.consumerfinance.gov/consumer-tools/military-financial-lifecycle/',
            text: 'Navigating the Military Financial Lifecycle',
          },
        },
      },
      disability: {
        name: 'Disability Benefits',
        icon: icons.disabilityBenefits,
        recurrenceTypes: ['monthly'],
        strategy: {
          id: 'disabilityBenefits',
          title: 'Explore the Focus on People with Disabilities Companion Guides',
          body:
            'These guides contains tips, information, tools, and skill-building resources for people with disabilities and from organizations that serve the disability community.',
          link: {
            href: 'https://www.consumerfinance.gov/about-us/blog/new-financial-empowerment-tools-people-disabilities/',
            text: 'Focus on People with Disabilities Guides',
          },
        },
      },
      socialSecurity: {
        name: 'Social Security Benefits',
        icon: icons.socialSecurity,
        recurrenceTypes: ['monthly'],
      },
      unemployment: {
        name: 'Unemployment',
        icon: icons.unemployment,
        recurrenceTypes: ['monthly'],
        strategy: {
          id: 'jobTraining',
          title: 'Explore CareerOneStop Job Training Opportunities',
          link: {
            href: 'https://www.careeronestop.org/localhelp/americanjobcenters/find-american-job-centers.aspx',
            text: 'Find your nearest American Job Center',
          },
        },
      },
      tanf: {
        name: 'TANF',
        icon: icons.tanf,
        recurrenceTypes: ['monthly'],
      },
      snap: {
        name: 'SNAP',
        icon: icons.snap,
        recurrenceTypes: ['monthly'],
        hasRestrictions: true,
        allowableExpenses: ['expense.food.groceries'],
      },
    },
    other: {
      name: 'Other',
      icon: icons.other,
      description: 'Includes child support payments, etc.',
      recurrenceTypes: ['weekly', 'biweekly', 'monthly', 'semimonthly'],
    },
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
          title: 'Refinance your mortgage',
          body:
            'Check with your mortgage lender to see if you qualify, then enter the new expense into the calendar to see how it affects your cash flow.',
          link: {
            href: 'https://www.consumerfinance.gov/owning-a-home/',
            text: 'Tools and resources for homebuyers',
          },
        },
      },
      rent: {
        name: 'Rent',
        icon: icons.rent,
        recurrenceTypes: ['weekly', 'monthly', 'biweekly'],
        hasBill: true,
      },
      propertyTaxes: {
        name: 'Property Tax',
        icon: icons.propertyTaxes,
        recurrenceTypes: ['monthly'],
        hasBill: true,
      },
      rentersInsurance: {
        name: 'Renters Insurance',
        icon: icons.rentersInsurance,
        recurrenceTypes: ['monthly'],
        hasBill: true,
      },
      homeownersInsurance: {
        name: 'Homeowners Insurance',
        icon: icons.homeownersInsurance,
        recurrenceTypes: ['monthly'],
        hasBill: true,
      },
    },
    utilities: {
      name: 'Utilities',
      icon: icons.utilities,
      fuel: {
        name: 'Natural Gas, Oil, Propane',
        icon: icons.naturalgas,
        recurrenceTypes: ['monthly', 'biweekly'],
        hasBill: true,
        strategy: {
          id: 'utilityPaymentPlans',
          title: 'Explore Level Payment Plans for Utilities',
          body:
            'Also known as budget billing, these plans average your bills out over the year. Check with your utility providers to see if you qualify, then enter the new monthly average into the calendar to see how it affects your cash flow.',
        },
      },
      waterSewage: {
        name: 'Water/Sewage',
        icon: icons.water,
        recurrenceTypes: ['monthly', 'biweekly'],
        hasBill: true,
        strategy: {
          id: 'utilityPaymentPlans',
          title: 'Explore Level Payment Plans for Utilities',
          body:
            'Also known as budget billing, these plans average your bills out over the year. Check with your utility providers to see if you qualify, then enter the new monthly average into the calendar to see how it affects your cash flow.',
        },
      },
      electricity: {
        name: 'Electricity',
        icon: icons.electricity,
        recurrenceTypes: ['monthly', 'biweekly'],
        hasBill: true,
        strategy: {
          id: 'utilityPaymentPlans',
          title: 'Explore Level Payment Plans for Utilities',
          body:
            'Also known as budget billing, these plans average your bills out over the year. Check with your utility providers to see if you qualify, then enter the new monthly average into the calendar to see how it affects your cash flow.',
        },
      },
      trash: {
        name: 'Trash',
        icon: icons.trash,
        recurrenceTypes: ['monthly', 'biweekly'],
        hasBill: true,
      },
      cable: {
        name: 'Cable/Satellite',
        icon: icons.cable,
        recurrenceTypes: ['monthly', 'biweekly'],
        hasBill: true,
        strategy: {
          id: 'cablePlans',
          title: 'Consider Entertainment Alternatives',
          body:
            'Many cable providers offer multiple options for new and existing customers. Contact your provider and ask about lower-cost plans or consider a cheaper streaming service.',
          link: {
            href: 'https://www.consumerfinance.gov/practitioner-resources/your-money-your-goals/toolkit/',
            text: 'Cutting Expenses (Your Money Your Goals)',
          },
        },
      },
      internet: {
        name: 'Internet',
        icon: icons.internet,
        recurrenceTypes: ['monthly', 'biweekly'],
        hasBill: true,
        strategy: {
          id: 'lifelinePhoneInternet',
          title: 'Explore Low Cost Phone and Internet Services',
          body:
            'If you qualify for the FCC\'s "Lifeline" phone rate you could lower the monthly cost of phone and internet service.',
          link: {
            href: 'https://www.fcc.gov/consumers/guides/lifeline-support-affordable-communications',
            text: 'Lifeline Support for Affordable Communications',
          },
        },
      },
      phone: {
        name: 'Phone/Cell',
        icon: icons.phone,
        recurrenceTypes: ['monthly', 'biweekly'],
        hasBill: true,
        strategy: {
          id: 'lifelinePhoneInternet',
          title: 'Explore Low Cost Phone and Internet Services',
          body:
            'If you qualify for the FCC\'s "Lifeline" phone rate you could lower the monthly cost of phone and internet service.',
          link: {
            href: 'https://www.fcc.gov/consumers/guides/lifeline-support-affordable-communications',
            text: 'Lifeline Support for Affordable Communications',
          },
        },
      },
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
          title: 'Refinance your car loan',
          body:
            'Check with your auto lender to see if you qualify, then enter the new expense into the calendar to see how it affects your cash flow.',
          link: {
            href: 'https://www.consumerfinance.gov/consumer-tools/auto-loans/',
            text: 'Car Loans',
          },
        },
      },
      carMaintenance: {
        name: 'Car Maintenance',
        icon: icons.carMaintenance,
        hasBill: false,
        strategy: {
          id: 'carMaintenance',
          title: 'Regularly maintain your car to cut repair costs',
          body:
            'Preventive measures (e.g., regularly changing your oil, maintaining proper tire pressure) can help you avoid car repair expenses.',
        },
      },
      carInsurance: {
        name: 'Car Insurance',
        icon: icons.carInsurance,
        recurrenceTypes: ['monthly'],
        hasBill: true,
        strategy: {
          id: 'compareInsuranceRates',
          title: 'Compare the Rates of Other Insurance Companies',
          body:
            'Most car Insurance providers offer quotes over the phone or online. Research other providers and reenter their quotes into the calendar to see how much you could save.',
        },
      },
      gas: {
        name: 'Gas',
        icon: icons.gas,
        recurrenceTypes: ['weekly'],
        hasBill: false,
        strategy: {
          id: 'carpoolRideShare',
          title: 'Carpool or Ride Share',
          body:
            'Carpooling or ridesharing can save a lot on fuel costs as well as allow you access to HOV lanes, freeing up money for your budget and shortening your commute.',
        },
      },
      publicTransportation: {
        name: 'Public Transportation Fare',
        icon: icons.publicTransportationFare,
        recurrenceTypes: ['weekly', 'monthly'],
        hasBill: false,
        strategy: {
          id: 'compareTransportationOptions',
          title: 'Compare Transportation Options',
          body:
            'Evaluate your avaliable modes of transportation to discover cheaper alternatives that can put more money in your budget.',
        },
      },
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
          title: 'Reduce your Expenses while eating out',
          body:
            'Preparing your lunch, avoiding fountain drinks and even finding local restaurants with specials, like "kids eat free" nights, can help reduce this expense.',
        },
      },
      groceries: {
        name: 'Grocery',
        icon: icons.groceries,
        recurrenceTypes: ['weekly', 'monthly'],
        hasBill: false,
        strategy: {
          id: 'reduceGroceryExpenses',
          title: 'Reduce your Grocery Expenses',
          body:
            'Using coupons and buying groceries and supplies in bulk with other family or friends can help reduce your grocery costs and put more money in your budget.',
        },
      },
    },
    emergencySavings: {
      name: 'Savings',
      icon: icons.emergencySavings,
      recurrenceTypes: ['weekly', 'monthly'],
      hasBill: false,
    },
    personal: {
      name: 'Personal',
      icon: icons.personal,
      healthcare: {
        name: 'Health Care',
        icon: icons.healthcare,
        recurrenceTypes: ['weekly', 'monthly'],
        hasBill: false,
      },
      subscriptions: {
        name: 'Subscription',
        icon: icons.subscriptions,
        recurrenceTypes: ['weekly', 'monthly'],
        hasBill: true,
        strategy: {
          id: 'cancelSubscriptions',
          title: 'Cancel Unnecessary Subscriptions',
          body: 'Remove auto-renew for subscriptions and cancel those you no longer use or need.',
        },
      },
      clothing: {
        name: 'Clothing',
        icon: icons.clothing,
        hasBill: false,
        strategy: {
          id: 'secondHandClothing',
          title: 'Consider Second-hand Shops',
          body:
            'Buying clothes and accessorits through classifieds ads, thrift shops, and consignment stores are much more cost effective alternatives to retail.',
          link: {
            href: 'https://www.consumerfinance.gov/about-us/blog/track-your-spending-with-this-easy-tool/',
            text: 'Track your spending with this easy tool',
          },
        },
      },
      giving: {
        name: 'Giving',
        icon: icons.giving,
        recurrenceTypes: ['weekly', 'monthly'],
        hasBill: false,
        strategy: {
          id: 'trackDonations',
          title: 'Keep track of Your Donations',
          body:
            'Your charitable donations my be tax deductible. Keep records and receipts of these exchanges to lower the cost of your annual taxes.',
          link: {
            href: 'https://www.irs.gov/charities-non-profits/charitable-contributions',
            text: 'Charitable Donations',
          },
        },
      },
      education: {
        name: 'Education',
        icon: icons.education,
        recurrenceTypes: ['weekly', 'monthly'],
        hasBill: true,
      },
      childCare: {
        name: 'Child Care',
        icon: icons.childCare,
        recurrenceTypes: ['weekly', 'monthly'],
        hasBill: true,
        strategy: {
          id: 'childCareAssistance',
          title: 'Get Child Care assistance',
          body:
            'There are a number of financial aid programs designed to help parents struggling with childcare costs. Enrolling in these programs could free more money in your budget.',
          link: {
            href: 'https://www.childcare.gov/consumer-education/get-help-paying-for-child-care',
            text: 'Get Help Paying for Childcare',
          },
        },
      },
      personalCare: {
        name: 'Personal Care/Cosmetics',
        icon: icons.personalCareCosmetics,
        recurrenceTypes: ['weekly', 'monthly'],
        hasBill: false,
      },
      pets: {
        name: 'Pet',
        icon: icons.pets,
        recurrenceTypes: ['weekly', 'monthly'],
        hasBill: false,
      },
      householdSupplies: {
        name: 'Household Supplies',
        icon: icons.householdSupplies,
        recurrenceTypes: ['weekly', 'monthly'],
        hasBill: false,
      },
      funMoney: {
        name: 'Fun Money',
        icon: icons.funMoney,
        recurrenceTypes: ['weekly', 'monthly'],
        hasBill: false,
      },
    },
    debt: {
      name: 'Debt',
      icon: icons.debt,
      strategy: {
        id: 'dealWithDebt',
        title: "Explore CFPB's Resources for Dealing With Debt",
        body:
          "Whether you're about to receive a medical procedure or are having trouble paying your medical bills, there are things you can do to help keep medical debt in check.",
        link: {
          href:
            'https://www.consumerfinance.gov/practitioner-resources/your-money-your-goals/toolkit/#dealing-with-debt',
          text: 'Dealing with Debt',
        },
      },
      medicalBill: {
        name: 'Medical Bill',
        icon: icons.medicalBill,
        recurrenceTypes: ['weekly', 'monthly'],
        hasBill: true,
        strategy: {
          id: 'medicaidCHIP',
          title: 'Sign up for Medicaid and CHIP',
          body:
            'Seek help with paying medical bills, because receiving timely medical care can help you maintain your earning potential.',
          link: {
            href:
              'https://www.consumerfinance.gov/practitioner-resources/your-money-your-goals/toolkit/#dealing-with-debt',
            text: 'Avoiding Medical Debt',
          },
        },
      },
      courtOrderedExpenses: {
        name: 'Court-Ordered Fee',
        icon: icons.courtOrderedExpenses,
        recurrenceTypes: ['weekly', 'monthly'],
        hasBill: true,
      },
      personalLoan: {
        name: 'Personal Loan',
        icon: icons.personalLoan,
        recurrenceTypes: ['monthly'],
        hasBill: true,
      },
      creditCard: {
        name: 'Credit Card',
        icon: icons.creditCard,
        recurrenceTypes: ['monthly'],
        hasBill: true,
      },
      studentLoan: {
        name: 'Student Loan',
        icon: icons.studentLoan,
        recurrenceTypes: ['monthly'],
        hasBill: true,
        strategy: {
          id: 'studentLoanRepayment',
          title: 'Explore Repayment Options',
          body:
            'You have choices when it comes to repaying student loans. Make sure you have the repayment plan that works best for you.',
          link: {
            href: 'https://www.consumerfinance.gov/paying-for-college/repay-student-debt/',
            text: 'Repay student debt',
          },
        },
      },
    },
    other: {
      name: 'Other',
      icon: icons.other,
      recurrenceTypes: ['monthly', 'weekly'],
      hasBill: false,
    },
  },
});
