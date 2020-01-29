import { useCallback } from 'react';
import { useHistory, Link } from "react-router-dom";
import Hero from '../../components/hero';
import Button from '../../components/button';
import { useScrollToTop } from '../../components/scroll-to-top';

import heroImg from 'img/Hero_2.png';
import arrowRight from 'cf-icons/src/icons/arrow-right.svg';

export default function Home() {
  useScrollToTop();

  const history = useHistory();

  const nextPage = useCallback((evt) => {
    evt.preventDefault();
    history.push('/wizard/starting-balance');
  }, [history]);

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
      <Button icon={arrowRight} iconSide="right" onClick={nextPage}>Get started</Button>
      <br />
      <br />
    </main>
  );
}
