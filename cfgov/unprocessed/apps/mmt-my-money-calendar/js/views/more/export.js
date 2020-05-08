import { observer } from 'mobx-react';
import { useParams } from 'react-router-dom';
import { ButtonLink } from '../../components/button';
import { useScrollToTop } from '../../components/scroll-to-top';
import { useBEM } from '../../lib/hooks';
import { useStore } from '../../stores';

function Export() {
  const { eventStore, strategiesStore } = useStore();
  const bem = useBEM('more');
  const { dataType } = useParams();

  useScrollToTop();

  return (
    <section className={bem()}>
      <header className={bem('header')}>
        <h1 className={bem('app-title')}>MyMoney Calendar</h1>
        <h2 className={bem('section-title')}>Save {dataType}</h2>
      </header>

      <ButtonLink to="/more" variant="secondary">Back</ButtonLink>
    </section>
  );
}

export default observer(Export);
