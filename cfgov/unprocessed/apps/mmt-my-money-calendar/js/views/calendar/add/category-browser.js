import clsx from 'clsx';
import { useEffect } from 'react';
import { observer } from 'mobx-react';
import { Link, useParams, useHistory } from 'react-router-dom';
import { useStore } from '../../../stores';
import { Categories } from '../../../stores/models/cash-flow-event';
import { useLogger } from '../../../lib/logger';
import dotProp from 'dot-prop';

const CategoryLink = ({ slug, label, icon = '' }) => <li key={slug}></li>;

function CategoryBrowser() {
  const { eventStore, uiStore } = useStore();
  const { categories = '' } = useParams();
  const history = useHistory();
  const categoryPath = categories.replace(/\//g, '.');
  const category = dotProp.get(Categories, categoryPath);

  useLogger(
    'categoryBrowser',
    (group) => {
      group.debug('Category browser category path: %O', categoryPath);
      group.debug('Category object: %O', category);
    },
    [categoryPath, category]
  );

  useEffect(() => {
    uiStore.setSelectedCategory(categoryPath);

    if (category && !category.subcategories) {
      history.push('/calendar/add/new');
    }
  }, [category, categoryPath]);

  return (
    <section className="category-browser">
      <h2>Income</h2>
      <ul>
        {Object.entries(Categories.income).map(([key, val]) => (
          <li key={key}>
            <Link to={`/calendar/add/income/${key}`}>{val.name}</Link>
          </li>
        ))}
      </ul>
    </section>
  );
}

export default observer(CategoryBrowser);
