import { observable, computed, action } from 'mobx';
import logger from '../lib/logger';

export default class UIStore {
  @observable navOpen = false;
  @observable pageTitle = 'myMoney Calendar';

  constructor(rootStore) {
    this.rootStore = rootStore;
    this.logger = logger.addGroup('uiStore');

    this.logger.debug('Initialize UI Store: %O', this);
  }

  @action setNavOpen(val) {
    this.navOpen = Boolean(val);
  }

  @action setPageTitle(title) {
    this.pageTitle = title;
  }

  toggleNav() {
    this.setNavOpen(!this.navOpen);
  }
}
