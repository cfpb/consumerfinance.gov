import Store from '../../../js/organisms/MortgagePerformanceTrends/stores/store';
import { UNDEFINED } from './util';

class YesStore extends Store {
  constructor( reducer, middlewares ) {
    super( middlewares );

    this.reducer = reducer;
    this.state = this.reduce( UNDEFINED );
  }

  reduce( state, action = { type: null } ) {
    return this.reducer( state, action );
  }
}

export default YesStore;
