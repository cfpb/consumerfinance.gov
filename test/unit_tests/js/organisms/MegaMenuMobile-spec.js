import MegaMenu from '../../../../cfgov/unprocessed/js/organisms/MegaMenu';
import { simulateEvent } from '../../../util/simulate-event';

const BASE_CLASS = 'o-mega-menu';
const HTML_SNIPPET = `
<nav class="o-mega-menu" data-js-hook="behavior_flyout-menu" aria-label="main menu">
    <button class="o-mega-menu_trigger" data-js-hook="behavior_flyout-menu_trigger" aria-haspopup="menu" aria-expanded="false">
        <span class="o-mega-menu_trigger-open">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 784.5 1200" class="cf-icon-svg"><path d="M65 370.5h654.5c35.9 0 65-29.1 65-65s-29.1-65-65-65H65c-35.9 0-65 29.1-65 65s29.1 65 65 65zM719.5 515H65c-35.9 0-65 29.1-65 65s29.1 65 65 65h654.5c35.9 0 65-29.1 65-65s-29.1-65-65-65zM719.5 789.4H65c-35.9 0-65 29.1-65 65s29.1 65 65 65h654.5c35.9 0 65-29.1 65-65s-29.1-65-65-65z"></path></svg>
        </span>
        <span class="o-mega-menu_trigger-close">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 718.9 1200" class="cf-icon-svg"><path d="M451.4 613.7l248.1-248.1c25.6-25.1 26-66.3.8-91.9s-66.3-26-91.9-.8l-.8.8-248.1 248.1-248.1-248.1c-25.4-25.4-66.5-25.4-91.9 0s-25.4 66.5 0 91.9l248.1 248.1L19.5 861.8c-25.6 25.1-26 66.3-.8 91.9s66.3 26 91.9.8l.8-.8 248.1-248.1 248.1 248.1c25.4 25.4 66.5 25.4 91.9 0s25.4-66.5 0-91.9L451.4 613.7z"></path></svg>
        </span>
        <span class="u-visually-hidden">Menu</span>
    </button>

    <div class="o-mega-menu_content o-mega-menu_content-1 u-hidden-overflow u-move-transition u-move-to-origin" aria-expanded="false" data-js-hook="behavior_flyout-menu_content">
        <div class="o-mega-menu_content-wrapper o-mega-menu_content-1-wrapper ">

            <div class="o-mega-menu_content-grid o-mega-menu_content-1-grid">

                <div class="o-mega-menu_content-lists o-mega-menu_content-1-lists ">

                    <div class="o-mega-menu_content-list o-mega-menu_content-1-list ">

                        <ul class="m-list m-list__unstyled">
                            <li class="m-list_item o-mega-menu_content-item o-mega-menu_content-1-item ">
                                <div class="m-global-header-cta
                                            m-global-header-cta__list">
                                    <a href="/complaint/" role="menuitem">
                                        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 825.1 1200" class="cf-icon-svg"><path d="M755.1 263.9H70c-38.6.1-69.9 31.4-70 70v459.5c.1 38.6 31.4 69.9 70 70h268.4l56.9 91.2c8.7 14 23 14 31.8 0l56.9-91.2h271.1c38.6-.1 69.9-31.4 70-70V333.9c-.1-38.7-31.4-69.9-70-70zm-375 132.5c0-17.9 14.6-32.5 32.5-32.5s32.5 14.6 32.5 32.5v204.2c0 17.9-14.6 32.5-32.5 32.5s-32.5-14.6-32.5-32.5V396.4zm32.5 364.4c-24.6 0-44.6-20-44.6-44.6s20-44.6 44.6-44.6 44.6 20 44.6 44.6c-.1 24.6-20 44.6-44.6 44.6z"></path></svg>
                                        Submit a Complaint
                                    </a>
                                </div>
                            </li>

                            <li class="m-list_item o-mega-menu_content-item o-mega-menu_content-1-item" data-js-hook="behavior_flyout-menu">
                                <a class="o-mega-menu_content-link o-mega-menu_content-1-link o-mega-menu_content-link__has-children o-mega-menu_content-1-link__has-children " href="#" data-js-hook="behavior_flyout-menu_trigger" aria-haspopup="menu" role="menuitem" data-gtm_ignore="true" aria-expanded="false">
                                      Consumer Tools
                                      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 559.6 1200" class="cf-icon-svg"><path d="M65.1 1090.2c-35.9 0-65-29-65.1-64.9 0-17.3 6.8-33.9 19.1-46.1l383.6-383.5L19.1 212.2c-25.1-25.6-24.8-66.8.9-92 25.3-24.8 65.8-24.8 91.1 0l429.5 429.5c25.4 25.4 25.4 66.5 0 91.9L111 1071.2c-12.1 12.2-28.7 19.1-45.9 19z"></path></svg>
                                </a>

                                <div class="o-mega-menu_content o-mega-menu_content-2 u-hidden-overflow u-move-transition" aria-expanded="false" data-js-hook="behavior_flyout-menu_content">
                                    <div class="o-mega-menu_content-wrapper o-mega-menu_content-2-wrapper ">
                                        <div class="wrapper">

                                            <button class="o-mega-menu_content-alt-trigger o-mega-menu_content-2-alt-trigger " data-js-hook="behavior_flyout-menu_alt-trigger" role="menuitem" aria-expanded="false">
                                                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 559.6 1200" class="cf-icon-svg"><path d="M494.5 1090.7c-17.3 0-33.8-6.8-46-19L19 642.1c-25.4-25.4-25.4-66.5 0-91.9l429.5-429.5c25.6-25.1 66.8-24.8 91.9.8 24.8 25.3 24.8 65.8 0 91.1L156.9 596.2l383.6 383.6c25.4 25.4 25.4 66.5.1 91.9-12.3 12.2-28.8 19-46.1 19z"></path></svg>
                                                Back
                                            </button>

                                            <div class="o-mega-menu_content-grid o-mega-menu_content-2-grid">
                                                <span class="o-mega-menu_content-overview o-mega-menu_content-2-overview ">
                                                    <a class="u-link__disabled
                                                              o-mega-menu_content-overview-link o-mega-menu_content-2-overview-link
                                                              ">
                                                        Consumer Tools
                                                    </a>
                                                </span>

                                                <div class="o-mega-menu_content-lists o-mega-menu_content-2-lists ">

                                                    <div class="o-mega-menu_content-list o-mega-menu_content-2-list ">
                                                        <div class="h5 o-mega-menu_group-heading">
                                                            Money Topics
                                                        </div>

                                                        <ul class="m-list m-list__unstyled">
                                                            <li class="m-list_item o-mega-menu_content-item o-mega-menu_content-2-item ">
                                                                <a class="o-mega-menu_content-link o-mega-menu_content-2-link " href="/consumer-tools/auto-loans/" role="menuitem">
                                                                      Auto Loans
                                                                      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 559.6 1200" class="cf-icon-svg"><path d="M65.1 1090.2c-35.9 0-65-29-65.1-64.9 0-17.3 6.8-33.9 19.1-46.1l383.6-383.5L19.1 212.2c-25.1-25.6-24.8-66.8.9-92 25.3-24.8 65.8-24.8 91.1 0l429.5 429.5c25.4 25.4 25.4 66.5 0 91.9L111 1071.2c-12.1 12.2-28.7 19.1-45.9 19z"></path></svg>
                                                                </a>
                                                            </li>

                                                            <li class="m-list_item o-mega-menu_content-item o-mega-menu_content-2-item ">
                                                                <a class="o-mega-menu_content-link o-mega-menu_content-2-link " href="/consumer-tools/bank-accounts/" role="menuitem">
                                                                      Bank Accounts &amp; Services
                                                                      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 559.6 1200" class="cf-icon-svg"><path d="M65.1 1090.2c-35.9 0-65-29-65.1-64.9 0-17.3 6.8-33.9 19.1-46.1l383.6-383.5L19.1 212.2c-25.1-25.6-24.8-66.8.9-92 25.3-24.8 65.8-24.8 91.1 0l429.5 429.5c25.4 25.4 25.4 66.5 0 91.9L111 1071.2c-12.1 12.2-28.7 19.1-45.9 19z"></path></svg>
                                                                </a>
                                                            </li>


                                                            <li class="m-list_item o-mega-menu_content-item o-mega-menu_content-2-item ">
                                                                <a class="o-mega-menu_content-link o-mega-menu_content-2-link " href="/ask-cfpb/category-credit-cards/" role="menuitem">
                                                                      Credit Cards
                                                                      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 559.6 1200" class="cf-icon-svg"><path d="M65.1 1090.2c-35.9 0-65-29-65.1-64.9 0-17.3 6.8-33.9 19.1-46.1l383.6-383.5L19.1 212.2c-25.1-25.6-24.8-66.8.9-92 25.3-24.8 65.8-24.8 91.1 0l429.5 429.5c25.4 25.4 25.4 66.5 0 91.9L111 1071.2c-12.1 12.2-28.7 19.1-45.9 19z"></path></svg>
                                                                </a>
                                                            </li>

                                                            <li class="m-list_item o-mega-menu_content-item o-mega-menu_content-2-item ">
                                                                <a class="o-mega-menu_content-link o-mega-menu_content-2-link " href="/consumer-tools/credit-reports-and-scores/" role="menuitem">
                                                                      Credit Reports &amp; Scores
                                                                      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 559.6 1200" class="cf-icon-svg"><path d="M65.1 1090.2c-35.9 0-65-29-65.1-64.9 0-17.3 6.8-33.9 19.1-46.1l383.6-383.5L19.1 212.2c-25.1-25.6-24.8-66.8.9-92 25.3-24.8 65.8-24.8 91.1 0l429.5 429.5c25.4 25.4 25.4 66.5 0 91.9L111 1071.2c-12.1 12.2-28.7 19.1-45.9 19z"></path></svg>
                                                                </a>
                                                            </li>

                                                            <li class="m-list_item o-mega-menu_content-item o-mega-menu_content-2-item ">
                                                                <a class="o-mega-menu_content-link o-mega-menu_content-2-link " href="/consumer-tools/debt-collection/" role="menuitem">
                                                                      Debt Collection
                                                                      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 559.6 1200" class="cf-icon-svg"><path d="M65.1 1090.2c-35.9 0-65-29-65.1-64.9 0-17.3 6.8-33.9 19.1-46.1l383.6-383.5L19.1 212.2c-25.1-25.6-24.8-66.8.9-92 25.3-24.8 65.8-24.8 91.1 0l429.5 429.5c25.4 25.4 25.4 66.5 0 91.9L111 1071.2c-12.1 12.2-28.7 19.1-45.9 19z"></path></svg>
                                                                </a>
                                                            </li>

                                                            <li class="m-list_item o-mega-menu_content-item o-mega-menu_content-2-item ">
                                                                <a class="o-mega-menu_content-link o-mega-menu_content-2-link " href="/consumer-tools/fraud/" role="menuitem">
                                                                      Fraud &amp; Scams
                                                                      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 559.6 1200" class="cf-icon-svg"><path d="M65.1 1090.2c-35.9 0-65-29-65.1-64.9 0-17.3 6.8-33.9 19.1-46.1l383.6-383.5L19.1 212.2c-25.1-25.6-24.8-66.8.9-92 25.3-24.8 65.8-24.8 91.1 0l429.5 429.5c25.4 25.4 25.4 66.5 0 91.9L111 1071.2c-12.1 12.2-28.7 19.1-45.9 19z"></path></svg>
                                                                </a>
                                                            </li>
                                                        </ul>
                                                    </div>

                                                </div>

                                                <div class="o-mega-menu_footer">
                                                    <p>
                                                        <span aria-hidden="true">
                                                            Browse answers to hundreds of financial questions.
                                                        </span>
                                                        <a aria-label="Browse answers to hundreds of financial questions with Ask CFPB." href="/ask-cfpb/">
                                                           Ask CFPB
                                                        </a>
                                                    </p>
                                                    <p>
                                                        <span aria-hidden="true">
                                                            Have an issue with a financial product?
                                                        </span>
                                                        <a aria-label="Have an issue with a financial product? Submit a complaint." href="/complaint/">
                                                           Submit a complaint
                                                        </a>
                                                    </p>
                                                </div>

                                            </div>

                                            <aside class="m-featured-menu-content">
                                                <a class="m-featured-menu-content_link" href="/consumer-tools/financial-well-being/">

                                                    <img src="/static/img/fmc-consumer-tools-540x300.png" alt="" height="150" width="270">

                                                    <div>
                                                      Get your financial well-being score
                                                    </div>
                                                </a>
                                                <p>
                                                    Answer ten questions and see your financial well-being score, along with national averages.
                                                </p>
                                            </aside>

                                        </div>
                                    </div>
                                </div>
                            </li>

                            <li class="m-list_item o-mega-menu_content-item o-mega-menu_content-1-item" data-js-hook="behavior_flyout-menu">

                                <a class="o-mega-menu_content-link o-mega-menu_content-1-link o-mega-menu_content-link__has-children o-mega-menu_content-1-link__has-children " href="/data-research/" data-js-hook="behavior_flyout-menu_trigger" aria-haspopup="menu" role="menuitem" data-gtm_ignore="true" aria-expanded="false">
                                      Data &amp; Research
                                      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 559.6 1200" class="cf-icon-svg"><path d="M65.1 1090.2c-35.9 0-65-29-65.1-64.9 0-17.3 6.8-33.9 19.1-46.1l383.6-383.5L19.1 212.2c-25.1-25.6-24.8-66.8.9-92 25.3-24.8 65.8-24.8 91.1 0l429.5 429.5c25.4 25.4 25.4 66.5 0 91.9L111 1071.2c-12.1 12.2-28.7 19.1-45.9 19z"></path></svg>
                                </a>

                                <div class="o-mega-menu_content o-mega-menu_content-2 u-hidden-overflow u-move-transition" aria-expanded="false" data-js-hook="behavior_flyout-menu_content">
                                    <div class="o-mega-menu_content-wrapper o-mega-menu_content-2-wrapper ">
                                        <div class="wrapper">

                                            <button class="o-mega-menu_content-alt-trigger o-mega-menu_content-2-alt-trigger " data-js-hook="behavior_flyout-menu_alt-trigger" role="menuitem" aria-expanded="false">
                                                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 559.6 1200" class="cf-icon-svg"><path d="M494.5 1090.7c-17.3 0-33.8-6.8-46-19L19 642.1c-25.4-25.4-25.4-66.5 0-91.9l429.5-429.5c25.6-25.1 66.8-24.8 91.9.8 24.8 25.3 24.8 65.8 0 91.1L156.9 596.2l383.6 383.6c25.4 25.4 25.4 66.5.1 91.9-12.3 12.2-28.8 19-46.1 19z"></path></svg>
                                                Back
                                            </button>

                                            <div class="o-mega-menu_content-grid o-mega-menu_content-2-grid">

                                                <span class="o-mega-menu_content-overview o-mega-menu_content-2-overview ">
                                                    <a class="o-mega-menu_content-overview-link
                                                              o-mega-menu_content-2-overview-link"
                                                       href="/data-research/">
                                                        Data &amp; Research Overview
                                                    </a>
                                                </span>

                                                <div class="o-mega-menu_content-lists o-mega-menu_content-2-lists ">

                                                    <div class="o-mega-menu_content-list o-mega-menu_content-2-list ">
                                                        <ul class="m-list m-list__unstyled">
                                                            <li class="m-list_item o-mega-menu_content-item o-mega-menu_content-2-item ">
                                                                <a class="o-mega-menu_content-link o-mega-menu_content-2-link " href="/data-research/research-reports/" role="menuitem">
                                                                      Research &amp; Reports
                                                                      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 559.6 1200" class="cf-icon-svg"><path d="M65.1 1090.2c-35.9 0-65-29-65.1-64.9 0-17.3 6.8-33.9 19.1-46.1l383.6-383.5L19.1 212.2c-25.1-25.6-24.8-66.8.9-92 25.3-24.8 65.8-24.8 91.1 0l429.5 429.5c25.4 25.4 25.4 66.5 0 91.9L111 1071.2c-12.1 12.2-28.7 19.1-45.9 19z"></path></svg>
                                                                </a>
                                                            </li>

                                                            <li class="m-list_item o-mega-menu_content-item o-mega-menu_content-2-item ">
                                                                <a class="o-mega-menu_content-link o-mega-menu_content-2-link " href="/data-research/consumer-complaints/" role="menuitem">
                                                                      Consumer Complaint Database
                                                                      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 559.6 1200" class="cf-icon-svg"><path d="M65.1 1090.2c-35.9 0-65-29-65.1-64.9 0-17.3 6.8-33.9 19.1-46.1l383.6-383.5L19.1 212.2c-25.1-25.6-24.8-66.8.9-92 25.3-24.8 65.8-24.8 91.1 0l429.5 429.5c25.4 25.4 25.4 66.5 0 91.9L111 1071.2c-12.1 12.2-28.7 19.1-45.9 19z"></path></svg>
                                                                </a>
                                                            </li>

                                                            <li class="m-list_item o-mega-menu_content-item o-mega-menu_content-2-item ">
                                                                <a class="o-mega-menu_content-link o-mega-menu_content-2-link " href="/data-research/mortgage-data-hmda/" role="menuitem">
                                                                      Mortgage Database (HMDA)
                                                                      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 559.6 1200" class="cf-icon-svg"><path d="M65.1 1090.2c-35.9 0-65-29-65.1-64.9 0-17.3 6.8-33.9 19.1-46.1l383.6-383.5L19.1 212.2c-25.1-25.6-24.8-66.8.9-92 25.3-24.8 65.8-24.8 91.1 0l429.5 429.5c25.4 25.4 25.4 66.5 0 91.9L111 1071.2c-12.1 12.2-28.7 19.1-45.9 19z"></path></svg>
                                                                </a>
                                                            </li>
                                                        </ul>
                                                    </div>

                                                </div>

                                            </div>

                                            <aside class="m-featured-menu-content">
                                                <a class="m-featured-menu-content_link" href="/data-research/financial-well-being-survey-data/">

                                                    <img src="/static/img/fmc-data-research-540x300.png" alt="" height="150" width="270">

                                                    <div>
                                                      Help advance financial well-being
                                                    </div>
                                                </a>
                                                <p>
                                                    Explore our national survey data and think about ways to empower families to achieve higher financial well-being.
                                                </p>
                                            </aside>

                                        </div>
                                    </div>
                                </div>
                            </li>

                            <li class="m-list_item o-mega-menu_content-item o-mega-menu_content-1-item" data-js-hook="behavior_flyout-menu">
                                <a class="o-mega-menu_content-link o-mega-menu_content-1-link o-mega-menu_content-link__has-children o-mega-menu_content-1-link__has-children " href="/about-us/" data-js-hook="behavior_flyout-menu_trigger" aria-haspopup="menu" role="menuitem" data-gtm_ignore="true" aria-expanded="false">
                                    About Us
                                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 559.6 1200" class="cf-icon-svg"><path d="M65.1 1090.2c-35.9 0-65-29-65.1-64.9 0-17.3 6.8-33.9 19.1-46.1l383.6-383.5L19.1 212.2c-25.1-25.6-24.8-66.8.9-92 25.3-24.8 65.8-24.8 91.1 0l429.5 429.5c25.4 25.4 25.4 66.5 0 91.9L111 1071.2c-12.1 12.2-28.7 19.1-45.9 19z"></path></svg>
                                </a>

                                <div class="o-mega-menu_content o-mega-menu_content-2 u-hidden-overflow u-move-transition" aria-expanded="false" data-js-hook="behavior_flyout-menu_content">
                                    <div class="o-mega-menu_content-wrapper o-mega-menu_content-2-wrapper ">
                                        <div class="wrapper">

                                            <button class="o-mega-menu_content-alt-trigger o-mega-menu_content-2-alt-trigger " data-js-hook="behavior_flyout-menu_alt-trigger" role="menuitem" aria-expanded="false">
                                                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 559.6 1200" class="cf-icon-svg"><path d="M494.5 1090.7c-17.3 0-33.8-6.8-46-19L19 642.1c-25.4-25.4-25.4-66.5 0-91.9l429.5-429.5c25.6-25.1 66.8-24.8 91.9.8 24.8 25.3 24.8 65.8 0 91.1L156.9 596.2l383.6 383.6c25.4 25.4 25.4 66.5.1 91.9-12.3 12.2-28.8 19-46.1 19z"></path></svg>
                                                Back
                                            </button>

                                            <div class="o-mega-menu_content-grid o-mega-menu_content-2-grid">

                                                <span class="o-mega-menu_content-overview o-mega-menu_content-2-overview ">
                                                    <a class="o-mega-menu_content-overview-link
                                                              o-mega-menu_content-2-overview-link"
                                                       href="/about-us/">
                                                        About Us Overview
                                                    </a>
                                                </span>

                                                <div class="o-mega-menu_content-lists o-mega-menu_content-2-lists ">

                                                    <div class="o-mega-menu_content-list o-mega-menu_content-2-list ">
                                                        <ul class="m-list m-list__unstyled">
                                                            <li class="m-list_item o-mega-menu_content-item o-mega-menu_content-2-item ">
                                                                <a class="o-mega-menu_content-link o-mega-menu_content-2-link " href="/about-us/the-bureau/" role="menuitem">
                                                                      The Bureau
                                                                      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 559.6 1200" class="cf-icon-svg"><path d="M65.1 1090.2c-35.9 0-65-29-65.1-64.9 0-17.3 6.8-33.9 19.1-46.1l383.6-383.5L19.1 212.2c-25.1-25.6-24.8-66.8.9-92 25.3-24.8 65.8-24.8 91.1 0l429.5 429.5c25.4 25.4 25.4 66.5 0 91.9L111 1071.2c-12.1 12.2-28.7 19.1-45.9 19z"></path></svg>
                                                                </a>
                                                            </li>

                                                            <li class="m-list_item o-mega-menu_content-item o-mega-menu_content-2-item ">
                                                                <a class="o-mega-menu_content-link o-mega-menu_content-2-link " href="/about-us/budget-strategy/" role="menuitem">
                                                                      Budget &amp; Strategy
                                                                      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 559.6 1200" class="cf-icon-svg"><path d="M65.1 1090.2c-35.9 0-65-29-65.1-64.9 0-17.3 6.8-33.9 19.1-46.1l383.6-383.5L19.1 212.2c-25.1-25.6-24.8-66.8.9-92 25.3-24.8 65.8-24.8 91.1 0l429.5 429.5c25.4 25.4 25.4 66.5 0 91.9L111 1071.2c-12.1 12.2-28.7 19.1-45.9 19z"></path></svg>
                                                                </a>
                                                            </li>

                                                            <li class="m-list_item o-mega-menu_content-item o-mega-menu_content-2-item ">
                                                                <a class="o-mega-menu_content-link o-mega-menu_content-2-link " href="/about-us/payments-harmed-consumers/" role="menuitem">
                                                                      Payments to Harmed Consumers
                                                                      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 559.6 1200" class="cf-icon-svg"><path d="M65.1 1090.2c-35.9 0-65-29-65.1-64.9 0-17.3 6.8-33.9 19.1-46.1l383.6-383.5L19.1 212.2c-25.1-25.6-24.8-66.8.9-92 25.3-24.8 65.8-24.8 91.1 0l429.5 429.5c25.4 25.4 25.4 66.5 0 91.9L111 1071.2c-12.1 12.2-28.7 19.1-45.9 19z"></path></svg>
                                                                </a>
                                                            </li>

                                                            <li class="m-list_item o-mega-menu_content-item o-mega-menu_content-2-item ">
                                                                <a class="o-mega-menu_content-link o-mega-menu_content-2-link " href="/about-us/diversity-and-inclusion/" role="menuitem">
                                                                      Diversity &amp; Inclusion
                                                                      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 559.6 1200" class="cf-icon-svg"><path d="M65.1 1090.2c-35.9 0-65-29-65.1-64.9 0-17.3 6.8-33.9 19.1-46.1l383.6-383.5L19.1 212.2c-25.1-25.6-24.8-66.8.9-92 25.3-24.8 65.8-24.8 91.1 0l429.5 429.5c25.4 25.4 25.4 66.5 0 91.9L111 1071.2c-12.1 12.2-28.7 19.1-45.9 19z"></path></svg>
                                                                </a>
                                                            </li>
                                                        </ul>
                                                    </div>

                                                    <div class="o-mega-menu_content-list o-mega-menu_content-2-list ">
                                                        <ul class="m-list m-list__unstyled">
                                                            <li class="m-list_item o-mega-menu_content-item o-mega-menu_content-2-item ">
                                                                <a class="o-mega-menu_content-link o-mega-menu_content-2-link " href="/activity-log/" role="menuitem">
                                                                      Recent Updates
                                                                      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 559.6 1200" class="cf-icon-svg"><path d="M65.1 1090.2c-35.9 0-65-29-65.1-64.9 0-17.3 6.8-33.9 19.1-46.1l383.6-383.5L19.1 212.2c-25.1-25.6-24.8-66.8.9-92 25.3-24.8 65.8-24.8 91.1 0l429.5 429.5c25.4 25.4 25.4 66.5 0 91.9L111 1071.2c-12.1 12.2-28.7 19.1-45.9 19z"></path></svg>
                                                                </a>
                                                            </li>

                                                            <li class="m-list_item o-mega-menu_content-item o-mega-menu_content-2-item ">
                                                                <a class="o-mega-menu_content-link o-mega-menu_content-2-link " href="/about-us/blog/" role="menuitem">
                                                                      Blog
                                                                      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 559.6 1200" class="cf-icon-svg"><path d="M65.1 1090.2c-35.9 0-65-29-65.1-64.9 0-17.3 6.8-33.9 19.1-46.1l383.6-383.5L19.1 212.2c-25.1-25.6-24.8-66.8.9-92 25.3-24.8 65.8-24.8 91.1 0l429.5 429.5c25.4 25.4 25.4 66.5 0 91.9L111 1071.2c-12.1 12.2-28.7 19.1-45.9 19z"></path></svg>
                                                                </a>
                                                            </li>

                                                            <li class="m-list_item o-mega-menu_content-item o-mega-menu_content-2-item ">
                                                                <a class="o-mega-menu_content-link o-mega-menu_content-2-link " href="/about-us/newsroom/" role="menuitem">
                                                                      Newsroom
                                                                      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 559.6 1200" class="cf-icon-svg"><path d="M65.1 1090.2c-35.9 0-65-29-65.1-64.9 0-17.3 6.8-33.9 19.1-46.1l383.6-383.5L19.1 212.2c-25.1-25.6-24.8-66.8.9-92 25.3-24.8 65.8-24.8 91.1 0l429.5 429.5c25.4 25.4 25.4 66.5 0 91.9L111 1071.2c-12.1 12.2-28.7 19.1-45.9 19z"></path></svg>
                                                                </a>
                                                            </li>

                                                            <li class="m-list_item o-mega-menu_content-item o-mega-menu_content-2-item ">
                                                                <a class="o-mega-menu_content-link o-mega-menu_content-2-link " href="/about-us/events/" role="menuitem">
                                                                      Events
                                                                      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 559.6 1200" class="cf-icon-svg"><path d="M65.1 1090.2c-35.9 0-65-29-65.1-64.9 0-17.3 6.8-33.9 19.1-46.1l383.6-383.5L19.1 212.2c-25.1-25.6-24.8-66.8.9-92 25.3-24.8 65.8-24.8 91.1 0l429.5 429.5c25.4 25.4 25.4 66.5 0 91.9L111 1071.2c-12.1 12.2-28.7 19.1-45.9 19z"></path></svg>
                                                                </a>
                                                            </li>
                                                        </ul>
                                                    </div>

                                                    <div class="o-mega-menu_content-list o-mega-menu_content-2-list ">
                                                        <ul class="m-list m-list__unstyled">
                                                            <li class="m-list_item o-mega-menu_content-item o-mega-menu_content-2-item " data-js-hook="behavior_flyout-menu">
                                                                <a class="o-mega-menu_content-link o-mega-menu_content-2-link o-mega-menu_content-link__has-children o-mega-menu_content-2-link__has-children " href="/about-us/careers/" data-js-hook="behavior_flyout-menu_trigger" aria-haspopup="menu" role="menuitem" data-gtm_ignore="true" aria-expanded="false">
                                                                      Careers
                                                                      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 559.6 1200" class="cf-icon-svg"><path d="M65.1 1090.2c-35.9 0-65-29-65.1-64.9 0-17.3 6.8-33.9 19.1-46.1l383.6-383.5L19.1 212.2c-25.1-25.6-24.8-66.8.9-92 25.3-24.8 65.8-24.8 91.1 0l429.5 429.5c25.4 25.4 25.4 66.5 0 91.9L111 1071.2c-12.1 12.2-28.7 19.1-45.9 19z"></path></svg>
                                                                </a>

                                                                <div class="o-mega-menu_content o-mega-menu_content-3 u-hidden-overflow u-move-transition" aria-expanded="false" data-js-hook="behavior_flyout-menu_content">
                                                                    <div class="o-mega-menu_content-wrapper o-mega-menu_content-3-wrapper ">
                                                                        <div class="wrapper">

                                                                            <button class="o-mega-menu_content-alt-trigger o-mega-menu_content-3-alt-trigger " data-js-hook="behavior_flyout-menu_alt-trigger" role="menuitem" aria-expanded="false">
                                                                                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 559.6 1200" class="cf-icon-svg"><path d="M494.5 1090.7c-17.3 0-33.8-6.8-46-19L19 642.1c-25.4-25.4-25.4-66.5 0-91.9l429.5-429.5c25.6-25.1 66.8-24.8 91.9.8 24.8 25.3 24.8 65.8 0 91.1L156.9 596.2l383.6 383.6c25.4 25.4 25.4 66.5.1 91.9-12.3 12.2-28.8 19-46.1 19z"></path></svg>
                                                                                Back
                                                                            </button>

                                                                            <div class="o-mega-menu_content-grid o-mega-menu_content-3-grid">

                                                                                <span class="o-mega-menu_content-overview o-mega-menu_content-3-overview ">
                                                                                    <a class="o-mega-menu_content-overview-link
                                                                                              o-mega-menu_content-3-overview-link"
                                                                                       href="/about-us/careers/">
                                                                                        Careers Overview
                                                                                    </a>
                                                                                </span>

                                                                                <div class="o-mega-menu_content-lists o-mega-menu_content-3-lists ">
                                                                                    <div class="o-mega-menu_content-list o-mega-menu_content-3-list ">
                                                                                        <ul class="m-list m-list__unstyled">
                                                                                            <li class="m-list_item o-mega-menu_content-item o-mega-menu_content-3-item ">
                                                                                                <a class="o-mega-menu_content-link o-mega-menu_content-3-link " href="/about-us/careers/working-at-cfpb/" role="menuitem">
                                                                                                      Working @ CFPB
                                                                                                      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 559.6 1200" class="cf-icon-svg"><path d="M65.1 1090.2c-35.9 0-65-29-65.1-64.9 0-17.3 6.8-33.9 19.1-46.1l383.6-383.5L19.1 212.2c-25.1-25.6-24.8-66.8.9-92 25.3-24.8 65.8-24.8 91.1 0l429.5 429.5c25.4 25.4 25.4 66.5 0 91.9L111 1071.2c-12.1 12.2-28.7 19.1-45.9 19z"></path></svg>
                                                                                                </a>
                                                                                            </li>

                                                                                            <li class="m-list_item o-mega-menu_content-item o-mega-menu_content-3-item ">
                                                                                                <a class="o-mega-menu_content-link o-mega-menu_content-3-link " href="/about-us/careers/application-process/" role="menuitem">
                                                                                                      Job Application Process
                                                                                                      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 559.6 1200" class="cf-icon-svg"><path d="M65.1 1090.2c-35.9 0-65-29-65.1-64.9 0-17.3 6.8-33.9 19.1-46.1l383.6-383.5L19.1 212.2c-25.1-25.6-24.8-66.8.9-92 25.3-24.8 65.8-24.8 91.1 0l429.5 429.5c25.4 25.4 25.4 66.5 0 91.9L111 1071.2c-12.1 12.2-28.7 19.1-45.9 19z"></path></svg>
                                                                                                </a>
                                                                                            </li>

                                                                                            <li class="m-list_item o-mega-menu_content-item o-mega-menu_content-3-item ">
                                                                                                <a class="o-mega-menu_content-link o-mega-menu_content-3-link " href="/about-us/careers/students-and-graduates/" role="menuitem">
                                                                                                      Students &amp; Recent Graduates
                                                                                                      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 559.6 1200" class="cf-icon-svg"><path d="M65.1 1090.2c-35.9 0-65-29-65.1-64.9 0-17.3 6.8-33.9 19.1-46.1l383.6-383.5L19.1 212.2c-25.1-25.6-24.8-66.8.9-92 25.3-24.8 65.8-24.8 91.1 0l429.5 429.5c25.4 25.4 25.4 66.5 0 91.9L111 1071.2c-12.1 12.2-28.7 19.1-45.9 19z"></path></svg>
                                                                                                </a>
                                                                                            </li>

                                                                                            <li class="m-list_item o-mega-menu_content-item o-mega-menu_content-3-item ">
                                                                                                <a class="o-mega-menu_content-link o-mega-menu_content-3-link " href="/about-us/careers/current-openings/" role="menuitem">
                                                                                                      All Current Openings
                                                                                                      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 559.6 1200" class="cf-icon-svg"><path d="M65.1 1090.2c-35.9 0-65-29-65.1-64.9 0-17.3 6.8-33.9 19.1-46.1l383.6-383.5L19.1 212.2c-25.1-25.6-24.8-66.8.9-92 25.3-24.8 65.8-24.8 91.1 0l429.5 429.5c25.4 25.4 25.4 66.5 0 91.9L111 1071.2c-12.1 12.2-28.7 19.1-45.9 19z"></path></svg>
                                                                                                </a>
                                                                                            </li>
                                                                                        </ul>
                                                                                    </div>
                                                                                </div>

                                                                            </div>

                                                                        </div>
                                                                    </div>
                                                                </div>
                                                            </li>

                                                            <li class="m-list_item o-mega-menu_content-item o-mega-menu_content-2-item ">
                                                                <a class="o-mega-menu_content-link o-mega-menu_content-2-link " href="/about-us/doing-business-with-us/" role="menuitem">
                                                                      Doing Business With Us
                                                                      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 559.6 1200" class="cf-icon-svg"><path d="M65.1 1090.2c-35.9 0-65-29-65.1-64.9 0-17.3 6.8-33.9 19.1-46.1l383.6-383.5L19.1 212.2c-25.1-25.6-24.8-66.8.9-92 25.3-24.8 65.8-24.8 91.1 0l429.5 429.5c25.4 25.4 25.4 66.5 0 91.9L111 1071.2c-12.1 12.2-28.7 19.1-45.9 19z"></path></svg>
                                                                </a>
                                                            </li>

                                                            <li class="m-list_item o-mega-menu_content-item o-mega-menu_content-2-item ">
                                                                <a class="o-mega-menu_content-link o-mega-menu_content-2-link " href="/about-us/advisory-groups/" role="menuitem">
                                                                      Advisory Groups
                                                                      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 559.6 1200" class="cf-icon-svg"><path d="M65.1 1090.2c-35.9 0-65-29-65.1-64.9 0-17.3 6.8-33.9 19.1-46.1l383.6-383.5L19.1 212.2c-25.1-25.6-24.8-66.8.9-92 25.3-24.8 65.8-24.8 91.1 0l429.5 429.5c25.4 25.4 25.4 66.5 0 91.9L111 1071.2c-12.1 12.2-28.7 19.1-45.9 19z"></path></svg>
                                                                </a>
                                                            </li>

                                                            <li class="m-list_item o-mega-menu_content-item o-mega-menu_content-2-item ">
                                                                <a class="o-mega-menu_content-link o-mega-menu_content-2-link " href="/about-us/project-catalyst/" role="menuitem">
                                                                      Project Catalyst
                                                                      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 559.6 1200" class="cf-icon-svg"><path d="M65.1 1090.2c-35.9 0-65-29-65.1-64.9 0-17.3 6.8-33.9 19.1-46.1l383.6-383.5L19.1 212.2c-25.1-25.6-24.8-66.8.9-92 25.3-24.8 65.8-24.8 91.1 0l429.5 429.5c25.4 25.4 25.4 66.5 0 91.9L111 1071.2c-12.1 12.2-28.7 19.1-45.9 19z"></path></svg>
                                                                </a>
                                                            </li>

                                                            <li class="m-list_item o-mega-menu_content-item o-mega-menu_content-2-item ">
                                                                <a class="o-mega-menu_content-link o-mega-menu_content-2-link " href="/about-us/contact-us/" role="menuitem">
                                                                      Contact Us
                                                                      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 559.6 1200" class="cf-icon-svg"><path d="M65.1 1090.2c-35.9 0-65-29-65.1-64.9 0-17.3 6.8-33.9 19.1-46.1l383.6-383.5L19.1 212.2c-25.1-25.6-24.8-66.8.9-92 25.3-24.8 65.8-24.8 91.1 0l429.5 429.5c25.4 25.4 25.4 66.5 0 91.9L111 1071.2c-12.1 12.2-28.7 19.1-45.9 19z"></path></svg>
                                                                </a>
                                                            </li>
                                                        </ul>
                                                    </div>

                                                </div>

                                            </div>

                                        </div>
                                    </div>

                                </div>
                            </li>
                        </ul>

                    </div>

                </div>

            </div>

        </div>
    </div>
    <button class="u-tab-trigger u-visually-hidden" aria-hidden="true">Collapse</button>
</nav>
`;

