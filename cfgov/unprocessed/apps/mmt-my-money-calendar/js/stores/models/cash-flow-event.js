import { observable, computed, action, extendObservable } from 'mobx';
import logger from '../../lib/logger';

export default class CashFlowEvent {
  static isCashFlowEvent(obj) {
    return obj instanceof CashFlowEvent;
  }

  constructor(store, props) {
    this.store = store;
    this.logger = logger.addGroup('cashFlowEvent');

    extendObservable(this, props);
  }
}
