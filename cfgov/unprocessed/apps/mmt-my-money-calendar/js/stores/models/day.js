import { observable, action, computed } from 'mobx';
import { toDayJS, dayjs } from '../../lib/calendar-helpers';
import logger from '../../lib/logger';

export default class Day {
  @observable date;

  @observable snapBalance = 0;

  @observable nonSnapBalance = 0;

  constructor(store, props = {}) {
    const { date = dayjs(), snapBalance = 0, nonSnapBalance = 0, previousDay } = props;
    this.store = store;
    this.date = toDayJS(date);
    this.snapBalance = snapBalance;
    this.nonSnapBalance = nonSnapBalance;
    this.logger = logger.addGroup('day');

    if (previousDay) {
      this.snapBalance = previousDay.snapBalance + this.snapTotal;
      this.nonSnapBalance = previousDay.nonSnapBalance + this.nonSnapTotal;
    }

    // SNAP can't go below 0
    // Deduct SNAP expenses from non-snap balance if snap would be negative
    if (this.snapBalance < 0) {
      this.nonSnapBalance += this.snapBalance;
      this.snapBalance = 0;
    }

    this.logger.debug('Initialize Day: %O', this);
  }

  @computed get totalBalance() {
    return this.snapBalance + this.nonSnapBalance;
  }

  @computed get timestamp() {
    return this.date.startOf('day').valueOf();
  }

  @computed get events() {
    return this.store.eventsByDate.get(this.timestamp) || [];
  }

  @computed get nonSnapExpenses() {
    return this.events.filter( event => event.category !== 'expense.food.groceries' && event.total < 0);
  }

  @computed get snapExpenses() {
    return this.events.filter( event => event.category === 'expense.food.groceries');
  }

  @computed get nonSnapIncome() {
    return this.events.filter( event => event.category !== 'income.benefits.snap' && event.total > 0);
  }

  @computed get snapIncome() {
    return this.events.filter( event => event.category === 'income.benefits.snap');
  }

  @computed get nonSnapTotal() {
    return [...this.nonSnapIncome, ...this.nonSnapExpenses].reduce((sum, event) => sum + event.total, 0);
  }

  @computed get snapTotal() {
    return [...this.snapExpenses, ...this.snapIncome].reduce((sum, event) => sum + event.total, 0);
  }

  @action setDate(date) {
    this.date = toDayJS(date);
  }

  @action setSnapBalance(balance) {
    this.snapBalance = Number(balance);
  }

  @action setNonSnapBalance(balance) {
    this.nonSnapBalance = Number(balance);
  }
}
