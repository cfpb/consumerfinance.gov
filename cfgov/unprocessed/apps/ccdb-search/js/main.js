import { LitElement, html, css } from 'lit';

const DEFAULT_MOUNT_ID = 'ccdb-ui-root';

const getConfig = () => globalThis.__CCDB_CONFIG__ || {};

class CcdbSearch extends LitElement {
  static properties = {
    cssHref: { type: String, attribute: 'data-css-href' },
    mountId: { type: String, attribute: 'data-mount-id' },
  };

  static styles = css`
    :host {
      display: block;
      width: 100%;
      max-width: 1170px;
      margin: 0 auto;
      box-sizing: border-box;
    }

    .ccdb-search {
      width: 100%;
      max-width: 100%;
      margin: 0;
      left: auto;
      right: auto;
      position: relative;
    }
  `;

  constructor() {
    super();
    this.cssHref = '';
    this.mountId = DEFAULT_MOUNT_ID;
    this._initialized = false;
  }

  firstUpdated() {
    if (this._initialized) {
      return;
    }
    this._initialized = true;

    const shadowRoot = this.renderRoot;
    globalThis.__CCDB_CONFIG__ = {
      ...getConfig(),
      root: shadowRoot,
      mountId: this.mountId || DEFAULT_MOUNT_ID,
    };

    import('@cfpb/ccdb5-ui/dist/ccdb5.js');
  }

  disconnectedCallback() {
    super.disconnectedCallback();
    const config = getConfig();
    if (config.root === this.renderRoot) {
      delete config.root;
      if (Object.keys(config).length) {
        globalThis.__CCDB_CONFIG__ = config;
      } else {
        delete globalThis.__CCDB_CONFIG__;
      }
    }
  }

  render() {
    const mountId = this.mountId || DEFAULT_MOUNT_ID;
    return html`
      ${
        this.cssHref
          ? html`<link rel="stylesheet" href=${this.cssHref} />`
          : null
      }
      <div class="ccdb-search">
        <div id=${mountId}></div>
      </div>
    `;
  }
}

if (!customElements.get('cfpb-ccdb-search')) {
  customElements.define('cfpb-ccdb-search', CcdbSearch);
}
