import { useScrollToTop } from '../../components/scroll-to-top';
import { ButtonLink } from '../../components/button';
import Hero from '../../components/hero';

import { arrowRight } from '../../lib/icons';
import hero from 'img/Hero_2.png';

export default function Start() {
  useScrollToTop();

  return (
    <>
      <Hero
        title='myMoney Calendar'
        subtitle='See how your money flows from week to week and learn how to avoid coming up short.'
        image={hero}
        alt='myMoney Calendar'
      />
      <br />
      <div className='m-hero_subhead'>
        <p>Enter your income, expenses, and cash-on-hand to build your calendar.</p>
        <p>It's okay to estimate.</p>

        <ButtonLink icon={arrowRight} iconSide='right' to='/money-on-hand/sources'>
          Get Started
        </ButtonLink>
      </div>
    </>
  );
}
