import clsx from 'clsx';
import { observer } from 'mobx-react';
import { NavLink } from 'react-router-dom';
import { useStore } from '../stores';

import calendar from '@cfpb/cfpb-icons/src/icons/calendar.svg';
import add from '@cfpb/cfpb-icons/src/icons/add.svg';
import lightbulb from '@cfpb/cfpb-icons/src/icons/lightbulb.svg';
import menu from '@cfpb/cfpb-icons/src/icons/menu.svg';

const NavItem = ({ href, icon, label, ...params }) => (
  <li className="bottom-nav__item">
    <NavLink className="bottom-nav__link" to={href} {...params}>
      <div className="bottom-nav__link-icon" dangerouslySetInnerHTML={{ __html: icon }} />
      <div className="bottom-nav__link-label">{label}</div>
    </NavLink>
  </li>
);

function BottomNav() {
  const { uiStore } = useStore();
  const classes = clsx('bottom-nav', uiStore.showBottomNav && 'bottom-nav--visible');

  return (
    <footer className={classes}>
      <nav className="bottom-nav__nav">
        <ul className="bottom-nav__items">
          <NavItem href="/calendar" icon={calendar} exact label="Calendar" />
          <NavItem href="/calendar/add/income" icon={add} label="Income/Expense" />
          <NavItem href="/strategies" icon={lightbulb} label="Strategies" />
          <NavItem href="/more" icon={menu} label="More" />
        </ul>
      </nav>
    </footer>
  );
}

export default observer(BottomNav);
