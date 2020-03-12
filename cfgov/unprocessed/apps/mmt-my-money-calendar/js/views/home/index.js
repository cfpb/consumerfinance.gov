import { observer } from 'mobx-react';
import { useHistory, Link, Redirect } from "react-router-dom";
import Hero from '../../components/hero';
import { ButtonLink } from '../../components/button';
import { useScrollToTop } from '../../components/scroll-to-top';
import { useStore } from '../../stores';

import heroImg from 'img/Hero_2.png';
import arrowRight from '@cfpb/cfpb-icons/src/icons/arrow-right.svg';

function Home() {
  useScrollToTop();

  const history = useHistory();
  const { eventStore } = useStore();

  if (eventStore.events.length > 0) return <Redirect to="/calendar" />;

  // This is the Home Page of the app
  return (
    <main className="mmt-view home">
      <Hero
        title="My Money Calendar"
        subtitle="Visualize your spending and learn strategies to manage your weekly and monthly budget"
        image={heroImg}
        alt="My Money Calendar"
      />
      <br />
      <div className="m-hero_subhead">
        Input your income, expenses, and cash-on-hand to build your calendar,
        Estimates are acceptable.
      </div>
      <br />
      <ButtonLink icon={arrowRight} iconSide="right" to="/calendar">Get started</ButtonLink>
    </main>
  );
}

export default observer(Home);
