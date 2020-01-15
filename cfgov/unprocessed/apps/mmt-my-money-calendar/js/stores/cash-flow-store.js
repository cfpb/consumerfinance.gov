import { observable, computed, action } from 'mobx';
import logger from '../lib/logger';
import CashFlowEvent from './models/cash-flow-event';

export default class CashFlowStore {
  @observable eventsById = new Map();

  constructor(rootStore) {
    this.rootStore = rootStore;
    this.logger = logger.addGroup('cashFlowStore');
  }

  /**
   * Whenever eventsById is updates, this will regenerate the Map of events by date automatically
   */
  @computed get eventsByDate() {
    const output = new Map();

    for (const event of this.eventsById.values()) {
      const events = output.get(event.date) || [];
      events.push(event);
      output.set(event.date, events);
    }

    return output;
  }

  @computed get allEvents() {
    return [...this.eventsById.values()];
  }

  @action addEvent(event) {
    this.eventsById.set(event.id, new CashFlowEvent(this, event));
  }

  @action deleteEvent(id) {
    this.eventsById.delete(id);
  }
}
