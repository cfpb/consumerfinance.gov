import clsx from 'clsx';
import { useEffect } from 'react';
import { observer } from 'mobx-react';
import { Link, NavLink, useParams, useHistory, withRouter } from 'react-router-dom';
import { useStore } from '../../../stores';
import { Categories } from '../../../stores/models/cash-flow-event';
import { useLogger } from '../../../lib/logger';
import dotProp from 'dot-prop';

const CategoryLink = ({ slug, label, icon = '' }) => <li key={slug}></li>;

function CategoryBrowser({ match }) {
  const { eventStore, uiStore } = useStore();
  const { categories = 'income' } = useParams();
  const history = useHistory();
  const categoryPath = categories.replace(/\//g, '.');
  const category = Categories.get(categoryPath);
  const categoryOptions = category ? category : Categories.all;

  useLogger(
    'categoryBrowser',
    (group) => {
      group.debug('Category browser category path: %O', categoryPath);
      group.debug('Category object: %O', category);
      group.debug('Category opts: %O', categoryOptions);
    },
    [categoryPath, category]
  );

  useEffect(() => {
    uiStore.setSelectedCategory(categoryPath);

    if (category && category.name && !category.subcategories) {
      history.push('/calendar/add/new');
    }
  }, [category, categoryPath]);

  return (
    <section className="category-browser">
      <nav className="category-browser__tab-nav">
        <ul>
          <li>
            <NavLink to={`/calendar/add/income`}>Income</NavLink>
          </li>
          <li>
            <NavLink to={`/calendar/add/expense`}>Expense</NavLink>
          </li>
        </ul>
      </nav>

      <ul className="category-links">
        {Object.entries(categoryOptions).map(([key, {name}]) => (
          <li key={key} className="category-links__item">
            <Link to={`/calendar/add/${categories}/${key}`}>{name}</Link>
          </li>
        ))}
      </ul>
    </section>
  );
}

export default observer(withRouter(CategoryBrowser));
