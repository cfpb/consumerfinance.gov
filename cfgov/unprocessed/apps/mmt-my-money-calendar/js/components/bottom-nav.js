import clsx from 'clsx';
import { useCallback } from 'react';
import { observer } from 'mobx-react';
import { NavLink } from 'react-router-dom';
import { useStore } from '../stores';

import { calendar, add, idea, menu } from '../lib/icons';

const NavItem = ({ href, icon, label, badge, disabled = false, ...params }) => {
  const classes = clsx('bottom-nav__link', disabled && 'disabled');
  const clickHandler = useCallback((event) => {
    if (!disabled) return true;

    event.preventDefault();
    event.stopPropagation();
  }, [disabled]);

  return (
    <li className="bottom-nav__item">
      <NavLink onClick={clickHandler} className={classes} disabled={disabled} to={href} {...params}>
        <div className="bottom-nav__link-icon" dangerouslySetInnerHTML={{ __html: icon }} />
        <div className="bottom-nav__link-label">{label}</div>
        {!!badge && <div className="bottom-nav__link-badge">{badge}</div>}
      </NavLink>
    </li>
  );
};

function BottomNav() {
  const { uiStore, strategiesStore, eventStore: { hasStartingBalance } } = useStore();
  const classes = clsx('bottom-nav', uiStore.showBottomNav && 'bottom-nav--visible');

  return (
    <footer className={classes}>
      <nav className="bottom-nav__nav">
        <ul className="bottom-nav__items">
          <NavItem href="/calendar" icon={calendar} exact label="Calendar" disabled={!hasStartingBalance} />
          <NavItem href="/calendar/add/income" icon={add} label="Income / Expense" disabled={!hasStartingBalance} />
          <NavItem href="/strategies" icon={idea} label="Strategies" badge={strategiesStore.strategyResults.length} disabled={!hasStartingBalance || !strategiesStore.strategyResults.length} />
          <NavItem href="/more" icon={menu} label="More" disabled={!hasStartingBalance} />
        </ul>
      </nav>
    </footer>
  );
}

export default observer(BottomNav);
