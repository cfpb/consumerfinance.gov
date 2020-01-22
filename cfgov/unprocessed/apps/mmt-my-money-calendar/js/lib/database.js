import * as idb from 'idb';
import logManager from './logger';

const DB_VERSION = 1;

const logger = logManager.addGroup('db');

const dbPromise = idb.openDB('myMoneyCalendar', DB_VERSION, {
  upgrade(db, oldVersion, newVersion, transaction) {

    logger.debug('Upgrade IndexedDB from %d to %d', oldVersion, newVersion);

    /**
     * Numbered DB version migrations
     *
     * Use these to make incremental changes or additions to the database in a way that allows the user's browser to
     * apply just the updates that are needed.
     */
    switch (oldVersion) {
      case 0: // The database doesn't exist and is being created
        // Simple key-value store for persisting UI state
        db.createObjectStore('ui', { keyPath: 'option' });

        // Cash flow event (income and expense) storage
        const eventStore = db.createObjectStore('events', { keyPath: 'id', autoIncrement: true });
        eventStore.createIndex('date', 'date', { unique: false });
        eventStore.createIndex('category', 'category', { unique: false });

        break;
    }
  },
});

export default dbPromise;
