import { observable, computed, action } from 'mobx';
import logger from '../lib/logger';
import { DateTime } from 'luxon';
import { limitMonthNumber, getWeekRows } from '../lib/calendar-helpers';

export default class UIStore {
  @observable navOpen = false;
  @observable pageTitle = 'myMoney Calendar';
  @observable subtitle;
  @observable description;
  @observable nextStepPath;
  @observable prevStepPath;
  @observable progress = 0;
  @observable error;
  @observable currentMonth = DateTime.local().startOf('month');
  @observable selectedDate;

  constructor(rootStore) {
    this.rootStore = rootStore;
    this.logger = logger.addGroup('uiStore');

    this.logger.debug('Initialize UI Store: %O', this);
  }

  @computed get monthCalendarRows() {
    return getWeekRows(this.currentMonth);
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

  @action setError(err) {
    this.error = err;
  }

  @action setCurrentMonth(month) {
    if (!Number.isInteger(month)) throw new Error('Current month must be an integer');

    this.currentMonth = limitMonthNumber(month);
  }

  @action setSelectedDate(date) {
    this.selectedDate = date;
  }

  toggleNav() {
    this.setNavOpen(!this.navOpen);
  }
}
