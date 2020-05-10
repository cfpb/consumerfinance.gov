import { observable, action, computed } from 'mobx';
import { toDayJS, dayjs } from '../../lib/calendar-helpers';
import logger from '../../lib/logger';

export default class Day {
  @observable date;

  constructor(store, date = dayjs()) {
    this.store = store;
    this.date = toDayJS(date);
    this.logger = logger.addGroup('day');

    this.logger.debug('Initialize Day: %O', this);
  }

  @computed get timestamp() {
    return this.date.startOf('day').valueOf();
  }

  @computed get events() {
    return this.store.eventsByDate.get(this.timestamp);
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

  @computed get snapBalance() {
    return this.store.getSnapBalanceForDate(this.date);
  }

  @computed get nonSnapBalance() {
    return this.store.getNonSnapBalanceForDate(this.date)
  }

  @computed get balance() {
    return this.store.getBalanceForDate(this.date);
  }

  @action setDate(date) {
    this.date = toDayJS(date);
  }
}
