import { useScrollToTop } from '../../components/scroll-to-top';
import { ButtonLink } from '../../components/button';
import Hero from '../../components/hero';

import heroImg from 'img/Hero_2.png';
import { arrowRight } from '../../lib/icons';

export default function Start() {
  useScrollToTop();

  return (
    <>
      <Hero
        title="MyMoney Calendar"
        subtitle="See how your money flows from week to week and learn how to avoid coming up short."
        image={heroImg}
        alt="MyMoney Calendar"
      />
      <br />
      <div className="m-hero_subhead">
        <p>Enter your income, expenses, and cash-on-hand to build your calendar.</p>
        <p>It's okay to estimate.</p>

        <ButtonLink icon={arrowRight} iconSide="right" to="/money-on-hand/sources">Get Started</ButtonLink>
      </div>
    </>
  );
}
