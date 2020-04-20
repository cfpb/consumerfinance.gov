import { observer } from 'mobx-react';
import { useHistory, Link, Redirect } from "react-router-dom";
import { useStore } from '../../stores';

function Home() {
  const { eventStore } = useStore();

  // Once IndexedDB data loads, redirect to either calendar or first run wizard:
  if (eventStore.eventsLoaded && eventStore.events.length > 0) return <Redirect to="/calendar" />;
  if (eventStore.eventsLoaded && !eventStore.events.length) return <Redirect to="/money-on-hand" />;

  // Display loading message until data is loaded:
  return (
    <main className="mmt-view home">
      <em>Loading...</em>
    </main>
  );
}

export default observer(Home);
