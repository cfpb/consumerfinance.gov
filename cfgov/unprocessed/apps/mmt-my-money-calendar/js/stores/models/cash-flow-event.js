import { observable, computed, action, extendObservable } from 'mobx';
import { RRule, rrulestr } from 'rrule';
import * as yup from 'yup';
import logger from '../../lib/logger';
import dbPromise from '../../lib/database';
import { transform } from '../../lib/object-helpers';

export default class CashFlowEvent {
  @observable name;
  @observable date;
  @observable category;
  @observable subcategory;
  @observable total = 0;
  @observable recurs = false;
  @observable recurrence;
  @observable errors;
  @observable persisted = false;

  static store = 'events';

  static schema = {
    name: yup.string().required(),
    date: yup.date().required(),
    category: yup.string().required(),
    subcategory: yup.string(),
    totalCents: yup.number().integer(),
    recurrence: yup.string(),
  };

  static isCashFlowEvent(obj) {
    return obj instanceof CashFlowEvent;
  }

  static async getAll() {
    const { store } = await this.transaction();
    return store.getAll();
  }

  static async get(id) {
    const { store } = await this.transaction();
    return store.get(id);
  }

  static async getByDateRange(start, end = new Date()) {
    const fromDate = new Date(start);
    const range = IDBKeyRange.lowerBound(fromDate);
    const { store } = await this.transaction();
    const index = store.index('date');
    let cursor = await index.openCursor(range);
    const results = [];

    while (cursor) {
      results.push(cursor.value)
      cursor = await cursor.continue();
    }

    return results;
  }

  static async count() {
    const { store } = await this.transaction();
    return store.count();
  }

  static async transaction(perms = 'readonly', stores = this.store) {
    const db = await dbPromise;
    const tx = db.transaction(stores, perms);

    return {
      tx,
      store: tx.objectStore(this.store),
    };
  }

  constructor(props) {
    this.logger = logger.addGroup('cashFlowEvent');

    this.update(props);
  }

  get yupSchema() {
    return yup.object().shapeOf(this.constructor.schema);
  }

  @computed get totalCents() {
    return this.total * 100;
  }

  @computed get recurrenceRule() {
    if (!this.recurrence || (typeof this.recurrence !== 'string')) return null;
    return rrulestr(this.recurrence);
  }

  @action update(props = {}) {
    for (const key in props) {
      this[key] = props[key];
    }
  }

  async save() {
    const { tx, store } = await this.transaction('readwrite');
    const record = this.asObject();

    store.add(record);
    return tx.complete;
  }

  async validate() {
    try {
      await this.yupSchema.validate();
      return true;
    } catch (err) {
      return err;
    }
  }

  async isValid() {
    return this.yupSchema.isValid();
  }

  asObject() {
    return transform(this.constructor.schema, (result, [key]) => {
      result[key] = this[key];
      return result;
    });
  }

  transaction(...args) {
    return this.constructor.transaction(...args);
  }
}
