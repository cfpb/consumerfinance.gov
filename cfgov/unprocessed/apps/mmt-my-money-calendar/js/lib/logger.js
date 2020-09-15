/* eslint-disable no-console */

import { useEffect } from 'react';

/** An object wrapping the Console API methods
 * @typedef {Object} ConsoleWrapper
 * @property {Function} debug
 * @property {Function} log
 * @property {Function} info
 * @property {Function} warn
 * @property {Function} error
 * @property {Function} time
 * @property {Function} timeEnd
 * @property {Function} count
 * @property {Function} group
 * @property {Function} groupEnd
 * @property {Function} groupCollapsed
 */

class Logger {
  /** The methods that will be present in the Console API wrapper object returned by addGroup
   * @type {string[]}
   */
  static wrappedMethods = [
    'debug',
    'log',
    'info',
    'warn',
    'error',
    'time',
    'timeEnd',
    'count',
    'group',
    'groupEnd',
    'groupCollapsed'
  ];

  /** The localStorage key under which a JSON object of persistent settings will be saved
   * @type {string}
   */
  static storageKey = 'mmtLogger';

  static defaults = {
    active: [],
  };

  /** An array of background/foreground hex string pairs used in color coding group messages
   * @type {Array<string[]>}
   */
  colors = [
    ['#a6cee3', '#000'],
    ['#1f78b4', '#fff'],
    ['#b2df8a', '#000'],
    ['#33a02c', '#fff'],
    ['#fb9a99', '#fff'],
    ['#e31a1c', '#fff'],
    ['#fdbf6f', '#000'],
    ['#ff7f00', '#fff'],
    ['#cab2d6', '#fff'],
    ['#6a3d9a', '#fff'],
    ['#ffff99', '#000'],
    ['#b15928', '#fff'],
    ['#e41a1c', '#fff'],
    ['#377eb8', '#fff'],
    ['#4daf4a', '#fff'],
    ['#984ea3', '#fff'],
    ['#ff7f00', '#fff'],
    ['#ffff33', '#000'],
    ['#a65628', '#fff'],
    ['#f781bf', '#fff'],
    ['#999999', '#fff'],
  ];

  usedColors = [];

  /** Computed property returning either localStorage or an ephemeral object in memory if
   * localStorage is not available (e.g. in incognito mode)
   * @type {Object}
   */
  get storage() {
    if (this._storage) return this._storage;

    if (!('localStorage' in window)) return {};

    try {
      localStorage.setItem('logger.test', '1');
      this._storage = localStorage;
      return this._storage;
    } catch (err) {
      this._warn('localStorage not available for logger config');
      this._storage = {};
      return this._storage;
    }
  }

  
  /** Configuration object, auto loaded from localStorage
   * @type {Object}
   */
  get config() {
    if (this._config) return this._config;

    this._config = this.loadConfig();
    return this._config;
  }

  
  /** Setter that automatically saves config object to localStorage
   */
  set config(obj) {
    this.storage[this.constructor.storageKey] = JSON.stringify(obj);
    this._config = obj;
  }

  
  /** An array of registered group names
   * @type {string[]}
   */
  get groupNames() {
    return [...this.groups.keys()];
  }

  
  /** An array of currently enabled groups
   * @type {string[]}
   */
  get activeGroups() {
    return this.config.active;
  }

  constructor() {
    const { storageKey, defaults } = this.constructor;
    this._config = null;
    //this.groups = {};
    this.groups = new Map();

    if (!this.storage[storageKey]) this.storage[storageKey] = JSON.stringify(defaults);
  }

  
  /** Get a random color pair
   *
   * @returns {string[]}
   */
  randomColor() {
    return this.colors[Math.floor(Math.random() * this.colors.length)];
  }

  unusedColorPair() {
    if (this.usedColors.length === this.colors.length) {
      this.usedColors = [];
    }

    const index = Math.floor(Math.random() * this.colors.length);
    const colorPair = this.colors[index];

    if (!this.usedColors.includes(index)) {
      this.usedColors.push(index);
      return colorPair;
    }

    return this.unusedColorPair();
  }

  
  /** Load and parse JSON configuration from localStorage
   *
   * @returns {Object}
   */
  loadConfig() {
    const config = this.storage[this.constructor.storageKey];
    const parsed = config ? JSON.parse(config) : {};
    return parsed;
  }

  
  /** Updates runtime config and persists it to localStorage
   *
   * @param {Object} params New configuration parameters
   * @returns {undefined}
   */
  updateConfig(params = {}) {
    this.config = Object.assign({}, this.config, params);
    this._info('Logger config updated: %O', this.config);
  }

  
  /** Registers a new message group and returns an object of wrapped console methods.
   *
   * @param {string} name The name of the new group
   * @returns {ConsoleWrapper}
   */
  addGroup(name) {
    if (this.groups.has(name)) return this.groups.get(name);

    const [bgColor, fgColor] = this.unusedColorPair();
    const labelStyle = `
      background-color: ${bgColor};
      color: ${fgColor};
      font-weight: bold;
      padding: 2px 4px;
    `;
    const resetStyle = `
      background-color: inherit;
      color: inherit;
      font-weight: normal;
      padding: 0;
    `;

    const group = this.constructor.wrappedMethods.reduce((obj, method) => {
      obj[method] = (...args) => {
        if (!this.config.active.includes(name)) return;

        if (typeof args[0] === 'string') {
          args[0] = `%c${name}%c ${args[0]}`;
          args.splice(1, 0, labelStyle, resetStyle);
        }

        return console[method](...args);
      };

      return obj;
    }, {});

    group.color = bgColor;

    this.groups.set(name, group);

    return group;
  }

  
  /** Makes messages from specified groups print to console
   *
   * @param  {...string} groupNames Names of groups to enable
   */
  enable(...groupNames) {
    for (const groupName of groupNames) {
      if (!this.groupNames.includes(groupName)) {
        this._warn('Group named %s is not registered', groupName);
        continue;
      }

      if (this.config.active.includes(groupName)) {
        this._info('Group %s is already active', groupName);
        continue;
      }

      const { active } = this.config;
      active.push(groupName);
      this.updateConfig({ active });
      this._info('Enabled logging for group %s', groupName);
    }
  }

  
  /** Hides messages from specified groups and prevents them from printing to console.
   *
   * @param  {...any} groupNames Names of groups to disable
   */
  disable(...groupNames) {
    for (const groupName of groupNames) {
      let { active } = this.config;

      if (!active.includes(groupName)) {
        this._info('Group %s is already disabled', groupName);
        continue;
      }

      this.updateConfig({
        active: active.filter((name) => name !== groupName),
      });
      this._info('Disabled logging for group %s', groupName);
    }
  }

  
  /** Enables all registered groups
   *
   * @returns {undefined}
   */
  enableAll() {
    this.updateConfig({
      active: this.groupNames,
    });
    this._info('Enabled all groups (%O)', this.groupNames);
  }

  
  /** Disables all registered groups
   *
   * @returns {undefined}
   */
  disableAll() {
    this.updateConfig({ active: [] });
    this._info('All groups disabled');
  }

  _warn(...args) {
    console.warn(...args);
  }

  _info(...args) {
    console.info(...args);
  }
}

const logger = new Logger();

window.logger = logger;

export function useLogger(groupName, callback, deps = []) {
  const group = logger.addGroup(groupName);

  useEffect(() => {
    callback(group);
  }, deps);
}

export default logger;
