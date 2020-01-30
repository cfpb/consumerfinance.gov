import { flow, observable, computed, action } from 'mobx';
import { computedFn } from 'mobx-utils';
import logger from '../lib/logger';
import { toDateTime } from '../lib/calendar-helpers';
import CashFlowEvent from './models/cash-flow-event';
import { DateTime } from 'luxon';

export default class CashFlowStore {
  @observable events = [];

  constructor(rootStore) {
    this.rootStore = rootStore;
    this.logger = logger.addGroup('cashFlowStore');

    this.loadEvents();

    this.logger.debug('Initialize CashFlowStore: %O', this);
  }

  /**
   * All events in the store as a map, keyed by date
   *
   * @type {Map}
   */
  @computed get eventsByDate() {
    return this.events.reduce((output, event) => {
      const list = output.get(event.date) || [];
      output.set(event.date, [...list, event]);
      return output;
    }, new Map());
  }

  /**
   * All events in the store as a map, keyed by ID
   *
   * @type {Map}
   */
  @computed get eventsById() {
    return new Map(this.events.map((event) => [event.id, event]));
  }

  getBalanceForDate = computedFn(function getBalanceForDate(stopDate) {
    stopDate = toDateTime(stopDate).endOf('day');

    if (!this.events.length) return 0;

    const totalInCents = this.events.reduce((total, event) => {
      const { milliseconds: diff } = event.dateTime.diff(stopDate).toObject();

      if (diff > 0) return total;

      return total + event.totalCents;
    }, 0);

    this.logger.info('Balance in cents for date %s: %d', stopDate.toFormat('D'), totalInCents);

    return totalInCents / 100;
  });

  // Flows are asynchronous actions, structured as generator functions:
  loadEvents = flow(function*() {
    const events = yield CashFlowEvent.getAllBy('date');
    this.events = events;
    this.logger.debug('Load all events from IDB store: %O', events);
  });

  addEvent = flow(function*(params) {
    const event = new CashFlowEvent(params);

    try {
      yield event.save();
      this.events.push(event);
    } catch (err) {
      this.rootStore.uiStore.setError(err);
    }
  });

  deleteEvent = flow(function*(id) {
    const event = this.eventsById.get(id);
    yield event.destroy();
    this.events = this.events.filter((e) => e.id !== id);
  });
}
