import Expandable from '@cfpb/cfpb-expandables/src/Expandable';
import checkbox from './templates/checkbox';
import checklistGroupView from './views/checklist-group';
import checklistMap from './models/checklist-map';
import error from './views/error';
import printButtonView from '../../../../../apps/youth-employment-success/js/views/print-button';
import printTableView from './views/print-table';
import selectedItems from './models/selected-items';
import updateExpandableButtonText from './expandables';

const TEMPLATE_SELECTOR = 'cbg-checklist';

const CHECKLIST_GROUP_SELECTOR = 'm-checklist-group';
const PRINT_BUTTON_SELECTOR = 'js-cbg-print';

const GOALS_TABLE_SELECTOR = 'cbg-print-goals';
const NEXT_STEPS_TABLE_SELECTOR = 'cbg-print-next-steps';

const EXPANDABLE_UI_CLASSES = Expandable.prototype.ui;
const EXPANDABLE_GROUP_SELECTOR = Expandable.prototype.classes.group;
const expandableEls = Array.prototype.slice.call(
  document.querySelectorAll(
    `${ EXPANDABLE_UI_CLASSES.base }`
  )
)
  .filter( e => e.parentNode.classList.contains( EXPANDABLE_GROUP_SELECTOR ) );

const expandableData = expandableEls.reduce( ( memo, expandable ) => {
  const labelText = expandable.querySelector( `${ EXPANDABLE_UI_CLASSES.label }` );
  const content = expandable.querySelector( `${ EXPANDABLE_UI_CLASSES.content }` );

  memo[labelText.textContent.trim()] = content.innerHTML;

  return memo;
}, {} );

document.querySelector( `.${ TEMPLATE_SELECTOR }` ).parentNode.classList.add( 'cbg-print-block' );

const items = selectedItems( { maxElements: 5 } );
const checklistLookup = checklistMap( expandableData );

const errorView = error( document.querySelector( `.${ error.CONTAINER }` ) );

updateExpandableButtonText( expandableEls );

checklistGroupView(
  document.querySelector( `.${ CHECKLIST_GROUP_SELECTOR }` ), {
    selectedItems: items
  }
).init();

printButtonView(
  document.querySelector( `.${ PRINT_BUTTON_SELECTOR }` ), {
    btnClass: PRINT_BUTTON_SELECTOR,
    onBeforePrint: updateTableView,
    onClick: handlePrintChecklist
  }
).init();

const goalsTableView = printTableView(
  document.querySelector( `.${ GOALS_TABLE_SELECTOR }` )
);
const nextStepsTableView = printTableView(
  document.querySelector( `.${ NEXT_STEPS_TABLE_SELECTOR }` )
);

function handlePrintChecklist( event, printFn ) {
  if ( items.isMinItemsSelected() ) {
    errorView.render( false );
    printFn( event );
  } else {
    errorView.render( true );
    event.preventDefault();
    event.stopImmediatePropagation();
  }
}

function updateTableView() {
  const selectedChecklistItems = items.elements();
  const goalsTableContent = selectedChecklistItems.reduce( ( memo, item ) => {
    const checklistItem = checkbox( item );
    const checklistItemDetail = checklistLookup.get( item );

    memo.push( [ checklistItem, checklistItemDetail ] );

    return memo;
  }, [] );

  goalsTableView.render( goalsTableContent );

  const remainingItems = checklistLookup.filterKeysBy( key => selectedChecklistItems.indexOf( key ) === -1 );
  const nextStepsTableContent = remainingItems.map( item => checkbox( item ) );

  nextStepsTableView.render( nextStepsTableContent );
}
