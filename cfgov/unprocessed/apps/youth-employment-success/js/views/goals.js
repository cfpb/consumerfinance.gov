import { checkDom, setInitFlag } from '../../../../js/modules/util/atomic-helpers';
import { toArray } from '../util';
import {
  updateGoalAction,
  updateGoalImportanceAction,
  updateGoalStepsAction,
  updateGoalTimelineAction
} from '../reducers/goal-reducer';
import inputView from './input';

const CLASSES = {
  CONTAINER: 'js-yes-goals',
  LONG_TERM_GOAL: 'js-long-term-goal',
  GOAL_IMPORTANCE: 'js-goal-importance',
  GOAL_STEPS: 'js-goal-steps',
  GOAL_TIMELINE: 'a-radio',
};

const GOALS_TO_ACTIONS = {
  'longTermGoal': updateGoalAction, 
  'goalImportance': updateGoalImportanceAction,
  'goalSteps':  updateGoalStepsAction
};

function goalsView(element, { store }) {
  const _dom = checkDom(element, CLASSES.CONTAINER);

  function _handleUpdateGoals({ name, event }) {
    const method = GOALS_TO_ACTIONS[name];

    if (method) {
      store.dispatch( method( {
        value: event.target.value
      }))
    }
  }

  function _handleTimelineUpdate({ event }) {
    store.dispatch(updateGoalTimelineAction({
      value: event.target.value
    }));
  }

  function _initInputs() {
    [
      CLASSES.LONG_TERM_GOAL,
      CLASSES.GOAL_IMPORTANCE,
      CLASSES.GOAL_STEPS,
    ].forEach(klass => {
      inputView(_dom.querySelector(`.${klass}`), {
        events: {
          blur: _handleUpdateGoals
        }
      }).init();
    });

    toArray(
      _dom.querySelectorAll(`.${CLASSES.GOAL_TIMELINE}`)
    ).forEach(radio => {
      inputView(radio, {
        events: {
          click: _handleTimelineUpdate
        },
        type: 'radio'
      }).init();
    });
  }

  return {
    init() {
      if (setInitFlag(_dom)) {
        _initInputs();

        store.subscribe(() => {
          console.log(store.getState())
        })
      }
    }
  }
}

goalsView.CLASSES = CLASSES;

export default goalsView;
