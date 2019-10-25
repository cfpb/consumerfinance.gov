import { checkDom, setInitFlag } from '../../../../../js/modules/util/atomic-helpers';
import printButton from './print-button';
import reviewChoiceView from './choice';
import reviewDetailsView from './details';
import reviewGoalsView from './goals';

function ReviewSectionView(element, {store }) {
  function _handleRouteChoice() {

  }

  return {
    init() {
      if (setInitFlag(_dom)) {
        reviewChoiceView(
          reviewChoiceView.CLASSES.CONTAINER,
          { store, onChooseRoute: _handleRouteChoice }
        ).init();
      }
    }
  }
}