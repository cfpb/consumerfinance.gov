import { observable, extendObservable, computed, action } from 'mobx';
import { transform } from '../lib/object-helpers';
import logger from '../lib/logger';

const capitalize = (str) => str.charAt(0).toUpperCase() + str.slice(1);

export default class WizardStore {
  fundingSourceOptions = {
    'checking': {
      name: 'Checking Account',
      label: 'How much do you have in your checking account?',
    },
    'savings': {
      name: 'Savings Account',
      label: 'How much do you have in your savings account?',
    },
    'cash': {
      name: 'Cash',
      label: 'How much cash do you have?',
    },
    'prepaid': {
      name: 'Prepaid Cards',
      label: 'How much do have in prepaid cards?',
    },
    'other': {
      name: 'Other',
      label: 'How much other money on hand do you have?',
    },
  };

  @observable fundingSources = [];

  constructor(rootStore) {
    this.rootStore = rootStore;
    this.logger = logger.addGroup('wizardStore');

    // Take funding source options and create observable properties to track their values in cents,
    // Also create getters for getting their values in dollars.
    extendObservable(this, transform(this.fundingSourceOptions, (result, [key]) => {
      result[`${key}Cents`] = 0;

      result[`set${capitalize(key)}Cents`] = function(cents) {
        this[`${key}Cents`] = cents;
      };

      return result;
    }, {}));

    this.logger.debug('initialize wizard store: %O', this);
  }

  @computed get totalStartingFunds() {
    return Object.values(this.startingFunds).reduce((sum, amount) => sum + amount, 0);
  }

  @action setFundingSources(sources = []) {
    this.fundingSources = sources;
  }

  @action setStartingFunds(obj = {}) {
    this.startingFunds = obj;
  }
}
