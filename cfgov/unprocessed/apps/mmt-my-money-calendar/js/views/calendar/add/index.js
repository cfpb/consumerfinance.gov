import { Switch, Route, withRouter } from 'react-router-dom';
import CategoryBrowser from './category-browser';
import Form from './form';
import Debug from './debug';

const Add = ({ match }) => (
  <Switch>
    <Route path={`${match.path}/debug`}>
      <Debug />
    </Route>

    <Route path={`${match.path}/new`}>
      <Form />
    </Route>

    <Route path={`${match.path}/:categories+`}>
      <CategoryBrowser />
    </Route>

    <Route path={match.path}>
      <CategoryBrowser />
    </Route>
  </Switch>
);

export default withRouter(Add);
