import * as idb from 'idb';
import logManager from './logger';

const DB_VERSION = 2;

const logger = logManager.addGroup( 'db' );

const dbPromise = idb.openDB( 'myMoneyCalendar', DB_VERSION, {
  upgrade( db, oldVersion, newVersion, transaction ) {

    logger.debug( 'Upgrade IndexedDB from %d to %d', oldVersion, newVersion );

    let eventStore;

    /**
     * Numbered DB version migrations
     *
     * Use these to make incremental changes or additions to the database in a way that allows the user's browser to
     * apply just the updates that are needed.
     */
    switch ( oldVersion ) {
      case 0: // The database doesn't exist and is being created
        // Simple key-value store for persisting UI state
        db.createObjectStore( 'ui', { keyPath: 'option' } );

        // Cash flow event (income and expense) storage
        eventStore = db.createObjectStore( 'events', { keyPath: 'id', autoIncrement: true } );
        eventStore.createIndex( 'date', 'date', { unique: false } );
        eventStore.createIndex( 'category', 'category', { unique: false } );
        logger.info( 'Create events object store' );
      default:
        eventStore = transaction.objectStore( 'events' );
        eventStore.createIndex( 'originalEventID', 'originalEventID', { unique: false } );
        eventStore.createIndex( 'originalEventID_date', [ 'originalEventID', 'date' ], { unique: true } );
        eventStore.createIndex( 'createdAt', 'createdAt', { unique: false } );
        eventStore.createIndex( 'updatedAt', 'updatedAt', { unique: false } );
        eventStore.createIndex( 'subcategory', 'subcategory', { unique: false } );
        eventStore.createIndex( 'totalCents', 'totalCents', { unique: false } );
        eventStore.createIndex( 'recurs', 'recurs', { unique: false } );
    }
  }
} );

export default dbPromise;
