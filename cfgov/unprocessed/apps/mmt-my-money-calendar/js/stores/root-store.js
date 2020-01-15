import { observable, action, computed } from 'mobx';
import logger from '../lib/logger';

export default class RootStore {
  @observable networkStatus = 'idle';

  constructor() {
    this.logger = logger.addGroup('RootStore');

    // TODO: Add child data store instances here
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
