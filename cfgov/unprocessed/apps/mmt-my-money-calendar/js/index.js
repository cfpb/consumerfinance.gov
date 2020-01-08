import { render } from 'react-dom';
import Greeting from './components/greeting';

const App = () => (
  <div className="hello">
    <Greeting />
  </div>
);

render(<App />, document.querySelector('#mmt-my-money-calendar'));
