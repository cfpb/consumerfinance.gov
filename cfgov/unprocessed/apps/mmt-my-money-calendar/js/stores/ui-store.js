import { observable, computed, action } from 'mobx';
import logger from '../lib/logger';

export default class UIStore {
  @observable navOpen = false;
  @observable pageTitle = 'myMoney Calendar';
  @observable subtitle;
  @observable description;
  @observable nextStepPath;
  @observable prevStepPath;
  @observable progress = 0;

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

  @action setSubtitle(subtitle) {
    this.subtitle = subtitle;
  }

  @action setDescription(desc) {
    this.description = desc;
  }

  @action updateWizardStep({ pageTitle, subtitle, description, nextStepPath, prevStepPath, progress }) {
    this.pageTitle = pageTitle;
    this.subtitle = subtitle;
    this.description = description;
    this.nextStepPath = nextStepPath;
    this.prevStepPath = prevStepPath;
    this.progress = progress;
  }

  toggleNav() {
    this.setNavOpen(!this.navOpen);
  }
}
