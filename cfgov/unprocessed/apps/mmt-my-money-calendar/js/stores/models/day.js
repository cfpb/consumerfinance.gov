import { observable, action, computed } from 'mobx';
import { toDayJS, dayjs } from '../../lib/calendar-helpers';
import logger from '../../lib/logger';

export default class Day {
  @observable date;
  @observable snapBalanceCents = 0;
  @observable nonSnapBalanceCents = 0;

  constructor(store, props = {}) {
    const { date = dayjs(), snapBalanceCents = 0, nonSnapBalanceCents = 0, previousDay } = props;
    this.store = store;
    this.date = toDayJS(date);
    this.snapBalanceCents = snapBalanceCents;
    this.nonSnapBalanceCents = nonSnapBalanceCents;
    this.logger = logger.addGroup('day');

    if (previousDay) {
      this.snapBalanceCents = this.snapTotal + previousDay.snapTotal;
      this.nonSnapBalanceCents = this.nonSnapTotal + previousDay.nonSnapTotal;
    }

    this.logger.debug('Initialize Day: %O', this);
  }

  @computed get totalBalanceCents() {
    return this.snapBalanceCents + this.nonSnapBalanceCents;
  }

  @computed get totalBalance() {
    return this.totalBalanceCents / 100;
  }

  @computed get timestamp() {
    return this.date.startOf('day').valueOf();
  }

  @computed get events() {
    return this.store.eventsByDate.get(this.timestamp) || [];
  }

  @computed get nonSnapExpenses() {
    return this.events.filter((event) => event.category !== 'expense.food.groceries' && event.totalCents < 0);
  }

  @computed get snapExpenses() {
    return this.events.filter((event) => event.category === 'expense.food.groceries');
  }

  @computed get nonSnapIncome() {
    return this.events.filter((event) => event.category !== 'income.benefits.snap' && event.totalCents > 0);
  }

  @computed get snapIncome() {
    return this.events.filter((event) => event.category === 'income.benefits.snap');
  }

  @computed get nonSnapTotal() {
    return [...this.nonSnapIncome, ...this.nonSnapExpenses].reduce((sum, event) => sum + event.totalCents, 0);
  }

  @computed get snapTotal() {
    return [...this.snapExpenses, ...this.snapIncome].reduce((sum, event) => sum + event.totalCents, 0);
  }

  @computed get snapBalance() {
    return this.snapBalanceCents / 100;
  }

  @computed get nonSnapBalance() {
    return this.nonSnapBalanceCents / 100;
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
