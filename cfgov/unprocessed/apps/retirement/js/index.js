import graphView from './views/graph-view';
import nextStepsView from './views/next-steps-view';
import questionsView from './views/questions-view';
import tooltipsView from './views/tooltips-view';

const app = {
  init: function() {
    graphView.init();
    questionsView.init();
    nextStepsView.init();
    tooltipsView.init();
  }
};

app.init();
