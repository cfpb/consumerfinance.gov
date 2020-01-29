import { flow, observable, computed, action } from 'mobx';
import logger from '../lib/logger';
import CashFlowEvent from './models/cash-flow-event';

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
