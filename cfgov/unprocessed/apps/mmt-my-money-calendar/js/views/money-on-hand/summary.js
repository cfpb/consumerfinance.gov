import { observer } from 'mobx-react';
import { useStore } from '../../stores';
import { useBEM } from '../../lib/hooks';
import { useScrollToTop } from '../../components/scroll-to-top';

import iconPlaceholder from '../../../img/icon-placeholder.png';

function Summary() {
  const { wizardStore } = useStore();
  const bem = useBEM('wizard');

  useScrollToTop();

  return (
    <>
      <header className={bem('header')}>
        <h2 className={bem('section-title')}>Money on Hand</h2>
      </header>

      <main className={bem('main')}>
        <figure className={bem('step-image')}>
          <img src={iconPlaceholder} alt="placeholder" />
        </figure>
      </main>
    </>
  )
}

export default observer(Summary);
