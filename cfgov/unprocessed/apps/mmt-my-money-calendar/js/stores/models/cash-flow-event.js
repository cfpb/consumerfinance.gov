import { observable, computed, action, extendObservable } from 'mobx';
import { RRule, rrulestr } from 'rrule';
import * as yup from 'yup';
import logger from '../../lib/logger';
import dbPromise from '../../lib/database';
import { transform } from '../../lib/object-helpers';
import { DateTime } from 'luxon';

export default class CashFlowEvent {
  @observable id;
  @observable name;
  @observable date;
  @observable category;
  @observable subcategory;
  @observable totalCents = 0;
  @observable isRecurrence = false;
  @observable recurs = false;
  @observable recurrence;
  @observable errors;
  @observable persisted = false;

  static directions = {
    DESC: 'prev',
    ASC: 'next',
  };

  static store = 'events';

  static schema = {
    id: yup.number().integer(),
    name: yup.string().required(),
    date: yup.date().required(),
    category: yup.string().required(),
    subcategory: yup.string(),
    totalCents: yup.number().integer(),
    recurrence: yup.string(),
  };

  /**
   * Indicates whether or not the object is an instance of CashFlowEvent
   *
   * @param {Object} obj - The object to check
   */
  static isCashFlowEvent(obj) {
    return obj instanceof CashFlowEvent;
  }

  /**
   * Fetch all cash flow events from the IndexedDB store
   *
   * @returns {Promise<CashFlowEvent[]>} An array of cash flow events
   */
  static async getAll() {
    const { store } = await this.transaction();
    const records = await store.getAll();
    return records.map((rec) => new CashFlowEvent(rec));
  }

  /**
   * Gets all entries in the IDB object store, sorted by the given index
   *
   * @param {String} indexName - The index to use for sorting
   * @param {String} direction - The direction in which to sort results ('next', 'nextunique', 'prev', or 'prevunique')
   * @returns {Promise<CashFlowEvent[]>} A promise resolving to an array of CashFlowEvent instances
   */
  static async getAllBy(indexName, direction = 'next') {
    const { store } = await this.transaction();
    const index = store.index(indexName);
    let cursor = await index.openCursor(null, direction);
    const results = [];

    while (cursor) {
      results.push(new CashFlowEvent(cursor.value));
      cursor = await cursor.continue();
    }

    return results;
  }

  /**
   * Retrieves a single cash flow event from the IDB store by its ID key
   *
   * @param {Number} id - The ID of the event to retrieve
   */
  static async get(id) {
    const { store } = await this.transaction();
    const record = await store.get(id);
    return new CashFlowEvent(record);
  }

  /**
   * Retrieves cash flow events from the specified date range from the IDB store
   *
   * @param {Date} start - The beginning date to query from
   * @param {Date} end - The end date
   * @returns {Promise<CashFlowEvent[]>} An array of cash flow events
   */
  static async getByDateRange(start, end = new Date()) {
    const fromDate = new Date(start);
    const range = IDBKeyRange.lowerBound(fromDate);
    const { store } = await this.transaction();
    const index = store.index('date');
    let cursor = await index.openCursor(range);
    const results = [];

    while (cursor) {
      results.push(new CashFlowEvent(cursor.value));
      cursor = await cursor.continue();
    }

    return results;
  }

  /**
   * Get the number of stored cash flow events in the IDB store
   *
   * @returns {Promise<Number>} The number of stored cash flow events
   */
  static async count() {
    const { store } = await this.transaction();
    return store.count();
  }

  /**
   * Begin an IDB transaction
   *
   * @param {String} [perms="readonly"] - The permissions the transaction is requesting
   * @param {String|String[]} [stores=this.store] - The stores the transaction will be interacting with
   * @returns {Promise<Object>} An object with tx and store properties
   */
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
    return yup.object().shape(this.constructor.schema);
  }

  @computed get asObject() {
    const obj = transform(this.constructor.schema, (result, [key]) => {
      result[key] = this[key];
      return result;
    });

    if (!obj.id) delete obj.id;

    return obj;
  }

  @computed get dateTime() {
    return new DateTime(this.date);
  }

  @computed get total() {
    return this.totalCents / 100;
  }

  @computed get recurrenceRule() {
    if (!this.recurrence || (typeof this.recurrence !== 'string')) return null;
    return rrulestr(this.recurrence);
  }

  /**
   * Update the observable properties of this instance
   *
   * @param {Object} props - Properties to update
   * @returns {undefined}
   */
  @action update(props = {}) {
    for (const key in props) {
      this[key] = props[key];
    }
  }

  @action setID(id) {
    this.id = id;
  }

  @action setPersisted(value = true) {
    this.persisted = Boolean(value);
  }

  /**
   * Save the cash flow event to IndexedDB store, or raise a validation error if it doesn't conform to schema
   *
   * @throws {ValidationError} A Yup validation error if the object is not valid
   * @returns {Number} The key of the added or updated record
   */
  async save() {
    await this.validate();

    const { tx, store } = await this.transaction('readwrite');
    const key = await store.put(this.asObject);
    await tx.complete;

    if (!this.id) this.setID(key);
    if (!this.persisted) this.setPersisted();

    return key;
  }

  /**
   * Removes this event from the IDB store
   *
   * @returns {CashFlowEvent|Boolean} the event that was just removed, or false if not deleteable
   */
  async destroy() {
    if (!this.persisted) return false;
    const { tx, store } = await this.transaction('readwrite');
    await store.delete(this.id);
    await tx.complete;
    return this;
  }

  /**
   * Validate the cash flow event according to its defined schema
   *
   * @throws {ValidationError} A Yup validation error if the instance does not conform to schema
   * @returns {Promise<Object>} A promise resolving to the properties of the cash flow event if it's valid
   */
  validate() {
    return this.yupSchema.validate(this.asObject);
  }

  /**
   * Asynchronously determines whether or not the cash flow event is valid
   *
   * @returns {Promise<Boolean>} Whether or not the event is valid
   */
  isValid() {
    return this.yupSchema.isValid();
  }

  /**
   * Creates an IndexedDB transaction in which queries can be run
   *
   * @param {Boolean} [perms='readonly'] - Transaction permissions (readwrite or readonly)
   * @param {String|String[]} [stores=this.constructor.store] - Names of the object stores to be operated on
   */
  transaction(...args) {
    return this.constructor.transaction(...args);
  }
}
