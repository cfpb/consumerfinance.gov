/**
 * Keep track of the card ordering dropdown so that it can be moved
 * outside the filters expandable to improve its visibility.
 * Doing this via JS instead of at the template level preserves the
 * HTML form for no-JS users. This is in its own file so that it can
 * be shared between initial page load JS and dynamic HTMX requests.
 */
const orderingDropdown = {
  container: document.querySelector('#tccp-ordering-container'),
  el: document.querySelector('#tccp-ordering'),
  move: () => {
    if (orderingDropdown.el) {
      orderingDropdown.container.append(orderingDropdown.el);
    }
  },
};

export default orderingDropdown;
