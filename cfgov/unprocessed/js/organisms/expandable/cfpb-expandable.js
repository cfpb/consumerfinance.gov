import { proxyCustomElement, HTMLElement, createEvent, h, Host } from '@stencil/core/internal/client';
import { g as getSlottedNodes } from './utils.js';

const cfpbExpandableCss = ".cf-icon-svg{height:1.1875em;vertical-align:text-top;fill:currentcolor}.o-expandable{position:relative}.o-expandable_header{display:-ms-flexbox;display:flex;-ms-flex-pack:justify;justify-content:space-between;padding:0;border:0;background-color:transparent;cursor:pointer}.o-expandable_header:focus{outline:1px dotted black;outline-offset:1px}.o-expandable_cue-close,.o-expandable_cue-open{display:none}button[aria-expanded='false'] .o-expandable_cue-open{display:block}button[aria-expanded='true'] .o-expandable_cue-close{display:block}button&{width:100%;text-align:left}.o-expandable_label{-ms-flex-positive:1;flex-grow:1;margin-bottom:0;color:black;font-weight:500}.o-expandable_cue{min-width:60px;text-align:right;color:#0072ce;font-size:1em;line-height:1}.o-expandable__padded .o-expandable_header{padding:0.625em\n        0.9375em}.o-expandable__padded .o-expandable_content{padding:0.9375em;padding-top:0}.o-expandable__padded .o-expandable_content::before{content:'';display:block;border-top:1px solid #b4b5b6;padding-top:0.9375em}.o-expandable__padded .o-expandable_content::after{padding-bottom:0.9375em;width:100%}.o-expandable__background{background:#f7f8f9}.o-expandable__border{border:1px solid #b4b5b6}:host{display:block;border:1px solid #b4b5b6;background:#f7f8f9;font-family:\"Avenir Next\", Arial, sans-serif}:host(:not(:last-child)){margin-bottom:0.8rem}:host(:last-child){margin-bottom:0.5rem}:host(:not([open])) #content,:host([open='false']) #content{display:none}h1,h2,h3,h4,h5,h6{margin:0}button{display:-ms-flexbox;display:flex;-ms-flex-pack:justify;justify-content:space-between;padding:0;border:0;background-color:transparent;cursor:pointer;width:100%;padding:0.625em 0.9375em;text-align:left;font-size:18px}#content::before{content:'';display:block;border-top:1px solid #b4b5b6;padding-top:0.9375em}#content{padding:0.9375em;padding-top:0}button[aria-expanded='false']:not(.usa-accordion__button){background-image:url('../../assets/plus.svg')}.header-text{display:-ms-flexbox;display:flex}p.subheader{font-weight:400;line-height:26px;margin:0;margin-top:0.25rem;display:-ms-flexbox;display:flex}::slotted([slot='headline']){display:none}::slotted([slot='icon']),::slotted([slot='subheader-icon']){width:1rem;margin-right:1.5rem}::slotted([slot='subheader-icon']){margin-top:0.5rem}";

const CfpbExpandable$1 = /*@__PURE__*/ proxyCustomElement(class CfpbExpandable extends HTMLElement {
  constructor() {
    super();
    this.__registerHost();
    this.__attachShadow();
    this.accordionItemToggled = createEvent(this, "accordionItemToggled", 7);
    /**
     * Toggle button reference
     */
    this.expandButton = null;
    this.header = undefined;
    this.subheader = null;
    this.open = false;
    this.level = 2;
    this.bordered = false;
    this.uswds = false;
    this.slotHeader = null;
    this.slotTag = null;
  }
  toggleOpen(e) {
    this.accordionItemToggled.emit(e);
  }
  // Using onSlotChange to fire event on inital load
  // Data access from slot html element is being perfomed by this function
  // Function allows us to provide context to state
  // State is then being digested by the Header Function below
  populateStateValues() {
    getSlottedNodes(this.el, null).forEach((node) => {
      this.slotHeader = node.innerHTML;
      this.slotTag = node.tagName.toLowerCase();
    });
  }
  componentDidLoad() {
    // auto-expand accordion if the window hash matches the ID
    if (this.el.id && this.el.id === window.location.hash.slice(1)) {
      const currentTarget = this.expandButton;
      if (currentTarget) {
        this.open = true;
        this.el.setAttribute('open', 'true');
        this.el.scrollIntoView();
      }
    }
  }
  render() {
    const Header = () => {
      const headline = this.el.querySelector('[slot="headline"]');
      const Tag = (headline && headline.tagName.includes("H"))
        ? headline.tagName.toLowerCase()
        : `h${this.level}`;
      return (h(Tag, null, h("button", { ref: el => {
          this.expandButton = el;
        }, onClick: this.toggleOpen.bind(this), "aria-expanded": this.open ? 'true' : 'false', "aria-controls": "content", part: "accordion-header" }, h("h3", { class: 'h4 o-expandable_label' }, this.header), h("span", { class: 'o-expandable_link' }, h("span", { class: 'o-expandable_cue o-expandable_cue-open' }, h("svg", { xmlns: "http://www.w3.org/2000/svg", viewBox: "0 0 17 19", class: "cf-icon-svg cf-icon-svg__plus-round" }, h("path", { d: "M16.416 9.583a7.916 7.916 0 1 1-15.833 0 7.916 7.916 0 0 1 15.833 0Zm-2.958.01a.792.792 0 0 0-.792-.792H9.284V5.42a.792.792 0 1 0-1.583 0V8.8H4.32a.792.792 0 0 0 0 1.584H7.7v3.382a.792.792 0 1 0 1.583 0v-3.382h3.382a.792.792 0 0 0 .792-.791Z" }))), h("span", { class: 'o-expandable_cue o-expandable_cue-close' }, h("svg", { xmlns: "http://www.w3.org/2000/svg", viewBox: "0 0 17 19", class: "cf-icon-svg cf-icon-svg__minus-round" }, h("path", { d: "M16.416 9.583a7.916 7.916 0 1 1-15.833 0 7.916 7.916 0 0 1 15.833 0Zm-2.958.01a.792.792 0 0 0-.792-.792H4.32a.792.792 0 0 0 0 1.583h8.346a.792.792 0 0 0 .792-.791Z" })))))));
    };
    return (h(Host, null, h(Header, null), h("slot", { name: "headline", onSlotchange: () => this.populateStateValues() }), h("div", { id: "content" }, h("slot", null))));
  }
  get el() { return this; }
  static get style() { return cfpbExpandableCss; }
}, [1, "cfpb-expandable", {
    "header": [1],
    "subheader": [1],
    "open": [4],
    "level": [2],
    "bordered": [4],
    "uswds": [4],
    "slotHeader": [32],
    "slotTag": [32]
  }]);
function defineCustomElement$1() {
  if (typeof customElements === "undefined") {
    return;
  }
  const components = ["cfpb-expandable"];
  components.forEach(tagName => { switch (tagName) {
    case "cfpb-expandable":
      if (!customElements.get(tagName)) {
        customElements.define(tagName, CfpbExpandable$1);
      }
      break;
  } });
}

const CfpbExpandable = CfpbExpandable$1;
const defineCustomElement = defineCustomElement$1;

export { CfpbExpandable, defineCustomElement };
