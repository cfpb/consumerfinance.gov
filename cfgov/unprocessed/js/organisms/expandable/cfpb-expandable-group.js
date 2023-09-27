import { proxyCustomElement, HTMLElement, createEvent, h, Host } from '@stencil/core/internal/client';
import { g as getSlottedNodes } from './utils.js';

const cfpbExpandableGroupCss = ":host(){display:block;width:100%;color:gray;--item-border:none;}:host([bordered='true']),:host([bordered='']){--item-border:3px solid var(--color-gray-lightest)}";

const VaAccordion = /*@__PURE__*/ proxyCustomElement(class VaAccordion extends HTMLElement {
  constructor() {
    super();
    this.__registerHost();
    this.__attachShadow();
    this.componentLibraryAnalytics = createEvent(this, "component-library-analytics", 7);
    this.expanded = false;
    this.openSingle = false;
    this.disableAnalytics = false;
    this.sectionHeading = null;
  }
  itemToggledHandler(event) {
    var _a;
    const clickedItem = event.target.closest('cfpb-expandable');
    // Usage for slot to provide context to analytics for header and level
    const header = clickedItem.querySelector('[slot="headline"]');
    // using the slot to provide context to analytics for header and level
    let headerText;
    let headerLevel;
    if (header) {
      headerText = header === null || header === void 0 ? void 0 : header.innerHTML;
      headerLevel = parseInt((_a = header === null || header === void 0 ? void 0 : header.tagName) === null || _a === void 0 ? void 0 : _a.toLowerCase().split('')[1]);
    }
    else {
      // using the props to provide context to analytics for header and level
      headerText = clickedItem.header;
      headerLevel = clickedItem.level;
    }
    if (this.openSingle) {
      getSlottedNodes(this.el, 'cfpb-expandable')
        .filter(item => item !== clickedItem)
        .forEach(item => item.setAttribute('open', 'false'));
    }
    const prevAttr = clickedItem.getAttribute('open') === 'true' ? true : false;
    if (!this.disableAnalytics) {
      const detail = {
        componentName: 'cfpb-expandable-group',
        action: prevAttr ? 'collapse' : 'expand',
        details: {
          header: headerText || clickedItem.header,
          level: headerLevel || clickedItem.level,
          sectionHeading: this.sectionHeading,
        },
      };
      this.componentLibraryAnalytics.emit(detail);
    }
    clickedItem.setAttribute('open', !prevAttr ? "true" : "false");
    if (!this.isScrolledIntoView(clickedItem)) {
      clickedItem.scrollIntoView();
    }
    // Check if all accordions are open or closed due to user clicks
    this.accordionsOpened();
  }
  accordionsOpened() {
    // Track user clicks on cfpb-expandable-item within an array to compare if all values are true or false
    let accordionItems = [];
    getSlottedNodes(this.el, 'cfpb-expandable').forEach(item => {
      accordionItems.push(item.getAttribute('open'));
    });
    const allOpen = currentValue => currentValue === 'true';
    const allClosed = currentValue => currentValue === 'false';
    if (accordionItems.every(allOpen)) {
      this.expanded = true;
    }
    if (accordionItems.every(allClosed)) {
      this.expanded = false;
    }
  }
  isScrolledIntoView(el) {
    const elemTop = el === null || el === void 0 ? void 0 : el.getBoundingClientRect().top;
    if (!elemTop && elemTop !== 0) {
      return false;
    }
    // Only partially || completely visible elements return true
    return elemTop >= 0 && elemTop <= window.innerHeight;
  }
  render() {
    return (h(Host, null, h("slot", null)));
  }
  get el() { return this; }
  static get style() { return cfpbExpandableGroupCss; }
}, [1, "cfpb-expandable-group", {
    "openSingle": [4, "open-single"],
    "disableAnalytics": [4, "disable-analytics"],
    "sectionHeading": [1, "section-heading"],
    "expanded": [32]
  }, [[0, "accordionItemToggled", "itemToggledHandler"]]]);
function defineCustomElement$1() {
  if (typeof customElements === "undefined") {
    return;
  }
  const components = ["cfpb-expandable-group"];
  components.forEach(tagName => { switch (tagName) {
    case "cfpb-expandable-group":
      if (!customElements.get(tagName)) {
        customElements.define(tagName, VaAccordion);
      }
      break;
  } });
}

const CfpbExpandableGroup = VaAccordion;
const defineCustomElement = defineCustomElement$1;

export { CfpbExpandableGroup, defineCustomElement };
