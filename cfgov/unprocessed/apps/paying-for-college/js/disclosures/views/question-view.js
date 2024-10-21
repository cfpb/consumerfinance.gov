import $ from '../../../../../js/modules/util/dollar-sign.js';
import { analyticsSendEvent } from '@cfpb/cfpb-analytics';
import postVerification from '../dispatchers/post-verify.js';
import getFinancial from '../dispatchers/get-financial-values.js';
import getSchool from '../dispatchers/get-school-values.js';

const questionView = {
  $settlementBigQuestion: $('.step__settlement'),
  $nonsettlementBigQuestion: $('.step__nonsettlement'),
  $getOptions: $('.get-options'),
  $followupNoNotSure: $('.followup--no-not-sure'),
  $followupYes: $('.followup--yes'),
  $optionsWrapper: $('.get-options--dynamic'),
  $options: $('.option'),
  $optionsSidebar: $('.get-options__sidebar'),
  $transferCredits: $('.option--transfer-credits'),
  $exploreSchools: $('.option--explore-schools'),
  $workWhileStudying: $('.option--work-while-studying'),
  $takeAction: $('.option--take-action'),
  $nextSteps: $('.next-steps'),

  /**
   * Initiates the object
   */
  init: function () {
    const settlementStatus = getSchool.values().settlementSchool || false;

    this.displayOptions(settlementStatus);
    this.bigQuestionListener(settlementStatus);
  },

  /**
   * Show the appropriate content in Step 3 for settlement schools.
   * @param {boolean} isSettlementStatus - Flag if this is a settlement school.
   */
  displayOptions: function (isSettlementStatus) {
    if (isSettlementStatus === true) {
      questionView.$settlementBigQuestion.show();
      questionView.$nonsettlementBigQuestion.hide();
      $('#question__answer-no').hide();
      questionView.$optionsWrapper.addClass(
        'get-options--settlement content__main',
      );
      questionView.$transferCredits.remove();
      questionView.$exploreSchools.remove();
      questionView.$takeAction.remove();
      questionView.$options.addClass('option--settlement');
      questionView.$optionsSidebar.show();
      questionView.$optionsWrapper.removeClass('get-options--dynamic');
    } else {
      questionView.$settlementBigQuestion.hide();
      questionView.$nonsettlementBigQuestion.show();
      questionView.$workWhileStudying.remove();
      questionView.$optionsSidebar.remove();
    }
  },

  /**
   * Listener function for the "big question"/"moment of pause" buttons.
   * @param {boolean} isSettlementStatus - Flag if this is a settlement school.
   */
  bigQuestionListener: function (isSettlementStatus) {
    const $answerButtons = $('.question__answers > button');
    $answerButtons.listen('click', function () {
      const values = getFinancial.values();
      if (isSettlementStatus === true) {
        postVerification.verify(values.offerID, values.schoolID, false);
      }
      $answerButtons.removeClass('active');
      $(this).addClass('active');

      if (isSettlementStatus === true) {
        questionView.$followupYes.hide();
        questionView.$followupNoNotSure.hide();
      } else if ($(this).attr('id') === 'question__answer-yes') {
        questionView.$followupYes.show();
        questionView.$followupNoNotSure.hide();
      } else {
        questionView.$followupNoNotSure.show();
        questionView.$followupYes.hide();
      }
      // Show the rest of the page
      questionView.$getOptions.show();
      questionView.$nextSteps.show();
      // $('html, body')
      //   .stop()
      //   .animate(
      //     {
      //       scrollTop: questionView.$getOptions.offset().top - 120,
      //     },
      //     900,
      //     'swing',
      //     function () {
      //       // Noop function.
      //     }
      //   );

      analyticsSendEvent({
        action: 'Step Completed',
        label: $(this).text().trim(),
      });
    });
  },
};

export default questionView;
