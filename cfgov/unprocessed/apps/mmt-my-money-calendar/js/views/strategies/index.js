import { observer } from 'mobx-react';
import { useStore } from '../../stores';
import { useScrollToTop } from '../../components/scroll-to-top';

function Strategies() {
  const { uiStore } = useStore();

  useScrollToTop();

  return (
    <section className="strategies">

    </section>
  )
}

export default observer(Strategies);
