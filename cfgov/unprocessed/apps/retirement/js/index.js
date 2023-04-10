import graphView from './views/graph-view.js';
import nextStepsView from './views/next-steps-view.js';
import questionsView from './views/questions-view.js';
import tooltipsView from './views/tooltips-view.js';

const app = {
  init: function () {
    graphView.init();
    questionsView.init();
    nextStepsView.init();
    tooltipsView.init();
  },
};

app.init();
