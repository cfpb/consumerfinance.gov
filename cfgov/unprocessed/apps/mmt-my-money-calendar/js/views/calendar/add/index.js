import { Switch, Route, withRouter } from 'react-router-dom';
import CategoryBrowser from './category-browser';
import Form from './form';

const Add = ({ match }) => (
  <Switch>
    <Route path={`${match.path}/:categories+/new`}>
      <Form />
    </Route>

    <Route path={`${match.path}/new`}>
      <Form />
    </Route>

    <Route path={`${match.path}/:id/edit`}>
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
