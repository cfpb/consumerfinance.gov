const HTML_SNIPPET = `
<div data-tdp-page="results" class="content_main tdp-survey-results" data-grade-select-url="../../assess/survey/">
        <p class="label">
            Your money journey results<span aria-hidden="true" style="display:none" class="initials-display">: <span class="initials-value"></span></span>
        </p>
        <h1>Congratulations, you’re <strong>well on your way</strong>. </h1>
        <p class="h3">  This means you use many types of skills and behaviors that help you manage your money. But remember that everyone can always continue to improve.</p>
        <div class="tdp-survey-results__wrapper">
  <span class="tdp-survey-results__marker starting-out">Starting out</span>
  <span class="tdp-survey-results__marker on-the-road">On the road</span>
  <span class="tdp-survey-results__marker well-on-your-way active">Well on your way</span>
</div>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 810 123">
    <g>
      <g>
        <rect x="0" y="32" width="270" height="88" fill="#addc91" class="svg-starting-out" style="fill-opacity: .3;"></rect>
        <path d="M 270 33 V 119" stroke="green"></path>
      </g>
      <g>
        <rect x="271" y="32" width="361" height="88" fill="#addc91" class="svg-on-the-road" style="fill-opacity: .6;"></rect>
        <path d="M 631 33 V 119" stroke="green"></path>
      </g>
      <g>
        <rect x="632" y="32" width="180" height="88" fill="#addc91" class="well-on-your-way" style="fill-opacity: 1;"></rect>
      </g>

      <line y1="73" x2="810" y2="73" fill="none" stroke="#101820" stroke-miterlimit="10" stroke-dasharray="4 6"></line>
    </g>
    <g>
      <rect x="1" y="32" width="808" height="88" fill="transparent" stroke="green"></rect>
    </g>
    <image x="650" y="35" width="110px" height="75px" href="/static/apps/teachers-digital-platform/img/car.4d73d6a4fe00.png"></image>
</svg>
<div class="o-modal" id="modal-share-url" tabindex="0" aria-hidden="true" role="alertdialog" aria-labelledby="modal-share-url_title" aria-describedby="modal-share-url_desc">
  <div class="o-modal_backdrop"></div>
  <div class="o-modal_container">
    <div class="o-modal_content">
      <div class="o-modal_body">
        <button class="o-modal_close a-btn a-btn__link" type="button">
          Close<span class="a-icon a-icon__large a-icon__space-before"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 17 20.4" class="cf-icon-svg"><path d="M16.417 10.283A7.917 7.917 0 1 1 8.5 2.366a7.916 7.916 0 0 1 7.917 7.917zm-6.804.01 3.032-3.033a.792.792 0 0 0-1.12-1.12L8.494 9.173 5.46 6.14a.792.792 0 0 0-1.12 1.12l3.034 3.033-3.033 3.033a.792.792 0 0 0 1.12 1.119l3.032-3.033 3.033 3.033a.792.792 0 0 0 1.12-1.12z"></path></svg></span>
        </button>
        <h2 id="modal-share-url_title" class="h3">Share</h2>
        <div id="modal-share-url_desc">
          <div class="m-notification m-notification__error tdp-survey__initials-error">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 17 20.4" class="cf-icon-svg"><path d="M16.417 10.283A7.917 7.917 0 1 1 8.5 2.366a7.916 7.916 0 0 1 7.917 7.917zm-6.804.01 3.032-3.033a.792.792 0 0 0-1.12-1.12L8.494 9.173 5.46 6.14a.792.792 0 0 0-1.12 1.12l3.034 3.033-3.033 3.033a.792.792 0 0 0 1.12 1.119l3.032-3.033 3.033 3.033a.792.792 0 0 0 1.12-1.12z"></path></svg>
            <div class="m-notification_content">
              <div class="h4 m-notification_message">You forgot to enter your initials.</div>
            </div>
          </div>

          <label class="a-label a-label__heading" for="modal-share-url-initials-input">
            Enter your initials to get a shareable link.
          </label>
          <input class="a-text-input tdp-survey__initials" type="text" id="modal-share-url-initials-input" required="" maxlength="4" autocomplete="off">
          <div style="margin-top:1rem">
            <button class="a-btn tdp-survey__initials-set">Get link</button>
          </div>
          <div class="share-output" hidden="" data-rparam="v1_6-8_u:14:u_443lf:tIEP0XJ0JOs54ilXO4qD47WuxyQ">
            <div>
              <h4>Shareable link:</h4>
              <a href="#">www.consumerfinance.gov/...</a>
            </div>
            <div>
              <button class="a-btn">Copy link</button>
              <div class="share-output__copied" hidden="">
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 17 20.4" class="cf-icon-svg"><path d="M16.417 10.283A7.917 7.917 0 1 1 8.5 2.366a7.916 7.916 0 0 1 7.917 7.917zm-4.105-4.498a.791.791 0 0 0-1.082.29l-3.828 6.63-1.733-2.08a.791.791 0 1 0-1.216 1.014l2.459 2.952a.792.792 0 0 0 .608.285.83.83 0 0 0 .068-.003.791.791 0 0 0 .618-.393L12.6 6.866a.791.791 0 0 0-.29-1.081z"></path></svg>
                <div>Link copied to clipboard</div>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div class="o-modal_footer">
        <button class="a-btn" type="button">Close</button>
      </div>
    </div>
  </div>
</div>
<div class="o-modal" id="modal-print" tabindex="0" aria-hidden="true" role="alertdialog" aria-labelledby="modal-print_title" aria-describedby="modal-print_desc">
  <div class="o-modal_backdrop"></div>
  <div class="o-modal_container">
    <div class="o-modal_content">
      <div class="o-modal_body">
        <button class="o-modal_close a-btn a-btn__link" type="button">
          Close<span class="a-icon a-icon__large a-icon__space-before"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 17 20.4" class="cf-icon-svg"><path d="M16.417 10.283A7.917 7.917 0 1 1 8.5 2.366a7.916 7.916 0 0 1 7.917 7.917zm-6.804.01 3.032-3.033a.792.792 0 0 0-1.12-1.12L8.494 9.173 5.46 6.14a.792.792 0 0 0-1.12 1.12l3.034 3.033-3.033 3.033a.792.792 0 0 0 1.12 1.119l3.032-3.033 3.033 3.033a.792.792 0 0 0 1.12-1.12z"></path></svg></span>
        </button>
        <h2 id="modal-print_title" class="h3">Print</h2>
        <div id="modal-print_desc">
          <div class="m-notification m-notification__error tdp-survey__initials-error">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 17 20.4" class="cf-icon-svg"><path d="M16.417 10.283A7.917 7.917 0 1 1 8.5 2.366a7.916 7.916 0 0 1 7.917 7.917zm-6.804.01 3.032-3.033a.792.792 0 0 0-1.12-1.12L8.494 9.173 5.46 6.14a.792.792 0 0 0-1.12 1.12l3.034 3.033-3.033 3.033a.792.792 0 0 0 1.12 1.119l3.032-3.033 3.033 3.033a.792.792 0 0 0 1.12-1.12z"></path></svg>
            <div class="m-notification_content">
              <div class="h4 m-notification_message">You forgot to enter your initials.</div>
            </div>
          </div>
          <label class="a-label a-label__heading" for="modal-print-initials-input">
              Enter your initials to print your results.
          </label>
          <input class="a-text-input tdp-survey__initials" type="text" id="modal-print-initials-input" required="" maxlength="4" autocomplete="off">
          <div style="margin-top:1rem">
            <button class="a-btn tdp-survey__initials-set">Print</button>
          </div>
        </div>
      </div>
      <div class="o-modal_footer">
        <button class="a-btn" type="button">Close</button>
      </div>
    </div>
  </div>
</div>
<div class="o-modal" id="modal-reset" tabindex="0" aria-hidden="true" role="alertdialog" aria-labelledby="modal-reset_title" aria-describedby="modal-reset_desc">
  <div class="o-modal_backdrop"></div>
  <div class="o-modal_container">
    <div class="o-modal_content">
      <div class="o-modal_body">
        <button class="o-modal_close a-btn a-btn__link" type="button">
          Close<span class="a-icon a-icon__large a-icon__space-before"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 17 20.4" class="cf-icon-svg"><path d="M16.417 10.283A7.917 7.917 0 1 1 8.5 2.366a7.916 7.916 0 0 1 7.917 7.917zm-6.804.01 3.032-3.033a.792.792 0 0 0-1.12-1.12L8.494 9.173 5.46 6.14a.792.792 0 0 0-1.12 1.12l3.034 3.033-3.033 3.033a.792.792 0 0 0 1.12 1.119l3.032-3.033 3.033 3.033a.792.792 0 0 0 1.12-1.12z"></path></svg></span>
        </button>
        <h2 id="modal-reset_title" class="h3">Reset survey and start over</h2>
        <div id="modal-reset_desc">
          <p>Resetting your survey will cause you to lose your results.</p>
          <p>Are you sure you want to reset your survey?</p>
        </div>
      </div>
      <div class="o-modal_footer">
        <div class="m-btn-group">
          <button class="a-btn a-btn__warning" data-cancel="">Reset</button>
          <button class="a-btn a-btn__link" data-cancel="1">Return to results page</button>
        </div>
      </div>
    </div>
  </div>
</div>
        <div class="block">
            <p><strong>Now what?</strong> Review your results in more detail. Think about things you’re
                doing well and ways you can improve your financial well-being. Be sure to save your results
                so you can see them again later or share them with your teacher or a trusted adult.</p>
        </div>
        <div class="block block__padded-top block__border-top">
            <h2>Exploring your results</h2>
            <p>Your overall result is based on how you answered questions in three important subjects.
                Explore each subject to learn more about your results and how to keep moving forward
                on your money journey.
            </p>
        </div>
        <div class="o-expandable-group">
            <div class="o-expandable o-expandable__padded" data-js-hook="state_atomic_init">
                <button class="o-expandable_header o-expandable_target o-expandable_target__collapsed" title="Expand content">
                    <h3 class="o-expandable_header-left o-expandable_label">
                        <img src="/static/apps/teachers-digital-platform/img/planning.3d9110136aec.svg" alt="planning icon"> Planning and self-control
                    </h3>
                    <span class="o-expandable_header-right o-expandable_link">
                <span class="o-expandable_cue o-expandable_cue-open">
                    <span class="u-visually-hidden-on-mobile">Show</span>
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 17 20.4" class="cf-icon-svg"><path d="M16.416 10.283A7.917 7.917 0 1 1 8.5 2.366a7.916 7.916 0 0 1 7.916 7.917zm-2.958.01a.792.792 0 0 0-.792-.792H9.284V6.12a.792.792 0 1 0-1.583 0V9.5H4.32a.792.792 0 0 0 0 1.584H7.7v3.382a.792.792 0 0 0 1.583 0v-3.382h3.382a.792.792 0 0 0 .792-.791z"></path></svg>
                </span>
                <span class="o-expandable_cue o-expandable_cue-close">
                    <span class="u-visually-hidden-on-mobile">Hide</span>
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 17 20.4" class="cf-icon-svg"><path d="M16.416 10.283A7.917 7.917 0 1 1 8.5 2.366a7.916 7.916 0 0 1 7.916 7.917zm-2.958.01a.792.792 0 0 0-.792-.792H4.32a.792.792 0 0 0 0 1.583h8.346a.792.792 0 0 0 .792-.791z"></path></svg>
                </span>
            </span>
                </button>
                <div class="o-expandable_content o-expandable_content__transition u-is-animating o-expandable_content__collapsed u-hidden" style="max-height: 0px;">
                    <div class="tdp-survey-results__wrapper">
  <span class="tdp-survey-results__marker starting-out">Starting out</span>
  <span class="tdp-survey-results__marker on-the-road">On the road</span>
  <span class="tdp-survey-results__marker well-on-your-way active">Well on your way</span>
</div>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 810 123">
    <g>
      <g>
        <rect x="0" y="32" width="270" height="88" fill="#93c1bf" class="svg-starting-out" style="fill-opacity: .3;"></rect>
        <path d="M 270 33 V 119" stroke="#3b8a86"></path>
      </g>
      <g>
        <rect x="271" y="32" width="361" height="88" fill="#93c1bf" class="svg-on-the-road" style="fill-opacity: .6;"></rect>
        <path d="M 631 33 V 119" stroke="#3b8a86"></path>
      </g>
      <g>
        <rect x="632" y="32" width="180" height="88" fill="#93c1bf" class="well-on-your-way" style="fill-opacity: 1;"></rect>
      </g>

      <line y1="73" x2="810" y2="73" fill="none" stroke="#101820" stroke-miterlimit="10" stroke-dasharray="4 6"></line>
    </g>
    <g>
      <rect x="1" y="32" width="808" height="88" fill="transparent" stroke="#3b8a86"></rect>
    </g>
    <image x="650" y="35" width="110px" height="75px" href="/static/apps/teachers-digital-platform/img/car.4d73d6a4fe00.png"></image>
</svg>
                    <div class="block">
                        <p>You’re <strong>well on your way</strong> to having strong planning and self-control skills! Planning ahead, remembering information, juggling tasks, and controlling impulses
                        are important skills for managing money.</p>
                    </div>
                    <div class="tdp-survey-results__2col">
                        <div>
                            <h4>Examples of these skills:</h4>
                            <ul>
                                <li>Being in control of your behavior</li>
                                <li>Giving something up now so that you can have something better later</li>
                                <li>Setting goals and making plans to meet them</li>
                                <li>Staying focused and being able to keep going even when things get hard</li>
                            </ul>
                        </div>
                        <div>
                            <h4>Stop and think:</h4>
                            <ul>
                                <li>Which skills in this area are your strongest?</li>
                                <li>Which ones do you think can improve to help you along your money journey?</li>
                            </ul>
                        </div>
                    </div>
                </div>
            </div>
            <div class="o-expandable o-expandable__padded" data-js-hook="state_atomic_init">
                <button class="o-expandable_header o-expandable_target o-expandable_target__collapsed" title="Expand content">
                    <h3 class="o-expandable_header-left o-expandable_label">
                        <img src="/static/apps/teachers-digital-platform/img/habits.b5e335a8247c.svg" alt="habits icon"> Money habits and values
                    </h3>
                    <span class="o-expandable_header-right o-expandable_link">
                <span class="o-expandable_cue o-expandable_cue-open">
                    <span class="u-visually-hidden-on-mobile">Show</span>
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 17 20.4" class="cf-icon-svg"><path d="M16.416 10.283A7.917 7.917 0 1 1 8.5 2.366a7.916 7.916 0 0 1 7.916 7.917zm-2.958.01a.792.792 0 0 0-.792-.792H9.284V6.12a.792.792 0 1 0-1.583 0V9.5H4.32a.792.792 0 0 0 0 1.584H7.7v3.382a.792.792 0 0 0 1.583 0v-3.382h3.382a.792.792 0 0 0 .792-.791z"></path></svg>
                </span>
                <span class="o-expandable_cue o-expandable_cue-close">
                    <span class="u-visually-hidden-on-mobile">Hide</span>
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 17 20.4" class="cf-icon-svg"><path d="M16.416 10.283A7.917 7.917 0 1 1 8.5 2.366a7.916 7.916 0 0 1 7.916 7.917zm-2.958.01a.792.792 0 0 0-.792-.792H4.32a.792.792 0 0 0 0 1.583h8.346a.792.792 0 0 0 .792-.791z"></path></svg>
                </span>
            </span>
                </button>
                <div class="o-expandable_content o-expandable_content__transition u-is-animating o-expandable_content__collapsed u-hidden" style="max-height: 0px;">
                    <div class="tdp-survey-results__wrapper">
  <span class="tdp-survey-results__marker starting-out">Starting out</span>
  <span class="tdp-survey-results__marker on-the-road">On the road</span>
  <span class="tdp-survey-results__marker well-on-your-way active">Well on your way</span>
</div>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 810 123">
    <g>
      <g>
        <rect x="0" y="32" width="270" height="88" fill="#519ad6" class="svg-starting-out" style="fill-opacity: .3;"></rect>
        <path d="M 270 33 V 119" stroke="#205d90"></path>
      </g>
      <g>
        <rect x="271" y="32" width="361" height="88" fill="#519ad6" class="svg-on-the-road" style="fill-opacity: .6;"></rect>
        <path d="M 631 33 V 119" stroke="#205d90"></path>
      </g>
      <g>
        <rect x="632" y="32" width="180" height="88" fill="#519ad6" class="well-on-your-way" style="fill-opacity: 1;"></rect>
      </g>

      <line y1="73" x2="810" y2="73" fill="none" stroke="#101820" stroke-miterlimit="10" stroke-dasharray="4 6"></line>
    </g>
    <g>
      <rect x="1" y="32" width="808" height="88" fill="transparent" stroke="#205d90"></rect>
    </g>
    <image x="650" y="35" width="110px" height="75px" href="/static/apps/teachers-digital-platform/img/car.4d73d6a4fe00.png"></image>
</svg>
                    <div class="block">
                        <p>You’re <strong>well on your way</strong> to having strong money habits and values! Money habits and values guide the way we spend and save money each day. These are the things we
                        believe about money and the rules we set for ourselves to help us navigate our money
                            choices. </p>
                    </div>
                    <div class="tdp-survey-results__2col">
                        <div>
                            <h4>Examples of these skills:</h4>
                            <ul>
                                <li>Developing a positive attitude about saving and spending</li>
                                <li>Making money choices based on your own values, not someone else’s</li>
                                <li>Using your own rules to live by when making money choices</li>
                                <li>Believing in your own ability to manage money and achieve your money goals</li>
                            </ul>
                        </div>
                        <div>
                            <h4>Stop and think:</h4>
                            <ul>
                                <li>Which skills in this area are your strongest?</li>
                                <li>Which ones do you think can improve to help you along your money journey?</li>
                            </ul>
                        </div>
                    </div>
                </div>
            </div>
            <div class="o-expandable o-expandable__padded" data-js-hook="state_atomic_init">
                <button class="o-expandable_header o-expandable_target o-expandable_target__collapsed" title="Expand content">
                    <h3 class="o-expandable_header-left o-expandable_label">
                        <img src="/static/apps/teachers-digital-platform/img/knowledge.f4ecb7c4cd00.svg" alt="knowledge icon"> Money knowledge and choices
                    </h3>
                    <span class="o-expandable_header-right o-expandable_link">
                <span class="o-expandable_cue o-expandable_cue-open">
                    <span class="u-visually-hidden-on-mobile">Show</span>
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 17 20.4" class="cf-icon-svg"><path d="M16.416 10.283A7.917 7.917 0 1 1 8.5 2.366a7.916 7.916 0 0 1 7.916 7.917zm-2.958.01a.792.792 0 0 0-.792-.792H9.284V6.12a.792.792 0 1 0-1.583 0V9.5H4.32a.792.792 0 0 0 0 1.584H7.7v3.382a.792.792 0 0 0 1.583 0v-3.382h3.382a.792.792 0 0 0 .792-.791z"></path></svg>
                </span>
                <span class="o-expandable_cue o-expandable_cue-close">
                    <span class="u-visually-hidden-on-mobile">Hide</span>
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 17 20.4" class="cf-icon-svg"><path d="M16.416 10.283A7.917 7.917 0 1 1 8.5 2.366a7.916 7.916 0 0 1 7.916 7.917zm-2.958.01a.792.792 0 0 0-.792-.792H4.32a.792.792 0 0 0 0 1.583h8.346a.792.792 0 0 0 .792-.791z"></path></svg>
                </span>
            </span>
                </button>
                <div class="o-expandable_content o-expandable_content__transition u-is-animating o-expandable_content__collapsed u-hidden" style="max-height: 0px;">
                    <div class="tdp-survey-results__wrapper">
  <span class="tdp-survey-results__marker starting-out">Starting out</span>
  <span class="tdp-survey-results__marker on-the-road">On the road</span>
  <span class="tdp-survey-results__marker well-on-your-way active">Well on your way</span>
</div>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 810 123">
    <g>
      <g>
        <rect x="0" y="32" width="270" height="88" fill="#FFCE8D" class="svg-starting-out" style="fill-opacity: .3;"></rect>
        <path d="M 270 33 V 119" stroke="#DC731C"></path>
      </g>
      <g>
        <rect x="271" y="32" width="361" height="88" fill="#FFCE8D" class="svg-on-the-road" style="fill-opacity: .6;"></rect>
        <path d="M 631 33 V 119" stroke="#DC731C"></path>
      </g>
      <g>
        <rect x="632" y="32" width="180" height="88" fill="#FFCE8D" class="well-on-your-way" style="fill-opacity: 1;"></rect>
      </g>

      <line y1="73" x2="810" y2="73" fill="none" stroke="#101820" stroke-miterlimit="10" stroke-dasharray="4 6"></line>
    </g>
    <g>
      <rect x="1" y="32" width="808" height="88" fill="transparent" stroke="#DC731C"></rect>
    </g>
    <image x="650" y="35" width="110px" height="75px" href="/static/apps/teachers-digital-platform/img/car.4d73d6a4fe00.png"></image>
</svg>

                    <div class="block">
                        <p>You’re <strong>well on your way</strong> toward strong money knowledge and decision-making skills! Money knowledge and choices means having the information and skills you need to make thoughtful
                        decisions about money.</p>
                    </div>
                    <div class="tdp-survey-results__2col">
                        <div>
                            <h4>Examples of these skills:</h4>
                            <ul>
                                <li>Understanding basic money concepts and using them with confidence</li>
                                <li>Managing money to reach your goal</li>
                                <li>Being able to identify trusted sources for information about money</li>
                                <li>Comparing choices before making a money decision</li>
                            </ul>
                        </div>
                        <div>
                            <h4>Stop and think:</h4>
                            <ul>
                                <li>Which skills in this area are your strongest?</li>
                                <li>Which ones do you think you can improve to help you along your money journey?</li>
                            </ul>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div class="o-well block">
            <h2>Three things you can do to get farther down the road on your money journey</h2>
            <h3>① Explore your strengths</h3>
            <p>The <a class="a-link a-link__icon" href="https://files.consumerfinance.gov/f/documents/cfpb_building_block_activities_middle-school-assessment-student-worksheet.pdf"><span class="a-link_text">Taking the next steps on your money journey</span> <svg class="cf-icon-svg" viewBox="0 0 12 19" xmlns="http://www.w3.org/2000/svg"><path d="M11.16 16.153a.477.477 0 0 1-.476.475H1.316a.476.476 0 0 1-.475-.475V3.046a.476.476 0 0 1 .475-.475h6.95l2.893 2.893zm-1.11-9.925H8.059a.575.575 0 0 1-.574-.573V3.679H1.95v11.84h8.102zm-1.234 5.604L6.388 14.26a.554.554 0 0 1-.784 0l-2.428-2.428a.554.554 0 1 1 .783-.784l1.483 1.482V7.41a.554.554 0 1 1 1.108 0v5.12l1.482-1.482a.554.554 0 0 1 .784.783z"></path></svg></a> worksheet can help you think about your strengths and set goals to get the money future you want.</p>
            <h3>② Talk with your teacher</h3>
            <p>Talk with your teacher about your money map. Your teacher can review your goals and find the right activities to support your progress on your money journey.</p>
            <h3>③ Talk with a parent or trusted adult</h3>
            <p>Talk with a parent or trusted adult about your money journey. You can explore these resources to help guide your conversation:</p>
            <ul>
                <li><a class="a-link a-link__icon" href="https://files.consumerfinance.gov/f/documents/cfpb_building_block_activities_who-shapes-my-money-choices_handout.pdf"><span class="a-link_text">Who shapes my money choices?</span> <svg class="cf-icon-svg" viewBox="0 0 12 19" xmlns="http://www.w3.org/2000/svg"><path d="M11.16 16.153a.477.477 0 0 1-.476.475H1.316a.476.476 0 0 1-.475-.475V3.046a.476.476 0 0 1 .475-.475h6.95l2.893 2.893zm-1.11-9.925H8.059a.575.575 0 0 1-.574-.573V3.679H1.95v11.84h8.102zm-1.234 5.604L6.388 14.26a.554.554 0 0 1-.784 0l-2.428-2.428a.554.554 0 1 1 .783-.784l1.483 1.482V7.41a.554.554 0 1 1 1.108 0v5.12l1.482-1.482a.554.554 0 0 1 .784.783z"></path></svg></a></li>
                <li><a class="a-link a-link__icon" href="https://files.consumerfinance.gov/f/documents/cfpb_building_block_activities_options-for-storing-savings_handout.pdf"><span class="a-link_text">Options for storing your savings</span> <svg class="cf-icon-svg" viewBox="0 0 12 19" xmlns="http://www.w3.org/2000/svg"><path d="M11.16 16.153a.477.477 0 0 1-.476.475H1.316a.476.476 0 0 1-.475-.475V3.046a.476.476 0 0 1 .475-.475h6.95l2.893 2.893zm-1.11-9.925H8.059a.575.575 0 0 1-.574-.573V3.679H1.95v11.84h8.102zm-1.234 5.604L6.388 14.26a.554.554 0 0 1-.784 0l-2.428-2.428a.554.554 0 1 1 .783-.784l1.483 1.482V7.41a.554.554 0 1 1 1.108 0v5.12l1.482-1.482a.554.554 0 0 1 .784.783z"></path></svg></a></li>
                <li><a class="a-link a-link__icon" href="https://files.consumerfinance.gov/f/documents/cfpb_building_block_activities_what-is-debt_handout.pdf"><span class="a-link_text">What is debt?</span> <svg class="cf-icon-svg" viewBox="0 0 12 19" xmlns="http://www.w3.org/2000/svg"><path d="M11.16 16.153a.477.477 0 0 1-.476.475H1.316a.476.476 0 0 1-.475-.475V3.046a.476.476 0 0 1 .475-.475h6.95l2.893 2.893zm-1.11-9.925H8.059a.575.575 0 0 1-.574-.573V3.679H1.95v11.84h8.102zm-1.234 5.604L6.388 14.26a.554.554 0 0 1-.784 0l-2.428-2.428a.554.554 0 1 1 .783-.784l1.483 1.482V7.41a.554.554 0 1 1 1.108 0v5.12l1.482-1.482a.554.554 0 0 1 .784.783z"></path></svg></a></li>
            </ul>
        </div>
        <div class="block block__padded-bottom block__border-bottom">
            <h2>What does it all mean?</h2>
            <p>Keep in mind that managing money is a lifelong journey. Everyone, no matter their age, can always improve
                their knowledge, skills, and habits! Knowing where you are today can help you plan to get the future you
                want. Come back and take the money journey survey again when you’re ready to check your progress.</p>
        </div>
        <div class="tdp-survey__save-block block">
  <h2>Save your results</h2>
  <div class="m-btn-group">
    <button type="button" class="a-btn" data-open-modal="modal-print">
      Print results <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 14 19" class="cf-icon-svg"><path d="m8.698 2.358 3.065 3.066v1.95h.16a1.112 1.112 0 0 1 1.109 1.108v4.837a1.112 1.112 0 0 1-1.109 1.108h-.16v1.726a.477.477 0 0 1-.475.475H2.712a.477.477 0 0 1-.475-.475v-1.726h-.16A1.112 1.112 0 0 1 .968 13.32V8.482a1.112 1.112 0 0 1 1.109-1.108h.16v-4.54a.476.476 0 0 1 .475-.476zm-.22 3.876a.61.61 0 0 1-.608-.608v-2.16H3.345v3.908h7.31v-1.14zm2.177 4.512h-7.31v4.773h7.31zm-1.054.874h-5.26v1.109h5.26zm0 1.962h-5.26v1.108h5.26zm2.437-4.485a.554.554 0 1 0-.554.554.554.554 0 0 0 .554-.554z"></path></svg>
    </button>
    <a class="a-btn" href="/consumer-tools/save-as-pdf-instructions/" target="_blank">How to save results
      as a PDF <svg class="cf-icon-svg" viewBox="0 0 14 19" xmlns="http://www.w3.org/2000/svg"><path d="M13.017 3.622v4.6a.554.554 0 0 1-1.108 0V4.96L9.747 7.122a1.65 1.65 0 0 1 .13.646v5.57A1.664 1.664 0 0 1 8.215 15h-5.57a1.664 1.664 0 0 1-1.662-1.663v-5.57a1.664 1.664 0 0 1 1.662-1.662h5.57A1.654 1.654 0 0 1 9 6.302l2.126-2.126H7.863a.554.554 0 1 1 0-1.108h4.6a.554.554 0 0 1 .554.554zM8.77 8.1l-2.844 2.844a.554.554 0 0 1-.784-.783l2.947-2.948H2.645a.555.555 0 0 0-.554.555v5.57a.555.555 0 0 0 .554.553h5.57a.555.555 0 0 0 .554-.554z"></path></svg></a>
    <button type="button" class="a-btn" data-open-modal="modal-share-url">
      Share results <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 15 19" class="cf-icon-svg"><path d="M14.395 14.803a2.64 2.64 0 1 1-5.118-.91l-4.093-2.589a2.645 2.645 0 1 1 0-3.608l4.093-2.588a2.644 2.644 0 1 1 .593.936L5.755 8.646a2.659 2.659 0 0 1 0 1.707l4.115 2.603a2.64 2.64 0 0 1 4.525 1.847z"></path></svg>
    </button>
  </div>
</div>
        <div class="survey-reset--link--wrap">
            <p>
                <button class="a-btn a-btn__link a-btn__warning" data-open-modal="modal-reset">
                    Reset survey and start over
                </button>
            </p>
        </div>
    </div>
`;

export default HTML_SNIPPET;
