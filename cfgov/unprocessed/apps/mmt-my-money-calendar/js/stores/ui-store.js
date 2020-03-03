import { observable, computed, action } from 'mobx';
import logger from '../lib/logger';
import { DateTime } from 'luxon';
import { limitMonthNumber, getWeekRows, toDateTime } from '../lib/calendar-helpers';

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
  @observable selectedCategory = '';
  @observable showBottomNav = true;

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
    this.currentMonth = toDateTime(month);
  }

  @action nextMonth() {
    this.currentMonth = this.currentMonth.plus({ months: 1 });
  }

  @action prevMonth() {
    this.currentMonth = this.currentMonth.minus({ months: 1 });
  }

  @action setSelectedDate(date) {
    this.selectedDate = toDateTime(date).startOf('day');
  }

  @action clearSelectedDate() {
    this.selectedDate = null;
  }

  @action gotoDate(date) {
    date = toDateTime(date);
    this.currentMonth = date.startOf('month');
    this.selectedDate = date.startOf('day');
  }

  @action setSelectedCategory(category) {
    this.selectedCategory = category;
  };

  @action toggleBottomNav(state) {
    if (typeof state === 'undefined') {
      this.showBottomNav = !this.showBottomNav;
      return;
    }

    this.showBottomNav = Boolean(state);
  }

  toggleNav() {
    this.setNavOpen(!this.navOpen);
  }
}
