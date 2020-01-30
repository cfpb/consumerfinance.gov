import { useEffect, useCallback } from 'react';
import { useLocation, useParams } from 'react-router-dom';
import { observer } from 'mobx-react';
import { useTitle } from 'react-use';
import { DateTime } from 'luxon';
import { useStore } from '../../stores';

function Calendar() {
  const { uiStore, eventStore } = useStore();
  const location = useLocation();
  const params = useParams();

  useTitle('Calendar');

  useEffect(() => {
    uiStore.setPageTitle('myMoney Calendar');
  }, [location, params]);

  return (
    <section className="calendar">
      <div className="calendar__rows">
      </div>
    </section>
  )
}

export default observer(Calendar);
