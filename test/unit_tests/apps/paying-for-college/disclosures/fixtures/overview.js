export default `
<main id="main" data-context="paying-for-college2">
    <div id="financial-offer" class="understanding-financial-aid-offer">
        <section class="m-hero">
            <div class="m-hero--wrapper wrapper">
                <div class="m-hero--text">
                    <h1 class="m-hero--heading">
                        Understanding your financial aid offer
                    </h1>
                    <p class="m-hero--subhead">
                        This personalized summary will help you evaluate your
                        financial aid offer from your school to see how
                        student debt may impact your future finances. </p>
                </div>
                <div class="m-hero--image-wrapper">
                  <div class="m-hero--image"></div>
                </div>
            </div>
        </section>
        <div class="content__line"></div>
        <section class="verify step wrapper">
            <div class="content__main">

                <div class="m-notification m-notification--error verify__content" data-missing-data-error="noSchool">
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 17 19" class="cf-icon-svg cf-icon-svg--error-round"><path d="M16.417 9.583a7.916 7.916 0 1 1-15.833 0 7.916 7.916 0 0 1 15.833 0Zm-6.804.01 3.032-3.033a.792.792 0 1 0-1.12-1.12L8.494 8.473 5.46 5.44a.792.792 0 0 0-1.12 1.12l3.033 3.033-3.032 3.033a.791.791 0 1 0 1.12 1.119l3.032-3.033 3.033 3.033a.79.79 0 0 0 1.12 0c.309-.31.309-.81 0-1.12L9.612 9.594Z"></path></svg>
                    <div class="m-notification__content">
                        <div class="m-notification__message">Error!</div>
                        <p class="m-notification__explanation">
                            The information your school provided is missing the school ID, which is vital information for this tool to work. Please contact your school and ask them to ensure they are sending us the right school ID and it's in the correct format.
                        </p>

                        <p class="m-notification__explanation">
                            Once your school provides you with an updated URL link, you will be able to return here so you can continue reviewing the information in the tool.
                        </p>
                    </div>
                </div>

                <div class="m-notification m-notification--error verify__content" data-missing-data-error="noProgram">
                   <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 17 19" class="cf-icon-svg cf-icon-svg--error-round"><path d="M16.417 9.583a7.916 7.916 0 1 1-15.833 0 7.916 7.916 0 0 1 15.833 0Zm-6.804.01 3.032-3.033a.792.792 0 1 0-1.12-1.12L8.494 8.473 5.46 5.44a.792.792 0 0 0-1.12 1.12l3.033 3.033-3.032 3.033a.791.791 0 1 0 1.12 1.119l3.032-3.033 3.033 3.033a.79.79 0 0 0 1.12 0c.309-.31.309-.81 0-1.12L9.612 9.594Z"></path></svg>
                   <div class="m-notification__content">
                        <div class="m-notification__message">Error!</div>
                        <p class="m-notification__explanation">
                            The information your school provided is missing the program ID, which is vital information for this tool to work. Please contact your school and ask them to ensure they are sending us the right program ID and it's in the correct format.
                        </p>

                        <p class="m-notification__explanation">
                            Once your school provides you with an updated URL link, you will be able to return here so you can continue reviewing the information in the tool.
                        </p>
                    </div>
                </div>
                <div class="m-notification m-notification--error verify__content" data-missing-data-error="noOffer">
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 17 19" class="cf-icon-svg cf-icon-svg--error-round"><path d="M16.417 9.583a7.916 7.916 0 1 1-15.833 0 7.916 7.916 0 0 1 15.833 0Zm-6.804.01 3.032-3.033a.792.792 0 1 0-1.12-1.12L8.494 8.473 5.46 5.44a.792.792 0 0 0-1.12 1.12l3.033 3.033-3.032 3.033a.791.791 0 1 0 1.12 1.119l3.032-3.033 3.033 3.033a.79.79 0 0 0 1.12 0c.309-.31.309-.81 0-1.12L9.612 9.594Z"></path></svg>
                    <div class="m-notification__content">
                        <div class="m-notification__message">Error!</div>
                        <p class="m-notification__explanation"></p>
                            The information your school provided is missing the offer ID, which is vital information for this tool to work. Please contact your school and ask them to ensure they are sending us the right offer ID and it's in the correct format.
                        <p></p>

                        <p class="m-notification__explanation"></p>
                            Once your school provides you with an updated URL link, you will be able to return here so you can continue reviewing the information in the tool.
                        <p></p>
                    </div>
                </div>
                <div class="verify__wrapper">
                    <div class="verify__content" data-warning="">
                        <h2 class="verify__prompt">
                            Make sure that the information below is correct
                            before reviewing your offer.
                        </h2>
                        <form class="verify__form">
                            <div class="verify__school">
                                South University-West Palm Beach
                            </div>
                            <div class="verify__location">
                                Royal Palm Beach, FL
                            </div>
                            <div class="verify__type">
                                For-profit school
                            </div>
                            <dl class="verify__list">
                                <dt class="verify__heading">
                                    Program
                                </dt>
                                <dd class="verify__value">
                                    Physician Assistant
                                </dd>
                                <dt class="verify__heading">
                                    Program type
                                </dt>
                                <dd class="verify__value">
                                    Graduate degree
                                </dd>
                                <dt class="verify__heading verify__direct-cost">
                                    Estimated total cost of program
                                </dt>
                                <dd class="verify__value verify__direct-cost">
                                    <span id="verify_totalDirectCost" data-financial="totalCost">$45,000</span> (tuition, fees, books, and supplies)
                                </dd>
                                <dt class="verify__heading verify__label
                                verify__estimate" for="estimated-years-attending">
                                    Estimated years to complete your program
                                </dt>
                                <dd class="verify__value verify__estimate">
                                    <p class="verify__label-explanation">
                                        Select how long you expect it to take to
                                        complete your program. This may be
                                        shorter than the program length below if
                                        you transferred in with credits that the
                                        school accepts. For example, it may be
                                        longer if you plan to attend part time
                                        or do not successfully complete your
                                        courses. We’ll use this to help
                                        calculate your total debt after
                                        graduation.
                                    </p>
                                    <div class="a-select">
                                        <select id="estimated-years-attending">
                                            <option value="0.5">
                                                6 months
                                            </option>
                                            <option value="1">
                                                1 year
                                            </option>
                                            <option value="1.5">
                                                1 ½ years
                                            </option>
                                            <option value="2">
                                                2 years
                                            </option>
                                            <option value="2.5">
                                                2 ½ years
                                            </option>
                                            <option value="3">
                                                3 years
                                            </option>
                                            <option value="3.5">
                                                3 ½ years
                                            </option>
                                            <option value="4">
                                                4 years
                                            </option>
                                            <option value="4.5">
                                                4 ½ years
                                            </option>
                                            <option value="5">
                                                5 years
                                            </option>
                                            <option value="5.5">
                                                5 ½ years
                                            </option>
                                            <option value="6">
                                                6 years
                                            </option>
                                        </select>
                                    </div>
                                </dd>
                                <dt class="verify__heading">
                                    Offer ID
                                </dt>
                                <dd class="verify__value">
                                    ABCDEAB
                                </dd>
                            </dl>
                            <div class="verify__controls">
                                <a href="#info-right" class="a-btn a-btn--full-on-xs" title="Yes, this information is correct" data-gtm_ignore="true">
                                    Yes, this is correct
                                </a>
                                <a href="#info-wrong" class="a-btn a-btn--full-on-xs a-btn--link
                                verify__wrong-info-btn" title="No, this is not my information" data-gtm_ignore="true">
                                    No, this is not my information
                                </a>
                            </div>
                        </form>
                    </div>
                </div>
                <div class="content__line"></div>
            </div>
        </section>
        <section id="info-right" class="information-right" tabindex="-1">
            <section class="instructions step wrapper">
                <div class="content__main">
                    <div class="instructions__wrapper">
                        <div class="instructions__content
                                    instructions__content--right">
                            <h2 class="step__heading">
                                As you go through the three sections of this
                                tool, you’ll:
                            </h2>
                            <ol>
                                <li>Review your first-year financial aid
                                    offer,</li>
                                <li>Evaluate the financial impact of accepting
                                    your financial aid offer by reviewing
                                    graduation rates, expected salaries,
                                    affordability, the program’s loan default
                                    rates, and other factors specific to your
                                    school and program, and</li>
                                <li>Learn about your options
                                to reduce student debt.</li>
                            </ol>
                            <p class="instructions__subheading">
                                You must complete steps 1 and 2 of this tool
                                before you can enroll.
                            </p>
                        </div>
                        <div class="instructions__about-wrapper">
                            <h2 class="instructions__about-heading">
                                About this tool
                            </h2>
                            <div class="instructions__about">
                                <p>This tool uses data, financial terms and
                                    estimations that may need additional
                                    explanation. Learn more about the financial
                                    language, how calculations are created, and
                                    where the data comes from.
                                </p>
                                <p>
                                    <a href="/paying-for-college2/understanding-your-financial-aid-offer/about-this-tool/" target="__blank" rel="noopener noreferrer">Get details
                                    about how this tool works</a>
                                </p>
                            </div>
                        </div>
                    </div>
                    <div class="content__line"></div>
                </div>
            </section>
            <section class="review step wrapper" data-section="review">
                <div class="content__main">
                    <div class="review__wrapper">
                        <div class="review__intro">
                            <h2 class="step__heading">
                                Step 1: Review your first year offer
                            </h2>
                            <p class="step__intro">
                                Here is your financial aid offer from
                                <span id="intro-school-name">South University-West Palm Beach</span>. Please review the amounts provided by
                                your school below and make any necessary changes
                                or add any missing information.  Please note any
                                changes you make here will not change your
                                financial aid offer or your eligibility for
                                grants or loans. You will need to contact your
                                school’s financial aid representative and work
                                with them to update your financial aid package.
                            </p>
                        </div>
                    </div>
                    <div class="recalculating-mobile" style="display: none;">Updating...</div>
                    <div class="offer-part cost-to-attend
                    column-well__wrapper--overflow-small">
                        <div class="offer-part__intro">
                            <div class="offer-part__intro-wrapper">
                                <div class="offer-part__intro-content">
                                    <h3 class="offer-part__heading">
                                        How much does it cost to attend this
                                        school?
                                    </h3>
                                </div>
                            </div>
                        </div>
                        <div class="offer-part__form-wrapper">
                            <form class="aid-form" action="#">
                                <div class="form-group cost-of-attendance">
                                    <div class="aid-form__group-header">
                                        <label class="form-label-header">
                                            Cost of attendance
                                        </label>
                                        <p class="aid-form__definition">
                                            Includes the annual cost of the program
                                            (tuition, fees, books, and supplies)
                                            as well as ordinary living expenses
                                            that may be incurred regardless of
                                            enrollment (housing, meals,
                                            transportation, and other personal
                                            expenses)
                                        </p>
                                    </div>
                                    <div class="form-group__item">
                                        <div class="aid-form__label-wrapper">
                                            <label class="form-label" for="costs__tuition">
                                                Tuition and fees
                                            </label>
                                        </div>
                                        <div class="aid-form__input-wrapper">
                                            <input class="aid-form__input
                                            aid-form__input--currency" type="text" id="costs__tuition" name="costs__tuition" data-financial="tuitionFees" autocorrect="off" value="0">
                                        </div>
                                    </div>
                                    <div class="form-group__item">
                                        <div class="aid-form__label-wrapper">
                                            <label class="form-label" for="costs__room-and-board">
                                                Housing and meals
                                            </label>
                                        </div>
                                        <div class="aid-form__input-wrapper">
                                            <input class="aid-form__input
                                            aid-form__input--currency" type="text" id="costs__room-and-board" name="costs__room-and-board" data-financial="roomBoard" autocorrect="off" value="0">
                                        </div>
                                    </div>
                                    <div class="form-group__item">
                                        <div class="aid-form__label-wrapper">
                                            <label class="form-label" for="costs__books">
                                                Books and supplies
                                            </label>
                                        </div>
                                        <div class="aid-form__input-wrapper">
                                            <input class="aid-form__input
                                            aid-form__input--currency" type="text" id="costs__books" name="costs__books" data-financial="books" autocorrect="off" value="0">
                                        </div>
                                    </div>
                                    <div class="form-group__item">
                                        <div class="aid-form__label-wrapper">
                                            <label class="form-label" for="costs__transportation">
                                                Transportation
                                            </label>
                                        </div>
                                        <div class="aid-form__input-wrapper">
                                            <input class="aid-form__input
                                            aid-form__input--currency" type="text" id="costs__transportation" name="costs__transportation" data-financial="transportation" autocorrect="off" value="0">
                                        </div>
                                    </div>
                                    <div class="form-group__item">
                                        <div class="aid-form__label-wrapper">
                                            <label class="form-label" for="costs__other">
                                                Other education costs
                                            </label>
                                            <p class="aid-form__definition">
                                                Personal expenses like
                                                computers, daycare,
                                                entertainment, laundry, etc.
                                            </p>
                                        </div>
                                        <div class="aid-form__input-wrapper">
                                            <input class="aid-form__input
                                            aid-form__input--currency" type="text" id="costs__other" name="costs__other" data-financial="otherExpenses" autocorrect="off" value="0">
                                        </div>
                                    </div>
                                    <div class="aid-form__inline-subtotal">
                                        <div class="content__line
                                        aid-form__equals-line"></div>
                                        <div class="line-item">
                                            <div class="line-item__title">
                                                Total cost of attendance
                                            </div>
                                            <div class="line-item__value">
                                                <span class="line-item__currency" style="">
                                                    $
                                                </span>
                                                <span class="line-item__amount" data-line-item="true" data-financial="costOfAttendance">43,626</span>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                                <div class="form-group
                                grants-and-scholarships">
                                    <div class="aid-form__group-header">
                                        <label class="form-label-header">
                                            Grants and scholarships
                                        </label>
                                        <p class="aid-form__definition">
                                            Money you don’t have to pay back
                                        </p>
                                    </div>
                                    <div class="form-group__item" data-section="pellgrant" style="display: none;">
                                        <div class="aid-form__label-wrapper">
                                            <label class="form-label" for="grants__pell">
                                                Federal Pell Grant
                                            </label>
                                            <p class="aid-form__definition">
                                                Based on financial need,
                                                <a class="a-link" href="https://studentaid.gov/understand-aid/types/grants/pell" rel="noopener noreferrer" target="__blank"><span class="a-link__text">see how you qualify</span> <svg class="cf-icon-svg cf-icon-svg--external-link" viewBox="0 0 14 19" xmlns="http://www.w3.org/2000/svg"><path d="M13.017 3.622v4.6a.554.554 0 0 1-1.108 0V4.96L9.747 7.122a1.65 1.65 0 0 1 .13.646v5.57A1.664 1.664 0 0 1 8.215 15h-5.57a1.664 1.664 0 0 1-1.662-1.663v-5.57a1.664 1.664 0 0 1 1.662-1.662h5.57A1.654 1.654 0 0 1 9 6.302l2.126-2.126H7.863a.554.554 0 1 1 0-1.108h4.6a.554.554 0 0 1 .554.554zM8.77 8.1l-2.844 2.844a.554.554 0 0 1-.784-.783l2.947-2.948H2.645a.555.555 0 0 0-.554.555v5.57a.555.555 0 0 0 .554.553h5.57a.555.555 0 0 0 .554-.554z"></path></svg></a>
                                            </p>
                                        </div>
                                        <div class="aid-form__input-wrapper">
                                            <input class="aid-form__input
                                            aid-form__input--currency" type="text" id="grants__pell" name="grants__pell" data-financial="pell" autocorrect="off" value="0">
                                            <div class="aid-form__calc-error" data-calc-error="pell" style="display: none;">
                                                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 17 19" class="cf-icon-svg cf-icon-svg--error-round"><path d="M16.417 9.583a7.916 7.916 0 1 1-15.833 0 7.916 7.916 0 0 1 15.833 0Zm-6.804.01 3.032-3.033a.792.792 0 1 0-1.12-1.12L8.494 8.473 5.46 5.44a.792.792 0 0 0-1.12 1.12l3.033 3.033-3.032 3.033a.791.791 0 1 0 1.12 1.119l3.032-3.033 3.033 3.033a.79.79 0 0 0 1.12 0c.309-.31.309-.81 0-1.12L9.612 9.594Z"></path></svg>
                                                The maximum that can be awarded per year is <span data-cap="pell">$9,293</span>
                                            </div>
                                            <div class="aid-form__calc-error" data-calc-error="overBorrowing" style="display: none;">
                                                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 17 19" class="cf-icon-svg cf-icon-svg--error-round"><path d="M16.417 9.583a7.916 7.916 0 1 1-15.833 0 7.916 7.916 0 0 1 15.833 0Zm-6.804.01 3.032-3.033a.792.792 0 1 0-1.12-1.12L8.494 8.473 5.46 5.44a.792.792 0 0 0-1.12 1.12l3.033 3.033-3.032 3.033a.791.791 0 1 0 1.12 1.119l3.032-3.033 3.033 3.033a.79.79 0 0 0 1.12 0c.309-.31.309-.81 0-1.12L9.612 9.594Z"></path></svg>
                                                The total of your federal aid can't be more than the total cost of attendance
                                            </div>
                                        </div>
                                    </div>
                                    <div class="form-group__item">
                                        <div class="aid-form__label-wrapper">
                                            <label class="form-label" for="grants__school">
                                                Grants and scholarships from
                                                your school
                                            </label>
                                            <p class="aid-form__definition">
                                                Total amount awarded from your
                                                school
                                            </p>
                                        </div>
                                        <div class="aid-form__input-wrapper">
                                            <input class="aid-form__input
                                            aid-form__input--currency" type="text" id="grants__school" name="grants__school" data-financial="schoolGrants" autocorrect="off" value="0">
                                        </div>
                                    </div>
                                    <div class="form-group__item">
                                        <div class="aid-form__label-wrapper">
                                            <label class="form-label" for="grants__state">
                                                Grants from your state
                                            </label>
                                            <p class="aid-form__definition">
                                                Total amount awarded from your
                                                state
                                            </p>
                                        </div>
                                        <div class="aid-form__input-wrapper">
                                            <input class="aid-form__input
                                            aid-form__input--currency" type="text" id="grants__state" name="grants__state" data-financial="stateGrants" autocorrect="off" value="0">
                                        </div>
                                    </div>
                                    <div class="form-group__item">
                                        <div class="aid-form__label-wrapper">
                                            <label class="form-label" for="grants__scholarships">
                                                Other grants and scholarships
                                            </label>
                                            <p class="aid-form__definition">
                                                Such as academic scholarships
                                                or grants from a foundation
                                            </p>
                                        </div>
                                        <div class="aid-form__input-wrapper">
                                            <input class="aid-form__input
                                            aid-form__input--currency" type="text" id="grants__scholarships" name="grants__scholarships" data-financial="otherScholarships" autocorrect="off" value="0">
                                        </div>
                                    </div>
                                    <div class="form-group__item" data-section="military">
                                        <div class="aid-form__label-wrapper">
                                            <label class="form-label" for="grants__military">
                                                Military tuition assistance
                                            </label>
                                            <p class="aid-form__definition">
                                                Money for active or reserve
                                                servicemembers that you don’t
                                                have to pay back
                                            </p>
                                        </div>
                                        <div class="aid-form__input-wrapper">
                                            <input class="aid-form__input
                                            aid-form__input--currency" type="text" id="grants__military" name="grants__military" data-financial="militaryTuitionAssistance" autocorrect="off" value="0">
                                            <div class="aid-form__calc-error" data-calc-error="militaryTuitionAssistance" style="display: none;">
                                                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 17 19" class="cf-icon-svg cf-icon-svg--error-round"><path d="M16.417 9.583a7.916 7.916 0 1 1-15.833 0 7.916 7.916 0 0 1 15.833 0Zm-6.804.01 3.032-3.033a.792.792 0 1 0-1.12-1.12L8.494 8.473 5.46 5.44a.792.792 0 0 0-1.12 1.12l3.033 3.033-3.032 3.033a.791.791 0 1 0 1.12 1.119l3.032-3.033 3.033 3.033a.79.79 0 0 0 1.12 0c.309-.31.309-.81 0-1.12L9.612 9.594Z"></path></svg>
                                                The maximum that can be awarded per
                                                year is <span data-cap="militaryTuitionAssistance">$4,500</span>
                                            </div>
                                        </div>
                                    </div>
                                    <div class="form-group__item" data-section="gibill">
                                        <div class="aid-form__label-wrapper">
                                            <label class="form-label" for="grants__gi">
                                                GI Bill
                                            </label>
                                            <p class="aid-form__definition">
                                                Money for service members or
                                                veterans that you don’t have
                                                to pay back; <a class="a-link" href="https://www.vets.gov/gi-bill-comparison-tool" rel="noopener noreferrer" target="__blank"><span class="a-link__text">see how much the
                                                GI Bill pays</span> <svg class="cf-icon-svg cf-icon-svg--external-link" viewBox="0 0 14 19" xmlns="http://www.w3.org/2000/svg"><path d="M13.017 3.622v4.6a.554.554 0 0 1-1.108 0V4.96L9.747 7.122a1.65 1.65 0 0 1 .13.646v5.57A1.664 1.664 0 0 1 8.215 15h-5.57a1.664 1.664 0 0 1-1.662-1.663v-5.57a1.664 1.664 0 0 1 1.662-1.662h5.57A1.654 1.654 0 0 1 9 6.302l2.126-2.126H7.863a.554.554 0 1 1 0-1.108h4.6a.554.554 0 0 1 .554.554zM8.77 8.1l-2.844 2.844a.554.554 0 0 1-.784-.783l2.947-2.948H2.645a.555.555 0 0 0-.554.555v5.57a.555.555 0 0 0 .554.553h5.57a.555.555 0 0 0 .554-.554z"></path></svg></a>
                                            </p>
                                        </div>
                                        <div class="aid-form__input-wrapper">
                                            <input class="aid-form__input
                                            aid-form__input--currency" type="text" id="grants__gi" name="grants__gi" data-financial="GIBill" autocorrect="off" value="0">
                                        </div>
                                    </div>
                                    <div class="aid-form__inline-subtotal">
                                        <div class="content__line
                                        aid-form__equals-line"></div>
                                        <div class="line-item">
                                            <div class="line-item__title">
                                                Total grants and scholarships
                                            </div>
                                            <div class="line-item__value">
                                                <span class="line-item__currency" style="">
                                                    $
                                                </span>
                                                <span class="line-item__amount" data-line-item="true" data-financial="grantsTotal">10,100</span>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </form>
                        </div>
                        <div class="offer-part__summary-wrapper column-well
                        column-well--bleed column-well--not-stacked">
                            <div class="aid-form__summary column-well__content">
                                <h4 class="aid-form__summary-heading">
                                    Cost summary
                                </h4>
                                <div class="line-item">
                                    <div class="line-item__title">
                                        Cost of attendance
                                    </div>
                                    <div class="line-item__value">
                                        <span class="line-item__currency" style="">
                                            $
                                        </span>
                                        <span class="line-item__amount" data-line-item="true" data-financial="costOfAttendance" id="summary__cost-of-attendance">43,626</span>
                                    </div>
                                </div>
                                <div class="line-item">
                                    <div class="line-item__title">
                                        Grants and scholarships
                                    </div>
                                    <div class="line-item__value">
                                        <span class="line-item__currency" style="">
                                            <span class="line-item__sign">
                                                ( − )
                                            </span>
                                            $
                                        </span>
                                        <span class="line-item__amount" data-line-item="true" data-financial="grantsTotal" id="summary__total-grants-scholarships">10,100</span>
                                    </div>
                                </div>
                                <div class="content__line aid-form__equals-line">
                                </div>
                                <div class="line-item line-item--total">
                                    <div class="line-item__title">
                                        Your out-of-pocket cost
                                    </div>
                                    <div class="line-item__value">
                                        <span class="line-item__currency" style="">
                                            $
                                        </span>
                                        <span class="line-item__amount" data-line-item="true" data-financial="firstYearNetCost" id="summary__total-cost">33,526</span>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="offer-part contributions
                    column-well__wrapper--overflow-small">
                        <div class="offer-part__intro">
                            <div class="offer-part__intro-wrapper">
                                <div class="offer-part__intro-content">
                                    <h3 class="offer-part__heading">
                                        How much can you contribute without
                                        going into debt?
                                    </h3>
                                    <p>
                                        This section includes loans that your
                                        family has to repay, but those loans are
                                        not included in <em>your</em> personal
                                        debt or student loan payments summary.
                                    </p>
                                </div>
                            </div>
                        </div>
                        <div class="offer-part__form-wrapper">
                            <form class="aid-form" action="#">
                                <div class="form-group
                                personal-family-contributions">
                                    <div class="aid-form__group-header">
                                        <label class="form-label-header">
                                            Personal and family/others contributions
                                        </label>
                                    </div>
                                    <div class="form-group__item">
                                        <div class="aid-form__label-wrapper">
                                            <label class="form-label" for="contrib__savings">
                                                Cash you will pay
                                            </label>
                                            <p class="aid-form__definition">
                                                Includes money that you can
                                                pay now or will earn during
                                                the school year
                                            </p>
                                        </div>
                                        <div class="aid-form__input-wrapper">
                                            <input class="aid-form__input
                                            aid-form__input--currency" type="text" id="contrib__savings" name="contrib__savings" data-financial="savings" autocorrect="off" value="0">
                                        </div>
                                    </div>
                                    <div class="form-group__item">
                                        <div class="aid-form__label-wrapper">
                                            <label class="form-label" for="contrib__family">
                                                Money your family or others will pay
                                            </label>
                                            <p class="aid-form__definition">
                                                Includes money given to you from
                                                family or others, private loans
                                                your parents take out, etc.
                                            </p>
                                        </div>
                                        <div class="aid-form__input-wrapper">
                                            <input class="aid-form__input
                                            aid-form__input--currency" type="text" id="contrib__family" name="contrib__family" data-financial="family" autocorrect="off" value="0">
                                        </div>
                                    </div>
                                    <div class="form-group__item">
                                        <div class="aid-form__label-wrapper">
                                            <label class="form-label" for="contrib__parent-plus">
                                                Parent PLUS loan
                                            </label>
                                            <p class="aid-form__definition">
                                                Federal loans your parents take out and repay;
                                                does not count toward your total student loan debt
                                                shown in this tool
                                            </p>
                                        </div>
                                        <div class="aid-form__input-wrapper">
                                            <input class="aid-form__input
                                            aid-form__input--currency" type="text" id="contrib__parent-plus" name="contrib__parent-plus" data-financial="parentPlus" autocorrect="off" value="0">
                                        </div>
                                    </div>
                                    <div class="form-group__item" data-section="workstudy">
                                        <div class="aid-form__label-wrapper">
                                            <label class="form-label" for="contrib__workstudy">
                                                Federal Work-Study
                                            </label>
                                            <p class="aid-form__definition">
                                                Money you earn per year from
                                                an eligible Federal Work-Study
                                                job while in school; awarded
                                                based on financial need
                                            </p>
                                        </div>
                                        <div class="aid-form__input-wrapper">
                                            <input class="aid-form__input
                                            aid-form__input--currency" type="text" id="contrib__workstudy" name="contrib__workstudy" data-financial="workstudy" autocorrect="off" value="0">
                                        </div>
                                    </div>
                                </div>
                            </form>
                        </div>
                        <div class="offer-part__summary-wrapper column-well
                        column-well--bleed column-well--not-stacked">
                            <div class="aid-form__summary column-well__content">
                                <h4 class="aid-form__summary-heading">
                                    Contributions summary
                                </h4>
                                <div class="line-item">
                                    <div class="line-item__title">
                                        Cash you will pay
                                    </div>
                                    <div class="line-item__value">
                                        <span class="line-item__currency" style="">
                                            $
                                        </span>
                                        <span class="line-item__amount" data-line-item="true" data-financial="savings">0</span>
                                    </div>
                                </div>
                                <div class="line-item">
                                    <div class="line-item__title">
                                        Money your family/others will pay
                                    </div>
                                    <div class="line-item__value">
                                        <span class="line-item__currency" style="">
                                            <span class="line-item__sign">
                                                ( + )
                                            </span>
                                            $
                                        </span>
                                        <span class="line-item__amount" data-line-item="true" data-financial="family">14,000</span>
                                    </div>
                                </div>
                                <div class="line-item">
                                    <div class="line-item__title">
                                        Parent PLUS loans
                                    </div>
                                    <div class="line-item__value">
                                        <span class="line-item__currency" style="">
                                            <span class="line-item__sign">
                                                ( + )
                                            </span>
                                            $
                                        </span>
                                        <span class="line-item__amount" data-line-item="true" data-financial="parentPlus">1,000</span>
                                    </div>
                                </div>
                                <div class="line-item" data-section="workstudy">
                                    <div class="line-item__title">
                                        Federal Work-Study
                                    </div>
                                    <div class="line-item__value">
                                        <span class="line-item__currency" style="">
                                            <span class="line-item__sign">
                                                ( + )
                                            </span>
                                            $
                                        </span>
                                        <span class="line-item__amount" data-line-item="true" data-financial="workstudy">3,000</span>
                                    </div>
                                </div>
                                <div class="content__line aid-form__equals-line">
                                </div>
                                <div class="line-item line-item--total">
                                    <div class="line-item__title">
                                        Your personal and family/others
                                        contributions
                                    </div>
                                    <div class="line-item__value">
                                        <span class="line-item__currency" style="">
                                            $
                                        </span>
                                        <span class="line-item__amount" data-line-item="true" data-financial="savingsTotal" id="summary__total-contributions">18,000</span>
                                    </div>
                                </div>
                            </div>
                            <div class="aid-form__summary big-picture
                            column-well__content">
                                <h4 class="aid-form__summary-heading">
                                    Big picture
                                </h4>
                                <div class="line-item">
                                    <div class="line-item__title">
                                        Your out-of-pocket cost
                                    </div>
                                    <div class="line-item__value">
                                        <span class="line-item__currency" style="">
                                            $
                                        </span>
                                        <span class="line-item__amount" data-line-item="true" data-financial="firstYearNetCost">33,526</span>
                                    </div>
                                </div>
                                <div class="line-item">
                                    <div class="line-item__title">
                                        Your contributions
                                    </div>
                                    <div class="line-item__value">
                                        <span class="line-item__currency" style="">
                                            <span class="line-item__sign">
                                                ( − )
                                            </span>
                                            $
                                        </span>
                                        <span class="line-item__amount" data-line-item="true" data-financial="savingsTotal">18,000</span>
                                    </div>
                                </div>
                                <div class="content__line aid-form__equals-line">
                                </div>
                                <div class="line-item line-item--total">
                                    <div class="line-item__title">
                                        Remaining cost
                                    </div>
                                    <div class="line-item__value">
                                        <span class="line-item__currency" style="">
                                            $
                                        </span>
                                        <span class="line-item__amount" data-line-item="true" id="summary__remaining-cost-after-contrib" data-financial="remainingCost">15,526</span>
                                    </div>
                                </div>
                                <p>
                                    This is an estimate of the remaining costs
                                    of studying your program at
                                    South University-West Palm Beach for one year.
                                </p>
                            </div>
                        </div>
                    </div>
                    <div class="offer-part loans
                    column-well__wrapper--overflow-small">
                        <div class="offer-part__intro">
                            <div class="offer-part__intro-wrapper">
                                <div class="offer-part__intro-content">
                                    <h3 class="offer-part__heading">
                                        How much would you have to borrow to
                                        cover the remaining cost?
                                    </h3>
                                </div>
                            </div>
                        </div>
                        <div class="offer-part__form-wrapper">
                            <form class="aid-form" action="#">
                                <div class="form-group federal-loans" data-section="federalLoans">
                                    <div class="aid-form__group-header">
                                        <label class="form-label-header">
                                            Federal loans
                                        </label>
                                        <p class="aid-form__definition">
                                            Money you borrow from the federal
                                            government this year and have to
                                            pay back over time. Interest rates
                                            and loan fees on future federal
                                            loans may increase or decrease
                                            year to year.
                                        </p>
                                    </div>
                                    <div class="form-group__item" data-section="perkins" style="display: none;">
                                        <div class="aid-form__label-wrapper">
                                            <label class="form-label" for="contrib__perkins">
                                                Perkins loans
                                            </label>
                                        </div>
                                        <div class="aid-form__input-wrapper">
                                            <input class="aid-form__input
                                            aid-form__input--currency" type="text" id="contrib__perkins" name="contrib__perkins" data-financial="perkins" autocorrect="off" value="0">
                                            <div class="aid-form__calc-error" data-calc-error="perkins" style="display: none;">
                                                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 17 19" class="cf-icon-svg cf-icon-svg--error-round"><path d="M16.417 9.583a7.916 7.916 0 1 1-15.833 0 7.916 7.916 0 0 1 15.833 0Zm-6.804.01 3.032-3.033a.792.792 0 1 0-1.12-1.12L8.494 8.473 5.46 5.44a.792.792 0 0 0-1.12 1.12l3.033 3.033-3.032 3.033a.791.791 0 1 0 1.12 1.119l3.032-3.033 3.033 3.033a.79.79 0 0 0 1.12 0c.309-.31.309-.81 0-1.12L9.612 9.594Z"></path></svg>
                                                The maximum that can be borrowed per year is
                                                <span data-cap="perkins">$8,000</span>
                                            </div>
                                        </div>
                                        <div class="offer-part__terms">
                                            <p class="offer-part__term">
                                                <span data-financial="perkinsRate" data-percentage_value="true">5</span>% interest
                                            </p>
                                            <p class="aid-form__definition">
                                                Reserved for students most in
                                                need; interest starts
                                                accumulating 9 months after you
                                                leave school; <a class="a-link" href="https://studentaid.ed.gov/sa/types/loans/perkins" rel="noopener noreferrer" target="__blank"><span class="a-link__text">
                                                see how you qualify</span> <svg class="cf-icon-svg cf-icon-svg--external-link" viewBox="0 0 14 19" xmlns="http://www.w3.org/2000/svg"><path d="M13.017 3.622v4.6a.554.554 0 0 1-1.108 0V4.96L9.747 7.122a1.65 1.65 0 0 1 .13.646v5.57A1.664 1.664 0 0 1 8.215 15h-5.57a1.664 1.664 0 0 1-1.662-1.663v-5.57a1.664 1.664 0 0 1 1.662-1.662h5.57A1.654 1.654 0 0 1 9 6.302l2.126-2.126H7.863a.554.554 0 1 1 0-1.108h4.6a.554.554 0 0 1 .554.554zM8.77 8.1l-2.844 2.844a.554.554 0 0 1-.784-.783l2.947-2.948H2.645a.555.555 0 0 0-.554.555v5.57a.555.555 0 0 0 .554.553h5.57a.555.555 0 0 0 .554-.554z"></path></svg></a>
                                            </p>
                                        </div>
                                    </div>
                                    <div class="content__line loans__line" data-section="perkins" style="display: none;"></div>
                                    <div class="form-group__item" data-section="subsidized" style="display: none;">
                                        <div class="aid-form__label-wrapper">
                                            <label class="form-label" for="contrib__subsidized">
                                                Subsidized loans
                                            </label>
                                        </div>
                                        <div class="aid-form__input-wrapper">
                                            <input class="aid-form__input
                                            aid-form__input--currency" type="text" id="contrib__subsidized" name="contrib__subsidized" data-financial="directSubsidized" autocorrect="off" value="0">
                                            <div class="aid-form__calc-error" data-calc-error="directSubsidized" style="display: none;">
                                                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 17 19" class="cf-icon-svg cf-icon-svg--error-round"><path d="M16.417 9.583a7.916 7.916 0 1 1-15.833 0 7.916 7.916 0 0 1 15.833 0Zm-6.804.01 3.032-3.033a.792.792 0 1 0-1.12-1.12L8.494 8.473 5.46 5.44a.792.792 0 0 0-1.12 1.12l3.033 3.033-3.032 3.033a.791.791 0 1 0 1.12 1.119l3.032-3.033 3.033 3.033a.79.79 0 0 0 1.12 0c.309-.31.309-.81 0-1.12L9.612 9.594Z"></path></svg>
                                                The maximum that can be borrowed per year is
                                                <span data-cap="directSubsidized">$NaN</span>
                                            </div>
                                        </div>
                                        <div class="offer-part__terms">
                                            <p class="offer-part__term">
                                                <span data-financial="subsidizedRate" data-percentage_value="true">4.99</span>% interest
                                            </p>
                                            <p class="aid-form__definition">
                                                Interest starts accumulating 6
                                                months after you leave school
                                            </p>
                                            <p class="offer-part__term">
                                                <span data-financial="DLOriginationFee" data-fee="origination" data-percentage_value="true">1.06</span>% loan fee
                                            </p>
                                            <p class="aid-form__definition">
                                                Fee is deducted immediately from
                                                your loan amount, lowering the
                                                total you receive (for example,
                                                if the loan fee is 1%, then $10
                                                will be subtracted from a $1,000
                                                loan, so you or your school will
                                                only receive $990 but you would
                                                have to repay $1,000)
                                            </p>
                                        </div>
                                    </div>
                                    <div class="content__line loans__line" data-section="subsidized" style="display: none;"></div>
                                    <div class="form-group__item" data-section="unsubsidized">
                                        <div class="aid-form__label-wrapper">
                                            <label class="form-label" for="contrib__unsubsidized">
                                                Unsubsidized loans
                                            </label>
                                        </div>
                                        <div class="aid-form__input-wrapper">
                                            <input class="aid-form__input
                                            aid-form__input--currency" type="text" id="contrib__unsubsidized" name="contrib__unsubsidized" data-financial="directUnsubsidized" autocorrect="off" value="0">
                                            <div class="aid-form__calc-error" data-calc-error="directUnsubsidized" style="display: none;">
                                                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 17 19" class="cf-icon-svg cf-icon-svg--error-round"><path d="M16.417 9.583a7.916 7.916 0 1 1-15.833 0 7.916 7.916 0 0 1 15.833 0Zm-6.804.01 3.032-3.033a.792.792 0 1 0-1.12-1.12L8.494 8.473 5.46 5.44a.792.792 0 0 0-1.12 1.12l3.033 3.033-3.032 3.033a.791.791 0 1 0 1.12 1.119l3.032-3.033 3.033 3.033a.79.79 0 0 0 1.12 0c.309-.31.309-.81 0-1.12L9.612 9.594Z"></path></svg>
                                                <span data-calc-error_content="directUnsubsidized">The maximum that can be borrowed per year is</span>
                                                <span data-cap="directUnsubsidized">$47,167</span>
                                            </div>
                                        </div>
                                        <div class="offer-part__terms">
                                            <p class="offer-part__term">
                                                <span data-financial="unsubsidizedRate" data-percentage_value="true">6.54</span>% interest
                                            </p>
                                            <p class="aid-form__definition">
                                                Interest starts accumulating
                                                when the money is sent to your
                                                school
                                            </p>
                                            <p class="offer-part__term">
                                                <span data-financial="DLOriginationFee" data-fee="origination" data-percentage_value="true">1.06</span>% loan fee
                                            </p>
                                            <p class="aid-form__definition">
                                                Fee is deducted immediately from
                                                your loan amount, lowering the
                                                total you receive (for example,
                                                if the loan fee is 1%, then $10
                                                will be subtracted from a $1,000
                                                loan, so you or your school will
                                                only receive $990 but you would
                                                have to repay $1,000)
                                            </p>
                                        </div>
                                    </div>
                                    <div data-section="gradPlus">
                                      <div class="content__line loans__line"></div>
                                      <div class="form-group__item">
                                          <div class="aid-form__label-wrapper">
                                              <label class="form-label" for="contrib__direct-plus">
                                                  Grad PLUS loan
                                              </label>
                                          </div>
                                          <div class="aid-form__input-wrapper">
                                              <input class="aid-form__input
                                              aid-form__input--currency" type="text" id="contrib__direct-plus" name="contrib__direct-plus" data-financial="gradPlus" autocorrect="off" value="0">
                                          </div>
                                          <div class="offer-part__terms">
                                              <p class="offer-part__term">
                                                  <span data-financial="gradPlusRate" data-percentage_value="true">7.54</span>% interest
                                              </p>
                                              <p class="aid-form__definition">
                                                  Interest starts accumulating
                                                  when the money is sent to your
                                                  school
                                              </p>
                                              <p class="offer-part__term">
                                                  <span data-financial="plusOriginationFee" data-fee="origination" data-percentage_value="true">4.23</span>% loan fee
                                              </p>
                                              <p class="aid-form__definition">
                                                Fee is deducted immediately from
                                                your loan amount, lowering the
                                                total you receive (for example,
                                                if the loan fee is 4%, then $40
                                                will be subtracted from a $1,000
                                                loan, so you or your school will
                                                only receive $960 but you would
                                                have to repay $1,000)
                                              </p>
                                          </div>
                                      </div>
                                    </div>
                                    <div class="aid-form__inline-subtotal" data-section="federalLoans">
                                        <div class="content__line
                                        aid-form__equals-line"></div>
                                        <div class="line-item">
                                            <div class="line-item__title">
                                                Total federal loans
                                            </div>
                                            <div class="line-item__value">
                                                <span class="line-item__currency" style="">
                                                    $
                                                </span>
                                                <span class="line-item__amount" data-line-item="true" data-financial="federalTotal">3,000</span>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                                <div class="form-group private-loans-group">
                                    <div class="aid-form__group-header">
                                        <label class="form-label-header">
                                            Private loans
                                        </label>
                                        <p class="aid-form__definition">
                                            Money from banks, schools, or others
                                            you have to pay back
                                        </p>
                                    </div>
                                    <div class="private-loans">
                                        <div class="private-loans--loan" data-private-loan="true">
                                            <div class="private-loans__heading">
                                                <div class="private-loans__heading-text">
                                                    Private loan
                                                </div>
                                                <button class="a-btn a-btn--link
                                                private-loans__remove-btn" type="button" title="Remove this private loan">
                                                    Remove
                                                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 17 19" class="cf-icon-svg cf-icon-svg--error-round"><path d="M16.417 9.583a7.916 7.916 0 1 1-15.833 0 7.916 7.916 0 0 1 15.833 0Zm-6.804.01 3.032-3.033a.792.792 0 1 0-1.12-1.12L8.494 8.473 5.46 5.44a.792.792 0 0 0-1.12 1.12l3.033 3.033-3.032 3.033a.791.791 0 1 0 1.12 1.119l3.032-3.033 3.033 3.033a.79.79 0 0 0 1.12 0c.309-.31.309-.81 0-1.12L9.612 9.594Z"></path></svg>

                                                </button>
                                            </div>
                                            <div class="form-group__item">
                                                <div class="aid-form__label-wrapper">
                                                    <label class="form-label" for="contrib__private-loan">
                                                        Loan amount
                                                    </label>
                                                </div>
                                                <div class="aid-form__input-wrapper">
                                                    <input class="aid-form__input
                                                    aid-form__input--currency" type="text" id="contrib__private-loan_0" name="contrib__private-loan" data-financial="privateLoan" data-private-loan_key="amount" autocorrect="off" value="0">
                                                </div>
                                            </div>
                                            <div class="form-group__item">
                                                <div class="aid-form__label-wrapper">
                                                    <label class="form-label" for="contrib__private-loan-interest">
                                                        Interest rate
                                                    </label>
                                                    <p class="aid-form__definition">
                                                        Interest starts
                                                        accumulating when you
                                                        sign the loan; may be a
                                                        variable rate and
                                                        increase or decrease in
                                                        the future
                                                    </p>
                                                </div>
                                                <div class="aid-form__input-wrapper">
                                                    <input class="aid-form__input
                                                    aid-form__input--percent" type="text" id="contrib__private-loan-interest_0" name="contrib__private-loan-interest" data-financial="privateLoanRate" data-private-loan_key="rate" data-percentage_value="true" autocorrect="off" value="7.9">
                                                    <span class="aid-form__unit">
                                                        %
                                                    </span>
                                                </div>
                                            </div>
                                            <div class="form-group__item">
                                                <div class="aid-form__label-wrapper">
                                                    <label class="form-label" for="contrib__private-loan-fees">
                                                        Loan fees
                                                    </label>
                                                    <p class="aid-form__definition">
                                                        Fee is added to the
                                                        total loan amount (for
                                                        example if the loan
                                                        fee is 3%, then $30
                                                        would be added to a
                                                        $1,000 loan, so you or
                                                        your school receive
                                                        $1,000 but you would
                                                        have to repay $1,030)
                                                    </p>
                                                </div>
                                                <div class="aid-form__input-wrapper">
                                                    <input class="aid-form__input
                                                    aid-form__input--percent" type="text" id="contrib__private-loan-fees_0" name="contrib__private-loan-fees" data-financial="privateLoanFees" data-percentage_value="true" data-private-loan_key="fees" autocorrect="off" value="0.049">
                                                    <span class="aid-form__unit">
                                                        %
                                                    </span>
                                                </div>
                                            </div>
                                        </div>


                                        <button class="a-btn a-btn--link
                                                       private-loans__add-btn"
                                                type="button" title="Add another private loan" data-add-loan-button="true">
                                            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 17 19" class="cf-icon-svg cf-icon-svg--plus-round"><path d="M16.416 9.583a7.916 7.916 0 1 1-15.833 0 7.916 7.916 0 0 1 15.833 0Zm-2.958.01a.792.792 0 0 0-.792-.792H9.284V5.42a.792.792 0 1 0-1.583 0V8.8H4.32a.792.792 0 0 0 0 1.584H7.7v3.382a.792.792 0 1 0 1.583 0v-3.382h3.382a.792.792 0 0 0 .792-.791Z"></path></svg>
                                            Add another private loan
                                        </button>
                                    </div>
                                    <div class="aid-form__inline-subtotal">
                                        <div class="content__line
                                        aid-form__equals-line"></div>
                                        <div class="line-item">
                                            <div class="line-item__title">
                                                Total private loans
                                            </div>
                                            <div class="line-item__value">
                                                <span class="line-item__currency" style="">
                                                    $
                                                </span>
                                                <span class="line-item__amount" data-line-item="true" data-financial="privateLoanTotal">3,000</span>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                                <div class="form-group tuition-payment-plan" data-section="tuitionpaymentplan">
                                    <div class="aid-form__group-header">
                                        <label class="form-label-header">
                                            Tuition payment plan from your
                                            school
                                        </label>
                                        <p class="aid-form__definition">
                                            A loan arrangement with your school
                                            that you pay back within a certain
                                            amount of time. The amount of the
                                            tuition payment plan shown here is
                                            the total awarded for the length of
                                            your entire program, not per year.
                                        </p>
                                    </div>
                                    <div class="form-group__item">
                                        <div class="aid-form__label-wrapper">
                                            <label class="form-label" for="contrib__payment-plan">
                                                Loan amount for entire program
                                            </label>
                                        </div>
                                        <div class="aid-form__input-wrapper">
                                            <input class="aid-form__input
                                            aid-form__input--currency" type="text" id="contrib__payment-plan" name="contrib__payment-plan" data-financial="tuitionRepay" autocorrect="off" value="0">
                                        </div>
                                    </div>
                                    <div class="form-group__item">
                                        <div class="aid-form__label-wrapper">
                                            <label class="form-label" for="contrib__payment-plan-yearly">
                                                Loan amount for one year
                                            </label>
                                            <p class="aid-form__definition">
                                                Full tuition payment plan amount
                                                divided by the estimated years
                                                to complete your program
                                            </p>
                                        </div>
                                        <div class="aid-form__input-wrapper">
                                            <input class="aid-form__input
                                            aid-form__input--currency" type="text" id="contrib__payment-plan-yearly" name="contrib__payment-plan-yearly" data-financial="tuitionRepayYearly" disabled="" autocorrect="off" value="0">
                                        </div>
                                    </div>
                                    <div class="form-group__item">
                                        <div class="offer-part__terms">
                                            <p class="offer-part__term">
                                                <span data-financial="tuitionRepayRate" data-percentage_value="true">4.55</span>% interest
                                            </p>
                                            <p class="aid-form__definition">
                                                Interest starts accumulating
                                                when you leave or finish school
                                            </p>
                                            <p class="offer-part__term">
                                                Payments start while you are in
                                                school and the loan must be paid
                                                back within <span data-financial="tuitionRepayTerm" data-currency="false">8</span> months
                                            </p>
                                        </div>
                                    </div>
                                    <div class="aid-form__inline-subtotal" data-section="tuitionpaymentplan" style="display: block;">
                                        <div class="content__line
                                        aid-form__equals-line"></div>
                                        <div class="line-item">
                                            <div class="line-item__title">
                                                Total payment plans
                                            </div>
                                            <div class="line-item__value">
                                                <span class="line-item__currency" style="">
                                                    $
                                                </span>
                                                <span class="line-item__amount" data-line-item="true" data-financial="tuitionRepay">3,000</span>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </form>
                        </div>
                        <div class="offer-part__summary-wrapper column-well
                        column-well--bleed column-well--not-stacked">
                            <div class="aid-form__summary column-well__content">
                                <h4 class="aid-form__summary-heading">
                                    Loans summary
                                </h4>
                                <div class="line-item" data-section="federalLoans">
                                    <div class="line-item__title">
                                        Federal loans
                                    </div>
                                    <div class="line-item__value">
                                        <span class="line-item__currency" style="">
                                            $
                                        </span>
                                        <span class="line-item__amount" data-line-item="true" data-financial="federalTotal" id="summary__total-federal-loans">3,000</span>
                                    </div>
                                </div>
                                <div class="line-item">
                                    <div class="line-item__title">
                                        Private loans
                                    </div>
                                    <div class="line-item__value">
                                        <span class="line-item__currency" style="">
                                            <span class="line-item__sign">
                                                ( + )
                                            </span>
                                            $
                                        </span>
                                        <span class="line-item__amount" data-line-item="true" data-financial="privateLoanTotal" id="summary__total-private-loans">3,000</span>
                                    </div>
                                </div>
                                <div class="line-item" data-section="tuitionpaymentplan">
                                    <div class="line-item__title">
                                        Tuition payment plan for one year
                                    </div>
                                    <div class="line-item__value">
                                        <span class="line-item__currency" style="">
                                            <span class="line-item__sign">
                                                ( + )
                                            </span>
                                            $
                                        </span>
                                        <span class="line-item__amount" data-line-item="true" data-financial="tuitionRepayYearly" id="summary__total-payment-plans">1,200</span>
                                    </div>
                                </div>
                                <div class="content__line aid-form__equals-line">
                                </div>
                                <div class="line-item line-item--total">
                                    <div class="line-item__title">
                                        Total student loan debt
                                    </div>
                                    <div class="line-item__value">
                                        <span class="line-item__currency" style="">
                                            $
                                        </span>
                                        <span class="line-item__amount" data-line-item="true" data-financial="summaryLoanTotal" id="summary__total-loans">7,200</span>
                                    </div>
                                </div>
                            </div>
                            <div class="aid-form__summary big-picture
                            column-well__content">
                                <h4 class="aid-form__summary-heading">
                                    Big picture
                                </h4>
                                <div class="line-item">
                                    <div class="line-item__title">
                                        Your out-of-pocket cost
                                    </div>
                                    <div class="line-item__value">
                                        <span class="line-item__currency" style="">
                                            $
                                        </span>
                                        <span class="line-item__amount" data-line-item="true" data-financial="firstYearNetCost">33,526</span>
                                    </div>
                                </div>
                                <div class="line-item">
                                    <div class="line-item__title">
                                        Your contributions
                                    </div>
                                    <div class="line-item__value">
                                        <span class="line-item__currency" style="">
                                            <span class="line-item__sign">
                                                ( − )
                                            </span>
                                            $
                                        </span>
                                        <span class="line-item__amount" data-line-item="true" data-financial="savingsTotal">18,000</span>
                                    </div>
                                </div>
                                <div class="line-item">
                                    <div class="line-item__title">
                                        Your debt
                                    </div>
                                    <div class="line-item__value">
                                        <span class="line-item__currency" style="">
                                            <span class="line-item__sign">
                                                ( − )
                                            </span>
                                            $
                                        </span>
                                        <span class="line-item__amount" data-line-item="true" data-financial="summaryLoanTotal">7,200</span>
                                    </div>
                                </div>
                                <div class="content__line aid-form__equals-line">
                                </div>
                                <div class="line-item line-item--total">
                                    <div class="line-item__title">
                                        Remaining cost
                                    </div>
                                    <div class="line-item__value">
                                        <span class="line-item__currency" style="">
                                            $
                                        </span>
                                        <span class="line-item__amount" data-line-item="true" id="summary__remaining-cost-after-loans" data-financial="gap">8,326</span>
                                    </div>
                                </div>
                                <p>
                                    This is an estimate of the remaining costs
                                    of studying your program at
                                    South University-West Palm Beach for one year based
                                    on your inputs above.
                                </p>
                            </div>
                        </div>
                    </div>
                    <div class="offer-part future
                    column-well__wrapper--overflow-small">
                        <div class="offer-part__intro">
                            <div class="offer-part__intro-wrapper">
                                <div class="offer-part__intro-content">
                                    <h3 class="offer-part__heading">
                                        What does this mean for your future?
                                    </h3>
                                </div>
                            </div>
                        </div>
                        <div class="offer-part__form-wrapper">
                            <p class="offer-part__content-positive-cost" style="display: block;">
                                It looks like you still have a remaining cost
                                of <span id="future__remaining-cost-positive" data-financial="gap">$8,326</span> to pay for
                                the first year of school. You’ll either need
                                to lower your cost of attendance, pay more
                                upfront, or increase your loan amount to cover
                                these costs.
                            </p>
                            <p class="offer-part__content-negative-cost" style="display: none;">
                                It looks like you are borrowing
                                <span id="future__remaining-cost-negative" data-financial="overborrowing">$0</span> more than
                                you need to pay for school. You can reduce
                                your future debt by decreasing your loan
                                amount to cover only what you need.
                            </p>
                            <p>
                                Think about how borrowing <span id="future__total-loans" data-financial="summaryLoanTotal">$7,200</span> this
                                year will affect your future finances. As you
                                can see in the summary, the
                                total cost of these loans after <span data-currency="false" data-financial="yearsAttending">two and a half years</span>
                                plus interest and fees equals <span id="future__total-debt" data-financial="loanLifetime">$25,412</span>.
                            </p>
                            <p>
                                Some students find themselves struggling to
                                repay student debt once they leave school. In
                                Step 2, learn how factors like graduation rates
                                and expected salary can affect your ability to
                                repay your student debt.
                            </p>
                        </div>
                        <div class="offer-part__summary-wrapper column-well
                        column-well--bleed column-well--not-stacked">
                            <div class="aid-form__summary big-picture
                            column-well__content">
                                <h4 class="aid-form__summary-heading">
                                    Big picture
                                </h4>
                                <div class="line-item">
                                    <div class="line-item__title">
                                        Your out-of-pocket cost
                                    </div>
                                    <div class="line-item__value">
                                        <span class="line-item__currency" style="">
                                            $
                                        </span>
                                        <span class="line-item__amount" data-line-item="true" data-financial="firstYearNetCost">33,526</span>
                                    </div>
                                </div>
                                <div class="line-item">
                                    <div class="line-item__title">
                                        Your contributions
                                    </div>
                                    <div class="line-item__value">
                                        <span class="line-item__currency" style="">
                                            <span class="line-item__sign">
                                                ( − )
                                            </span>
                                            $
                                        </span>
                                        <span class="line-item__amount" data-line-item="true" data-financial="savingsTotal">18,000</span>
                                    </div>
                                </div>
                                <div class="line-item">
                                    <div class="line-item__title">
                                        Your debt
                                    </div>
                                    <div class="line-item__value">
                                        <span class="line-item__currency" style="">
                                            <span class="line-item__sign">
                                                ( − )
                                            </span>
                                            $
                                        </span>
                                        <span class="line-item__amount" data-line-item="true" data-financial="summaryLoanTotal">7,200</span>
                                    </div>
                                </div>
                                <div class="content__line aid-form__equals-line">
                                </div>
                                <div class="line-item line-item--total">
                                    <div class="line-item__title">
                                        Remaining cost
                                    </div>
                                    <div class="line-item__value">
                                        <span class="line-item__currency" style="">
                                            $
                                        </span>
                                        <span class="line-item__amount" data-line-item="true" data-financial="gap" id="summary__remaining-cost-final">8,326</span>
                                    </div>
                                </div>
                                <p class="offer-part__content-positive-cost" style="display: block;">
                                    After all the grants, scholarships, loans,
                                    and personal contributions, this is how
                                    much you still need to pay to attend
                                    South University-West Palm Beach for one year.
                                </p>
                            </div>
                            <div class="aid-form__summary debt-summary
                            column-well__content">
                                <h4 class="aid-form__summary-heading">
                                    Debt summary
                                </h4>
                                <div class="line-item" data-multi_year="true">
                                    <div class="line-item__title">
                                        Loans for first year
                                    </div>
                                    <div class="line-item__value">
                                        <span class="line-item__currency" style="">
                                            $
                                        </span>
                                        <span class="line-item__amount" data-line-item="true" data-financial="summaryLoanTotal">7,200</span>
                                    </div>
                                </div>
                                <div class="line-item">
                                    <div class="line-item__title" data-multi_year="false" style="display: none;">
                                        Loans for program length
                                    </div>
                                    <div class="line-item__title" data-multi_year="true" style="display: inline-block;">
                                        Loans for <span id="future__years-attending" data-financial="yearsAttending" data-currency="false">two and a half years</span> (program length)
                                    </div>
                                    <div class="line-item__value">
                                        <span class="line-item__currency" style="">
                                            $
                                        </span>
                                        <span class="line-item__amount" data-line-item="true" data-financial="totalProgramDebt" id="summary__total-program-debt">18,000</span>
                                    </div>
                                </div>
                                <div class="line-item">
                                    <div class="line-item__title">
                                        Total cost of repayment with interest
                                        and fees
                                        <span class="line-item__explanation">
                                            Assuming all interest rates and loan
                                            amounts remain the same for the
                                            entire program and a standard
                                            10-year repayment plan
                                        </span>
                                    </div>
                                    <div class="line-item__value">
                                        <span class="line-item__currency" style="">
                                            $
                                        </span>
                                        <span class="line-item__amount" data-line-item="true" data-financial="loanLifetime" id="summary__total-repayment">25,412</span>
                                    </div>
                                </div>
                                <p>
                                    You may be eligible for a
                                    repayment plan that allows you to pay your
                                    loans over a period greater than 10
                                    years.
                                </p>
                            </div>
                        </div>
                    </div>
                </div>
            </section>
            <section class="continue step">
                <div class="wrapper">
                    <div class="content__main">
                        <div class="continue__wrapper">
                            <div class="continue__content">
                                <h2 class="step__heading">
                                    Don’t forget you can edit amounts in your
                                    offer. These loan numbers will be used in
                                    Step 2 to help you evaluate your offer.
                                </h2>
                                <p>
                                    Editing amounts does not change your offer
                                    or your eligibility for grants or loans. If
                                    you want to change your financial aid
                                    package, you will need to contact your
                                    school’s financial aid representative and
                                    work with them to determine your
                                    eligibility.
                                </p>
                                <div class="continue--controls">
                                    <button class="a-btn a-btn--full-on-xs" title="Continue to Step 2" type="button">
                                    Continue to Step 2
                                    </button>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </section>
            <section class="evaluate step wrapper" data-section="evaluate">
                <div class="content__main">
                    <div class="evaluate__wrapper">
                        <div class="evaluate__intro">
                            <h2 class="step__heading">
                                Step 2: Weigh the financial impact of your offer
                            </h2>
                            <p class="step__intro">
                                The information in this section will help you
                                understand how accepting this offer could
                                affect your ability to pay back your student
                                debt and impact your financial future.
                            </p>
                        </div>
                    </div>
                    <section class="criteria column-well__wrapper">
                        <h3 class="criteria__heading">
                            How many students graduate?
                        </h3>
                        <div class="criteria__wrapper">
                            <div class="criteria__intro">
                                <p class="content__grad-cohort" style="display: none;">
                                    For first-time students enrolled full-time
                                    in Physician Assistant at
                                    South University-West Palm Beach,
                                    None out of
                                    None
                                    graduated.
                                </p>
                                <p>
                                    Remember, whether you get your
                                    diploma or not, you’ll still have to repay
                                    federal and private loans (and possibly
                                    even some grants). If you don’t graduate,
                                    you won’t have the added benefit of your
                                    degree to help earn more money to put
                                    toward paying off student loans.
                                </p>
                            </div>
                            <section class="metric graduation-rate column-well
                            column-well--bleed column-well--not-stacked">
                                <div class="column-well__content">
                                    <h4 class="metric__heading">
                                        Graduation rate
                                    </h4>
                                    <p class="metric__explanation">
                                        Percentage of first-time, full-time
                                        students who graduate from
                                        <span class="content-grad-program" style="display: none;">your
                                            program at</span> this school
                                    </p>
                                    <div class="bar-graph" data-metric="gradRate" data-national-metric="completionRateMedian" data-incoming-format="decimal-percent" data-graph-min="0" data-graph-max="1">
                                        <div class="bar-graph__bar"></div>
                                        <div class="bar-graph__point
                                        bar-graph__point--you u-clearfix" style="bottom: 48.16px;">
                                            <div class="bar-graph__label" data-graph_label="completionRate">This school</div>
                                            <div class="bar-graph__line"></div>
                                            <div class="bar-graph__value">
                                                <div data-bar-graph_number="you" class="bar-graph__number">26%</div>
                                            </div>
                                        </div>
                                        <div class="bar-graph__point
                                        bar-graph__point--average u-clearfix" style="display: none;">
                                            <div class="bar-graph__label">
                                                National average
                                            </div>
                                            <div class="bar-graph__line"></div>
                                            <div class="bar-graph__value">
                                                <div data-bar-graph_number="average" class="bar-graph__number">48%</div>
                                            </div>
                                        </div>
                                    </div>
                                    <div class="metric__notification cf-notification metric__notification--worse cf-notification--error" data-better-direction="higher" style="display: none;">

                                        <p class="cf-notification__text
                                        metric__notification__text--better">
                                            Higher graduation rate than national
                                            average
                                        </p>
                                        <p class="cf-notification__text
                                        metric__notification__text--same">
                                            About the same graduation rate as
                                            national average
                                        </p>
                                        <p class="cf-notification__text
                                        metric__notification__text--worse">
                                            <span class="cf-notification__icon
                                                         cf-notification__icon--error">
                                                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 17 19" class="cf-icon-svg cf-icon-svg--error-round"><path d="M16.417 9.583a7.916 7.916 0 1 1-15.833 0 7.916 7.916 0 0 1 15.833 0Zm-6.804.01 3.032-3.033a.792.792 0 1 0-1.12-1.12L8.494 8.473 5.46 5.44a.792.792 0 0 0-1.12 1.12l3.033 3.033-3.032 3.033a.791.791 0 1 0 1.12 1.119l3.032-3.033 3.033 3.033a.79.79 0 0 0 1.12 0c.309-.31.309-.81 0-1.12L9.612 9.594Z"></path></svg>
                                            </span>
                                            Lower graduation rate than national
                                            average
                                        </p>
                                        <p class="cf-notification__text
                                        metric__notification__text--no-you">
                                            We currently don’t have data to
                                            display for your school
                                        </p>
                                        <p class="cf-notification__text
                                        metric__notification__text--no-average">
                                            We currently don’t have national
                                            average data to display
                                        </p>
                                        <p class="cf-notification__text
                                        metric__notification__text--no-data">
                                            We currently don’t have data to
                                            display
                                        </p>
                                    </div>
                                    <div class="metric__link">
                                        <p>
                                            Curious about the graduation rate
                                            for the entire school? <a href="https://collegescorecard.ed.gov/school/?133465#graduation" target="__blank" rel="noopener noreferrer" class="graduation-link a-link">See
                                            how this school’s graduation rate
                                            compares to the national average </a>
                                        </p>
                                    </div>
                                </div>
                            </section>
                        </div>
                    </section>
                    <section class="criteria column-well__wrapper">
                        <h3 class="criteria__heading">
                            How do I know if I'm about to take on too much debt?
                        </h3>
                        <div class="criteria__wrapper">
                            <div class="criteria__intro">
                                <p id="content__salary">
                                    <span id="content__median-salary">The typical salary for students who started attending this school 10 years ago is</span> <span id="criteria__median-salary" data-financial="medianSalary">$33,400</span>
                                    per year. In reality, you could end up
                                    making more or less than the salary
                                    shown here.
                                </p>
                                <p>
                                    If your total debt is too high, it
                                    increases the chances of not being able to
                                    repay your loan on time and incurring late
                                    fees and more interest, or not being able
                                    to pay for other necessities, like rent or
                                    groceries. Since it’s difficult to predict
                                    your future salary, one way to lower your
                                    debt is to reduce the amount of student
                                    loans you take out.
                                </p>
                            </div>
                            <section class="metric salary-and-debt
                            column-well column-well--bleed
                            column-well--not-stacked">
                                <div class="column-well__content">
                                    <h4 class="metric__heading">
                                        Your salary and total student debt
                                    </h4>
                                    <p>
                                        A general rule of thumb <span class="content__graduate-program">for
                                        undergraduates</span> is that you should
                                        avoid borrowing more for school than
                                        you’ll earn your first year out of
                                        school.
                                    </p>
                                    <p class="content__graduate-program">
                                        For graduate students, especially in
                                        medical residency programs, this rule of
                                        thumb may not apply.
                                    </p>
                                    <div id="salary-and-debt-metric" class="salary-and-debt__projection">
                                        <div id="content__salary-metric" class="salary-and-debt__projection-name">Typical salary for this school</div>
                                        <div class="salary-and-debt__projection-value">
                                            <span data-financial="medianSalary">$33,400</span>
                                        </div>
                                    </div>
                                    <div class="salary-and-debt__projection">
                                        <div class="salary-and-debt__projection-name">
                                          Estimated debt when repayment begins
                                          <span class="salary-and-debt__explanation">
                                              Includes interest and fees
                                              accrued while in school
                                          </span>
                                        </div>
                                        <div class="salary-and-debt__projection-value">
                                            <span data-financial="totalDebt">$17,011</span>
                                      </div>
                                    </div>
                                    <div class="metric__notification" data-better-direction="higher">
                                        <p class="cf-notification__text
                                        metric__notification__text--better">
                                            Projected first-year salary is
                                            higher than total student debt
                                        </p>
                                        <p class="cf-notification__text
                                        metric__notification__text--same">
                                            Projected first-year salary is
                                            about the same as total student debt
                                        </p>
                                        <p class="cf-notification__text
                                        metric__notification__text--worse">
                                            <span class="cf-notification__icon
                                                         cf-notification__icon--error">
                                                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 17 19" class="cf-icon-svg cf-icon-svg--error-round"><path d="M16.417 9.583a7.916 7.916 0 1 1-15.833 0 7.916 7.916 0 0 1 15.833 0Zm-6.804.01 3.032-3.033a.792.792 0 1 0-1.12-1.12L8.494 8.473 5.46 5.44a.792.792 0 0 0-1.12 1.12l3.033 3.033-3.032 3.033a.791.791 0 1 0 1.12 1.119l3.032-3.033 3.033 3.033a.79.79 0 0 0 1.12 0c.309-.31.309-.81 0-1.12L9.612 9.594Z"></path></svg>
                                            </span>
                                            Projected first-year salary is
                                            lower than total student debt
                                        </p>
                                        <p class="cf-notification__text
                                        metric__notification__text--no-you">
                                            We currently don’t have salary data
                                            to display for your school
                                        </p>
                                        <p class="cf-notification__text
                                        metric__notification__text--no-data">
                                            We currently don’t have salary data
                                            to display
                                        </p>
                                    </div>
                                </div>
                            </section>
                        </div>
                    </section>
                    <section class="criteria column-well__wrapper">
                        <h3 class="criteria__heading">
                            How much will I pay per month for all of my student loans?
                        </h3>
                        <div class="criteria__wrapper">
                            <div class="criteria__intro">
                                <p>
                                  Currently, your projected monthly student loan
                                  payment is <span id="criteria__loan-monthly" data-financial="loanMonthly">$562</span>,
                                  based on standard loan terms of <span data-financial="repaymentTerm" data-currency="false">10</span> years. Once
                                  you leave school, you are able to choose one
                                  of <a class="a-link" href="https://studentaid.gov/manage-loans/repayment/plans" rel="noopener noreferrer" target="__blank"><span class="a-link__text">several
                                  different repayment options for your federal
                                  loans</span> <svg class="cf-icon-svg cf-icon-svg--external-link" viewBox="0 0 14 19" xmlns="http://www.w3.org/2000/svg"><path d="M13.017 3.622v4.6a.554.554 0 0 1-1.108 0V4.96L9.747 7.122a1.65 1.65 0 0 1 .13.646v5.57A1.664 1.664 0 0 1 8.215 15h-5.57a1.664 1.664 0 0 1-1.662-1.663v-5.57a1.664 1.664 0 0 1 1.662-1.662h5.57A1.654 1.654 0 0 1 9 6.302l2.126-2.126H7.863a.554.554 0 1 1 0-1.108h4.6a.554.554 0 0 1 .554.554zM8.77 8.1l-2.844 2.844a.554.554 0 0 1-.784-.783l2.947-2.948H2.645a.555.555 0 0 0-.554.555v5.57a.555.555 0 0 0 .554.553h5.57a.555.555 0 0 0 .554-.554z"></path></svg></a> that may help reduce your monthly
                                  student loan payment.
                                </p>
                                <p>
                                    Tuition, certain other educational expenses,
                                    and interest paid on federal loans may
                                    qualify for a federal tax credit or
                                    deduction. As a result, when you start
                                    repaying your loans, you may be able to
                                    <a class="a-link" href="https://www.irs.gov/newsroom/tax-benefits-for-education-information-center" rel="noopener noreferrer" target="__blank"><span class="a-link__text">reduce your
                                    federal tax burden</span> <svg class="cf-icon-svg cf-icon-svg--external-link" viewBox="0 0 14 19" xmlns="http://www.w3.org/2000/svg"><path d="M13.017 3.622v4.6a.554.554 0 0 1-1.108 0V4.96L9.747 7.122a1.65 1.65 0 0 1 .13.646v5.57A1.664 1.664 0 0 1 8.215 15h-5.57a1.664 1.664 0 0 1-1.662-1.663v-5.57a1.664 1.664 0 0 1 1.662-1.662h5.57A1.654 1.654 0 0 1 9 6.302l2.126-2.126H7.863a.554.554 0 1 1 0-1.108h4.6a.554.554 0 0 1 .554.554zM8.77 8.1l-2.844 2.844a.554.554 0 0 1-.784-.783l2.947-2.948H2.645a.555.555 0 0 0-.554.555v5.57a.555.555 0 0 0 .554.553h5.57a.555.555 0 0 0 .554-.554z"></path></svg></a>. Please consult with
                                    your tax advisor.
                                </p>
                                <p>
                                  Many of these alternative repayment plans are
                                  based on income and family size, which means
                                  the lower your salary, the lower your student
                                  loan payment. For instance, if you have a
                                  family of four with an annual income of
                                  $50,000, a monthly student loan payment would
                                  be set at $114. Depending on your income
                                  and family size it could be as low as $0. If
                                  you select one of these income based repayment
                                  plans you may be paying off your loans for up
                                  to of 20 to 25 years.
                                </p>
                                <p data-term-toggle="repaymentContent__30KFederalLoans" style="display: none;">
                                  Another payment option extends your
                                  repayment over 25 years, which means you
                                  would have a lower monthly student loan
                                  payment but a higher total cost of interest
                                  over the life of the loan.
                                </p>
                                <p>
                                  These repayment plans typically aren’t
                                  available for private student loans. If
                                  you’re still not able to make payments on
                                  your loans, you could go into default.
                                </p>
                            </div>
                            <section class="metric salary-and-debt
                            column-well column-well--bleed
                            column-well--not-stacked" data-repayment-section="monthly-payment">
                                <div class="column-well__content">
                                    <h4 class="metric__heading repaymentContent">
                                        Your estimated monthly payment
                                    </h4>
                                    <p class="metric__explanation
                                    repaymentContent">
                                        Based on a standard loan term of 10
                                        years
                                    </p>
                                    <h4 class="metric__heading" data-term-toggle="repaymentContent__30KFederalLoans" style="display: none;">
                                        Calculate your monthly payment
                                    </h4>
                                    <p data-term-toggle="repaymentContent__30KFederalLoans" style="display: none;">
                                        Once you leave school, you can choose
                                        one of several available repayment
                                        options.
                                    </p>
                                    <div class="salary-and-debt__projection">
                                        <div class="salary-and-debt__projection-name">
                                         Your projected loan payment
                                        </div>
                                        <div class="salary-and-debt__projection-value">
                                            <span data-financial="loanMonthly">$562</span>
                                        </div>
                                    </div>
                                    <div class="salary-and-debt__projection">
                                        <div class="salary-and-debt__projection-name">
                                          Total cost of repayment with interest
                                          and fees
                                        </div>
                                        <div class="salary-and-debt__projection-value">
                                            <span data-financial="loanLifetime">$25,412</span>
                                      </div>
                                    </div>
                                    <div data-term-toggle="debtBurden" style="display: none;">
                                      <p>
                                        See how loan length affects your
                                        payments
                                      </p>
                                      <div class="salary-and-debt__payment-term" id="monthly-payment__term">
                                        <label for="monthly-payment__term_10">
                                          <input id="monthly-payment__term_10" type="radio" name="monthly-payment__term" value="10" checked=""> 10 years
                                        </label>
                                        <label for="monthly-payment__term_25">
                                          <input id="monthly-payment__term_25" type="radio" name="monthly-payment__term" value="25">
                                          25 years
                                        </label>
                                      </div>
                                    </div>
                                    <div>
                                        <p>
                                          <a class="a-link" href="https://studentaid.gov/manage-loans/repayment/plans" rel="noopener noreferrer" target="__blank"><span class="a-link__text">
                                            Learn about other federal repayment options
                                          </span> <svg class="cf-icon-svg cf-icon-svg--external-link" viewBox="0 0 14 19" xmlns="http://www.w3.org/2000/svg"><path d="M13.017 3.622v4.6a.554.554 0 0 1-1.108 0V4.96L9.747 7.122a1.65 1.65 0 0 1 .13.646v5.57A1.664 1.664 0 0 1 8.215 15h-5.57a1.664 1.664 0 0 1-1.662-1.663v-5.57a1.664 1.664 0 0 1 1.662-1.662h5.57A1.654 1.654 0 0 1 9 6.302l2.126-2.126H7.863a.554.554 0 1 1 0-1.108h4.6a.554.554 0 0 1 .554.554zM8.77 8.1l-2.844 2.844a.554.554 0 0 1-.784-.783l2.947-2.948H2.645a.555.555 0 0 0-.554.555v5.57a.555.555 0 0 0 .554.553h5.57a.555.555 0 0 0 .554-.554z"></path></svg></a>
                                        </p>
                                    </div>
                                </div>
                            </section>
                        </div>
                    </section>
                    <section class="criteria
                    column-well__wrapper--overflow-small">
                        <h3 class="criteria__heading">
                            How will I afford my loan payment?
                        </h3>
                        <div class="criteria__wrapper">
                            <div class="criteria__intro">
                                <p>
                                    Think about how much money you can expect to
                                    make if you graduate and get a job in your
                                    field, and then evaluate how much of that
                                    will go toward living expenses and loan
                                    payments. In reality, you could end up
                                    making more or less than the salaries shown here.
                                </p>
                                <p class="content__job-placement" id="criteria__job-placement-content" style="display: none;">
                                    Keep in mind your school has a <a href="/paying-for-college2/understanding-your-financial-aid-offer/about-this-tool/#job-placement-rate" target="__blank" rel="noopener noreferrer">job
                                    placement rate</a> of <span id="criteria__job-placement-rate" data-financial="jobRate" data-percentage_value="true">0</span>%
                                    for students who graduate and get a job in
                                    their field of study within six months of
                                    graduating.
                                </p>
                            </div>
                            <section class="metric debt-burden column-well
                              column-well--bleed column-well--not-stacked" data-repayment-section="debt-burden">
                                  <div class="column-well__content">
                                      <h4 class="metric__heading">
                                          Your estimated debt burden
                                      </h4>
                                      <p class="metric__explanation">
                                          We calculate your debt burden by
                                          dividing your monthly loan payment by
                                          the average <span id="content__debt-burden-salary">salary
                                          for students who attended your
                                          school</span>.
                                      </p>
                                      <div class="debt-burden__projection">
                                          <div class="debt-burden__projection-name">
                                              Your projected loan payment
                                          </div>
                                          <div class="debt-burden__projection-value">
                                              <span data-debt-burden="loanMonthly">$562</span>
                                              / mo.
                                          </div>
                                      </div>
                                      <div class="debt-burden__projection">
                                          <div class="debt-burden__projection-name">
                                              Average salary
                                          </div>
                                          <div class="debt-burden__projection-value">
                                              <span data-debt-burden="annualSalary">$33,400</span>
                                              / yr.<br>
                                              <span data-debt-burden="monthlySalary">$2,783</span>
                                              / mo.
                                          </div>
                                      </div>
                                      <div class="debt-equation u-clearfix">
                                          <div class="debt-equation__part
                                          debt-equation__part--loan">
                                              <div class="debt-equation__number">
                                                  <span data-debt-burden="loanMonthly">$562</span>
                                              </div>
                                              <div class="debt-equation__label">
                                                  loan payment
                                              </div>
                                          </div>
                                          <div class="debt-equation__symbol">
                                              /
                                          </div>
                                          <div class="debt-equation__part
                                          debt-equation__part--income">
                                              <div class="debt-equation__number">
                                                  <span data-debt-burden="monthlySalary">$2,783</span>
                                              </div>
                                              <div class="debt-equation__label">
                                                  monthly salary
                                              </div>
                                          </div>
                                          <div class="debt-equation__symbol">
                                              =
                                          </div>
                                          <div class="debt-equation__part
                                          debt-equation__part--percent">
                                              <div class="debt-equation__number">
                                                  <span data-debt-burden="debtBurden">20%</span>
                                              </div>
                                              <div class="debt-equation__label">
                                                  of your income
                                              </div>
                                          </div>
                                      </div>
                                      <div class="metric__notification" data-better-direction="lower" style="display: none;">
                                          <p class="cf-notification__text
                                          metric__notification__text--better">
                                              Loan payment is lower than
                                              recommended 8% of salary
                                          </p>
                                          <p class="cf-notification__text
                                          metric__notification__text--same">
                                              Loan payment is equal to
                                              recommended 8% of salary
                                          </p>
                                          <p class="cf-notification__text
                                          metric__notification__text--worse">
                                            <span class="cf-notification__icon
                                                         cf-notification__icon--error">
                                                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 17 19" class="cf-icon-svg cf-icon-svg--error-round"><path d="M16.417 9.583a7.916 7.916 0 1 1-15.833 0 7.916 7.916 0 0 1 15.833 0Zm-6.804.01 3.032-3.033a.792.792 0 1 0-1.12-1.12L8.494 8.473 5.46 5.44a.792.792 0 0 0-1.12 1.12l3.033 3.033-3.032 3.033a.791.791 0 1 0 1.12 1.119l3.032-3.033 3.033 3.033a.79.79 0 0 0 1.12 0c.309-.31.309-.81 0-1.12L9.612 9.594Z"></path></svg>
                                            </span>
                                              Loan payment is higher than
                                              recommended 8% of salary
                                          </p>
                                      </div>
                                      <div class="debt-burden__payment-term" id="estimated-debt-burden__term" data-repayment-section="estimated-debt-burden" data-term-toggle="debtBurden" style="display: none;">
                                      <p>
                                        See how loan length affects your debt
                                        burden
                                      </p>
                                        <label for="estimated-debt-burden_term_10">
                                          <input id="estimated-debt-burden_term_10" type="radio" name="estimated-debt-burden__term" value="10" checked=""> 10 years
                                        </label>
                                        <label for="estimated-debt-burden_term_25">
                                          <input id="estimated-debt-burden_term_25" type="radio" name="estimated-debt-burden__term" value="25">
                                          25 years
                                        </label>
                                      </div>
                                  </div>
                              </section>
                            <section class="estimated-expenses">
                                <form class="aid-form" action="#">
                                    <div class="aid-form__heading">
                                        <h4 class="aid-form__title">
                                            Estimated budget after you leave
                                            school (adjust as needed)
                                        </h4>
                                        <p>
                                            Average monthly living expenses for
                                            someone and their family making
                                            <span data-financial="medianSalary">$33,400</span>/year <span id="content__expenses-nat-salary">
                                            (the average national salary for all
                                            students who attended
                                            college)</span> in the region you
                                            plan to live (Source: <a class="a-link" href="http://www.bls.gov/cex/" rel="noopener noreferrer" target="__blank"><span class="a-link__text">Bureau of Labor
                                            Statistics</span> <svg class="cf-icon-svg cf-icon-svg--external-link" viewBox="0 0 14 19" xmlns="http://www.w3.org/2000/svg"><path d="M13.017 3.622v4.6a.554.554 0 0 1-1.108 0V4.96L9.747 7.122a1.65 1.65 0 0 1 .13.646v5.57A1.664 1.664 0 0 1 8.215 15h-5.57a1.664 1.664 0 0 1-1.662-1.663v-5.57a1.664 1.664 0 0 1 1.662-1.662h5.57A1.654 1.654 0 0 1 9 6.302l2.126-2.126H7.863a.554.554 0 1 1 0-1.108h4.6a.554.554 0 0 1 .554.554zM8.77 8.1l-2.844 2.844a.554.554 0 0 1-.784-.783l2.947-2.948H2.645a.555.555 0 0 0-.554.555v5.57a.555.555 0 0 0 .554.553h5.57a.555.555 0 0 0 .554-.554z"></path></svg></a>). Your expenses may
                                            be higher or lower.
                                        </p>
                                        <div class="estimated-expenses__region">
                                            <div class="a-select">
                                              <select id="bls-region-select">
                                                <option value="WE">West region</option>
                                                <option value="SO">South region</option>
                                                <option value="NE">Northeast region</option>
                                                <option value="MW">Midwest region</option>
                                              </select>
                                            </div>
                                        </div>
                                    </div>
                                    <div class="line-item">
                                        <div class="line-item__title">
                                            Average monthly salary
                                            <span class="line-item__explanation">
                                                Before taxes
                                            </span>
                                        </div>
                                        <div class="line-item__value">
                                            <span class="line-item__currency" style="">
                                                $
                                            </span>
                                            <span class="line-item__amount" data-line-item="true" data-financial="monthlySalary" id="summary__monthly-salary">2,783</span>
                                        </div>
                                    </div>
                                    <div class="line-item">
                                        <div class="line-item__title">
                                            Monthly student loan payment
                                            <span class="line-item__explanation">
                                                Based on <span data-financial="repaymentTerm" data-currency="false">10</span>-year repayment plan
                                            </span>
                                        </div>
                                        <div class="line-item__value">
                                            <span class="line-item__sign" style="">
                                                ( − )
                                            </span>
                                            <span class="line-item__currency" style="">
                                                $
                                            </span>
                                            <span class="line-item__amount" data-line-item="true" data-financial="loanMonthly">562</span>
                                        </div>
                                    </div>
                                    <div class="form-group__item">
                                        <label class="form-label--wrapped">
                                            <span class="form-label__text-wrapper">
                                                Housing
                                                <span class="line-item__explanation">
                                                    Includes utilities, cell
                                                    phone
                                                </span>
                                            </span>
                                            <span class="aid-form__input-wrapper">
                                                <span class="aid-form__sign">
                                                    ( − )
                                                </span>
                                                <input class="aid-form__input
                                                aid-form__input--currency" type="text" id="expenses--rent" name="expenses--rent" data-expenses="housing" autocorrect="off" value="0">
                                            </span>
                                        </label>
                                    </div>
                                    <div class="form-group__item">
                                        <label class="form-label--wrapped">
                                            <span class="form-label__text-wrapper">
                                                Food
                                            </span>
                                            <span class="aid-form__input-wrapper">
                                                <span class="aid-form__sign">
                                                    ( − )
                                                </span>
                                                <input class="aid-form__input
                                                aid-form__input--currency" type="text" id="expenses--food" name="expenses--food" data-expenses="food" autocorrect="off" value="0">
                                            </span>
                                        </label>
                                    </div>
                                    <div class="form-group__item">
                                        <label class="form-label--wrapped">
                                            <span class="form-label__text-wrapper">
                                                Clothing
                                            </span>
                                            <span class="aid-form__input-wrapper">
                                                <span class="aid-form__sign">
                                                    ( − )
                                                </span>
                                                <input class="aid-form__input
                                                aid-form__input--currency" type="text" id="expenses--clothing" name="expenses--clothing" data-expenses="clothing" autocorrect="off" value="0">
                                            </span>
                                        </label>
                                    </div>
                                    <div class="form-group__item">
                                        <label class="form-label--wrapped">
                                            <span class="form-label__text-wrapper">
                                                Transportation
                                            </span>
                                            <span class="aid-form__input-wrapper">
                                                <span class="aid-form__sign">
                                                    ( − )
                                                </span>
                                                <input class="aid-form__input
                                                aid-form__input--currency" type="text" id="expenses--transportation" name="expenses--transportation" data-expenses="transportation" autocorrect="off" value="0">
                                            </span>
                                        </label>
                                    </div>
                                    <div class="form-group__item">
                                        <label class="form-label--wrapped">
                                            <span class="form-label__text-wrapper">
                                                Healthcare
                                            </span>
                                            <span class="aid-form__input-wrapper">
                                                <span class="aid-form__sign">
                                                    ( − )
                                                </span>
                                                <input class="aid-form__input
                                                aid-form__input--currency" type="text" id="expenses--healthcare" name="expenses--healthcare" data-expenses="healthcare" autocorrect="off" value="0">
                                            </span>
                                        </label>
                                    </div>
                                    <div class="form-group__item">
                                        <label class="form-label--wrapped">
                                            <span class="form-label__text-wrapper">
                                                Entertainment
                                            </span>
                                            <span class="aid-form__input-wrapper">
                                                <span class="aid-form__sign">
                                                    ( − )
                                                </span>
                                                <input class="aid-form__input
                                                aid-form__input--currency" type="text" id="expenses--entertainment" name="expenses--entertainment" data-expenses="entertainment" autocorrect="off" value="0">
                                            </span>
                                        </label>
                                    </div>
                                    <div class="form-group__item">
                                        <label class="form-label--wrapped">
                                            <span class="form-label__text-wrapper">
                                                Retirement and savings
                                            </span>
                                            <span class="aid-form__input-wrapper">
                                                <span class="aid-form__sign">
                                                    ( − )
                                                </span>
                                                <input class="aid-form__input
                                                aid-form__input--currency" type="text" id="expenses--retirement" name="expenses--retirement" data-expenses="retirement" autocorrect="off" value="0">
                                            </span>
                                        </label>
                                    </div>
                                    <div class="form-group__item">
                                        <label class="form-label--wrapped">
                                            <span class="form-label__text-wrapper">
                                                Taxes
                                                <span class="line-item__explanation">
                                                    Federal, state, local
                                                </span>
                                            </span>
                                            <span class="aid-form__input-wrapper">
                                                <span class="aid-form__sign">
                                                    ( − )
                                                </span>
                                                <input class="aid-form__input
                                                aid-form__input--currency" type="text" id="expenses--taxes" name="expenses--taxes" data-expenses="taxes" autocorrect="off" value="0">
                                            </span>
                                        </label>
                                    </div>
                                    <div class="form-group__item">
                                        <label class="form-label--wrapped">
                                            <span class="form-label__text-wrapper">
                                                Other
                                            </span>
                                            <span class="aid-form__input-wrapper">
                                                <span class="aid-form__sign">
                                                    ( − )
                                                </span>
                                                <input class="aid-form__input
                                                aid-form__input--currency" type="text" id="expenses--other" name="expenses--other" data-expenses="other" autocorrect="off" value="0">
                                            </span>
                                        </label>
                                    </div>
                                </form>
                                <div class="aid-form__summary">
                                    <div class="content__line
                                    aid-form__equals-line"></div>
                                    <div class="line-item line-item--total">
                                        <div class="line-item__title">
                                            Total left at the end of the month
                                        </div>
                                        <div class="line-item__value">
                                            <span class="line-item__amount" data-currency="true" data-line-item="true" data-expenses="monthlyLeftover" id="summary__monthly-left-over">-$756</span>
                                        </div>
                                    </div>
                                    <div class="aid-form--higher-expenses">
                                        Your total expenses are higher than your
                                        estimated monthly salary
                                    </div>
                                </div>
                            </section>
                        </div>
                    </section>
                    <section class="criteria column-well__wrapper">
                        <h3 class="criteria__heading">
                            What if I can’t afford my student loan payments?
                        </h3>
                        <div class="criteria__wrapper">
                            <div class="criteria__intro">
                                <p>
                                    Defaulting on a loan can happen when you
                                    fail to make scheduled payments over a
                                    certain period of time. This length of time
                                    can vary based on the type of loan. It can
                                    also mean added fees and interest because
                                    the debt isn’t paid off in time. Defaulting
                                    on a loan can negatively impact your credit
                                    rating, which could make it more difficult
                                    in the future to borrow money to purchase a
                                    car or a home. Defaulting could also result
                                    in wage garnishment.
                                </p>
                            </div>
                            <section class="metric loan-default-rates
                            column-well column-well--bleed
                            column-well--not-stacked">
                                <div class="column-well__content">
                                    <h4 class="metric__heading">
                                        Loan default rates
                                    </h4>
                                    <p class="metric__explanation">
                                        Percentage of students from this
                                        <span class="content-default-program">program</span>
                                        who default on loans after
                                        entering repayment
                                    </p>
                                    <div class="bar-graph bar-graph--missing-average" data-metric="defaultRate" data-national-metric="loanDefaultRate" data-incoming-format="decimal-percent" data-graph-min="0" data-graph-max="0.4">
                                        <div class="bar-graph__top-label">
                                            40%
                                        </div>
                                        <div class="bar-graph__bar"></div>
                                        <div class="bar-graph__point
                                        bar-graph__point--you u-clearfix" style="bottom: 20px;">
                                            <div class="bar-graph__label" data-graph_label="defaultRate">This program</div>
                                            <div class="bar-graph__line"></div>
                                            <div class="bar-graph__value">
                                                <div data-bar-graph_number="you" class="bar-graph__number">0%</div>
                                            </div>
                                        </div>
                                        <div class="bar-graph__point
                                        bar-graph__point--average u-clearfix" style="display: none;">
                                            <div class="bar-graph__label">
                                                National average
                                            </div>
                                            <div class="bar-graph__line"></div>
                                            <div class="bar-graph__value">
                                                <div data-bar-graph_number="average" class="bar-graph__number"></div>
                                            </div>
                                        </div>
                                    </div>
                                    <div class="metric__notification cf-notification metric__notification--no-average cf-notification--warning" data-better-direction="lower" style="display: none;">
                                        <p class="cf-notification__text
                                        metric__notification__text--better">
                                            Lower default rate than national
                                            average
                                        </p>
                                        <p class="cf-notification__text
                                        metric__notification__text--same">
                                            The same default rate as
                                            national average
                                        </p>
                                        <p class="cf-notification__text
                                        metric__notification__text--worse">
                                            <span class="cf-notification__icon
                                                         cf-notification__icon--error">
                                                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 17 19" class="cf-icon-svg cf-icon-svg--error-round"><path d="M16.417 9.583a7.916 7.916 0 1 1-15.833 0 7.916 7.916 0 0 1 15.833 0Zm-6.804.01 3.032-3.033a.792.792 0 1 0-1.12-1.12L8.494 8.473 5.46 5.44a.792.792 0 0 0-1.12 1.12l3.033 3.033-3.032 3.033a.791.791 0 1 0 1.12 1.119l3.032-3.033 3.033 3.033a.79.79 0 0 0 1.12 0c.309-.31.309-.81 0-1.12L9.612 9.594Z"></path></svg>
                                            </span>
                                            Higher default rate than national
                                            average
                                        </p>
                                        <p class="cf-notification__text
                                        metric__notification__text--no-you">
                                            We currently don’t have data to
                                            display for your school
                                        </p>
                                        <p class="cf-notification__text
                                        metric__notification__text--no-average">
                                            We currently don’t have national
                                            average data to display
                                        </p>
                                        <p class="cf-notification__text
                                        metric__notification__text--no-data">
                                            We currently don’t have data to
                                            display
                                        </p>
                                    </div>
                                    <div class="metric__link">
                                        <p>
                                            <a href="http://nces.ed.gov/collegenavigator/?id=133465#fedloans" target="__blank" rel="noopener noreferrer" class="loan-default-link a-link">See
                                            the loan default rates for the
                                            entire school </a>
                                        </p>
                                    </div>
                                </div>
                            </section>
                        </div>
                    </section>
                </div>
            </section>
            <section class="question step">
                <div class="wrapper">
                    <div class="content__main">
                        <div class="question__wrapper">
                            <div class="question__content">
                                <h2 class="step__heading step--settlement">
                                    It's estimated you'll owe <span data-financial="loanLifetime">$25,412</span>
                                    to complete this program in Physician Assistant at
                                    South University-West Palm Beach. Do you better
                                    understand how this may impact your future
                                    finances?
                                </h2>
                                <h2 class="step__heading step--nonsettlement" style="display: none;">
                                    Do you feel like going into <span data-financial="loanLifetime">$25,412</span>
                                    of debt to attend this school is a good
                                    investment in your future?
                                </h2>
                                <div class="question--answers m-btn-group">
                                    <button class="a-btn" id="question--answer-no" name="question--answer-no" type="button" style="display: none;">
                                        No
                                    </button>
                                    <button class="a-btn" id="question--answer-yes" name="question--answer-yes" type="button">
                                        Yes
                                    </button>
                                    <button class="a-btn" id="question--answer-not-sure" name="question--answer-not-sure" type="button" data-gtm_ignore="true">
                                        Not sure
                                    </button>
                                </div>
                                <p>
                                    Your response will not be shared with your
                                    school and does not affect your ability to
                                    accept or reject the actual offer from your
                                    school.
                                </p>
                            </div>
                        </div>
                    </div>
                </div>
            </section>
            <section class="get-options step wrapper
            column-well__wrapper">
                <div class="content__main">
                    <div class="get-options__wrapper">
                        <div class="get-options__intro followup--no-not-sure">
                            <h2 class="step__heading">
                                Step 3: Consider your options
                            </h2>
                            <p class="step__intro">
                                If you are interested in lowering your amount of
                                debt, there are things you can do. Here are some
                                choices you can make that may help you improve
                                your financial future.
                            </p>
                        </div>
                        <div class="get-options__intro followup--yes">
                            <h2 class="step__heading">
                                Step 3: A few more things to consider
                            </h2>
                            <p class="step__intro">
                                It’s important to feel confident in the
                                financial decisions you are making. Here are
                                some additional choices you can make that may
                                help you improve your financial future even
                                more.
                            </p>
                        </div>
                        <div class="get-options__intro followup--settlement
                        step--settlement">
                            <h2 class="step__heading">
                                Step 3: Consider your options
                            </h2>
                            <p class="step__intro">
                                If you are interested in lowering your amount of
                                debt, there are things you can do.
                            </p>
                            <p class="step__intro">
                                Here are some choices you can make that may help
                                you improve your financial future.
                            </p>
                        </div>
                    </div>
                    <div class="get-options__wrapper">
                        <div class="get-options--settlement content__main">
                            <section class="option option--maximize-grants option--settlement">
                                <h3 class="option__heading">
                                    Maximize all available grants and scholarships.
                                </h3>
                                <p>
                                    Consider applying for <a class="a-link" href="https://studentaid.gov/understand-aid/types/grants" rel="noopener noreferrer" target="__blank"><span class="a-link__text">additional
                                    scholarships and grants</span> <svg class="cf-icon-svg cf-icon-svg--external-link" viewBox="0 0 14 19" xmlns="http://www.w3.org/2000/svg"><path d="M13.017 3.622v4.6a.554.554 0 0 1-1.108 0V4.96L9.747 7.122a1.65 1.65 0 0 1 .13.646v5.57A1.664 1.664 0 0 1 8.215 15h-5.57a1.664 1.664 0 0 1-1.662-1.663v-5.57a1.664 1.664 0 0 1 1.662-1.662h5.57A1.654 1.654 0 0 1 9 6.302l2.126-2.126H7.863a.554.554 0 1 1 0-1.108h4.6a.554.554 0 0 1 .554.554zM8.77 8.1l-2.844 2.844a.554.554 0 0 1-.784-.783l2.947-2.948H2.645a.555.555 0 0 0-.554.555v5.57a.555.555 0 0 0 .554.553h5.57a.555.555 0 0 0 .554-.554z"></path></svg></a>,
                                    which provide money you don’t have to repay.
                                    By increasing the amount of this type of
                                    aid, you can decrease the overall amount of
                                    debt you have to borrow—and
                                    consequently pay back.
                                </p>
                            </section>
                            <section class="option option--reduce-costs option--settlement">
                                <h3 class="option__heading">
                                    Reduce your living costs.
                                </h3>
                                <p>
                                    Living at home or finding cheaper off-campus
                                    housing can
                                    <a class="a-link" href="https://studentaid.gov/resources/prepare-for-college/students/choosing-schools/consider-costs#how-can-i" rel="noopener noreferrer" target="__blank"><span class="a-link__text">reduce the
                                    cost of attendance</span> <svg class="cf-icon-svg cf-icon-svg--external-link" viewBox="0 0 14 19" xmlns="http://www.w3.org/2000/svg"><path d="M13.017 3.622v4.6a.554.554 0 0 1-1.108 0V4.96L9.747 7.122a1.65 1.65 0 0 1 .13.646v5.57A1.664 1.664 0 0 1 8.215 15h-5.57a1.664 1.664 0 0 1-1.662-1.663v-5.57a1.664 1.664 0 0 1 1.662-1.662h5.57A1.654 1.654 0 0 1 9 6.302l2.126-2.126H7.863a.554.554 0 1 1 0-1.108h4.6a.554.554 0 0 1 .554.554zM8.77 8.1l-2.844 2.844a.554.554 0 0 1-.784-.783l2.947-2.948H2.645a.555.555 0 0 0-.554.555v5.57a.555.555 0 0 0 .554.553h5.57a.555.555 0 0 0 .554-.554z"></path></svg></a>, meaning you can
                                    borrow less money overall.
                                </p>
                            </section>
                            <section class="option option--different-program option--settlement">
                                <h3 class="option__heading">
                                    Consider a different program with better
                                    outcomes.
                                </h3>
                                <p>
                                    Salaries are often influenced by the degree
                                    you earn. If the projected salary of your
                                    program is far below the national average or
                                    the job placement rate seems low, you might
                                    consider a different program with a higher
                                    projected earning potential. Ask your
                                    admission representative or search for
                                    gainful employment information on your <a href="https://www.southuniversity.edu/west-palm-beach#location=West%20Palm%20Beach,%20FL" target="__blank" rel="noopener noreferrer" class="school-link">school’s website</a>
                                    to learn more about job placement rates and
                                    the average salaries of graduates.
                                </p>
                            </section>


                            <section class="option option--work-while-studying option--settlement">
                                <h3 class="option__heading">
                                    Think about working while you study.
                                </h3>
                                <p>
                                    Nearly two-thirds of college students work
                                    while they are enrolled in school. While not
                                    for everyone, earning money from a job, even
                                    if it’s not related to your field of study,
                                    can help reduce the amount of money you need
                                    to borrow to pay for school, resulting in
                                    long-term benefits of reducing overall debt.
                                    Check out <a class="a-link" href="https://www.careeronestop.org/jobsearch/job-search.aspx" rel="noopener noreferrer" target="__blank"><span class="a-link__text">resources for finding a
                                    job</span> <svg class="cf-icon-svg cf-icon-svg--external-link" viewBox="0 0 14 19" xmlns="http://www.w3.org/2000/svg"><path d="M13.017 3.622v4.6a.554.554 0 0 1-1.108 0V4.96L9.747 7.122a1.65 1.65 0 0 1 .13.646v5.57A1.664 1.664 0 0 1 8.215 15h-5.57a1.664 1.664 0 0 1-1.662-1.663v-5.57a1.664 1.664 0 0 1 1.662-1.662h5.57A1.654 1.654 0 0 1 9 6.302l2.126-2.126H7.863a.554.554 0 1 1 0-1.108h4.6a.554.554 0 0 1 .554.554zM8.77 8.1l-2.844 2.844a.554.554 0 0 1-.784-.783l2.947-2.948H2.645a.555.555 0 0 0-.554.555v5.57a.555.555 0 0 0 .554.553h5.57a.555.555 0 0 0 .554-.554z"></path></svg></a>, including links to job search
                                    sites, tips for writing a
                                    résumé, and more.
                                </p>
                            </section>
                        </div>
                        <aside class="get-options--sidebar
                                      column-well
                                      column-well--emphasis
                                      content__sidebar">
                            <div class="column-well__content">
                                <h3 class="option--take-action-header">
                                    What you can do
                                </h3>
                                <p>
                                    You can adjust some of the offer amounts
                                    in the tool using some of the strategies
                                    outlined above. For instance, you can
                                    try reducing the amount of federal or
                                    private loans to see how it affects your
                                    overall debt and you can try reducing
                                    your out-of-school expenses.
                                </p>
                                <p>
                                    Changing amounts in this tool has no
                                    effect on what financial aid is
                                    actually being offered. If you want to
                                    move forward with different amounts,
                                    you will need to contact your school’s
                                    financial aid representative to have
                                    your financial aid package updated.
                                </p>
                                <h4>
                                    Useful resources for new
                                    college students
                                </h4>
                                <div>
                                    <a class="a-link" href="https://collegescorecard.ed.gov" rel="noopener noreferrer" target="__blank"><span class="a-link__text">College
                                    Scorecard</span> <svg class="cf-icon-svg cf-icon-svg--external-link" viewBox="0 0 14 19" xmlns="http://www.w3.org/2000/svg"><path d="M13.017 3.622v4.6a.554.554 0 0 1-1.108 0V4.96L9.747 7.122a1.65 1.65 0 0 1 .13.646v5.57A1.664 1.664 0 0 1 8.215 15h-5.57a1.664 1.664 0 0 1-1.662-1.663v-5.57a1.664 1.664 0 0 1 1.662-1.662h5.57A1.654 1.654 0 0 1 9 6.302l2.126-2.126H7.863a.554.554 0 1 1 0-1.108h4.6a.554.554 0 0 1 .554.554zM8.77 8.1l-2.844 2.844a.554.554 0 0 1-.784-.783l2.947-2.948H2.645a.555.555 0 0 0-.554.555v5.57a.555.555 0 0 0 .554.553h5.57a.555.555 0 0 0 .554-.554z"></path></svg></a>
                                    <p>Compare <a href="https://collegescorecard.ed.gov/school/?133465" target="__blank" rel="noopener noreferrer" class="scorecard-school a-link">your
                                        school </a>’s annual costs,
                                        graduation rates, and post-college
                                        earnings.</p>
                                </div>
                                <p>
                                    <a class="a-link" href="https://www.consumer.ftc.gov/articles/0395-choosing-college-questions-ask" rel="noopener noreferrer" target="__blank"><span class="a-link__text">Questions to ask
                                        your college</span> <svg class="cf-icon-svg cf-icon-svg--external-link" viewBox="0 0 14 19" xmlns="http://www.w3.org/2000/svg"><path d="M13.017 3.622v4.6a.554.554 0 0 1-1.108 0V4.96L9.747 7.122a1.65 1.65 0 0 1 .13.646v5.57A1.664 1.664 0 0 1 8.215 15h-5.57a1.664 1.664 0 0 1-1.662-1.663v-5.57a1.664 1.664 0 0 1 1.662-1.662h5.57A1.654 1.654 0 0 1 9 6.302l2.126-2.126H7.863a.554.554 0 1 1 0-1.108h4.6a.554.554 0 0 1 .554.554zM8.77 8.1l-2.844 2.844a.554.554 0 0 1-.784-.783l2.947-2.948H2.645a.555.555 0 0 0-.554.555v5.57a.555.555 0 0 0 .554.553h5.57a.555.555 0 0 0 .554-.554z"></path></svg></a>
                                </p>
                                <div>
                                    <a class="a-link" href="https://studentaid.gov/h/apply-for-aid/fafsa" rel="noopener noreferrer" target="__blank"><span class="a-link__text">FAFSA®</span> <svg class="cf-icon-svg cf-icon-svg--external-link" viewBox="0 0 14 19" xmlns="http://www.w3.org/2000/svg"><path d="M13.017 3.622v4.6a.554.554 0 0 1-1.108 0V4.96L9.747 7.122a1.65 1.65 0 0 1 .13.646v5.57A1.664 1.664 0 0 1 8.215 15h-5.57a1.664 1.664 0 0 1-1.662-1.663v-5.57a1.664 1.664 0 0 1 1.662-1.662h5.57A1.654 1.654 0 0 1 9 6.302l2.126-2.126H7.863a.554.554 0 1 1 0-1.108h4.6a.554.554 0 0 1 .554.554zM8.77 8.1l-2.844 2.844a.554.554 0 0 1-.784-.783l2.947-2.948H2.645a.555.555 0 0 0-.554.555v5.57a.555.555 0 0 0 .554.553h5.57a.555.555 0 0 0 .554-.554z"></path></svg></a>
                                    <p>Apply for federal, state, and school
                                        financial aid.</p>
                                </div>
                                <div>
                                    <a href="https://www.consumerfinance.gov/paying-for-college/choose-a-student-loan/" target="__blank" rel="noopener noreferrer">Student
                                    loan guide</a>
                                    <p>Choose a student loan that’s right
                                        for you.</p>
                                </div>
                                <div>
                                    <a href="https://www.consumerfinance.gov/paying-for-college/manage-your-college-money/" target="__blank" rel="noopener noreferrer">Student banking guide</a>
                                    <p>Manage your college money.</p>
                                </div>
                            </div>
                        </aside>
                    </div>
                </div>
            </section>
            <section class="next-steps step wrapper">
                <div class="content__main">
                    <div class="content__line"></div>
                    <div class="next-steps__wrapper">
                        <div class="next-steps__intro">
                            <h2 class="step__heading">
                                Next steps
                            </h2>
                            <p class="step__intro">
                                We have notified your school that you have
                                reviewed your personalized offer. You can now
                                move forward in the enrollment process.
                            </p>
                        </div>
                    </div>
                    <ol class="super-numerals next-steps__list">
                        <li class="super-numerals next-steps__list-item">
                            <p class="next-steps__list-intro">
                                Review any changes you made to your offer. If
                                you decide to move forward using any adjusted
                                amount of aid, you need to contact your
                                financial aid representative and work with them
                                to update your financial aid plan.
                            </p>
                            <p>
                                Changes you make using this tool are meant for
                                your guidance only. They are not sent to your
                                school and do not affect your actual financial
                                aid offer.
                            </p>
                            <p>
                                If you want to change your offer in any way,
                                contact your school’s financial aid
                                representative to have your financial aid offer
                                updated.
                            </p>
                        </li>
                        <li class="super-numerals next-steps__list-item">
                            <p class="next-steps__list-intro">
                                Keep a copy of this personalized aid
                                information.
                            </p>
                            <p>
                                You can print a summary of the aid information
                                in this tool or save it as a PDF. Use this as a
                                reference while talking with your school.
                            </p>
                            <div class="next-steps__controls">
                                <button class="a-btn a-btn--full-on-xs" type="button" data-gtm_ignore="true">
                                    <span class="a-btn--icon--on-left">
                                        <svg xmlns="http://www.w3.org/2000/svg" class="cf-icon-svg cf-icon-svg--print" viewBox="0 0 14 19"><path d="m8.698 2.358 3.065 3.066v1.95h.16a1.112 1.112 0 0 1 1.109 1.108v4.837a1.112 1.112 0 0 1-1.109 1.108h-.16v1.726a.477.477 0 0 1-.475.475H2.712a.477.477 0 0 1-.475-.475v-1.726h-.16A1.112 1.112 0 0 1 .968 13.32V8.482a1.112 1.112 0 0 1 1.109-1.108h.16v-4.54a.476.476 0 0 1 .475-.476zm-.22 3.876a.61.61 0 0 1-.608-.608v-2.16H3.345v3.908h7.31v-1.14zm2.177 4.512h-7.31v4.773h7.31zm-1.054.874h-5.26v1.109h5.26zm0 1.962h-5.26v1.108h5.26zm2.437-4.485a.554.554 0 1 0-.554.554.554.554 0 0 0 .554-.554z"></path></svg>
                                    </span>
                                    Print
                                </button>
                            </div>
                        </li>
                    </ol>
                </div>
            </section>
        </section>
        <section id="info-wrong" class="information-wrong" tabindex="-1">
            <section class="instructions step wrapper">
                <div class="content__main">
                    <div class="instructions__wrapper">
                        <div class="instructions__content
                                    instructions__content--wrong">
                            <p>
                                If the information provided is not correct,
                                please contact your school and ask them to fix
                                it. Once your school provides you with an
                                updated link, you will be able to return so you
                                can continue reviewing the information in the
                                tool.
                            </p>
                        </div>
                    </div>
                </div>
            </section>
        </section>
    </div>
</main>`
