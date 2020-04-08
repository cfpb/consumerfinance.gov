import clsx from 'clsx';
import { observer } from 'mobx-react';
import { NavLink } from 'react-router-dom';
import { useStore } from '../stores';

import { calendar, add, idea, menu } from '../lib/icons';

const NavItem = ({ href, icon, label, badge, disabled = false, ...params }) => (
  <li className="bottom-nav__item">
    <NavLink className="bottom-nav__link" disabled={disabled} to={href} {...params}>
      <div className="bottom-nav__link-icon" dangerouslySetInnerHTML={{ __html: icon }} />
      <div className="bottom-nav__link-label">{label}</div>
      {!!badge && <div className="bottom-nav__link-badge">{badge}</div>}
    </NavLink>
  </li>
);

function BottomNav() {
  const { uiStore, strategiesStore } = useStore();
  const classes = clsx('bottom-nav', uiStore.showBottomNav && 'bottom-nav--visible');

  return (
    <footer className={classes}>
      <nav className="bottom-nav__nav">
        <ul className="bottom-nav__items">
          <NavItem href="/calendar" icon={calendar} exact label="Calendar" />
          <NavItem href="/calendar/add/income" icon={add} label="Income / Expense" />
          <NavItem href="/strategies" icon={idea} label="Strategies" badge={strategiesStore.strategyResults.length} />
          <NavItem href="/more" icon={menu} label="More" />
        </ul>
      </nav>
    </footer>
  );
}

export default observer(BottomNav);
