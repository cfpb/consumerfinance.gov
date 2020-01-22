import { observable, computed, action, extendObservable } from 'mobx';
import logger from '../../lib/logger';
import dbPromise from '../../lib/database';

export default class CashFlowEvent {
  static store = 'events';

  static isCashFlowEvent(obj) {
    return obj instanceof CashFlowEvent;
  }

  static async getAll() {
    const { tx, store } = await this.transaction();
    return store.getAll();
  }

  static async get(id) {
    const { tx, store } = await this.transaction();
    return store.get(id);
  }

  static async getDateRange(start, end = new Date()) {
    const fromDate = new Date(date);
    const range = IDBKeyRange.lowerBound(fromDate);
    const { tx, store } = this.transaction();
    const index = store.index('date');
    const cursor = await index.openCursor(range);
  }

  static async transaction(stores = this.store, perms = 'readonly') {
    const db = await dbPromise;
    const tx = db.transaction(stores, perms);

    return {
      tx,
      store: tx.objectStore(this.store),
    };
  }

  constructor(store, props) {
    this.store = store;
    this.logger = logger.addGroup('cashFlowEvent');

    extendObservable(this, props);
  }
}
