/* eslint-disable no-console */

import { useEffect } from 'react';

class Logger {
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
    'groupCollapsed',
  ];

  static storageKey = 'mmtLogger';

  static defaults = {
    active: [],
  };

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

  get config() {
    if (this._config) return this._config;

    this._config = this.loadConfig();
    return this._config;
  }

  set config(obj) {
    this.storage[this.constructor.storageKey] = JSON.stringify(obj);
    this._config = obj;
  }

  get groupNames() {
    return [...this.groups.keys()];
  }

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

  loadConfig() {
    const config = this.storage[this.constructor.storageKey];
    const parsed = config ? JSON.parse(config) : {};
    return parsed;
  }

  updateConfig(params = {}) {
    this.config = Object.assign({}, this.config, params);
    this._info('Logger config updated: %O', this.config);
  }

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

  enableAll() {
    this.updateConfig({
      active: this.groupNames,
    });
    this._info('Enabled all groups (%O)', this.groupNames);
  }

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
