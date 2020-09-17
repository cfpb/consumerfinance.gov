import { useCallback, useEffect, useState } from 'react';
import { observer } from 'mobx-react';
import { useHistory, useParams } from 'react-router-dom';
import { useStore } from '../../../stores';
import { Card, CardGroup } from '../../../components/card';
import { useScrollToTop } from '../../../components/scroll-to-top';
import { formatCurrency } from '../../../lib/currency-helpers';
import { dayjs } from '../../../lib/calendar-helpers';
import { Button, ButtonLink } from '../../../components/button';
import Strategies from '../index';

import { arrowLeft, pencil } from '../../../lib/icons';
import NarrativeModal from '../../../components/narrative-notification';
import { narrativeCopy } from '../../../lib/narrative-copy';

const FixItButton = ( { result } ) => {
  const href = result.event ? `/calendar/add/${ result.event.id }/edit` : result.link.href;
  const label = result.event ? `Edit ${ result.event.categoryDetails.name }` : result.link.text;
  const { eventStore } = useStore();
  const history = useHistory();
  const buttonAction = useCallback(
    async evt => {
      evt.preventDefault();
      await history.push( href );
    },
    [ result.event, href ]
  );

  return (
    <Button icon={pencil} onClick={buttonAction} variant='strategy'>
      {label}
    </Button>
  );
};

const StrategyCards = ( { results } ) => <main className='strategies-cards'>
  <CardGroup columns={2}>
    {results.map( ( result, index ) => <Card title={result.title} icon={result.icon1} type='general' key={`strategy-${ index }`}>
      <p>{result.text}</p>
      <div className='m-card_footer'>
        {result.title === 'Explore Your General Strategies' ? null : <FixItButton result={result} />}
      </div>
    </Card>
    )}
  </CardGroup>
</main>;
function FixItStrategies() {
  const { uiStore, eventStore, strategiesStore: strategies } = useStore();
  const { week } = useParams();
  const [ showModal, setShowModal ] = useState();

  const handleModalSession = () => {
    const fixItVisit = localStorage.getItem( 'fixItVisit' );

    if ( fixItVisit ) {
      setShowModal( false );
    } else {
      setShowModal( true );
    }
  };

  useEffect( () => {
    if ( !uiStore.currentWeek && !week ) {
      uiStore.setCurrentWeek( dayjs() );
      return;
    }

    const weekInt = Number( week );

    if ( weekInt && weekInt !== uiStore.currentWeek.valueOf() ) uiStore.setCurrentWeek( dayjs( weekInt ) );
    handleModalSession();
  }, [] );

  const handleToggleModal = event => {
    event.preventDefault();
    localStorage.setItem( 'fixItVisit', true );
    setShowModal( !showModal );
  };

  useScrollToTop();

  const events = eventStore.getPositiveEventsForWeek( uiStore.currentWeek ) || [];
  const positiveFilter = events.filter( event => event.total > 0 );
  const initialBalance = positiveFilter.find( event => event.category === 'income.startingBalance' );
  const positiveEvents = positiveFilter.filter( event => event.category !== 'income.startingBalance' && event.category !== 'income.benefits.snap' );
  const weekIncome = positiveEvents.reduce( ( acc, event ) => acc + event.total, 0 );
  const negativeFilter = events.filter( event => event.total < 0 );
  const weekExpenses = negativeFilter.reduce( ( acc, event ) => acc + event.total, 0 );
  return (
    <section className='strategies'>
      {showModal &&
        <NarrativeModal showModal={showModal} handleOkClick={handleToggleModal} copy={narrativeCopy.step3} />
      }
      <header className='strategies-header'>
        <div className='strategy-cards'>
          <h2 className='strategies-header__week-range'>Week of {uiStore.weekRangeText}</h2>
          <CardGroup columns={2}>
            <div className='fixit-header'>
              <div className='fixit-header__line-first'>
                <div>Amount that you went over: </div>
                <div className='fixit-header__amount'>{uiStore.weekEndingBalanceText}</div>
              </div>

              <div className='fixit-header__line'>
                The amount you went over is what you should try to reduce. The strategies below can help.
              </div>
            </div>
            <div className='fixit-header'>
              <div className='fixit-header__comment'>
                <div>Starting Balance:</div>
                <div className='fixit-header__comment-value'>{initialBalance ? formatCurrency( initialBalance.total ) : uiStore.weekStartingBalanceText}</div>
              </div>
              <div className='fixit-header__comment'>
                <div>Income: </div>
                <div className='fixit-header__comment-value'>{formatCurrency( weekIncome )}</div>
              </div>
              <div className='fixit-header__comment'>
                <div>Expense:</div>
                <div className='fixit-header__comment-value'>{formatCurrency( weekExpenses )}</div>
              </div>
            </div>
            <div className='fixit-header'>
              <div className='fixit-header__comment'>
                <div>You currently have a SNAP balance of {uiStore.weekEndingSnapBalanceText}.</div>
              </div>
            </div>
          </CardGroup>
        </div>
      </header>
      <h2 className='strategies-header__title'>Fix-It Strategies</h2>
      <div>{strategies.fixItResults.length > 0 && <StrategyCards results={strategies.fixItResults} />}</div>
      <div>
        <Strategies />
      </div>

      <footer className='strategies-footer'>
        <ButtonLink iconSide='left' icon={arrowLeft} to='/calendar'>
          Back to Calendar
        </ButtonLink>
      </footer>
    </section>
  );
}

export default observer( FixItStrategies );
