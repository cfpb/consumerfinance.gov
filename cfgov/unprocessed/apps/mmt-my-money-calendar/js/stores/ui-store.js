import { observable, computed, action } from 'mobx';
import logger from '../lib/logger';
import { getWeekRows, toDayJS, dayjs } from '../lib/calendar-helpers';
import { formatCurrency } from '../lib/currency-helpers';
import Day from './models/day';

export default class UIStore {
  @observable navOpen = false;
  @observable pageTitle = 'myMoney Calendar';
  @observable subtitle;
  @observable description;
  @observable nextStepPath;
  @observable prevStepPath;
  @observable progress = 0;
  @observable error;
  @observable currentMonth = dayjs().startOf('month');
  @observable selectedDate;
  @observable currentWeek = dayjs().startOf('week');
  @observable selectedCategory = '';
  @observable showBottomNav = true;
  @observable isTouchDevice = false;
  @observable installPromptEvent;
  @observable days = [];
  @observable hasSpotlight;

  constructor(rootStore) {
    this.rootStore = rootStore;
    this.logger = logger.addGroup('uiStore');

    this.logger.debug('Initialize UI Store: %O', this);

    // Detect whether user is interacting with the site via a multitouch-capable input device:
    window.addEventListener('touchstart', this.setIsTouchDevice);

    /**
     * Save Chrome's install prompt event in order to customize the PWA installation process
     * @see {@link https://web.dev/customize-install/}
     */
    window.addEventListener('beforeinstallprompt', this.setInstallPromptEvent);
  }

  @computed get monthCalendarRows() {
    return getWeekRows(this.currentMonth);
  }

  @computed get weekRangeText() {
    const start = this.currentWeek.startOf('week');
    const end = this.currentWeek.endOf('week');
    return `${start.format('MMMM D')} - ${end.format('MMMM D')}`;
  }

  @computed get weekStartingBalance() {
    return this.rootStore.eventStore.getDay(this.currentWeek.startOf('week')).nonSnapBalance;
  }

  @computed get weekEndingBalance() {
    return this.rootStore.eventStore.getDay(this.currentWeek.endOf('week')).nonSnapBalance;
  }

  @computed get weekStartingNonSnapBalance() {
    return this.rootStore.eventStore.getDay(this.currentWeek.startOf('week')).nonSnapBalance;
  }

  @computed get weekStartingSnapBalance() {
    return this.rootStore.eventStore.getDay(this.currentWeek.startOf('week')).snapBalance;
  }

  @computed get weekStartingNonSnapBalanceText() {
    if (typeof this.weekStartingNonSnapBalance === 'undefined') return '$0.00';
    return formatCurrency(this.weekStartingNonSnapBalance);
  }

  @computed get weekStartingSnapBalanceText() {
    if (typeof this.weekStartingSnapBalance === 'undefined') return '$0.00';
    return formatCurrency(this.weekStartingSnapBalance);
  }

  @computed get weekStartingBalanceText() {
    if (typeof this.weekStartingBalance === 'undefined') return '$0.00';
    return formatCurrency(this.weekStartingBalance);
  }

  @computed get weekEndingNonSnapBalance() {
    return this.rootStore.eventStore.getDay(this.currentWeek.endOf('week')).nonSnapBalance;
  }

  @computed get weekEndingSnapBalance() {
    return this.rootStore.eventStore.getDay(this.currentWeek.endOf('week')).snapBalance;
  }

  @computed get weekEndingNonSnapBalanceText() {
    if (typeof this.weekEndingNonSnapBalance === 'undefined') return '$0.00';
    return formatCurrency(this.weekEndingNonSnapBalance);
  }

  @computed get weekEndingSnapBalanceText() {
    if (typeof this.weekEndingSnapBalance === 'undefined') return '$0.00';
    return formatCurrency(this.weekEndingSnapBalance);
  }

  @computed get weekEndingBalanceText() {
    if (typeof this.weekEndingBalance === 'undefined') return '$0.00';
    return formatCurrency(this.weekEndingBalance);
  }

  @computed get weekHasEvents() {
    const events = this.rootStore.eventStore.eventsByWeek.get(this.currentWeek.startOf('week').valueOf());
    return events && events.length;
  }

  @computed get weekHasNegativeBalance() {
    return this.weekEndingBalance < 0;
  }
  
  @computed get weekHasPositiveBalance() {
    return this.weekEndingBalance > 0;
  }

  @computed get weekHasZeroBalance() {
    return this.weekEndingBalance === 0;
  }

  @computed get isRunningAsApp() {
    return navigator.standalone || matchMedia('(display-mode: standalone)').matches;
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
    const date = toDayJS(month);
    this.currentMonth = date;
    this.currentWeek = date.startOf('month').startOf('week');
  }

  @action nextMonth() {
    this.setCurrentMonth(this.currentMonth.add(1, 'month'));
  }

  @action prevMonth() {
    this.setCurrentMonth(this.currentMonth.subtract(1, 'month'));
  }

  @action setSelectedDate(date) {
    date = toDayJS(date);
    this.selectedDate = date.startOf('day');
    this.currentWeek = date.startOf('week');
  }

  @action setCurrentWeek(date) {
    date = toDayJS(date);
    this.currentWeek = date.startOf('week');

    if (!date.isSame(this.currentMonth, 'month')) this.currentMonth = date.startOf('month');
  }

  @action nextWeek() {
    this.setCurrentWeek(this.currentWeek.add(1, 'week'));
    this.selectedDate = null;
  }

  @action prevWeek() {
    this.setCurrentWeek(this.currentWeek.subtract(1, 'week'));
    this.selectedDate = null;
  }

  @action clearSelectedDate() {
    this.selectedDate = null;
  }

  @action gotoDate(date) {
    date = toDayJS(date);
    this.currentMonth = date.startOf('month');
    this.selectedDate = date.startOf('day');
    this.currentWeek = date.startOf('week');
  }

  @action setSelectedCategory(category) {
    this.selectedCategory = category;
  }

  @action toggleBottomNav(state) {
    if (typeof state === 'undefined') {
      this.showBottomNav = !this.showBottomNav;
      return;
    }

    this.showBottomNav = Boolean(state);
  }

  @action setIsTouchDevice = () => {
    this.isTouchDevice = true;
    this.logger.debug('touch device detected');
    window.removeEventListener('touchstart', this.setIsTouchDevice);
  };

  @action setInstallPromptEvent = (event) => {
    this.installPromptEvent = event;
    this.logger.debug('Store install prompt event: %O', this.installPromptEvent);
    window.removeEventListener('beforeinstallprompt', this.setInstallPromptEvent);
  };

  @action toggleSpotlight = (bool) => {
    this.hasSpotlight = bool;
  };

  async showInstallPrompt() {
    if (!this.installPromptEvent) return false;
    this.installPromptEvent.prompt();
    const { outcome } = await this.installPromptEvent.userChoice;
    return outcome;
  }
}
