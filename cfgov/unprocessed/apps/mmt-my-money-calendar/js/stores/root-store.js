import { observable, action, computed } from 'mobx';
import logger from '../lib/logger';
import UIStore from './ui-store';
import CashFlowStore from './cash-flow-store';

export default class RootStore {
  @observable networkStatus = 'idle';

  constructor() {
    this.logger = logger.addGroup('rootStore');
    this.uiStore = new UIStore(this);
    this.eventStore = new CashFlowStore(this);

    this.logger.debug('Initialize RootStore: %O', this);
  }

  @computed get isLoading() {
    return this.networkStatus === 'loading';
  }

  @computed get hasNetworkError() {
    return this.networkStatus === 'error';
  }

  @action setNetworkStatus(val) {
    this.networkStatus = val;
  }
}