describe( 'MegaMenu', () => {
  let navElem;
  let megaMenu;
  let thisMegaMenu;

  beforeEach( () => {
    document.body.innerHTML = HTML_SNIPPET;
    navElem = document.querySelector( `.${ BASE_CLASS }` );
    megaMenu = new MegaMenu( navElem );
    thisMegaMenu = megaMenu.init();
  } );

  describe( 'sub-menu click handler', () => {

    /* CAUTION: With the addition of manually firing the transitionend event
       for some reason this test fails if it's not the first test.
       Revisit changing the order of this test when JSDom supports transition
       events fully.
       See https://github.com/jsdom/jsdom/issues/1781
    */
    it( 'should expand on the first level sub-menu button click', done => {
      window.innerWidth = 420;
      const menuTrigger = navElem.querySelector( '.o-mega-menu_trigger' );
      const subTrigger = navElem.querySelector( '.o-mega-menu_content-1-link__has-children' );
      const subContent = navElem.querySelector( '.o-mega-menu_content-2' );
      const subContentWrapper = navElem.querySelector( '.o-mega-menu_content-2-wrapper' );
      let isExpanded;

      function resolveFirstClick() {
        simulateEvent( 'click', subTrigger );

        /* The transitionend event should fire on its own,
           but for some reason the transitionend event is not firing within JSDom.
           In a future JSDom update this should be revisited.
           See https://github.com/jsdom/jsdom/issues/1781
        */
        subContentWrapper.dispatchEvent( new Event( 'transitionend' ) );

        window.setTimeout( resolveSecondClick, 1000 );
      }

      function resolveSecondClick() {
        isExpanded = subContent.getAttribute( 'aria-expanded' );

        expect( isExpanded ).toEqual( 'true' );
        done();
      }

      simulateEvent( 'click', menuTrigger );

      window.setTimeout( resolveFirstClick, 1000 );
    } );

    it( 'should not be expanded by default', () => {
      window.innerWidth = 420;
      const subContent = navElem.querySelector( '.o-mega-menu_content-2' );
      const isExpanded = subContent.getAttribute( 'aria-expanded' );

      expect( isExpanded ).toEqual( 'false' );
    } );

    it( 'should not be expanded on the main trigger click', done => {
      window.innerWidth = 420;
      const menuTrigger = navElem.querySelector( '.o-mega-menu_trigger' );
      const subTrigger = navElem.querySelector( '.o-mega-menu_content-1-link__has-children' );
      const subContent = navElem.querySelector( '.o-mega-menu_content-2' );
      let isExpanded;

      function resolveFirstClick() {
        isExpanded = subContent.getAttribute( 'aria-expanded' );

        expect( isExpanded ).toEqual( 'false' );
        done();
      }

      simulateEvent( 'click', menuTrigger );

      window.setTimeout( resolveFirstClick, 1000 );
    } );

    it( 'should collapse on the first level sub-menu back button click', done => {
      window.innerWidth = 420;
      const menuTrigger = navElem.querySelector( '.o-mega-menu_trigger' );
      const subTrigger = navElem.querySelector( '.o-mega-menu_content-1-link__has-children' );
      const subContent = navElem.querySelector( '.o-mega-menu_content-2' );
      const subAltTrigger = subContent.querySelector( '.o-mega-menu_content-alt-trigger' );
      let isExpanded;

      function resolveFirstClick() {
        simulateEvent( 'click', subTrigger );

        window.setTimeout( resolveSecondClick, 1000 );
      }

      function resolveSecondClick() {
        simulateEvent( 'click', subAltTrigger );

        window.setTimeout( resolveThirdClick, 1000 );
      }

      function resolveThirdClick() {
        isExpanded = subContent.getAttribute( 'aria-expanded' );

        expect( isExpanded ).toEqual( 'false' );
        done();
      }

      simulateEvent( 'click', menuTrigger );

      window.setTimeout( resolveFirstClick, 1000 );
    } );

    it( 'should collapse on the second level sub-menu back button click', done => {
      window.innerWidth = 420;
      const menuTrigger = navElem.querySelector( '.o-mega-menu_trigger' );
      const itemWithSecondLevel = navElem.querySelectorAll( '.o-mega-menu_content-1-item' )[3];
      const firstSubTrigger = itemWithSecondLevel.querySelector( '.o-mega-menu_content-1-link__has-children' );
      const firstSubContent = itemWithSecondLevel.querySelector( '.o-mega-menu_content-2' );
      const secondSubTrigger = firstSubContent.querySelector( '.o-mega-menu_content-2-link__has-children' );
      const secondSubContent = firstSubContent.querySelector( '.o-mega-menu_content-3' );
      const secondSubAltTrigger = secondSubContent.querySelector( '.o-mega-menu_content-alt-trigger' );
      let isExpanded;

      function resolveFirstClick() {
        simulateEvent( 'click', firstSubTrigger );

        window.setTimeout( resolveSecondClick, 1000 );
      }

      function resolveSecondClick() {
        simulateEvent( 'click', secondSubTrigger );

        window.setTimeout( resolveThirdClick, 1000 );
      }

      function resolveThirdClick() {
        simulateEvent( 'click', secondSubAltTrigger );

        window.setTimeout( resolveFourthClick, 1000 );
      }

      function resolveFourthClick() {
        isExpanded = secondSubContent.getAttribute( 'aria-expanded' );

        expect( isExpanded ).toEqual( 'false' );
        done();
      }

      simulateEvent( 'click', menuTrigger );

      window.setTimeout( resolveFirstClick, 1000 );
    } );
  } );
} );
