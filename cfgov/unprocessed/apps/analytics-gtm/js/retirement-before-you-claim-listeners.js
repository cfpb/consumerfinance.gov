import { analyticsSendEvent, analyticsLog } from '@cfpb/cfpb-analytics';

// Retirement - Before You Claim custom analytics file

(function () {
  const questionsAnswered = [];
  let sliderClicks = 0;
  let sliderIsActive = false;
  let stepOneSubmitted = false;

  /**
   * @param {number} month - Month of birth.
   * @param {number} day - Day of birth.
   * @param {number} year - Year of birth.
   * @returns {number} The age, in years, based on current date.
   */
  function calculateAge(month, day, year) {
    const now = new Date();
    const birthdate = new Date(year, Number(month) - 1, day);
    let age = now.getFullYear() - birthdate.getFullYear();
    const m = now.getMonth() - birthdate.getMonth();
    if (m < 0 || (m === 0 && now.getDate() < birthdate.getDate())) {
      age--;
    }
    if (isNaN(age)) {
      return false;
    }
    return age;
  }

  const stepOneForm = document.querySelector('#step-one-form');
  stepOneForm.addEventListener('submit', formSubmitted);

  /**
   * Handle submission of the form.
   * @param {Event} evt - Form submit event object.
   */
  function formSubmitted(evt) {
    evt.preventDefault();
    stepOneSubmitted = true;

    // Track birthdate.
    const month = document.querySelector('#bd-month').value;
    const day = document.querySelector('#bd-day').value;
    analyticsSendEvent({
      event: 'Before You Claim Interaction',
      action: 'Get Your Estimates submit birthdate',
      label: 'Birthdate Month and Day - ' + month + '/' + day,
    });

    // Track age.
    const year = document.querySelector('#bd-year').value;
    const age = calculateAge(month, day, year);
    analyticsSendEvent({
      event: 'Before You Claim Interaction',
      action: 'Get Your Estimates submit age',
      label: 'Age ' + age,
    });

    // Start mouseflow heatmap capture.
    if (window.mouseflow) {
      // Stop any in-progress heatmap capturing.
      window.mouseflow.stop();
      // Start a new heatmap recording.
      window.mouseflow.start();
      analyticsLog('Mouseflow capture started!');
    }

    document
      .querySelector('#claim-canvas')
      .addEventListener('mousedown', function (event) {
        if (event.target.classList.contains('graph--bar')) {
          const age = event.target.getAttribute('data-bar_age');
          analyticsSendEvent({
            event: 'Before You Claim Interaction',
            action: 'Graph Age Bar clicked',
            label: 'Age ' + age,
          });
        }
      });

    document
      .querySelector('#graph__slider-input')
      .addEventListener('mousedown', function () {
        sliderIsActive = true;
        sliderClicks++;
        analyticsSendEvent({
          event: 'Before You Claim Interaction',
          action: 'Slider clicked',
          label: 'Slider clicked ' + sliderClicks + ' times',
        });
      });

    document
      .querySelector('#claim-canvas')
      .addEventListener('click', function (event) {
        const target = event.target.parentNode;
        if (target.classList.contains('age-text')) {
          const age = target.getAttribute('data-age-value');
          analyticsSendEvent({
            event: 'Before You Claim Interaction',
            action: 'Age Text Box clicked',
            label: 'Age ' + age,
          });
        }
      });

    document.body.addEventListener('mouseup', function () {
      if (sliderIsActive === true) {
        const age = document.querySelector('.selected-age').innerText;
        analyticsSendEvent({
          event: 'Before You Claim Interaction',
          action: 'Slider released',
          label: 'Age ' + age,
        });
        sliderIsActive = false;
      }
    });

    const lifestyleBtns = document.querySelectorAll('button.lifestyle-btn');
    for (let i = 0, len = lifestyleBtns.length; i < len; i++) {
      lifestyleBtns[i].addEventListener('click', function (event) {
        const target = event.currentTarget;
        const $container = target.closest('.lifestyle-question__container');
        const question = $container.querySelector('h3').innerText.trim();
        const value = target.value;
        if (questionsAnswered.indexOf(question) === -1) {
          questionsAnswered.push(question);
        }
        if (questionsAnswered.length === 5) {
          analyticsSendEvent({
            event: 'Before You Claim Interaction',
            action: 'All Lifestyle Buttons clicked',
            label: 'All button clicks',
          });
        }
        analyticsSendEvent({
          event: 'Before You Claim Interaction',
          action: 'Lifestyle Button clicked',
          label: 'Question: ' + question + ' - ' + value,
        });
      });
    }

    const benefitsRadios = document.querySelectorAll(
      'input[name="benefits-display"]',
    );
    for (let i = 0, len = benefitsRadios.length; i < len; i++) {
      benefitsRadios[i].addEventListener('click', function (event) {
        if (stepOneSubmitted) {
          const val = event.currentTarget.value;
          analyticsSendEvent({
            event: 'Before You Claim Interaction',
            action: 'Benefits View clicked',
            label: val,
          });
        }
      });
    }

    document
      .querySelector('#retirement-age-selector')
      .addEventListener('change', function (event) {
        const target = event.currentTarget;
        if (target.selectedIndex > -1) {
          const val = target[target.selectedIndex].value;
          analyticsSendEvent({
            event: 'Before You Claim Interaction',
            action: 'Planned Retirement Age selected',
            label: val,
          });
        }
      });

    document
      .querySelector('[data-tooltip-target]')
      .addEventListener('click', function (event) {
        const target = event.currentTarget.getAttribute('data-tooltip-target');
        analyticsSendEvent({
          event: 'Before You Claim Interaction',
          action: 'Tooltip clicked',
          label: 'Target: ' + target,
        });
      });
  }
})();
