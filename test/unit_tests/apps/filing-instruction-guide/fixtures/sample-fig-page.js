export default `
<main class="u-layout-grid u-layout-grid--1-3 o-fig" id="main">
    <div class="u-layout-grid__wrapper">
        <div class="u-layout-grid__breadcrumbs">
            <nav class="breadcrumbs" aria-label="Breadcrumbs">
                <svg xmlns="http://www.w3.org/2000/svg" class="cf-icon-svg cf-icon-svg--left" viewBox="0 0 10 19">
                    <path d="M8.4 17.269a1.026 1.026 0 0 1-.727-.302l-6.801-6.8a1.03 1.03 0 0 1 0-1.456l6.8-6.8a1.03 1.03 0 0 1 1.456 1.455L3.055 9.439l6.073 6.073A1.03 1.03 0 0 1 8.4 17.27z"></path>
                </svg>
                <a href="/data-research/"> Data &amp; Research </a> / <a href="/data-research/small-business-lending/"> Small Business Lending Database </a> /
                <a href="/data-research/small-business-lending/filing-instructions-guide/"> Small Business Lending Rule Filing Instructions Guides </a>
            </nav>
        </div>
        <aside class="u-layout-grid__secondary-nav u-layout-grid__secondary-nav--sticky">
            <div class="o-fig__sidebar">
                <div class="u-hide-on-tablet">
                    <h3>Table of contents</h3>
                </div>
                <nav class="o-secondary-nav" aria-label="Table of contents" data-js-hook="state_atomic_init behavior_flyout-menu">
                    <button class="o-secondary-nav__header" type="button" aria-expanded="false" data-js-hook="behavior_flyout-menu_trigger">
                        <span class="o-secondary-nav__label"> Table of contents </span>
                        <span class="o-secondary-nav__cues">
                            <span class="o-secondary-nav__cue-open" aria-label="Show">
                                <svg xmlns="http://www.w3.org/2000/svg" class="cf-icon-svg cf-icon-svg__down" viewBox="0 0 17 19"><path d="M8.5 15.313a1.026 1.026 0 0 1-.728-.302l-6.8-6.8a1.03 1.03 0 0 1 1.455-1.456L8.5 12.828l6.073-6.073a1.03 1.03 0 0 1 1.455 1.456l-6.8 6.8a1.026 1.026 0 0 1-.728.302z"></path></svg>
                            </span>
                            <span class="o-secondary-nav__cue-close" aria-label="Hide">
                                <svg xmlns="http://www.w3.org/2000/svg" class="cf-icon-svg cf-icon-svg__up" viewBox="0 0 17 19"><path d="M15.3 15.32a1.026 1.026 0 0 1-.727-.302L8.5 8.946l-6.073 6.072a1.03 1.03 0 0 1-1.456-1.455l6.801-6.8a1.03 1.03 0 0 1 1.456 0l6.8 6.8a1.03 1.03 0 0 1-.727 1.757z"></path></svg>
                            </span>
                        </span>
                    </button>
                    <div class="o-secondary-nav__content u-max-height-transition u-max-height-zero" data-js-hook="behavior_flyout-menu_content" data-open="false" style="max-height: 1693px;" hidden="">
                        <div id="ctrl-f">
                            <div class="tw-relative tw-pointer-events-auto">
                                <button type="button" class="tw-border tw-border-slate-600 tw-border-solid tw-w-full md:tw-bg-white tw-flex tw-bg-white tw-mt-2.5 tw-mb-4 tw-items-center tw-text-slate-600 tw-py-1.5 tw-pl-2">
                                    <svg width="24" height="24" fill="none" aria-hidden="true" class="tw-mr-1 tw-flex-none">
                                        <path d="m19 19-3.5-3.5" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"></path>
                                        <circle cx="11" cy="11" r="6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"></circle>
                                    </svg>
                                    Search this guide
                                </button>
                            </div>
                        </div>
                        <ul class="o-secondary-nav__list o-secondary-nav__list--parents">
                            <li>
                                <a class="o-secondary-nav__link o-secondary-nav__link--parent" href="#1"> 1. What is the filing instructions guide? </a>
                            </li>
                            <li>
                                <a class="o-secondary-nav__link o-secondary-nav__link--parent" href="#2"> 2. Filing process overview </a>
                                <ul class="o-secondary-nav__list o-secondary-nav__list--children u-hide-on-desktop">
                                    <li class="m-list__item">
                                        <a class="o-secondary-nav__link" href="#2.1"> 2.1. About the small business lending platform </a>
                                    </li>
                                    <li class="m-list__item">
                                        <a class="o-secondary-nav__link" href="#2.2"> 2.2. File format </a>
                                    </li>
                                </ul>
                            </li>
                            <li>
                                <a class="o-secondary-nav__link o-secondary-nav__link--parent" href="#3"> 3. Data points </a>
                                <ul class="o-secondary-nav__list o-secondary-nav__list--children">
                                    <li class="m-list__item">
                                        <a class="o-secondary-nav__link" href="#uid"> 3.1. Unique identifier </a>
                                    </li>
                                    <li class="m-list__item">
                                        <a class="o-secondary-nav__link" href="#application-date"> 3.2. Application date </a>
                                    </li>
                                    <li class="m-list__item">
                                        <a class="o-secondary-nav__link o-secondary-nav__link--current" href="#application-method"> 3.3. Application method </a>
                                    </li>
                                    <li class="m-list__item">
                                        <a class="o-secondary-nav__link" href="#application-recipient"> 3.4. Application recipient </a>
                                    </li>
                                    <li class="m-list__item">
                                        <a class="o-secondary-nav__link" href="#credit-type"> 3.5. Credit type </a>
                                    </li>
                                    <li class="m-list__item">
                                        <a class="o-secondary-nav__link" href="#credit-purpose"> 3.6. Credit purpose </a>
                                    </li>
                                    <li class="m-list__item">
                                        <a class="o-secondary-nav__link" href="#amount-applied-for"> 3.7. Amount applied for </a>
                                    </li>
                                    <li class="m-list__item">
                                        <a class="o-secondary-nav__link" href="#amount-approved-or-originated"> 3.8. Amount approved or originated </a>
                                    </li>
                                    <li class="m-list__item">
                                        <a class="o-secondary-nav__link" href="#action-taken"> 3.9. Action taken </a>
                                    </li>
                                    <li class="m-list__item">
                                        <a class="o-secondary-nav__link" href="#action-taken-date"> 3.10. Action taken date </a>
                                    </li>
                                    <li class="m-list__item">
                                        <a class="o-secondary-nav__link" href="#denial-reasons"> 3.11. Denial reasons </a>
                                    </li>
                                    <li class="m-list__item">
                                        <a class="o-secondary-nav__link" href="#pricing-information"> 3.12. Pricing information </a>
                                    </li>
                                    <li class="m-list__item">
                                        <a class="o-secondary-nav__link" href="#census-tract"> 3.13. Census tract </a>
                                    </li>
                                    <li class="m-list__item">
                                        <a class="o-secondary-nav__link" href="#gross-annual-revenue"> 3.14. Gross annual revenue </a>
                                    </li>
                                    <li class="m-list__item">
                                        <a class="o-secondary-nav__link" href="#naics-code"> 3.15. North American Industry Classification System (NAICS) code </a>
                                    </li>
                                    <li class="m-list__item">
                                        <a class="o-secondary-nav__link" href="#number-of-workers"> 3.16. Number of workers </a>
                                    </li>
                                    <li class="m-list__item">
                                        <a class="o-secondary-nav__link" href="#time-in-business"> 3.17. Time in business </a>
                                    </li>
                                    <li class="m-list__item">
                                        <a class="o-secondary-nav__link" href="#minority-women-lgbtqi-owned-business-status"> 3.18. Minority-owned, women-owned, and LGBTQI+-owned business statuses </a>
                                    </li>
                                    <li class="m-list__item">
                                        <a class="o-secondary-nav__link" href="#number-of-principal-owners"> 3.19. Number of principal owners </a>
                                    </li>
                                    <li class="m-list__item">
                                        <a class="o-secondary-nav__link" href="#rse-of-principal-owner-1"> 3.20. Demographic information of principal owner 1 </a>
                                    </li>
                                    <li class="m-list__item">
                                        <a class="o-secondary-nav__link" href="#rse-of-principal-owner-2"> 3.21. Demographic information of principal owner 2 </a>
                                    </li>
                                    <li class="m-list__item">
                                        <a class="o-secondary-nav__link" href="#rse-of-principal-owner-3"> 3.22. Demographic information of principal owner 3 </a>
                                    </li>
                                    <li class="m-list__item">
                                        <a class="o-secondary-nav__link" href="#rse-of-principal-owner-4"> 3.23. Demographic information of principal owner 4 </a>
                                    </li>
                                </ul>
                            </li>
                            <li>
                                <a class="o-secondary-nav__link o-secondary-nav__link--parent" href="#4"> 4. Data validation </a>
                                <ul class="o-secondary-nav__list o-secondary-nav__list--children u-hide-on-desktop">
                                    <li class="m-list__item">
                                        <a class="o-secondary-nav__link" href="#4.1"> 4.1. Single-field errors </a>
                                    </li>
                                    <li class="m-list__item">
                                        <a class="o-secondary-nav__link" href="#4.2"> 4.2. Multi-field errors </a>
                                    </li>
                                    <li class="m-list__item">
                                        <a class="o-secondary-nav__link" href="#4.3"> 4.3. Register-level errors </a>
                                    </li>
                                    <li class="m-list__item">
                                        <a class="o-secondary-nav__link" href="#4.4"> 4.4. Single-field warnings </a>
                                    </li>
                                    <li class="m-list__item">
                                        <a class="o-secondary-nav__link" href="#4.5"> 4.5. Multi-field warnings </a>
                                    </li>
                                </ul>
                            </li>
                            <li>
                                <a class="o-secondary-nav__link o-secondary-nav__link--parent" href="#5"> 5. Where to get help </a>
                            </li>
                            <li>
                                <a class="o-secondary-nav__link o-secondary-nav__link--parent" href="#6"> 6. Paperwork Reduction Act </a>
                            </li>
                        </ul>
                    </div>
                </nav>
            </div>
        </aside>
        <div class="u-layout-grid__main content--flush-bottom research-report o-fig__main" id="content__main">
            <div class="eyebrow"></div>
            <h1>Filing instructions guide for small business lending data collected in 2024</h1>
            <div class="lead-paragraph"></div>
            <div class="block block--border-top u-fig-print-link">
                <a class="a-link a-link--jump" href="javascript:window.print()">
                    <span class="a-link__text">Print this guide</span>
                    <svg class="cf-icon-svg cf-icon-svg__print" viewBox="0 0 14 19" xmlns="http://www.w3.org/2000/svg">
                        <path
                            d="m8.698 2.358 3.065 3.066v1.95h.16a1.112 1.112 0 0 1 1.109 1.108v4.837a1.112 1.112 0 0 1-1.109 1.108h-.16v1.726a.477.477 0 0 1-.475.475H2.712a.477.477 0 0 1-.475-.475v-1.726h-.16A1.112 1.112 0 0 1 .968 13.32V8.482a1.112 1.112 0 0 1 1.109-1.108h.16v-4.54a.476.476 0 0 1 .475-.476zm-.22 3.876a.61.61 0 0 1-.608-.608v-2.16H3.345v3.908h7.31v-1.14zm2.177 4.512h-7.31v4.773h7.31zm-1.054.874h-5.26v1.109h5.26zm0 1.962h-5.26v1.108h5.26zm2.437-4.485a.554.554 0 1 0-.554.554.554.554 0 0 0 .554-.554z"
                        ></path>
                    </svg>
                </a>
            </div>
            <div class="o-fig__section" data-search-section="" data-scrollspy="1">
                <h2 class="o-fig__heading">
                    <a id="1" href="#1"> 1. What is the filing instructions guide? </a>
                </h2>
                <p data-block-key="nwusr">
                    The 2024 filing instructions guide is a set of resources to help you file small business lending data with the Consumer Financial Protection Bureau (CFPB) in 2025 covering the period from October 1, 2024 to December 31,
                    2024. These resources are briefly described in this section and are further detailed throughout this web page in individual sections.
                </p>
                <p data-block-key="d9mc2">These resources may be useful for employees in a variety of roles, for example:</p>
                <ul>
                    <li data-block-key="3osb">Staff who collect, prepare, and submit data</li>
                    <li data-block-key="3lgo1">Technology support staff</li>
                    <li data-block-key="dkfmb">Compliance officers</li>
                </ul>
                <h4 data-block-key="2752q">
                    <br />
                    The guide includes the following sections:
                </h4>
                <h5 data-block-key="8jred">Filing process overview</h5>
                <p data-block-key="cdjla">
                    Section 2 provides an overview of the process to file small business lending data with the CFPB. It describes the data submission platform (the platform), which is the system that filers will use to submit their data. It
                    also describes the file format that will be required for submitting the data.
                </p>
                <h5 data-block-key="1bopa">Data points</h5>
                <p data-block-key="crqmu">
                    Section 3 provides instructions for what to enter into each data field in the small business lending application register (register). A machine-readable version of the data specification is provided.
                </p>
                <h5 data-block-key="1v4jh">Data validation</h5>
                <p data-block-key="d56dk">Section 4 lists the validation requirements that a register must meet before it can be filed with the CFPB. A machine-readable version of the validation specification is provided.</p>
                <h5 data-block-key="3tdu1">Where to get help</h5>
                <p data-block-key="ef50k">Section 5 provides a summary of resources available from the CFPB to assist with small business lending rule-related inquiries.</p>
            </div>
            <div class="o-fig__section" data-search-section="" data-scrollspy="2">
                <h2 class="o-fig__heading">
                    <a id="2" href="#2"> 2. Filing process overview </a>
                </h2>
                <p data-block-key="nwusr">
                    This section provides instructions on filing small business lending data with the CFPB. This document is not a substitute for the small business lending rule, found in Regulation B (12 CFR part 1002), Subpart B. Refer to
                    the rule for guidance and clarification regarding the reporting requirements for each data field.
                </p>
            </div>
            <div class="o-fig__section--sub" data-search-section="" data-scrollspy="2.1">
                <h3 class="o-fig__heading">
                    <a id="2.1" href="#2.1"> 2.1. About the small business lending platform </a>
                </h3>
                <p data-block-key="anq0g">
                    Filers will submit their data to the platform via a web interface. There will be a process for individuals representing a financial institution to register for an account to access the online submission platform.
                </p>
                <p data-block-key="ffal8">
                    Using the platform, each filer will provide financial institution identifying information per 12 CFR § 1002.109(b). The platform will walk filers through the small business lending application register filing process,
                    including uploading data, performing validation checks on the data, and certifying the data. An authorized representative of the filer with knowledge of the data submitted will certify to the accuracy and completeness of
                    the data submitted.
                </p>
            </div>
            <div class="o-fig__section--sub" data-search-section="" data-scrollspy="2.2">
                <h3 class="o-fig__heading">
                    <a id="2.2" href="#2.2"> 2.2. File format </a>
                </h3>
                <p data-block-key="anq0g">Your register must be submitted in a comma-separated values (CSV) file format.</p>
                <p data-block-key="685k1">Your CSV file should adhere to the following standards:</p>
                <ol>
                    <li data-block-key="fl1ga">The register must be a comma-delimited text file.</li>
                    <li data-block-key="76rjr">
                        The first line of the file is a header row.&nbsp;The contents of the header row must be the column names specified in the Data points section of this guide, in the order of the field numbering used in the guide,
                        separated by commas.
                    </li>
                    <li data-block-key="bul6h">
                        Each following line of the file represents a covered application record. Each record in the file must contain the data fields described in the Data points section of this guide, in order, corresponding to the order
                        of the column names in the header row.
                    </li>
                    <li data-block-key="9aij6">
                        Each data field within each row must be separated with a comma (","). That means that if you leave a field blank, the field should still be denoted by commas (example: three fields containing
                        <i>1, [blank], 3</i> would be formatted as <i>1,,3</i>).
                    </li>
                    <li data-block-key="a8an9">If any field contains space(s) (" ") before and/or after the comma delimiter, the space(s) will be ignored.</li>
                    <li data-block-key="opd6">This is not a fixed-width formatted file. Do not include leading zeros, tabs, or spaces for the purpose of making a data field a specific number of characters.</li>
                    <li data-block-key="2tds5">
                        If a field contains a comma character, the field must be enclosed in double quotes (e.g., "Confederated Tribes of the Coos, Lower Umpqua and Siuslaw Indians of Oregon"). Fields not containing a comma can also be
                        enclosed in double quotes, but this is not required.
                    </li>
                    <li data-block-key="50fl8">
                        No field in a row may contain a line break, newline, or carriage-return. Line breaks should only appear at the end of a row. Each row of the file should represent a whole application record.
                    </li>
                    <li data-block-key="ed57d">Files must use UTF-8 encoding (note that all-ASCII files are always valid UTF-8).</li>
                </ol>
                <p data-block-key="1vl8o">Any file not conforming to these specifications cannot be submitted as a register.</p>
            </div>
            <div class="o-fig__section" data-search-section="" data-scrollspy="3">
                <h2 class="o-fig__heading">
                    <a id="3" href="#3"> 3. Data points </a>
                </h2>
                <p data-block-key="nwusr">
                    This section provides instructions on entering data in the small business lending application register for small business lending data collected in 2024. This document is not a substitute for the rule, found in
                    Regulation B (12 CFR part 1002), Subpart B. Refer to the rule for guidance and clarification regarding the reporting requirements for each data field.
                </p>
                <p data-block-key="cqkhf">Data fields are presented below in the order they are recorded in the register. For a machine-readable view of the data specification, see the following link:</p>
                <p data-block-key="cvu2g">
                    <a class="a-link a-link--jump"
                       href="https://raw.githubusercontent.com/cfpb/sbl-content/2024-v1/fig-files/file-spec/2024-data-points.csv">
                        <span class="a-link__text">Data spec (CSV)</span>
                        <svg class="cf-icon-svg cf-icon-svg--external-link" viewBox="0 0 14 19" xmlns="http://www.w3.org/2000/svg">
                            <path
                                d="M13.017 3.622v4.6a.554.554 0 0 1-1.108 0V4.96L9.747 7.122a1.65 1.65 0 0 1 .13.646v5.57A1.664 1.664 0 0 1 8.215 15h-5.57a1.664 1.664 0 0 1-1.662-1.663v-5.57a1.664 1.664 0 0 1 1.662-1.662h5.57A1.654 1.654 0 0 1 9 6.302l2.126-2.126H7.863a.554.554 0 1 1 0-1.108h4.6a.554.554 0 0 1 .554.554zM8.77 8.1l-2.844 2.844a.554.554 0 0 1-.784-.783l2.947-2.948H2.645a.555.555 0 0 0-.554.555v5.57a.555.555 0 0 0 .554.553h5.57a.555.555 0 0 0 .554-.554z"
                            ></path>
                        </svg>
                    </a>
                </p>
                <div class="o-fig__section--sub" data-search-section="" data-scrollspy="uid">
                    <h3 class="report-header o-fig__heading">
                        <a id="uid" href="#uid"> 3.1 Unique identifier </a>
                    </h3>
                    <p>Rule section: 12 CFR 1002.107(a)(1)</p>
                    <p></p>
                </div>
                <div class="o-fig__section--sub-sub" data-search-section="" data-scrollspy="uid">
                    <h4 class="report-header o-fig__heading">
                        <a id="uid" href="#uid"> Field 1: Unique identifier </a>
                    </h4>
                    <h5>Column name</h5>
                    uid
                    <h5>Instructions</h5>
                    <ul>
                        <li>Field type: Text (width 21 to 45 characters)</li>
                        <li>Required for all application records</li>
                    </ul>
                    <p>Enter a unique identifier for each application or extension of credit that:</p>
                    <ul>
                        <li>Begins with the financial institution's Legal Entity Identifier as defined in comment 1002.109(b)(6)-1</li>
                        <li>
                            Follows the Legal Entity Identifier with up to 25 additional characters to identify the covered loan or application, which:
                            <ul>
                                <li>May be uppercase letters, numerals, or a combination of uppercase letters and numerals (cannot contain dashes, other special characters, or characters with diacritics)</li>
                                <li>Must be unique within the financial institution</li>
                                <li>Must not include any information that could be used to directly identify the applicant or borrower</li>
                            </ul>
                        </li>
                    </ul>
                    <p></p>
                    <h5>Examples</h5>
                    <ul>
                        <li>10BX939C5543TQA1144M999143938</li>
                    </ul>
                    <h5>Validations</h5>
                    <ul>
                        <li>Must be at least 21 characters in length and at most 45 characters in length</li>
                        <li>May contain any combination of numbers and/or uppercase letters (i.e., 0-9 and A-Z), and must not contain any other characters</li>
                        <li>May not be used in more than one record within a small business lending application register</li>
                        <li>The first 20 characters should match the Legal Entity Identifier (LEI) for the financial institution</li>
                    </ul>
                </div>
                <div class="o-fig__section--sub" data-search-section="" data-scrollspy="application-date">
                    <h3 class="report-header o-fig__heading">
                        <a id="application-date" href="#application-date"> 3.2 Application date </a>
                    </h3>
                    <p>Rule section: 12 CFR 1002.107(a)(2)</p>
                    <p></p>
                </div>
                <div class="o-fig__section--sub-sub" data-search-section="" data-scrollspy="application-date">
                    <h4 class="report-header o-fig__heading">
                        <a id="app_date" href="#app_date"> Field 2: Application date </a>
                    </h4>
                    <h5>Column name</h5>
                    app_date
                    <h5>Instructions</h5>
                    <ul>
                        <li>Field type: Date</li>
                        <li>Required for all application records</li>
                    </ul>
                    <p>Enter, in numeral form, the date the application was received or the date shown on the application form by year, month, and day, using YYYYMMDD format.</p>
                    <p></p>
                    <h5>Examples</h5>
                    <ul>
                        <li>For October 1, 2024, enter 20241001</li>
                    </ul>
                    <h5>Validations</h5>
                    <ul>
                        <li>Must be a real calendar date using YYYYMMDD format</li>
                    </ul>
                </div>
                <div class="o-fig__section--sub" data-search-section="" data-scrollspy="application-method">
                    <h3 class="report-header o-fig__heading">
                        <a id="application-method" href="#application-method"> 3.3 Application method </a>
                    </h3>
                    <p>Rule section: 12 CFR 1002.107(a)(3)</p>
                    <p></p>
                </div>
                <div class="o-fig__section--sub-sub" data-search-section="" data-scrollspy="application-method">
                    <h4 class="report-header o-fig__heading">
                        <a id="app_method" href="#app_method"> Field 3: Application method </a>
                    </h4>
                    <h5>Column name</h5>
                    app_method
                    <h5>Instructions</h5>
                    <ul>
                        <li>Field type: Single response</li>
                        <li>Required for all application records</li>
                    </ul>
                    <p>Indicate the means by which the applicant submitted the application by entering one of the specified codes.</p>
                    <p></p>
                    <table class="o-table o-table--stack-on-small">
                        <thead>
                            <tr>
                                <th>Valid values</th>
                                <th>Codes</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td data-label="Valid values">1</td>
                                <td data-label="Codes">Code 1 - In-person</td>
                            </tr>
                            <tr>
                                <td data-label="Valid values">2</td>
                                <td data-label="Codes">Code 2 - Telephone</td>
                            </tr>
                            <tr>
                                <td data-label="Valid values">3</td>
                                <td data-label="Codes">Code 3 - Online</td>
                            </tr>
                            <tr>
                                <td data-label="Valid values">4</td>
                                <td data-label="Codes">Code 4 - Mail</td>
                            </tr>
                        </tbody>
                    </table>
                    <h5>Validations</h5>
                    <ul>
                        <li>Must equal 1, 2, 3 or 4</li>
                    </ul>
                </div>
                <div class="o-fig__section--sub" data-search-section="" data-scrollspy="application-recipient">
                    <h3 class="report-header o-fig__heading">
                        <a id="application-recipient" href="#application-recipient"> 3.4 Application recipient </a>
                    </h3>
                    <p>Rule section: 12 CFR 1002.107(a)(4)</p>
                    <p></p>
                </div>
                <div class="o-fig__section--sub-sub" data-search-section="" data-scrollspy="application-recipient">
                    <h4 class="report-header o-fig__heading">
                        <a id="app_recipient" href="#app_recipient"> Field 4: Application recipient </a>
                    </h4>
                    <h5>Column name</h5>
                    app_recipient
                    <h5>Instructions</h5>
                    <ul>
                        <li>Field type: Single response</li>
                        <li>Required for all application records</li>
                    </ul>
                    <p>Indicate the application recipient by entering one of the specified codes.</p>
                    <p></p>
                    <table class="o-table o-table--stack-on-small">
                        <thead>
                            <tr>
                                <th>Valid values</th>
                                <th>Codes</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td data-label="Valid values">1</td>
                                <td data-label="Codes">Code 1 - The applicant submitted the application directly to the financial institution or its affiliate</td>
                            </tr>
                            <tr>
                                <td data-label="Valid values">2</td>
                                <td data-label="Codes">Code 2 - The applicant submitted the application indirectly to the financial institution via a third party</td>
                            </tr>
                        </tbody>
                    </table>
                    <h5>Validations</h5>
                    <ul>
                        <li>Must equal 1 or 2</li>
                    </ul>
                </div>
                <div class="o-fig__section--sub" data-search-section="" data-scrollspy="credit-type">
                    <h3 class="report-header o-fig__heading">
                        <a id="credit-type" href="#credit-type"> 3.5 Credit type </a>
                    </h3>
                    <p>Rule section: 12 CFR 1002.107(a)(5)</p>
                    <p></p>
                    <ul class="m-list m-list--links">
                        <li class="m-list__item">
                            <a href="#ct_credit_product"> Field 5: Credit product </a>
                        </li>
                        <li class="m-list__item">
                            <a href="#ct_credit_product_ff"> Field 6: Free-form text field for other credit products </a>
                        </li>
                        <li class="m-list__item">
                            <a href="#ct_guarantee"> Field 7: Type of guarantee </a>
                        </li>
                        <li class="m-list__item">
                            <a href="#ct_guarantee_ff"> Field 8: Free-form text field for other guarantee </a>
                        </li>
                        <li class="m-list__item">
                            <a href="#ct_loan_term_flag"> Field 9: Loan term: NA/NP flag </a>
                        </li>
                        <li class="m-list__item">
                            <a href="#ct_loan_term"> Field 10: Loan term </a>
                        </li>
                    </ul>
                </div>
                <div class="o-fig__section--sub-sub" data-search-section="" data-scrollspy="credit-type">
                    <h4 class="report-header o-fig__heading">
                        <a id="ct_credit_product" href="#ct_credit_product"> Field 5: Credit product </a>
                    </h4>
                    <p>Rule section: 12 CFR 1002.107(a)(5)(i)</p>
                    <h5>Column name</h5>
                    ct_credit_product
                    <h5>Instructions</h5>
                    <ul>
                        <li>Field type: Single response</li>
                        <li>Required for all application records</li>
                    </ul>
                    <p>Indicate the credit product by entering one of the specified codes.</p>
                    <p></p>
                    <table class="o-table o-table--stack-on-small">
                        <thead>
                            <tr>
                                <th>Valid values</th>
                                <th>Codes</th>
                                <th>Instructions</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td data-label="Valid values">1</td>
                                <td data-label="Codes">Code 1 - Term loan - unsecured</td>
                                <td data-label="Instructions"></td>
                            </tr>
                            <tr>
                                <td data-label="Valid values">2</td>
                                <td data-label="Codes">Code 2 - Term loan - secured</td>
                                <td data-label="Instructions"></td>
                            </tr>
                            <tr>
                                <td data-label="Valid values">3</td>
                                <td data-label="Codes">Code 3 - Line of credit - unsecured</td>
                                <td data-label="Instructions"></td>
                            </tr>
                            <tr>
                                <td data-label="Valid values">4</td>
                                <td data-label="Codes">Code 4 - Line of credit - secured</td>
                                <td data-label="Instructions"></td>
                            </tr>
                            <tr>
                                <td data-label="Valid values">5</td>
                                <td data-label="Codes">Code 5 - Credit card account, not private-label</td>
                                <td data-label="Instructions"></td>
                            </tr>
                            <tr>
                                <td data-label="Valid values">6</td>
                                <td data-label="Codes">Code 6 - Private-label credit card account</td>
                                <td data-label="Instructions"></td>
                            </tr>
                            <tr>
                                <td data-label="Valid values">7</td>
                                <td data-label="Codes">Code 7 - Merchant cash advance</td>
                                <td data-label="Instructions"></td>
                            </tr>
                            <tr>
                                <td data-label="Valid values">8</td>
                                <td data-label="Codes">Code 8 - Other sales-based financing transaction</td>
                                <td data-label="Instructions"></td>
                            </tr>
                            <tr>
                                <td data-label="Valid values">977</td>
                                <td data-label="Codes">Code 977 - Other</td>
                                <td data-label="Instructions">When this code is entered, also specify the credit product in the associated free-form text field.</td>
                            </tr>
                            <tr>
                                <td data-label="Valid values">988</td>
                                <td data-label="Codes">Code 988 - Not provided by applicant and otherwise undetermined</td>
                                <td data-label="Instructions">Enter code 988 if the credit product is not provided by applicant and is otherwise undetermined.</td>
                            </tr>
                        </tbody>
                    </table>
                    <h5>Validations</h5>
                    <ul>
                        <li>Must equal 1, 2, 3, 4, 5, 6, 7, 8, 977, or 988</li>
                    </ul>
                </div>
                <div class="o-fig__section--sub-sub" data-search-section="" data-scrollspy="credit-type">
                    <h4 class="report-header o-fig__heading">
                        <a id="ct_credit_product_ff" href="#ct_credit_product_ff"> Field 6: Free-form text field for other credit products </a>
                    </h4>
                    <p>Rule section: 12 CFR 1002.107(a)(5)(i)</p>
                    <h5>Column name</h5>
                    ct_credit_product_ff
                    <h5>Instructions</h5>
                    <ul>
                        <li>Field type: Text (width up to 300 characters)</li>
                        <li>Conditionally required if 'credit product' is code 977. Leave blank if code 977 is not entered.</li>
                    </ul>
                    <p>Specify in text the other credit product if code 977 is entered.</p>
                    <p></p>
                    <h5>Validations</h5>
                    <ul>
                        <li>Must not exceed 300 characters in length</li>
                    </ul>
                </div>
                <div class="o-fig__section--sub-sub" data-search-section="" data-scrollspy="credit-type">
                    <h4 class="report-header o-fig__heading">
                        <a id="ct_guarantee" href="#ct_guarantee"> Field 7: Type of guarantee </a>
                    </h4>
                    <p>Rule section: 12 CFR 1002.107(a)(5)(ii)</p>
                    <h5>Column name</h5>
                    ct_guarantee
                    <h5>Instructions</h5>
                    <ul>
                        <li>Field type: Multiple response</li>
                        <li>Required for all application records</li>
                    </ul>
                    <p>
                        Indicate the type or types of guarantees by entering up to five of the specified codes. If there is more than one type of guarantee, enter each, in any order, separated by a semicolon. A maximum of five types of
                        guarantees, including any 'other' guarantee(s) specified in the free-form text field, may be entered.
                    </p>
                    <p></p>
                    <table class="o-table o-table--stack-on-small">
                        <thead>
                            <tr>
                                <th>Valid values</th>
                                <th>Codes</th>
                                <th>Instructions</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td data-label="Valid values">1</td>
                                <td data-label="Codes">Code 1 - Personal guarantee - owner(s)</td>
                                <td data-label="Instructions"></td>
                            </tr>
                            <tr>
                                <td data-label="Valid values">2</td>
                                <td data-label="Codes">Code 2 - Personal guarantee - non-owner(s)</td>
                                <td data-label="Instructions"></td>
                            </tr>
                            <tr>
                                <td data-label="Valid values">3</td>
                                <td data-label="Codes">Code 3 - SBA guarantee - 7(a) program</td>
                                <td data-label="Instructions"></td>
                            </tr>
                            <tr>
                                <td data-label="Valid values">4</td>
                                <td data-label="Codes">Code 4 - SBA guarantee - 504 program</td>
                                <td data-label="Instructions"></td>
                            </tr>
                            <tr>
                                <td data-label="Valid values">5</td>
                                <td data-label="Codes">Code 5 - SBA guarantee - other</td>
                                <td data-label="Instructions"></td>
                            </tr>
                            <tr>
                                <td data-label="Valid values">6</td>
                                <td data-label="Codes">Code 6 - USDA guarantee</td>
                                <td data-label="Instructions"></td>
                            </tr>
                            <tr>
                                <td data-label="Valid values">7</td>
                                <td data-label="Codes">Code 7 - FHA insurance</td>
                                <td data-label="Instructions"></td>
                            </tr>
                            <tr>
                                <td data-label="Valid values">8</td>
                                <td data-label="Codes">Code 8 - Bureau of Indian Affairs guarantee</td>
                                <td data-label="Instructions"></td>
                            </tr>
                            <tr>
                                <td data-label="Valid values">9</td>
                                <td data-label="Codes">Code 9 - Other Federal guarantee</td>
                                <td data-label="Instructions"></td>
                            </tr>
                            <tr>
                                <td data-label="Valid values">10</td>
                                <td data-label="Codes">Code 10 - State government guarantee</td>
                                <td data-label="Instructions"></td>
                            </tr>
                            <tr>
                                <td data-label="Valid values">11</td>
                                <td data-label="Codes">Code 11 - Local government guarantee</td>
                                <td data-label="Instructions"></td>
                            </tr>
                            <tr>
                                <td data-label="Valid values">977</td>
                                <td data-label="Codes">Code 977 - Other</td>
                                <td data-label="Instructions">When this code is entered, also specify the type of guarantee in the associated free-form text field.</td>
                            </tr>
                            <tr>
                                <td data-label="Valid values">999</td>
                                <td data-label="Codes">Code 999 - No guarantee</td>
                                <td data-label="Instructions"></td>
                            </tr>
                        </tbody>
                    </table>
                    <h5>Validations</h5>
                    <ul>
                        <li>Each value (separated by semicolons) must equal 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 977, or 999</li>
                        <li>Must contain at least one and at most five values, separated by semicolons</li>
                        <li>When code 999 is reported, should not contain any other values</li>
                        <li>Should not contain duplicated values</li>
                    </ul>
                </div>
                <div class="o-fig__section--sub-sub" data-search-section="" data-scrollspy="credit-type">
                    <h4 class="report-header o-fig__heading">
                        <a id="ct_guarantee_ff" href="#ct_guarantee_ff"> Field 8: Free-form text field for other guarantee </a>
                    </h4>
                    <p>Rule section: 12 CFR 1002.107(a)(5)(ii)</p>
                    <h5>Column name</h5>
                    ct_guarantee_ff
                    <h5>Instructions</h5>
                    <ul>
                        <li>Field type: Text (width up to 300 characters)</li>
                        <li>Conditionally required if 'type of guarantee' contains code 977. Leave blank if code 977 is not entered.</li>
                    </ul>
                    <p>Specify in text the other guarantee if code 977 is entered. If there is more than one other guarantee, separate each with a semicolon.</p>
                    <p></p>
                    <h5>Validations</h5>
                    <ul>
                        <li>Must not exceed 300 characters in length</li>
                    </ul>
                </div>
                <div class="o-fig__section--sub-sub" data-search-section="" data-scrollspy="credit-type">
                    <h4 class="report-header o-fig__heading">
                        <a id="ct_loan_term_flag" href="#ct_loan_term_flag"> Field 9: Loan term: NA/NP flag </a>
                    </h4>
                    <p>Rule section: 12 CFR 1002.107(a)(5)(iii)</p>
                    <h5>Column name</h5>
                    ct_loan_term_flag
                    <h5>Instructions</h5>
                    <ul>
                        <li>Field type: Single response</li>
                        <li>Required for all application records</li>
                    </ul>
                    <p>Indicate whether 'loan term' is applicable for this application for credit by entering one of the specified codes.</p>
                    <p></p>
                    <table class="o-table o-table--stack-on-small">
                        <thead>
                            <tr>
                                <th>Valid values</th>
                                <th>Codes</th>
                                <th>Instructions</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td data-label="Valid values">900</td>
                                <td data-label="Codes">Code 900 - Applicable and reported</td>
                                <td data-label="Instructions"></td>
                            </tr>
                            <tr>
                                <td data-label="Valid values">988</td>
                                <td data-label="Codes">Code 988 - Applicable but not provided by applicant and otherwise undetermined</td>
                                <td data-label="Instructions">
                                    Enter code 988 if any of the following conditions apply:
                                    <ul>
                                        <li>The product generally has a loan term, but the application is denied, withdrawn, or determined to be incomplete before a loan term has been identified</li>
                                        <li>The 'credit product' is code 7 (merchant cash advance) or code 8 (other sales-based financing transaction) and the product does not have a loan term</li>
                                    </ul>
                                </td>
                            </tr>
                            <tr>
                                <td data-label="Valid values">999</td>
                                <td data-label="Codes">Code 999 - Not applicable</td>
                                <td data-label="Instructions">Enter code 999 if the product type does not have a loan term, such as a credit card.</td>
                            </tr>
                        </tbody>
                    </table>
                    <h5>Validations</h5>
                    <ul>
                        <li>Must equal 900, 988, or 999</li>
                    </ul>
                </div>
                <div class="o-fig__section--sub-sub" data-search-section="" data-scrollspy="credit-type">
                    <h4 class="report-header o-fig__heading">
                        <a id="ct_loan_term" href="#ct_loan_term"> Field 10: Loan term </a>
                    </h4>
                    <p>Rule section: 12 CFR 1002.107(a)(5)(iii)</p>
                    <h5>Column name</h5>
                    ct_loan_term
                    <h5>Instructions</h5>
                    <ul>
                        <li>Field type: Numeric</li>
                        <li>Conditionally required if 'credit type: loan term: NA/NP flag' is code 900. Leave blank if code 900 is not entered.</li>
                    </ul>
                    <p>Enter, in numerical form, the number of months in the loan term for products that have a loan term. If the product has a loan term of less than 1 month, enter 1.</p>
                    <p></p>
                    <h5>Examples</h5>
                    <ul>
                        <li>For a loan term of 36 months, enter 36</li>
                        <li>For a loan term of less than 1 month, enter 1</li>
                    </ul>
                    <h5>Validations</h5>
                    <ul>
                        <li>When present, must be a whole number</li>
                        <li>When present, must be greater than or equal to 1</li>
                        <li>When present, should be less than 1200 (100 years)</li>
                    </ul>
                </div>
                <div class="o-fig__section--sub" data-search-section="" data-scrollspy="credit-purpose">
                    <h3 class="report-header o-fig__heading">
                        <a id="credit-purpose" href="#credit-purpose"> 3.6 Credit purpose </a>
                    </h3>
                    <p>Rule section: 12 CFR 1002.107(a)(6)</p>
                    <p></p>
                </div>
                <div class="o-fig__section--sub-sub" data-search-section="" data-scrollspy="credit-purpose">
                    <h4 class="report-header o-fig__heading">
                        <a id="credit_purpose" href="#credit_purpose"> Field 11: Credit purpose </a>
                    </h4>
                    <h5>Column name</h5>
                    credit_purpose
                    <h5>Instructions</h5>
                    <ul>
                        <li>Field type: Multiple response</li>
                        <li>Required for all application records</li>
                    </ul>
                    <p>Indicate the credit purpose(s) by entering up to three of the specified codes. If there is more than one credit purpose, enter each, in any order, separated by a semicolon.</p>
                    <p></p>
                    <table class="o-table o-table--stack-on-small">
                        <thead>
                            <tr>
                                <th>Valid values</th>
                                <th>Codes</th>
                                <th>Instructions</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td data-label="Valid values">1</td>
                                <td data-label="Codes">Code 1 - Purchase, construction/improvement, or refinance of non-owner-occupied real property</td>
                                <td data-label="Instructions"></td>
                            </tr>
                            <tr>
                                <td data-label="Valid values">2</td>
                                <td data-label="Codes">Code 2 - Purchase, construction/improvement, or refinance of owner-occupied real property</td>
                                <td data-label="Instructions"></td>
                            </tr>
                            <tr>
                                <td data-label="Valid values">3</td>
                                <td data-label="Codes">Code 3 - Purchase, refinance, or rehabilitation/repair of motor vehicle(s) (including light and heavy trucks)</td>
                                <td data-label="Instructions"></td>
                            </tr>
                            <tr>
                                <td data-label="Valid values">4</td>
                                <td data-label="Codes">Code 4 - Purchase, refinance, or rehabilitation/repair of equipment</td>
                                <td data-label="Instructions"></td>
                            </tr>
                            <tr>
                                <td data-label="Valid values">5</td>
                                <td data-label="Codes">Code 5 - Working capital (includes inventory or floor planning)</td>
                                <td data-label="Instructions"></td>
                            </tr>
                            <tr>
                                <td data-label="Valid values">6</td>
                                <td data-label="Codes">Code 6 - Business start-up</td>
                                <td data-label="Instructions"></td>
                            </tr>
                            <tr>
                                <td data-label="Valid values">7</td>
                                <td data-label="Codes">Code 7 - Business expansion</td>
                                <td data-label="Instructions"></td>
                            </tr>
                            <tr>
                                <td data-label="Valid values">8</td>
                                <td data-label="Codes">Code 8 - Business acquisition</td>
                                <td data-label="Instructions"></td>
                            </tr>
                            <tr>
                                <td data-label="Valid values">9</td>
                                <td data-label="Codes">Code 9 - Refinance existing debt (other than refinancings listed above)</td>
                                <td data-label="Instructions"></td>
                            </tr>
                            <tr>
                                <td data-label="Valid values">10</td>
                                <td data-label="Codes">Code 10 - Line increase</td>
                                <td data-label="Instructions"></td>
                            </tr>
                            <tr>
                                <td data-label="Valid values">11</td>
                                <td data-label="Codes">Code 11 - Overdraft</td>
                                <td data-label="Instructions"></td>
                            </tr>
                            <tr>
                                <td data-label="Valid values">977</td>
                                <td data-label="Codes">Code 977 - Other</td>
                                <td data-label="Instructions">When this code is entered, also specify the credit purpose in the associated free-form text field.</td>
                            </tr>
                            <tr>
                                <td data-label="Valid values">988</td>
                                <td data-label="Codes">Code 988 - Not provided by applicant and otherwise undetermined</td>
                                <td data-label="Instructions">Enter code 988 if the credit purpose for the application is not provided by applicant and otherwise undetermined.</td>
                            </tr>
                            <tr>
                                <td data-label="Valid values">999</td>
                                <td data-label="Codes">Code 999 - Not applicable</td>
                                <td data-label="Instructions">Enter code 999 for a credit product that generally has indeterminate or numerous potential purposes, such as a credit card.</td>
                            </tr>
                        </tbody>
                    </table>
                    <h5>Validations</h5>
                    <ul>
                        <li>Each value (separated by semicolons) must equal 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 977, 988, or 999</li>
                        <li>Must contain at least one and at most three values, separated by semicolons</li>
                        <li>When code 988 or 999 is reported, should not contain any other values</li>
                        <li>Should not contain duplicated values</li>
                    </ul>
                </div>
                <div class="o-fig__section--sub-sub" data-search-section="" data-scrollspy="credit-purpose">
                    <h4 class="report-header o-fig__heading">
                        <a id="credit_purpose_ff" href="#credit_purpose_ff"> Field 12: Free-form text field for other credit purpose </a>
                    </h4>
                    <h5>Column name</h5>
                    credit_purpose_ff
                    <h5>Instructions</h5>
                    <ul>
                        <li>Field type: Text (width up to 300 characters)</li>
                        <li>Conditionally required if 'credit purpose' contains code 977. Leave blank if code 977 is not entered.</li>
                    </ul>
                    <p>Specify in text the other credit purpose if code 977 is entered. Do not enter more than one other credit purpose.</p>
                    <p></p>
                    <h5>Validations</h5>
                    <ul>
                        <li>Must not exceed 300 characters in length</li>
                    </ul>
                </div>
                <div class="o-fig__section--sub" data-search-section="" data-scrollspy="amount-applied-for">
                    <h3 class="report-header o-fig__heading">
                        <a id="amount-applied-for" href="#amount-applied-for"> 3.7 Amount applied for </a>
                    </h3>
                    <p>Rule section: 12 CFR 1002.107(a)(7)</p>
                    <p></p>
                </div>
                <div class="o-fig__section--sub-sub" data-search-section="" data-scrollspy="amount-applied-for">
                    <h4 class="report-header o-fig__heading">
                        <a id="amount_applied_for_flag" href="#amount_applied_for_flag"> Field 13: Amount applied for: NA/NP flag </a>
                    </h4>
                    <h5>Column name</h5>
                    amount_applied_for_flag
                    <h5>Instructions</h5>
                    <ul>
                        <li>Field type: Single response</li>
                        <li>Required for all application records</li>
                    </ul>
                    <p>Indicate whether 'amount applied for' is provided by entering one of the specified codes.</p>
                    <p></p>
                    <table class="o-table o-table--stack-on-small">
                        <thead>
                            <tr>
                                <th>Valid values</th>
                                <th>Codes</th>
                                <th>Instructions</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td data-label="Valid values">900</td>
                                <td data-label="Codes">Code 900 - Applicable and reported</td>
                                <td data-label="Instructions"></td>
                            </tr>
                            <tr>
                                <td data-label="Valid values">988</td>
                                <td data-label="Codes">Code 988 - Applicable but not provided by applicant and otherwise undetermined</td>
                                <td data-label="Instructions">
                                    Enter code 988 if the product applied for does involve a specific amount requested or underwritten, but the amount requested or underwritten is not provided by the applicant and otherwise undetermined.
                                </td>
                            </tr>
                            <tr>
                                <td data-label="Valid values">999</td>
                                <td data-label="Codes">Code 999 - Not applicable</td>
                                <td data-label="Instructions">Enter code 999 if the product applied for does not involve a specific amount requested.</td>
                            </tr>
                        </tbody>
                    </table>
                    <h5>Validations</h5>
                    <ul>
                        <li>Must equal 900, 988 or 999</li>
                    </ul>
                </div>
                <div class="o-fig__section--sub-sub" data-search-section="" data-scrollspy="amount-applied-for">
                    <h4 class="report-header o-fig__heading">
                        <a id="amount_applied_for" href="#amount_applied_for"> Field 14: Amount applied for </a>
                    </h4>
                    <h5>Column name</h5>
                    amount_applied_for
                    <h5>Instructions</h5>
                    <ul>
                        <li>Field type: Numeric</li>
                        <li>Conditionally required if 'amount applied for: NA/NP flag' is code 900. Leave blank if code 900 is not entered.</li>
                    </ul>
                    <p>Enter one of the following:</p>
                    <ul>
                        <li>The dollar amount for initial amount of credit/credit limit requested by applicant at the application stage</li>
                        <li>If application is in response to a firm offer that specifies an amount or limit, the dollar amount of the firm offer, unless the applicant requested a different amount</li>
                        <li>If application is in response to a firm offer that does not specify an amount or limit and the applicant did not request a specific amount, the dollar amount underwritten</li>
                        <li>If application is in response to a firm offer that specifies an amount or limit as a range and the applicant did not request a specific amount, the dollar amount underwritten</li>
                        <li>If applicant did not request a particular amount but the financial institution underwrites for a specific amount, the dollar amount underwritten</li>
                        <li>If applicant requested a range of dollar amounts, the midpoint of that range</li>
                        <li>If application is a request for additional amounts on an existing account, the dollar amount of additional credit requested</li>
                    </ul>
                    <p></p>
                    <h5>Examples</h5>
                    <ul>
                        <li>For $12,345, enter 12345</li>
                    </ul>
                    <h5>Validations</h5>
                    <ul>
                        <li>When present, must be a numeric value</li>
                        <li>When present, must be greater than 0</li>
                    </ul>
                </div>
                <div class="o-fig__section--sub" data-search-section="" data-scrollspy="amount-approved-or-originated">
                    <h3 class="report-header o-fig__heading">
                        <a id="amount-approved-or-originated" href="#amount-approved-or-originated"> 3.8 Amount approved or originated </a>
                    </h3>
                    <p>Rule section: 12 CFR 1002.107(a)(8)</p>
                    <p></p>
                </div>
                <div class="o-fig__section--sub-sub" data-search-section="" data-scrollspy="amount-approved-or-originated">
                    <h4 class="report-header o-fig__heading">
                        <a id="amount_approved" href="#amount_approved"> Field 15: Amount approved or originated </a>
                    </h4>
                    <h5>Column name</h5>
                    amount_approved
                    <h5>Instructions</h5>
                    <ul>
                        <li>Field type: Numeric</li>
                        <li>Conditionally required if 'action taken' is code 1 or 2. Report not applicable by leaving blank if codes 1 or 2 are not entered.</li>
                    </ul>
                    <p>Enter one of the following:</p>
                    <ul>
                        <li>For a closed-end origination, the amount of the originated loan</li>
                        <li>For a closed-end application, the highest amount approved if the application was approved but not accepted</li>
                        <li>For an open-end origination, the amount of the credit limit established</li>
                        <li>For an open-end application, the highest amount approved if the application was approved but not accepted</li>
                        <li>For additional credit amounts that were approved for or originated on an existing account, report the additional credit amount approved or originated, and not any previous amount extended</li>
                        <li>Leave blank if amount approved or originated is not applicable because an application is denied, withdrawn, or incomplete</li>
                    </ul>
                    <p></p>
                    <h5>Examples</h5>
                    <ul>
                        <li>For $101.23, enter 101.23</li>
                    </ul>
                    <h5>Validations</h5>
                    <ul>
                        <li>When present, must be a numeric value</li>
                        <li>When present, must be greater than 0</li>
                    </ul>
                </div>
                <div class="o-fig__section--sub" data-search-section="" data-scrollspy="action-taken">
                    <h3 class="report-header o-fig__heading">
                        <a id="action-taken" href="#action-taken"> 3.9 Action taken </a>
                    </h3>
                    <p>Rule section: 12 CFR 1002.107(a)(9)</p>
                    <p></p>
                </div>
                <div class="o-fig__section--sub-sub" data-search-section="" data-scrollspy="action-taken">
                    <h4 class="report-header o-fig__heading">
                        <a id="action_taken" href="#action_taken"> Field 16: Action taken </a>
                    </h4>
                    <h5>Column name</h5>
                    action_taken
                    <h5>Instructions</h5>
                    <ul>
                        <li>Field type: Single response</li>
                        <li>Required for all application records</li>
                    </ul>
                    <p>Indicate what action is taken by entering one of the specified codes.</p>
                    <p></p>
                    <table class="o-table o-table--stack-on-small">
                        <thead>
                            <tr>
                                <th>Valid values</th>
                                <th>Codes</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td data-label="Valid values">1</td>
                                <td data-label="Codes">Code 1 - Originated</td>
                            </tr>
                            <tr>
                                <td data-label="Valid values">2</td>
                                <td data-label="Codes">Code 2 - Approved but not accepted</td>
                            </tr>
                            <tr>
                                <td data-label="Valid values">3</td>
                                <td data-label="Codes">Code 3 - Denied</td>
                            </tr>
                            <tr>
                                <td data-label="Valid values">4</td>
                                <td data-label="Codes">Code 4 - Withdrawn by the applicant</td>
                            </tr>
                            <tr>
                                <td data-label="Valid values">5</td>
                                <td data-label="Codes">Code 5 - Incomplete</td>
                            </tr>
                        </tbody>
                    </table>
                    <h5>Validations</h5>
                    <ul>
                        <li>Must equal 1, 2, 3, 4, or 5</li>
                    </ul>
                </div>
                <div class="o-fig__section--sub" data-search-section="" data-scrollspy="action-taken-date">
                    <h3 class="report-header o-fig__heading">
                        <a id="action-taken-date" href="#action-taken-date"> 3.10 Action taken date </a>
                    </h3>
                    <p>Rule section: 12 CFR 1002.107(a)(10)</p>
                    <p></p>
                </div>
                <div class="o-fig__section--sub-sub" data-search-section="" data-scrollspy="action-taken-date">
                    <h4 class="report-header o-fig__heading">
                        <a id="action_taken_date" href="#action_taken_date"> Field 17: Action taken date </a>
                    </h4>
                    <h5>Column name</h5>
                    action_taken_date
                    <h5>Instructions</h5>
                    <ul>
                        <li>Field type: Date</li>
                        <li>Required for all application records</li>
                    </ul>
                    <p>Enter, in numeral form, the date the action was taken as a year, month, and day (YYYYMMDD).</p>
                    <p></p>
                    <h5>Examples</h5>
                    <ul>
                        <li>For October 25, 2024, enter 20241025</li>
                    </ul>
                    <h5>Validations</h5>
                    <ul>
                        <li>Must be a real calendar date using YYYYMMDD format</li>
                        <li>The date indicated must occur within the current reporting period: October 1, 2024 to December 31, 2024</li>
                    </ul>
                </div>
                <div class="o-fig__section--sub" data-search-section="" data-scrollspy="denial-reasons">
                    <h3 class="report-header o-fig__heading">
                        <a id="denial-reasons" href="#denial-reasons"> 3.11 Denial reasons </a>
                    </h3>
                    <p>Rule section: 12 CFR 1002.107(a)(11)</p>
                    <p></p>
                </div>
                <div class="o-fig__section--sub-sub" data-search-section="" data-scrollspy="denial-reasons">
                    <h4 class="report-header o-fig__heading">
                        <a id="denial_reasons" href="#denial_reasons"> Field 18: Denial reason(s) </a>
                    </h4>
                    <h5>Column name</h5>
                    denial_reasons
                    <h5>Instructions</h5>
                    <ul>
                        <li>Field type: Multiple response</li>
                        <li>Required for all application records</li>
                    </ul>
                    <p>
                        For a denied application, indicate the principal reason(s) for denial by entering up to four of the specified codes. If there is more than one principal reason for denial, enter each, in any order, separated by a
                        semicolon. A maximum of four denial reasons, including any 'other' denial reason(s) specified in the free-form text field, may be entered.
                    </p>
                    <p></p>
                    <h5>Examples</h5>
                    <ul>
                        <li>If Cashflow, enter 4</li>
                        <li>If Cashflow, Collateral, Time in business, and Government loan program criteria, enter 4;5;6;7 or 7;5;6;4 etc.</li>
                    </ul>
                    <table class="o-table o-table--stack-on-small">
                        <thead>
                            <tr>
                                <th>Valid values</th>
                                <th>Codes</th>
                                <th>Instructions</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td data-label="Valid values">1</td>
                                <td data-label="Codes">Code 1 - Credit characteristics of the business</td>
                                <td data-label="Instructions"></td>
                            </tr>
                            <tr>
                                <td data-label="Valid values">2</td>
                                <td data-label="Codes">Code 2 - Credit characteristics of the principal owner(s) or guarantor(s)</td>
                                <td data-label="Instructions"></td>
                            </tr>
                            <tr>
                                <td data-label="Valid values">3</td>
                                <td data-label="Codes">Code 3 - Use of credit proceeds</td>
                                <td data-label="Instructions"></td>
                            </tr>
                            <tr>
                                <td data-label="Valid values">4</td>
                                <td data-label="Codes">Code 4 - Cashflow</td>
                                <td data-label="Instructions"></td>
                            </tr>
                            <tr>
                                <td data-label="Valid values">5</td>
                                <td data-label="Codes">Code 5 - Collateral</td>
                                <td data-label="Instructions"></td>
                            </tr>
                            <tr>
                                <td data-label="Valid values">6</td>
                                <td data-label="Codes">Code 6 - Time in business</td>
                                <td data-label="Instructions"></td>
                            </tr>
                            <tr>
                                <td data-label="Valid values">7</td>
                                <td data-label="Codes">Code 7 - Government loan program criteria</td>
                                <td data-label="Instructions"></td>
                            </tr>
                            <tr>
                                <td data-label="Valid values">8</td>
                                <td data-label="Codes">Code 8 - Aggregate exposure</td>
                                <td data-label="Instructions"></td>
                            </tr>
                            <tr>
                                <td data-label="Valid values">9</td>
                                <td data-label="Codes">Code 9 - Unverifiable information</td>
                                <td data-label="Instructions"></td>
                            </tr>
                            <tr>
                                <td data-label="Valid values">977</td>
                                <td data-label="Codes">Code 977 - Other</td>
                                <td data-label="Instructions">When this code is entered, also specify the denial reason(s) in the associated free-form text field.</td>
                            </tr>
                            <tr>
                                <td data-label="Valid values">999</td>
                                <td data-label="Codes">Code 999 - Not applicable</td>
                                <td data-label="Instructions">
                                    Enter code 999 if application was not denied (i.e., application is withdrawn by applicant, incomplete, or approved but not accepted, or loan is originated by the financial institution).
                                </td>
                            </tr>
                        </tbody>
                    </table>
                    <h5>Validations</h5>
                    <ul>
                        <li>Each value (separated by semicolons) must equal 1, 2, 3, 4, 5, 6, 7, 8, 9, 977, or 999</li>
                        <li>Must contain at least one and at most four values, separated by semicolons</li>
                        <li>When code 999 is reported, should not contain any other values</li>
                        <li>Should not contain duplicated values</li>
                    </ul>
                </div>
                <div class="o-fig__section--sub-sub" data-search-section="" data-scrollspy="denial-reasons">
                    <h4 class="report-header o-fig__heading">
                        <a id="denial_reasons_ff" href="#denial_reasons_ff"> Field 19: Free-form text field for other denial reason(s) </a>
                    </h4>
                    <h5>Column name</h5>
                    denial_reasons_ff
                    <h5>Instructions</h5>
                    <ul>
                        <li>Field type: Text (width up to 300 characters)</li>
                        <li>Conditionally required if 'denial reason(s)' contains code 977. Leave blank if code 977 is not entered.</li>
                    </ul>
                    <p>Specify in text the other denial reason(s) if code 977 is entered. If there is more than one other denial reason, separate each with a semicolon.</p>
                    <p></p>
                    <h5>Validations</h5>
                    <ul>
                        <li>Must not exceed 300 characters in length</li>
                    </ul>
                </div>
                <div class="o-fig__section--sub" data-search-section="" data-scrollspy="pricing-information">
                    <h3 class="report-header o-fig__heading">
                        <a id="pricing-information" href="#pricing-information"> 3.12 Pricing information </a>
                    </h3>
                    <p>Rule section: 12 CFR 1002.107(a)(12)</p>
                    <p></p>
                    <ul class="m-list m-list--links">
                        <li class="m-list__item">
                            <a href="#pricing_interest_rate_type"> Field 20: Interest rate type </a>
                        </li>
                        <li class="m-list__item">
                            <a href="#pricing_init_rate_period"> Field 21: Initial rate period </a>
                        </li>
                        <li class="m-list__item">
                            <a href="#pricing_fixed_rate"> Field 22: Fixed rate: interest rate </a>
                        </li>
                        <li class="m-list__item">
                            <a href="#pricing_var_margin"> Field 23: Variable rate transaction: margin </a>
                        </li>
                        <li class="m-list__item">
                            <a href="#pricing_var_index_name"> Field 24: Variable rate transaction: index name </a>
                        </li>
                        <li class="m-list__item">
                            <a href="#pricing_var_index_name_ff"> Field 25: Variable rate transaction: index name: other </a>
                        </li>
                        <li class="m-list__item">
                            <a href="#pricing_var_index_value"> Field 26: Variable rate transaction: index value </a>
                        </li>
                        <li class="m-list__item">
                            <a href="#pricing_origination_charges"> Field 27: Total origination charges </a>
                        </li>
                        <li class="m-list__item">
                            <a href="#pricing_broker_fees"> Field 28: Amount of total broker fees </a>
                        </li>
                        <li class="m-list__item">
                            <a href="#pricing_initial_charges"> Field 29: Initial annual charges </a>
                        </li>
                        <li class="m-list__item">
                            <a href="#pricing_mca_addcost_flag"> Field 30: MCA/sales-based: additional cost for merchant cash advances or other sales-based financing: NA flag </a>
                        </li>
                        <li class="m-list__item">
                            <a href="#pricing_mca_addcost"> Field 31: MCA/sales-based: additional cost for merchant cash advances or other sales-based financing </a>
                        </li>
                        <li class="m-list__item">
                            <a href="#pricing_prepenalty_allowed"> Field 32: Prepayment penalty could be imposed </a>
                        </li>
                        <li class="m-list__item">
                            <a href="#pricing_prepenalty_exists"> Field 33: Prepayment penalty exists </a>
                        </li>
                    </ul>
                </div>
                <div class="o-fig__section--sub-sub" data-search-section="" data-scrollspy="pricing-information">
                    <h4 class="report-header o-fig__heading">
                        <a id="pricing_interest_rate_type" href="#pricing_interest_rate_type"> Field 20: Interest rate type </a>
                    </h4>
                    <p>Rule section: 12 CFR 1002.107(a)(12)(i)</p>
                    <h5>Column name</h5>
                    pricing_interest_rate_type
                    <h5>Instructions</h5>
                    <ul>
                        <li>Field type: Single response</li>
                        <li>Required for all application records</li>
                    </ul>
                    <p>
                        Indicate the type of interest rate relevant to this transaction by entering one of the specified codes. If any code besides 999 is reported, use the subsequent fields to report the initial rate period, fixed rate
                        transaction information, and variable rate transaction information, as applicable.
                    </p>
                    <p></p>
                    <table class="o-table o-table--stack-on-small">
                        <thead>
                            <tr>
                                <th>Valid values</th>
                                <th>Codes</th>
                                <th>Instructions</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td data-label="Valid values">1</td>
                                <td data-label="Codes">Code 1 - The transaction has a variable interest rate and <b>does not</b> have an initial rate period</td>
                                <td data-label="Instructions"></td>
                            </tr>
                            <tr>
                                <td data-label="Valid values">2</td>
                                <td data-label="Codes">Code 2 - The transaction has a fixed interest rate and <b>does not</b> have an initial rate period</td>
                                <td data-label="Instructions"></td>
                            </tr>
                            <tr>
                                <td data-label="Valid values">3</td>
                                <td data-label="Codes">Code 3 - The transaction has an initial rate period greater than 12 months, during which the interest rate is variable</td>
                                <td data-label="Instructions"></td>
                            </tr>
                            <tr>
                                <td data-label="Valid values">4</td>
                                <td data-label="Codes">Code 4 - The transaction has an initial rate period greater than 12 months, during which the interest rate is fixed</td>
                                <td data-label="Instructions"></td>
                            </tr>
                            <tr>
                                <td data-label="Valid values">5</td>
                                <td data-label="Codes">Code 5 - The transaction has an initial rate period less than or equal to 12 months, after which the interest rate is variable</td>
                                <td data-label="Instructions"></td>
                            </tr>
                            <tr>
                                <td data-label="Valid values">6</td>
                                <td data-label="Codes">Code 6 - The transaction has an initial rate period less than or equal to 12 months, after which the interest rate is fixed</td>
                                <td data-label="Instructions"></td>
                            </tr>
                            <tr>
                                <td data-label="Valid values">999</td>
                                <td data-label="Codes">Code 999 - Not applicable</td>
                                <td data-label="Instructions">
                                    Enter code 999 if any of the following conditions apply:
                                    <ul>
                                        <li>The application is denied, withdrawn, or incomplete</li>
                                        <li>The originated or approved but not accepted transaction has no interest rate</li>
                                    </ul>
                                </td>
                            </tr>
                        </tbody>
                    </table>
                    <h5>Validations</h5>
                    <ul>
                        <li>Must equal 1, 2, 3, 4, 5, 6, or 999</li>
                    </ul>
                </div>
                <div class="o-fig__section--sub-sub" data-search-section="" data-scrollspy="pricing-information">
                    <h4 class="report-header o-fig__heading">
                        <a id="pricing_init_rate_period" href="#pricing_init_rate_period"> Field 21: Initial rate period </a>
                    </h4>
                    <p>Rule section: 12 CFR 1002.107(a)(12)(i)(B)</p>
                    <h5>Column name</h5>
                    pricing_init_rate_period
                    <h5>Instructions</h5>
                    <ul>
                        <li>Field type: Numeric</li>
                        <li>Conditionally required if 'interest rate type' is code 3, 4, 5, or 6. Leave blank if codes 3, 4, 5, or 6 are not entered.</li>
                    </ul>
                    <p>For originated credit and credit that is approved but not accepted, if the transaction has an initial rate period, enter, as a whole number, the length of the initial rate period expressed in months.</p>
                    <p></p>
                    <h5>Examples</h5>
                    <ul>
                        <li>24</li>
                    </ul>
                    <h5>Validations</h5>
                    <ul>
                        <li>When present, must be a whole number</li>
                        <li>When present, must be greater than 0</li>
                    </ul>
                </div>
                <div class="o-fig__section--sub-sub" data-search-section="" data-scrollspy="pricing-information">
                    <h4 class="report-header o-fig__heading">
                        <a id="pricing_fixed_rate" href="#pricing_fixed_rate"> Field 22: Fixed rate: interest rate </a>
                    </h4>
                    <p>Rule section: 12 CFR 1002.107(a)(12)(i)(A)</p>
                    <h5>Column name</h5>
                    pricing_fixed_rate
                    <h5>Instructions</h5>
                    <ul>
                        <li>Field type: Numeric</li>
                        <li>Conditionally required if 'interest rate type' is code 2, 4, or 6. Leave blank if codes 2, 4, or 6 are not entered.</li>
                    </ul>
                    <p>
                        For originated credit and credit that is approved but not accepted, that has a covered fixed rate component, enter the interest rate, as a percentage, to at least three (3) decimal places. Numbers calculated to
                        beyond three (3) decimal places may either be reported beyond three (3) decimal places or rounded or truncated to three (3) decimal places. Decimal place trailing zeros may be either included or omitted.
                    </p>
                    <p></p>
                    <h5>Examples</h5>
                    <ul>
                        <li>If 4.125%, enter 4.125</li>
                        <li>If 4.500%, enter 4.5, 4.50, or 4.500</li>
                    </ul>
                    <h5>Validations</h5>
                    <ul>
                        <li>When present, must be a numeric value</li>
                        <li>When present, should generally be greater than 0.1</li>
                    </ul>
                </div>
                <div class="o-fig__section--sub-sub" data-search-section="" data-scrollspy="pricing-information">
                    <h4 class="report-header o-fig__heading">
                        <a id="pricing_var_margin" href="#pricing_var_margin"> Field 23: Variable rate transaction: margin </a>
                    </h4>
                    <p>Rule section: 12 CFR 1002.107(a)(12)(i)(B)</p>
                    <h5>Column name</h5>
                    pricing_var_margin
                    <h5>Instructions</h5>
                    <ul>
                        <li>Field type: Numeric</li>
                        <li>Conditionally required if 'interest rate type' is code 1, 3, or 5. Leave blank if codes 1, 3, or 5 are not entered.</li>
                    </ul>
                    <p>
                        For originated credit and credit that is approved but not accepted, that has a covered variable rate component, enter the margin rate, as a percentage, to at least three (3) decimal places. Numbers calculated to
                        beyond three (3) decimal places may either be reported beyond three (3) decimal places or rounded or truncated to three (3) decimal places. Decimal place trailing zeros may be either included or omitted.
                    </p>
                    <p></p>
                    <h5>Examples</h5>
                    <ul>
                        <li>If 2.525%, enter 2.525</li>
                        <li>If 2.500%, enter 2.5, 2.50, or 2.500</li>
                    </ul>
                    <h5>Validations</h5>
                    <ul>
                        <li>When present, must be a numeric value</li>
                        <li>When present, should generally be greater than 0.1</li>
                    </ul>
                </div>
                <div class="o-fig__section--sub-sub" data-search-section="" data-scrollspy="pricing-information">
                    <h4 class="report-header o-fig__heading">
                        <a id="pricing_var_index_name" href="#pricing_var_index_name"> Field 24: Variable rate transaction: index name </a>
                    </h4>
                    <p>Rule section: 12 CFR 1002.107(a)(12)(i)(B)</p>
                    <h5>Column name</h5>
                    pricing_var_index_name
                    <h5>Instructions</h5>
                    <ul>
                        <li>Field type: Single response</li>
                        <li>Required for all application records</li>
                    </ul>
                    <p>For originated credit and credit that is approved but not accepted, that has a covered variable rate component, indicate the index name by entering one of the specified codes.</p>
                    <p></p>
                    <table class="o-table o-table--stack-on-small">
                        <thead>
                            <tr>
                                <th>Valid values</th>
                                <th>Codes</th>
                                <th>Instructions</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td data-label="Valid values">1</td>
                                <td data-label="Codes">Code 1 - Wall Street Journal Prime</td>
                                <td data-label="Instructions"></td>
                            </tr>
                            <tr>
                                <td data-label="Valid values">2</td>
                                <td data-label="Codes">Code 2 - 6-month CD rate</td>
                                <td data-label="Instructions"></td>
                            </tr>
                            <tr>
                                <td data-label="Valid values">3</td>
                                <td data-label="Codes">Code 3 - 1-year T-Bill</td>
                                <td data-label="Instructions"></td>
                            </tr>
                            <tr>
                                <td data-label="Valid values">4</td>
                                <td data-label="Codes">Code 4 - 3-year T-Bill</td>
                                <td data-label="Instructions"></td>
                            </tr>
                            <tr>
                                <td data-label="Valid values">5</td>
                                <td data-label="Codes">Code 5 - 5-year T-Note</td>
                                <td data-label="Instructions"></td>
                            </tr>
                            <tr>
                                <td data-label="Valid values">6</td>
                                <td data-label="Codes">Code 6 - 12-month average of 10-year T-Bill</td>
                                <td data-label="Instructions"></td>
                            </tr>
                            <tr>
                                <td data-label="Valid values">7</td>
                                <td data-label="Codes">Code 7 - Cost of Funds Index (COFI) - National</td>
                                <td data-label="Instructions"></td>
                            </tr>
                            <tr>
                                <td data-label="Valid values">8</td>
                                <td data-label="Codes">Code 8 - Cost of Funds Index (COFI) - 11th District</td>
                                <td data-label="Instructions"></td>
                            </tr>
                            <tr>
                                <td data-label="Valid values">9</td>
                                <td data-label="Codes">Code 9 - Constant Maturity Treasury (CMT)</td>
                                <td data-label="Instructions"></td>
                            </tr>
                            <tr>
                                <td data-label="Valid values">10</td>
                                <td data-label="Codes">Code 10 - Internal Proprietary Index</td>
                                <td data-label="Instructions"></td>
                            </tr>
                            <tr>
                                <td data-label="Valid values">977</td>
                                <td data-label="Codes">Code 977 - Other</td>
                                <td data-label="Instructions">When this code is entered, also specify the index name in the associated free-form text field.</td>
                            </tr>
                            <tr>
                                <td data-label="Valid values">999</td>
                                <td data-label="Codes">Code 999 - Not applicable</td>
                                <td data-label="Instructions">Enter code 999 if 'interest rate type' is not 1, 3, or 5.</td>
                            </tr>
                        </tbody>
                    </table>
                    <h5>Validations</h5>
                    <ul>
                        <li>Must equal 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 977 or 999</li>
                    </ul>
                </div>
                <div class="o-fig__section--sub-sub" data-search-section="" data-scrollspy="pricing-information">
                    <h4 class="report-header o-fig__heading">
                        <a id="pricing_var_index_name_ff" href="#pricing_var_index_name_ff"> Field 25: Variable rate transaction: index name: other </a>
                    </h4>
                    <p>Rule section: 12 CFR 1002.107(a)(12)(i)(B)</p>
                    <h5>Column name</h5>
                    pricing_var_index_name_ff
                    <h5>Instructions</h5>
                    <ul>
                        <li>Field type: Text (width up to 300 characters)</li>
                        <li>Conditionally required if 'variable rate transaction: index name' is code 977. Leave blank if code 977 is not entered.</li>
                    </ul>
                    <p>Specify in text the other index name if code 977 is entered.</p>
                    <p></p>
                    <h5>Validations</h5>
                    <ul>
                        <li>Must not exceed 300 characters in length</li>
                    </ul>
                </div>
                <div class="o-fig__section--sub-sub" data-search-section="" data-scrollspy="pricing-information">
                    <h4 class="report-header o-fig__heading">
                        <a id="pricing_var_index_value" href="#pricing_var_index_value"> Field 26: Variable rate transaction: index value </a>
                    </h4>
                    <p>Rule section: 12 CFR 1002.107(a)(12)(i)(B)</p>
                    <h5>Column name</h5>
                    pricing_var_index_value
                    <h5>Instructions</h5>
                    <ul>
                        <li>Field type: Numeric</li>
                        <li>Conditionally required if 'interest rate type' is code 1 or 3. Leave blank if codes 1 or 3 are not entered.</li>
                    </ul>
                    <p>
                        For originated credit and credit that is approved but not accepted, that has a covered variable rate component, enter the index value used to set the rate that is or would be applicable to the covered transaction, as
                        a percentage, to at least three (3) decimal places. Numbers calculated to beyond three (3) decimal places may either be reported beyond three (3) decimal places or rounded or truncated to three (3) decimal places.
                        Decimal place trailing zeros may be either included or omitted.
                    </p>
                    <p></p>
                    <h5>Examples</h5>
                    <ul>
                        <li>If 1.025%, enter 1.025</li>
                        <li>If 3.100%, enter 3.1, 3.10, or 3.100</li>
                    </ul>
                    <h5>Validations</h5>
                    <ul>
                        <li>When present, must be a numeric value</li>
                    </ul>
                </div>
                <div class="o-fig__section--sub-sub" data-search-section="" data-scrollspy="pricing-information">
                    <h4 class="report-header o-fig__heading">
                        <a id="pricing_origination_charges" href="#pricing_origination_charges"> Field 27: Total origination charges </a>
                    </h4>
                    <p>Rule section: 12 CFR 1002.107(a)(12)(ii)</p>
                    <h5>Column name</h5>
                    pricing_origination_charges
                    <h5>Instructions</h5>
                    <ul>
                        <li>Field type: Numeric</li>
                        <li>Conditionally required if 'action taken' is code 1 or 2. Report not applicable by leaving blank if codes 1 or 2 are not entered.</li>
                    </ul>
                    <p>
                        For originated credit and credit that is approved but not accepted, enter, in dollars, the amount of the total origination charges. Enter 0 if there are no origination charges associated with the application. Leave
                        blank if this is not applicable because the application is denied, withdrawn, or incomplete.
                    </p>
                    <p></p>
                    <h5>Examples</h5>
                    <ul>
                        <li>If $2,500, enter 2500 or 2500.00</li>
                        <li>If $2,582.91, enter 2582.91</li>
                        <li>If $0, enter 0</li>
                        <li>If -$100, enter -100</li>
                    </ul>
                    <h5>Validations</h5>
                    <ul>
                        <li>When present, must be a numeric value</li>
                    </ul>
                </div>
                <div class="o-fig__section--sub-sub" data-search-section="" data-scrollspy="pricing-information">
                    <h4 class="report-header o-fig__heading">
                        <a id="pricing_broker_fees" href="#pricing_broker_fees"> Field 28: Amount of total broker fees </a>
                    </h4>
                    <p>Rule section: 12 CFR 1002.107(a)(12)(iii)</p>
                    <h5>Column name</h5>
                    pricing_broker_fees
                    <h5>Instructions</h5>
                    <ul>
                        <li>Field type: Numeric</li>
                        <li>Conditionally required if 'action taken' is code 1 or 2. Report not applicable by leaving blank if codes 1 or 2 are not entered.</li>
                    </ul>
                    <p>
                        For originated credit and credit that is approved but not accepted, enter, in dollars, the amount of the total broker fees. Enter 0 if there are no broker fees associated with the application. Leave blank if this is
                        not applicable because the application is denied, withdrawn, or incomplete.
                    </p>
                    <p></p>
                    <h5>Examples</h5>
                    <ul>
                        <li>If $1,125, enter 1125 or 1125.00</li>
                        <li>If $1,125.76, enter 1125.76</li>
                        <li>If $0, enter 0</li>
                    </ul>
                    <h5>Validations</h5>
                    <ul>
                        <li>When present, must be a numeric value</li>
                    </ul>
                </div>
                <div class="o-fig__section--sub-sub" data-search-section="" data-scrollspy="pricing-information">
                    <h4 class="report-header o-fig__heading">
                        <a id="pricing_initial_charges" href="#pricing_initial_charges"> Field 29: Initial annual charges </a>
                    </h4>
                    <p>Rule section: 12 CFR 1002.107(a)(12)(iv)</p>
                    <h5>Column name</h5>
                    pricing_initial_charges
                    <h5>Instructions</h5>
                    <ul>
                        <li>Field type: Numeric</li>
                        <li>Conditionally required if 'action taken' is code 1 or 2. Report not applicable by leaving blank if codes 1 or 2 are not entered.</li>
                    </ul>
                    <p>
                        For originated credit and credit that is approved but not accepted, enter, in dollars, the amount of the total non-interest charges scheduled to be imposed over the first annual period. Enter 0 if there are no
                        non-interest charges scheduled to be imposed over the first annual period. Leave blank if this is not applicable because the application is denied, withdrawn, or incomplete.
                    </p>
                    <p></p>
                    <h5>Examples</h5>
                    <ul>
                        <li>If $1,034, enter 1034 or 1034.00</li>
                        <li>If $1,034.97, enter 1034.97</li>
                        <li>If $0, enter 0</li>
                    </ul>
                    <h5>Validations</h5>
                    <ul>
                        <li>When present, must be a numeric value</li>
                    </ul>
                </div>
                <div class="o-fig__section--sub-sub" data-search-section="" data-scrollspy="pricing-information">
                    <h4 class="report-header o-fig__heading">
                        <a id="pricing_mca_addcost_flag" href="#pricing_mca_addcost_flag"> Field 30: MCA/sales-based: additional cost for merchant cash advances or other sales-based financing: NA flag </a>
                    </h4>
                    <p>Rule section: 12 CFR 1002.107(a)(12)(v)</p>
                    <h5>Column name</h5>
                    pricing_mca_addcost_flag
                    <h5>Instructions</h5>
                    <ul>
                        <li>Field type: Single response</li>
                        <li>Required for all application records</li>
                    </ul>
                    <p>Indicate whether 'MCA/sales-based: additional cost for merchant cash advances or other sales-based financing' is applicable by entering one of the specified codes.</p>
                    <p></p>
                    <table class="o-table o-table--stack-on-small">
                        <thead>
                            <tr>
                                <th>Valid values</th>
                                <th>Codes</th>
                                <th>Instructions</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td data-label="Valid values">900</td>
                                <td data-label="Codes">Code 900 - Applicable</td>
                                <td data-label="Instructions"></td>
                            </tr>
                            <tr>
                                <td data-label="Valid values">999</td>
                                <td data-label="Codes">Code 999 - Not applicable</td>
                                <td data-label="Instructions">
                                    Enter code 999 if any of the following conditions apply:
                                    <ul>
                                        <li>The application is denied, withdrawn, or incomplete</li>
                                        <li>The approved transaction is not a merchant cash advance or other sales-based financing</li>
                                    </ul>
                                </td>
                            </tr>
                        </tbody>
                    </table>
                    <h5>Validations</h5>
                    <ul>
                        <li>Must equal 900 or 999</li>
                    </ul>
                </div>
                <div class="o-fig__section--sub-sub" data-search-section="" data-scrollspy="pricing-information">
                    <h4 class="report-header o-fig__heading">
                        <a id="pricing_mca_addcost" href="#pricing_mca_addcost"> Field 31: MCA/sales-based: additional cost for merchant cash advances or other sales-based financing </a>
                    </h4>
                    <p>Rule section: 12 CFR 1002.107(a)(12)(v)</p>
                    <h5>Column name</h5>
                    pricing_mca_addcost
                    <h5>Instructions</h5>
                    <ul>
                        <li>Field type: Numeric</li>
                        <li>Conditionally required if 'MCA/sales-based: additional cost for merchant cash advances or other sales-based financing: NA flag' is code 900. Leave blank if code 900 is not entered.</li>
                    </ul>
                    <p>
                        For originated credit and credit that is approved but not accepted, if a merchant cash advance or other sales-based financing transaction, enter, in dollars, the difference between the amount advanced and the amount
                        to be repaid.
                    </p>
                    <p></p>
                    <h5>Examples</h5>
                    <ul>
                        <li>If $3,500, enter 3500 or 3500.00</li>
                        <li>If $3,527.14, enter 3527.14</li>
                        <li>If $0, enter 0</li>
                    </ul>
                    <h5>Validations</h5>
                    <ul>
                        <li>When present, must be a numeric value</li>
                    </ul>
                </div>
                <div class="o-fig__section--sub-sub" data-search-section="" data-scrollspy="pricing-information">
                    <h4 class="report-header o-fig__heading">
                        <a id="pricing_prepenalty_allowed" href="#pricing_prepenalty_allowed"> Field 32: Prepayment penalty could be imposed </a>
                    </h4>
                    <p>Rule section: 12 CFR 1002.107(a)(12)(vi)(A)</p>
                    <h5>Column name</h5>
                    pricing_prepenalty_allowed
                    <h5>Instructions</h5>
                    <ul>
                        <li>Field type: Single response</li>
                        <li>Required for all application records</li>
                    </ul>
                    <p>For originated credit and credit that is approved but not accepted, indicate whether a prepayment penalty could be included under current policies and procedures by entering one of the specified codes.</p>
                    <p></p>
                    <table class="o-table o-table--stack-on-small">
                        <thead>
                            <tr>
                                <th>Valid values</th>
                                <th>Codes</th>
                                <th>Instructions</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td data-label="Valid values">1</td>
                                <td data-label="Codes">Code 1 - Yes</td>
                                <td data-label="Instructions"></td>
                            </tr>
                            <tr>
                                <td data-label="Valid values">2</td>
                                <td data-label="Codes">Code 2 - No</td>
                                <td data-label="Instructions"></td>
                            </tr>
                            <tr>
                                <td data-label="Valid values">999</td>
                                <td data-label="Codes">Code 999 - Not applicable</td>
                                <td data-label="Instructions">Enter code 999 if the application is denied, withdrawn, or incomplete.</td>
                            </tr>
                        </tbody>
                    </table>
                    <h5>Validations</h5>
                    <ul>
                        <li>Must equal 1, 2 or 999</li>
                    </ul>
                </div>
                <div class="o-fig__section--sub-sub" data-search-section="" data-scrollspy="pricing-information">
                    <h4 class="report-header o-fig__heading">
                        <a id="pricing_prepenalty_exists" href="#pricing_prepenalty_exists"> Field 33: Prepayment penalty exists </a>
                    </h4>
                    <p>Rule section: 12 CFR 1002.107(a)(12)(vi)(B)</p>
                    <h5>Column name</h5>
                    pricing_prepenalty_exists
                    <h5>Instructions</h5>
                    <ul>
                        <li>Field type: Single response</li>
                        <li>Required for all application records</li>
                    </ul>
                    <p>For originated credit and credit that is approved but not accepted, indicate whether the terms of the transaction include a prepayment penalty by entering one of the specified codes.</p>
                    <p></p>
                    <table class="o-table o-table--stack-on-small">
                        <thead>
                            <tr>
                                <th>Valid values</th>
                                <th>Codes</th>
                                <th>Instructions</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td data-label="Valid values">1</td>
                                <td data-label="Codes">Code 1 - Yes</td>
                                <td data-label="Instructions"></td>
                            </tr>
                            <tr>
                                <td data-label="Valid values">2</td>
                                <td data-label="Codes">Code 2 - No</td>
                                <td data-label="Instructions"></td>
                            </tr>
                            <tr>
                                <td data-label="Valid values">999</td>
                                <td data-label="Codes">Code 999 - Not applicable</td>
                                <td data-label="Instructions">Enter code 999 if the application is denied, withdrawn, or incomplete.</td>
                            </tr>
                        </tbody>
                    </table>
                    <h5>Validations</h5>
                    <ul>
                        <li>Must equal 1, 2 or 999</li>
                    </ul>
                </div>
                <div class="o-fig__section--sub" data-search-section="" data-scrollspy="census-tract">
                    <h3 class="report-header o-fig__heading">
                        <a id="census-tract" href="#census-tract"> 3.13 Census tract </a>
                    </h3>
                    <p>Rule section: 12 CFR 1002.107(a)(13)</p>
                    <p></p>
                </div>
                <div class="o-fig__section--sub-sub" data-search-section="" data-scrollspy="census-tract">
                    <h4 class="report-header o-fig__heading">
                        <a id="census_tract_adr_type" href="#census_tract_adr_type"> Field 34: Type of address </a>
                    </h4>
                    <h5>Column name</h5>
                    census_tract_adr_type
                    <h5>Instructions</h5>
                    <ul>
                        <li>Field type: Single response</li>
                        <li>Required for all application records</li>
                    </ul>
                    <p>Indicate the type of address or location used to determine the census tract by entering one of the specified codes.</p>
                    <p></p>
                    <table class="o-table o-table--stack-on-small">
                        <thead>
                            <tr>
                                <th>Valid values</th>
                                <th>Codes</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td data-label="Valid values">1</td>
                                <td data-label="Codes">Code 1 - Address or location where the loan proceeds will principally be applied</td>
                            </tr>
                            <tr>
                                <td data-label="Valid values">2</td>
                                <td data-label="Codes">Code 2 - Address or location of borrower's main office or headquarters</td>
                            </tr>
                            <tr>
                                <td data-label="Valid values">3</td>
                                <td data-label="Codes">Code 3 - Another address or location associated with the applicant</td>
                            </tr>
                            <tr>
                                <td data-label="Valid values">988</td>
                                <td data-label="Codes">Code 988 - Not provided by applicant and otherwise undetermined</td>
                            </tr>
                        </tbody>
                    </table>
                    <h5>Validations</h5>
                    <ul>
                        <li>Must equal 1, 2, 3 or 988</li>
                    </ul>
                </div>
                <div class="o-fig__section--sub-sub" data-search-section="" data-scrollspy="census-tract">
                    <h4 class="report-header o-fig__heading">
                        <a id="census_tract_number" href="#census_tract_number"> Field 35: Tract number </a>
                    </h4>
                    <h5>Column name</h5>
                    census_tract_number
                    <h5>Instructions</h5>
                    <ul>
                        <li>Field type: Special (width 11 characters)</li>
                        <li>Conditionally required if 'type of address' is code 1, 2, or 3. Leave blank if code 988 is entered.</li>
                    </ul>
                    <p>Enter the 11-digit census tract number as defined by the U.S. Census Bureau of the appropriate one of the following:</p>
                    <ul>
                        <li>Address where the loan proceeds will principally be applied, if known</li>
                        <li>If the proceeds address is not known, location of borrower's main office or headquarters</li>
                        <li>If neither of those addresses are known, another address or location associated with the applicant</li>
                    </ul>
                    Do not use decimals.
                    <p></p>
                    <h5>Examples</h5>
                    <ul>
                        <li>06037264000 (a census tract within Los Angeles County, CA)</li>
                    </ul>
                    <h5>Validations</h5>
                    <ul>
                        <li>When present, must be a GEOID with exactly 11 digits</li>
                        <li>When present, should be a valid census tract GEOID as defined by the U.S. Census Bureau</li>
                    </ul>
                </div>
                <div class="o-fig__section--sub" data-search-section="" data-scrollspy="gross-annual-revenue">
                    <h3 class="report-header o-fig__heading">
                        <a id="gross-annual-revenue" href="#gross-annual-revenue"> 3.14 Gross annual revenue </a>
                    </h3>
                    <p>Rule section: 12 CFR 1002.107(a)(14)</p>
                    <p></p>
                </div>
                <div class="o-fig__section--sub-sub" data-search-section="" data-scrollspy="gross-annual-revenue">
                    <h4 class="report-header o-fig__heading">
                        <a id="gross_annual_revenue_flag" href="#gross_annual_revenue_flag"> Field 36: Gross annual revenue: NP flag </a>
                    </h4>
                    <h5>Column name</h5>
                    gross_annual_revenue_flag
                    <h5>Instructions</h5>
                    <ul>
                        <li>Field type: Single response</li>
                        <li>Required for all application records</li>
                    </ul>
                    <p>Indicate whether 'gross annual revenue' is reported by entering one of the specified codes.</p>
                    <p></p>
                    <table class="o-table o-table--stack-on-small">
                        <thead>
                            <tr>
                                <th>Valid values</th>
                                <th>Codes</th>
                                <th>Instructions</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td data-label="Valid values">900</td>
                                <td data-label="Codes">Code 900 - Provided</td>
                                <td data-label="Instructions"></td>
                            </tr>
                            <tr>
                                <td data-label="Valid values">988</td>
                                <td data-label="Codes">Code 988 - Not provided by applicant and otherwise undetermined</td>
                                <td data-label="Instructions">Enter code 988 if gross annual revenue is not provided by applicant and is otherwise undetermined.</td>
                            </tr>
                        </tbody>
                    </table>
                    <h5>Validations</h5>
                    <ul>
                        <li>Must equal 900 or 988</li>
                    </ul>
                </div>
                <div class="o-fig__section--sub-sub" data-search-section="" data-scrollspy="gross-annual-revenue">
                    <h4 class="report-header o-fig__heading">
                        <a id="gross_annual_revenue" href="#gross_annual_revenue"> Field 37: Gross annual revenue </a>
                    </h4>
                    <h5>Column name</h5>
                    gross_annual_revenue
                    <h5>Instructions</h5>
                    <ul>
                        <li>Field type: Numeric</li>
                        <li>Conditionally required if 'gross annual revenue: NP flag' is code 900. Leave blank if code 900 is not entered.</li>
                    </ul>
                    <p>
                        Enter the dollar amount of the applicant's gross annual revenue for its preceding full fiscal year. A financial institution is permitted, but not required, to report the gross annual revenue for the applicant that
                        includes the revenue of affiliates as well. If a business has no gross annual revenue to report (e.g., a startup, a new line of business, and/or a business with a change in structure or ownership), the financial
                        institution would report that the applicant's gross annual revenue in its preceding full fiscal year is 0.
                    </p>
                    <p></p>
                    <h5>Examples</h5>
                    <ul>
                        <li>If $855,430, enter 855430 or 855430.00</li>
                        <li>If $855,430.17, enter 855430.17</li>
                        <li>If $0, enter 0</li>
                    </ul>
                    <h5>Validations</h5>
                    <ul>
                        <li>When present, must be a numeric value</li>
                    </ul>
                </div>
                <div class="o-fig__section--sub" data-search-section="" data-scrollspy="naics-code">
                    <h3 class="report-header o-fig__heading">
                        <a id="naics-code" href="#naics-code"> 3.15 North American Industry Classification System (NAICS) code </a>
                    </h3>
                    <p>Rule section: 12 CFR 1002.107(a)(15)</p>
                    <p></p>
                </div>
                <div class="o-fig__section--sub-sub" data-search-section="" data-scrollspy="naics-code">
                    <h4 class="report-header o-fig__heading">
                        <a id="naics_code_flag" href="#naics_code_flag"> Field 38: North American Industry Classification System (NAICS) code: NP flag </a>
                    </h4>
                    <h5>Column name</h5>
                    naics_code_flag
                    <h5>Instructions</h5>
                    <ul>
                        <li>Field type: Single response</li>
                        <li>Required for all application records</li>
                    </ul>
                    <p>Indicate whether NAICS code is provided by entering one of the specified codes.</p>
                    <p></p>
                    <table class="o-table o-table--stack-on-small">
                        <thead>
                            <tr>
                                <th>Valid values</th>
                                <th>Codes</th>
                                <th>Instructions</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td data-label="Valid values">900</td>
                                <td data-label="Codes">Code 900 - Reported</td>
                                <td data-label="Instructions"></td>
                            </tr>
                            <tr>
                                <td data-label="Valid values">988</td>
                                <td data-label="Codes">Code 988 - Not provided by applicant and otherwise undetermined</td>
                                <td data-label="Instructions">Enter code 988 if NAICS code is not provided by applicant and is otherwise undetermined.</td>
                            </tr>
                        </tbody>
                    </table>
                    <h5>Validations</h5>
                    <ul>
                        <li>Must equal 900 or 988</li>
                    </ul>
                </div>
                <div class="o-fig__section--sub-sub" data-search-section="" data-scrollspy="naics-code">
                    <h4 class="report-header o-fig__heading">
                        <a id="naics_code" href="#naics_code"> Field 39: North American Industry Classification System (NAICS) code </a>
                    </h4>
                    <h5>Column name</h5>
                    naics_code
                    <h5>Instructions</h5>
                    <ul>
                        <li>Field type: Special (width 3 characters)</li>
                        <li>Conditionally required if 'North American Industry Classification System (NAICS) code: NP flag' is code 900. Leave blank if code 900 is not entered.</li>
                    </ul>
                    <p>Enter a three-digit NAICS code appropriate for the applicant.</p>
                    <p></p>
                    <h5>Examples</h5>
                    <ul>
                        <li>311 (a business engaged in the food processing sector)</li>
                    </ul>
                    <h5>Validations</h5>
                    <ul>
                        <li>When present, must be exactly three numeric characters</li>
                        <li>When present, should be a valid NAICS code</li>
                    </ul>
                </div>
                <div class="o-fig__section--sub" data-search-section="" data-scrollspy="number-of-workers">
                    <h3 class="report-header o-fig__heading">
                        <a id="number-of-workers" href="#number-of-workers"> 3.16 Number of workers </a>
                    </h3>
                    <p>Rule section: 12 CFR 1002.107(a)(16)</p>
                    <p></p>
                </div>
                <div class="o-fig__section--sub-sub" data-search-section="" data-scrollspy="number-of-workers">
                    <h4 class="report-header o-fig__heading">
                        <a id="number_of_workers" href="#number_of_workers"> Field 40: Number of workers </a>
                    </h4>
                    <h5>Column name</h5>
                    number_of_workers
                    <h5>Instructions</h5>
                    <ul>
                        <li>Field type: Single response</li>
                        <li>Required for all application records</li>
                    </ul>
                    <p>
                        Indicate the range of the number of workers by entering one of the specified codes. Includes full-time, part-time, and seasonal workers as well as contractors working primarily for the applicant but does not include
                        principal owners.
                    </p>
                    <p></p>
                    <table class="o-table o-table--stack-on-small">
                        <thead>
                            <tr>
                                <th>Valid values</th>
                                <th>Codes</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td data-label="Valid values">1</td>
                                <td data-label="Codes">Code 1 - Firms with no workers</td>
                            </tr>
                            <tr>
                                <td data-label="Valid values">2</td>
                                <td data-label="Codes">Code 2 - Firms with 1 to 4 workers</td>
                            </tr>
                            <tr>
                                <td data-label="Valid values">3</td>
                                <td data-label="Codes">Code 3 - Firms with 5 to 9 workers</td>
                            </tr>
                            <tr>
                                <td data-label="Valid values">4</td>
                                <td data-label="Codes">Code 4 - Firms with 10 to 19 workers</td>
                            </tr>
                            <tr>
                                <td data-label="Valid values">5</td>
                                <td data-label="Codes">Code 5 - Firms with 20 to 49 workers</td>
                            </tr>
                            <tr>
                                <td data-label="Valid values">6</td>
                                <td data-label="Codes">Code 6 - Firms with 50 to 99 workers</td>
                            </tr>
                            <tr>
                                <td data-label="Valid values">7</td>
                                <td data-label="Codes">Code 7 - Firms with 100 to 249 workers</td>
                            </tr>
                            <tr>
                                <td data-label="Valid values">8</td>
                                <td data-label="Codes">Code 8 - Firms with 250 to 499 workers</td>
                            </tr>
                            <tr>
                                <td data-label="Valid values">9</td>
                                <td data-label="Codes">Code 9 - Firms with 500 workers or more</td>
                            </tr>
                            <tr>
                                <td data-label="Valid values">988</td>
                                <td data-label="Codes">Code 988 - Not provided by applicant and otherwise undetermined</td>
                            </tr>
                        </tbody>
                    </table>
                    <h5>Validations</h5>
                    <ul>
                        <li>Must equal 1, 2, 3, 4, 5, 6, 7, 8, 9 or 988</li>
                    </ul>
                </div>
                <div class="o-fig__section--sub" data-search-section="" data-scrollspy="time-in-business">
                    <h3 class="report-header o-fig__heading">
                        <a id="time-in-business" href="#time-in-business"> 3.17 Time in business </a>
                    </h3>
                    <p>Rule section: 12 CFR 1002.107(a)(17)</p>
                    <p></p>
                </div>
                <div class="o-fig__section--sub-sub" data-search-section="" data-scrollspy="time-in-business">
                    <h4 class="report-header o-fig__heading">
                        <a id="time_in_business_type" href="#time_in_business_type"> Field 41: Type of response </a>
                    </h4>
                    <h5>Column name</h5>
                    time_in_business_type
                    <h5>Instructions</h5>
                    <ul>
                        <li>Field type: Single response</li>
                        <li>Required for all application records</li>
                    </ul>
                    <p>Indicate whether the applicant provided information on 'time in business' by entering one of the specified codes.</p>
                    <p></p>
                    <table class="o-table o-table--stack-on-small">
                        <thead>
                            <tr>
                                <th>Valid values</th>
                                <th>Codes</th>
                                <th>Instructions</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td data-label="Valid values">1</td>
                                <td data-label="Codes">Code 1 - The number of years the applicant has been in business is collected or obtained by the financial institution</td>
                                <td data-label="Instructions">
                                    Enter code 1 If you collected or otherwise obtained the number of years the applicant has been in business. When this code is entered, also specify in the associated numeric entry field the number of
                                    whole years.
                                </td>
                            </tr>
                            <tr>
                                <td data-label="Valid values">2</td>
                                <td data-label="Codes">Code 2 - Applicant has been in business less than two years</td>
                                <td data-label="Instructions">
                                    Enter code 2 or 3 If you did not collect or otherwise obtain the number of years the applicant has been in business as determined by you or provided by the applicant, accordingly.
                                </td>
                            </tr>
                            <tr>
                                <td data-label="Valid values">3</td>
                                <td data-label="Codes">Code 3 - Applicant has been in business two or more years</td>
                                <td data-label="Instructions">
                                    Enter code 2 or 3 If you did not collect or otherwise obtain the number of years the applicant has been in business as determined by you or provided by the applicant, accordingly.
                                </td>
                            </tr>
                            <tr>
                                <td data-label="Valid values">988</td>
                                <td data-label="Codes">Code 988 - Not provided by applicant and otherwise undetermined</td>
                                <td data-label="Instructions"></td>
                            </tr>
                        </tbody>
                    </table>
                    <h5>Validations</h5>
                    <ul>
                        <li>Must equal 1, 2, 3, or 988</li>
                    </ul>
                </div>
                <div class="o-fig__section--sub-sub" data-search-section="" data-scrollspy="time-in-business">
                    <h4 class="report-header o-fig__heading">
                        <a id="time_in_business" href="#time_in_business"> Field 42: Time in business </a>
                    </h4>
                    <h5>Column name</h5>
                    time_in_business
                    <h5>Instructions</h5>
                    <ul>
                        <li>Field type: Numeric</li>
                        <li>Conditionally required if 'time in business: type of response' is code 1. Leave blank if code 1 is not entered.</li>
                    </ul>
                    <p>Enter the number of years the applicant has been in business, as collected or obtained by the financial institution, rounding down to the nearest whole number of years.</p>
                    <p></p>
                    <h5>Examples</h5>
                    <ul>
                        <li>12</li>
                    </ul>
                    <h5>Validations</h5>
                    <ul>
                        <li>When present, must be a whole number</li>
                        <li>When present, must be greater than or equal to 0</li>
                    </ul>
                </div>
                <div class="o-fig__section--sub" data-search-section="" data-scrollspy="minority-women-lgbtqi-owned-business-status">
                    <h3 class="report-header o-fig__heading">
                        <a id="minority-women-lgbtqi-owned-business-status" href="#minority-women-lgbtqi-owned-business-status"> 3.18 Minority-owned, women-owned, and LGBTQI+-owned business statuses </a>
                    </h3>
                    <p>Rule section: 12 CFR 1002.107(a)(18)</p>
                    <p></p>
                </div>
                <div class="o-fig__section--sub-sub" data-search-section="" data-scrollspy="minority-women-lgbtqi-owned-business-status">
                    <h4 class="report-header o-fig__heading">
                        <a id="business_ownership_status" href="#business_ownership_status"> Field 43: Business ownership status </a>
                    </h4>
                    <h5>Column name</h5>
                    business_ownership_status
                    <h5>Instructions</h5>
                    <ul>
                        <li>Field type: Multiple response</li>
                        <li>Required for all application records</li>
                    </ul>
                    <p>
                        Indicate whether the applicant is a minority-owned, women-owned, and/or LGBTQI+-owned business by entering, as appropriate, from the specified codes. Use the codes below to report the selections that the applicant
                        made (such as on the demographic data collection form), except where otherwise noted in 'Instructions'. If the applicant selects more than one applicable business ownership status, enter each, in any order, separated
                        by a semicolon. If the applicant reports that they are a women-owned, minority-owned, and/or LGBTQI+-owned business but also responds that they do not wish to provide this information, enter codes 1, 2, and/or 3 as
                        appropriate. Do not report code 966 if any other codes apply.
                    </p>
                    <p></p>
                    <h5>Examples</h5>
                    <ul>
                        <li>If women-owned, enter 2</li>
                        <li>If women-owned and LGBTQI+-owned, enter 2;3 or 3;2</li>
                        <li>If LGBTQI+-owned and the applicant responded that they did not wish to provide this information, enter 3</li>
                    </ul>
                    <table class="o-table o-table--stack-on-small">
                        <thead>
                            <tr>
                                <th>Valid values</th>
                                <th>Codes</th>
                                <th>Instructions</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td data-label="Valid values">1</td>
                                <td data-label="Codes">Code 1 - Minority-owned business</td>
                                <td data-label="Instructions"></td>
                            </tr>
                            <tr>
                                <td data-label="Valid values">2</td>
                                <td data-label="Codes">Code 2 - Women-owned business</td>
                                <td data-label="Instructions"></td>
                            </tr>
                            <tr>
                                <td data-label="Valid values">3</td>
                                <td data-label="Codes">Code 3 - LGBTQI+-owned business</td>
                                <td data-label="Instructions"></td>
                            </tr>
                            <tr>
                                <td data-label="Valid values">955</td>
                                <td data-label="Codes">Code 955 - None of these apply</td>
                                <td data-label="Instructions"></td>
                            </tr>
                            <tr>
                                <td data-label="Valid values">966</td>
                                <td data-label="Codes">Code 966 - The applicant responded that they did not wish to provide this information</td>
                                <td data-label="Instructions">Do not enter code 966 if the applicant selected any of the minority-owned business, women-owned business, or LGBTQI+-owned business response options.</td>
                            </tr>
                            <tr>
                                <td data-label="Valid values">988</td>
                                <td data-label="Codes">Code 988 - Not provided by applicant</td>
                                <td data-label="Instructions">Enter code 988 if the applicant does not select any response options.</td>
                            </tr>
                        </tbody>
                    </table>
                    <h5>Validations</h5>
                    <ul>
                        <li>Each value (separated by semicolons) must equal 1, 2, 3, 955, 966, or 988</li>
                        <li>Must contain at least one value</li>
                        <li>Should not contain duplicated values</li>
                        <li>When code 966 or 988 is reported, should not contain any other values</li>
                    </ul>
                </div>
                <div class="o-fig__section--sub" data-search-section="" data-scrollspy="number-of-principal-owners">
                    <h3 class="report-header o-fig__heading">
                        <a id="number-of-principal-owners" href="#number-of-principal-owners"> 3.19 Number of principal owners </a>
                    </h3>
                    <p>Rule section: 12 CFR 1002.107(a)(20)</p>
                    <p></p>
                </div>
                <div class="o-fig__section--sub-sub" data-search-section="" data-scrollspy="number-of-principal-owners">
                    <h4 class="report-header o-fig__heading">
                        <a id="num_principal_owners_flag" href="#num_principal_owners_flag"> Field 44: Number of principal owners: NP flag </a>
                    </h4>
                    <h5>Column name</h5>
                    num_principal_owners_flag
                    <h5>Instructions</h5>
                    <ul>
                        <li>Field type: Single response</li>
                        <li>Required for all application records</li>
                    </ul>
                    <p>Indicate whether number of principal owners is provided by entering one of the specified codes.</p>
                    <p></p>
                    <table class="o-table o-table--stack-on-small">
                        <thead>
                            <tr>
                                <th>Valid values</th>
                                <th>Codes</th>
                                <th>Instructions</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td data-label="Valid values">900</td>
                                <td data-label="Codes">Code 900 - Reported</td>
                                <td data-label="Instructions"></td>
                            </tr>
                            <tr>
                                <td data-label="Valid values">988</td>
                                <td data-label="Codes">Code 988 - Not provided by applicant and otherwise undetermined</td>
                                <td data-label="Instructions">Enter code 988 if number of principal owners is not provided by applicant and otherwise undetermined.</td>
                            </tr>
                        </tbody>
                    </table>
                    <h5>Validations</h5>
                    <ul>
                        <li>Must equal 900 or 988</li>
                    </ul>
                </div>
                <div class="o-fig__section--sub-sub" data-search-section="" data-scrollspy="number-of-principal-owners">
                    <h4 class="report-header o-fig__heading">
                        <a id="num_principal_owners" href="#num_principal_owners"> Field 45: Number of principal owners </a>
                    </h4>
                    <h5>Column name</h5>
                    num_principal_owners
                    <h5>Instructions</h5>
                    <ul>
                        <li>Field type: Single response</li>
                        <li>Conditionally required if 'number of principal owners: NP flag' is code 900. Leave blank if code 900 is not entered.</li>
                    </ul>
                    <p>Enter the number of the applicant's principal owners. If no principal owner has at least 25% ownership of the business, enter 0.</p>
                    <p></p>
                    <h5>Validations</h5>
                    <ul>
                        <li>When present, must equal 0, 1, 2, 3, or 4</li>
                    </ul>
                </div>
                <div class="o-fig__section--sub" data-search-section="" data-scrollspy="rse-of-principal-owner-1">
                    <h3 class="report-header o-fig__heading">
                        <a id="rse-of-principal-owner-1" href="#rse-of-principal-owner-1"> 3.20 Demographic information of principal owner 1 </a>
                    </h3>
                    <p>Rule section: 12 CFR 1002.107(a)(19)</p>
                    <p></p>
                    <ul class="m-list m-list--links">
                        <li class="m-list__item">
                            <a href="#po_1_ethnicity"> Field 46: Ethnicity of principal owner 1 </a>
                        </li>
                        <li class="m-list__item">
                            <a href="#po_1_ethnicity_ff"> Field 47: Ethnicity of principal owner 1: free-form text field for other Hispanic or Latino ethnicity </a>
                        </li>
                        <li class="m-list__item">
                            <a href="#po_1_race"> Field 48: Race of principal owner 1 </a>
                        </li>
                        <li class="m-list__item">
                            <a href="#po_1_race_anai_ff"> Field 49: Race of principal owner 1: free-form text field for American Indian or Alaska Native Enrolled or Principal Tribe </a>
                        </li>
                        <li class="m-list__item">
                            <a href="#po_1_race_asian_ff"> Field 50: Race of principal owner 1: free-form text field for other Asian race </a>
                        </li>
                        <li class="m-list__item">
                            <a href="#po_1_race_baa_ff"> Field 51: Race of principal owner 1: free-form text field for other Black or African American race </a>
                        </li>
                        <li class="m-list__item">
                            <a href="#po_1_race_pi_ff"> Field 52: Race of principal owner 1: free-form text field for other Pacific Islander race </a>
                        </li>
                        <li class="m-list__item">
                            <a href="#po_1_gender_flag"> Field 53: Sex/gender of principal owner 1: NP flag </a>
                        </li>
                        <li class="m-list__item">
                            <a href="#po_1_gender_ff"> Field 54: Sex/gender of principal owner 1: free-form text field for self-identified sex/gender </a>
                        </li>
                    </ul>
                </div>
                <div class="o-fig__section--sub-sub" data-search-section="" data-scrollspy="rse-of-principal-owner-1">
                    <h4 class="report-header o-fig__heading">
                        <a id="po_1_ethnicity" href="#po_1_ethnicity"> Field 46: Ethnicity of principal owner 1 </a>
                    </h4>
                    <h5>Column name</h5>
                    po_1_ethnicity
                    <h5>Instructions</h5>
                    <ul>
                        <li>Field type: Multiple response</li>
                        <li>Conditionally required if there is at least one principal owner. Report not applicable by leaving blank if there are no principal owners.</li>
                    </ul>
                    <p>
                        Indicate the ethnicity of the applicant's principal owner 1 by entering, as appropriate, from the specified codes. Use the codes below to report the selections that the applicant made (such as on the demographic data
                        collection form), except where otherwise noted in 'Instructions'. If the applicant selects more than one ethnicity for a principal owner, enter each, in any order, separated by a semicolon. If the applicant selects
                        an ethnicity for a principal owner or responds in the free-form text field but also responds that they do not wish to provide this information, enter the ethnicity codes (1, 11, 12, 13, 14, 2, and/or 977) as
                        appropriate. Do not report code 966 if any other codes apply. If an applicant responds in the free-form text field, but does not select Other Hispanic or Latino, you are permitted, but not required, to report Other
                        Hispanic or Latino.
                    </p>
                    <p></p>
                    <h5>Examples</h5>
                    <ul>
                        <li>If Mexican, enter 12</li>
                        <li>If Mexican and Puerto Rican, enter 12;13 or 13;12</li>
                        <li>If Mexican and the applicant responded that they did not wish to provide this information, enter 12</li>
                        <li>If responded Argentinean in the free form-text field but the applicant did not select Other Hispanic or Latino ethnicity, enter 977. May also enter 14.</li>
                    </ul>
                    <table class="o-table o-table--stack-on-small">
                        <thead>
                            <tr>
                                <th>Valid values</th>
                                <th>Codes</th>
                                <th>Instructions</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td data-label="Valid values">1</td>
                                <td data-label="Codes">Code 1 - Hispanic or Latino</td>
                                <td data-label="Instructions"></td>
                            </tr>
                            <tr>
                                <td data-label="Valid values">11</td>
                                <td data-label="Codes">Code 11 - Cuban</td>
                                <td data-label="Instructions"></td>
                            </tr>
                            <tr>
                                <td data-label="Valid values">12</td>
                                <td data-label="Codes">Code 12 - Mexican</td>
                                <td data-label="Instructions"></td>
                            </tr>
                            <tr>
                                <td data-label="Valid values">13</td>
                                <td data-label="Codes">Code 13 - Puerto Rican</td>
                                <td data-label="Instructions"></td>
                            </tr>
                            <tr>
                                <td data-label="Valid values">14</td>
                                <td data-label="Codes">Code 14 - Other Hispanic or Latino Ethnicity</td>
                                <td data-label="Instructions"></td>
                            </tr>
                            <tr>
                                <td data-label="Valid values">2</td>
                                <td data-label="Codes">Code 2 - Not Hispanic or Latino</td>
                                <td data-label="Instructions"></td>
                            </tr>
                            <tr>
                                <td data-label="Valid values">966</td>
                                <td data-label="Codes">Code 966 - The applicant responded that they did not wish to provide this information</td>
                                <td data-label="Instructions">Do not enter code 966 if the applicant selected any of the ethnicity response options.</td>
                            </tr>
                            <tr>
                                <td data-label="Valid values">977</td>
                                <td data-label="Codes">Code 977 - The applicant responded in the free-form text field</td>
                                <td data-label="Instructions">When this code is entered, also specify the applicant's response in the associated free-form text field for other Hispanic or Latino.</td>
                            </tr>
                            <tr>
                                <td data-label="Valid values">988</td>
                                <td data-label="Codes">Code 988 - Not provided by applicant</td>
                                <td data-label="Instructions">Enter code 988 if the applicant does not select any response options and does not respond in the free-form text field.</td>
                            </tr>
                        </tbody>
                    </table>
                    <h5>Validations</h5>
                    <ul>
                        <li>When present, each value (separated by semicolons) must equal 1, 11, 12, 13, 14, 2, 966, 977, or 988</li>
                        <li>Should not contain duplicated values</li>
                        <li>When code 966 or 988 is reported, should not contain any other values</li>
                    </ul>
                </div>
                <div class="o-fig__section--sub-sub" data-search-section="" data-scrollspy="rse-of-principal-owner-1">
                    <h4 class="report-header o-fig__heading">
                        <a id="po_1_ethnicity_ff" href="#po_1_ethnicity_ff"> Field 47: Ethnicity of principal owner 1: free-form text field for other Hispanic or Latino ethnicity </a>
                    </h4>
                    <h5>Column name</h5>
                    po_1_ethnicity_ff
                    <h5>Instructions</h5>
                    <ul>
                        <li>Field type: Text (width up to 300 characters)</li>
                        <li>Conditionally required if 'ethnicity of principal owner 1' contains code 977. Report not applicable by leaving blank if code 977 is not entered.</li>
                    </ul>
                    <p>Specify in text the other Hispanic or Latino ethnicity if code 977 is entered. Otherwise, leave this data field blank.</p>
                    <p></p>
                    <h5>Examples</h5>
                    <ul>
                        <li>Guatemalan</li>
                    </ul>
                    <h5>Validations</h5>
                    <ul>
                        <li>Must not exceed 300 characters in length</li>
                    </ul>
                </div>
                <div class="o-fig__section--sub-sub" data-search-section="" data-scrollspy="rse-of-principal-owner-1">
                    <h4 class="report-header o-fig__heading">
                        <a id="po_1_race" href="#po_1_race"> Field 48: Race of principal owner 1 </a>
                    </h4>
                    <h5>Column name</h5>
                    po_1_race
                    <h5>Instructions</h5>
                    <ul>
                        <li>Field type: Multiple response</li>
                        <li>Conditionally required if there is at least one principal owner. Report not applicable by leaving blank if there are no principal owners.</li>
                    </ul>
                    <p>
                        Indicate the race of the applicant's principal owner 1 by entering, as appropriate, from the specified codes. Use the codes below to report the selections that the applicant made (such as on the demographic data
                        collection form), except where otherwise noted in 'Instructions'. If the applicant selects more than one race for a principal owner, enter each, in any order, separated by a semicolon. If the applicant selects a race
                        for a principal owner or responds in a free-form text field but also responds that they do not wish to provide this information, enter the race codes (1, 2, 21, 22, 23, 24, 25, 26, 27, 3, 31, 32, 33, 34, 35, 36, 37,
                        4, 41, 42, 43, 44, 5, 971, 972, 973, and/or 974) as appropriate. Do not report code 966 if any other codes apply.
                    </p>
                    <p></p>
                    <h5>Examples</h5>
                    <ul>
                        <li>If Haitian and White, enter 33;5 or 5;33</li>
                        <li>If Asian and the applicant responded that they did not wish to provide this information, enter 2.</li>
                        <li>If responded Thai in the free form-text field for other Asian race but the applicant did not select Other Asian race, enter 972. May also enter 27.</li>
                    </ul>
                    <table class="o-table o-table--stack-on-small">
                        <thead>
                            <tr>
                                <th>Valid values</th>
                                <th>Codes</th>
                                <th>Instructions</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td data-label="Valid values">1</td>
                                <td data-label="Codes">Code 1 - American Indian or Alaska Native</td>
                                <td data-label="Instructions"></td>
                            </tr>
                            <tr>
                                <td data-label="Valid values">2</td>
                                <td data-label="Codes">Code 2 - Asian</td>
                                <td data-label="Instructions"></td>
                            </tr>
                            <tr>
                                <td data-label="Valid values">21</td>
                                <td data-label="Codes">Code 21 - Asian Indian</td>
                                <td data-label="Instructions"></td>
                            </tr>
                            <tr>
                                <td data-label="Valid values">22</td>
                                <td data-label="Codes">Code 22 - Chinese</td>
                                <td data-label="Instructions"></td>
                            </tr>
                            <tr>
                                <td data-label="Valid values">23</td>
                                <td data-label="Codes">Code 23 - Filipino</td>
                                <td data-label="Instructions"></td>
                            </tr>
                            <tr>
                                <td data-label="Valid values">24</td>
                                <td data-label="Codes">Code 24 - Japanese</td>
                                <td data-label="Instructions"></td>
                            </tr>
                            <tr>
                                <td data-label="Valid values">25</td>
                                <td data-label="Codes">Code 25 - Korean</td>
                                <td data-label="Instructions"></td>
                            </tr>
                            <tr>
                                <td data-label="Valid values">26</td>
                                <td data-label="Codes">Code 26 - Vietnamese</td>
                                <td data-label="Instructions"></td>
                            </tr>
                            <tr>
                                <td data-label="Valid values">27</td>
                                <td data-label="Codes">Code 27 - Other Asian Race</td>
                                <td data-label="Instructions"></td>
                            </tr>
                            <tr>
                                <td data-label="Valid values">3</td>
                                <td data-label="Codes">Code 3 - Black or African American</td>
                                <td data-label="Instructions"></td>
                            </tr>
                            <tr>
                                <td data-label="Valid values">31</td>
                                <td data-label="Codes">Code 31 - African American</td>
                                <td data-label="Instructions"></td>
                            </tr>
                            <tr>
                                <td data-label="Valid values">32</td>
                                <td data-label="Codes">Code 32 - Ethiopian</td>
                                <td data-label="Instructions"></td>
                            </tr>
                            <tr>
                                <td data-label="Valid values">33</td>
                                <td data-label="Codes">Code 33 - Haitian</td>
                                <td data-label="Instructions"></td>
                            </tr>
                            <tr>
                                <td data-label="Valid values">34</td>
                                <td data-label="Codes">Code 34 - Jamaican</td>
                                <td data-label="Instructions"></td>
                            </tr>
                            <tr>
                                <td data-label="Valid values">35</td>
                                <td data-label="Codes">Code 35 - Nigerian</td>
                                <td data-label="Instructions"></td>
                            </tr>
                            <tr>
                                <td data-label="Valid values">36</td>
                                <td data-label="Codes">Code 36 - Somali</td>
                                <td data-label="Instructions"></td>
                            </tr>
                            <tr>
                                <td data-label="Valid values">37</td>
                                <td data-label="Codes">Code 37 - Other Black or African American Race</td>
                                <td data-label="Instructions"></td>
                            </tr>
                            <tr>
                                <td data-label="Valid values">4</td>
                                <td data-label="Codes">Code 4 - Native Hawaiian or Other Pacific Islander</td>
                                <td data-label="Instructions"></td>
                            </tr>
                            <tr>
                                <td data-label="Valid values">41</td>
                                <td data-label="Codes">Code 41 - Guamanian or Chamorro</td>
                                <td data-label="Instructions"></td>
                            </tr>
                            <tr>
                                <td data-label="Valid values">42</td>
                                <td data-label="Codes">Code 42 - Native Hawaiian</td>
                                <td data-label="Instructions"></td>
                            </tr>
                            <tr>
                                <td data-label="Valid values">43</td>
                                <td data-label="Codes">Code 43 - Samoan</td>
                                <td data-label="Instructions"></td>
                            </tr>
                            <tr>
                                <td data-label="Valid values">44</td>
                                <td data-label="Codes">Code 44 - Other Pacific Islander Race</td>
                                <td data-label="Instructions"></td>
                            </tr>
                            <tr>
                                <td data-label="Valid values">5</td>
                                <td data-label="Codes">Code 5 - White</td>
                                <td data-label="Instructions"></td>
                            </tr>
                            <tr>
                                <td data-label="Valid values">966</td>
                                <td data-label="Codes">Code 966 - The applicant responded that they did not wish to provide this information</td>
                                <td data-label="Instructions">Do not enter code 966 if the applicant selected any of the race response options.</td>
                            </tr>
                            <tr>
                                <td data-label="Valid values">971</td>
                                <td data-label="Codes">Code 971 - The applicant responded in the free-form text field for American Indian or Alaska Native Enrolled or Principal Tribe</td>
                                <td data-label="Instructions">When this code is entered, also specify the applicant's response in the associated free-form text field for American Indian or Alaska Native Enrolled or Principal Tribe.</td>
                            </tr>
                            <tr>
                                <td data-label="Valid values">972</td>
                                <td data-label="Codes">Code 972 - The applicant responded in the free-form text field for Other Asian race</td>
                                <td data-label="Instructions">When this code is entered, also specify the applicant's response in the associated free-form text field for other Asian race.</td>
                            </tr>
                            <tr>
                                <td data-label="Valid values">973</td>
                                <td data-label="Codes">Code 973 - The applicant responded in the free-form text field for Other Black or African race</td>
                                <td data-label="Instructions">When this code is entered, also specify the applicant's response in the associated free-form text field for other Black or African race.</td>
                            </tr>
                            <tr>
                                <td data-label="Valid values">974</td>
                                <td data-label="Codes">Code 974 - The applicant responded in the free-form text field for Other Pacific Islander race</td>
                                <td data-label="Instructions">When this code is entered, also specify the applicant's response in the associated free-form text field for other Pacific Islander race.</td>
                            </tr>
                            <tr>
                                <td data-label="Valid values">988</td>
                                <td data-label="Codes">Code 988 - Not provided by applicant</td>
                                <td data-label="Instructions">Enter code 988 if the applicant does not select any response options and does not respond in the free-form text field.</td>
                            </tr>
                        </tbody>
                    </table>
                    <h5>Validations</h5>
                    <ul>
                        <li>When present, each value (separated by semicolons) must equal 1, 2, 21, 22, 23, 24, 25, 26, 27, 3, 31, 32, 33, 34, 35, 36, 37, 4, 41, 42, 43, 44, 5, 966, 971, 972, 973, 974, or 988</li>
                        <li>Should not contain duplicated values</li>
                        <li>When code 966 or 988 is reported, should not contain any other values</li>
                    </ul>
                </div>
                <div class="o-fig__section--sub-sub" data-search-section="" data-scrollspy="rse-of-principal-owner-1">
                    <h4 class="report-header o-fig__heading">
                        <a id="po_1_race_anai_ff" href="#po_1_race_anai_ff"> Field 49: Race of principal owner 1: free-form text field for American Indian or Alaska Native Enrolled or Principal Tribe </a>
                    </h4>
                    <h5>Column name</h5>
                    po_1_race_anai_ff
                    <h5>Instructions</h5>
                    <ul>
                        <li>Field type: Text (width up to 300 characters)</li>
                        <li>Conditionally required if 'race of principal owner 1' contains code 971. Report not applicable by leaving blank if code 971 is not entered</li>
                    </ul>
                    <p>Specify in text the principal owner 1's American Indian or Alaska Native Enrolled or Principal Tribe if provided by the applicant. Otherwise, leave this data field blank.</p>
                    <p></p>
                    <h5>Examples</h5>
                    <ul>
                        <li>Navajo</li>
                    </ul>
                    <h5>Validations</h5>
                    <ul>
                        <li>Must not exceed 300 characters in length</li>
                    </ul>
                </div>
                <div class="o-fig__section--sub-sub" data-search-section="" data-scrollspy="rse-of-principal-owner-1">
                    <h4 class="report-header o-fig__heading">
                        <a id="po_1_race_asian_ff" href="#po_1_race_asian_ff"> Field 50: Race of principal owner 1: free-form text field for other Asian race </a>
                    </h4>
                    <h5>Column name</h5>
                    po_1_race_asian_ff
                    <h5>Instructions</h5>
                    <ul>
                        <li>Field type: Text (width up to 300 characters)</li>
                        <li>Conditionally required if 'race of principal owner 1' contains code 972. Report not applicable by leaving blank if code 972 is not entered</li>
                    </ul>
                    <p>Specify in text the principal owner 1's other Asian race(s) if provided by the applicant. Otherwise, leave this data field blank.</p>
                    <p></p>
                    <h5>Examples</h5>
                    <ul>
                        <li>Cambodian</li>
                    </ul>
                    <h5>Validations</h5>
                    <ul>
                        <li>Must not exceed 300 characters in length</li>
                    </ul>
                </div>
                <div class="o-fig__section--sub-sub" data-search-section="" data-scrollspy="rse-of-principal-owner-1">
                    <h4 class="report-header o-fig__heading">
                        <a id="po_1_race_baa_ff" href="#po_1_race_baa_ff"> Field 51: Race of principal owner 1: free-form text field for other Black or African American race </a>
                    </h4>
                    <h5>Column name</h5>
                    po_1_race_baa_ff
                    <h5>Instructions</h5>
                    <ul>
                        <li>Field type: Text (width up to 300 characters)</li>
                        <li>Conditionally required if 'race of principal owner 1' contains code 973. Report not applicable by leaving blank if code 973 is not entered</li>
                    </ul>
                    <p>Specify in text the principal owner 1's other Black or African American race(s) if provided by the applicant. Otherwise, leave this data field blank.</p>
                    <p></p>
                    <h5>Examples</h5>
                    <ul>
                        <li>Malawian</li>
                    </ul>
                    <h5>Validations</h5>
                    <ul>
                        <li>Must not exceed 300 characters in length</li>
                    </ul>
                </div>
                <div class="o-fig__section--sub-sub" data-search-section="" data-scrollspy="rse-of-principal-owner-1">
                    <h4 class="report-header o-fig__heading">
                        <a id="po_1_race_pi_ff" href="#po_1_race_pi_ff"> Field 52: Race of principal owner 1: free-form text field for other Pacific Islander race </a>
                    </h4>
                    <h5>Column name</h5>
                    po_1_race_pi_ff
                    <h5>Instructions</h5>
                    <ul>
                        <li>Field type: Text (width up to 300 characters)</li>
                        <li>Conditionally required if 'race of principal owner 1' contains code 974. Report not applicable by leaving blank if code 974 is not entered</li>
                    </ul>
                    <p>Specify in text the principal owner 1's other Pacific Islander race(s) if provided by the applicant. Otherwise, leave this data field blank.</p>
                    <p></p>
                    <h5>Examples</h5>
                    <ul>
                        <li>Marshallese</li>
                    </ul>
                    <h5>Validations</h5>
                    <ul>
                        <li>Must not exceed 300 characters in length</li>
                    </ul>
                </div>
                <div class="o-fig__section--sub-sub" data-search-section="" data-scrollspy="rse-of-principal-owner-1">
                    <h4 class="report-header o-fig__heading">
                        <a id="po_1_gender_flag" href="#po_1_gender_flag"> Field 53: Sex/gender of principal owner 1: NP flag </a>
                    </h4>
                    <h5>Column name</h5>
                    po_1_gender_flag
                    <h5>Instructions</h5>
                    <ul>
                        <li>Field type: Single response</li>
                        <li>Conditionally required if there is at least one principal owner. Report not applicable by leaving blank if there are no principal owners.</li>
                    </ul>
                    <p>
                        Indicate whether the sex/gender of the applicant's principal owner 1 is provided (such as on the demographic data collection form) by entering one of the specified codes. If the applicant responds in the free-form
                        text field but also responds that they do not wish to provide this information, enter the sex/gender code 1, not code 966.
                    </p>
                    <p></p>
                    <h5>Examples</h5>
                    <ul>
                        <li>If the applicant responded in free-form text field and also responded that they did not wish to provide this information, enter 1.</li>
                    </ul>
                    <table class="o-table o-table--stack-on-small">
                        <thead>
                            <tr>
                                <th>Valid values</th>
                                <th>Codes</th>
                                <th>Instructions</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td data-label="Valid values">1</td>
                                <td data-label="Codes">Code 1 - The applicant responded in the free-form text field</td>
                                <td data-label="Instructions">When this code is entered, also specify the applicant's response in the associated free-form text field for self-identified sex/gender.</td>
                            </tr>
                            <tr>
                                <td data-label="Valid values">966</td>
                                <td data-label="Codes">Code 966 - The applicant responded that they did not wish to provide this information</td>
                                <td data-label="Instructions">Do not enter code 966 if the applicant responds in the free-form text field.</td>
                            </tr>
                            <tr>
                                <td data-label="Valid values">988</td>
                                <td data-label="Codes">Code 988 - Not provided by applicant</td>
                                <td data-label="Instructions">Enter code 988 if the applicant does not select any response options and does not respond in the free-form text field.</td>
                            </tr>
                        </tbody>
                    </table>
                    <h5>Validations</h5>
                    <ul>
                        <li>When present, must equal 1, 966, or 988</li>
                    </ul>
                </div>
                <div class="o-fig__section--sub-sub" data-search-section="" data-scrollspy="rse-of-principal-owner-1">
                    <h4 class="report-header o-fig__heading">
                        <a id="po_1_gender_ff" href="#po_1_gender_ff"> Field 54: Sex/gender of principal owner 1: free-form text field for self-identified sex/gender </a>
                    </h4>
                    <h5>Column name</h5>
                    po_1_gender_ff
                    <h5>Instructions</h5>
                    <ul>
                        <li>Field type: Text (width up to 300 characters)</li>
                        <li>Conditionally required if 'sex/gender of principal owner 1' is code 1. Report not applicable by leaving blank if code 1 is not entered.</li>
                    </ul>
                    <p>Specify in text the principal owner 1's self-identified sex/gender if provided by the applicant. Otherwise, leave this data field blank.</p>
                    <p></p>
                    <h5>Validations</h5>
                    <ul>
                        <li>Must not exceed 300 characters in length</li>
                    </ul>
                </div>
                <div class="o-fig__section--sub" data-search-section="" data-scrollspy="rse-of-principal-owner-2">
                    <h3 class="report-header o-fig__heading">
                        <a id="rse-of-principal-owner-2" href="#rse-of-principal-owner-2"> 3.21 Demographic information of principal owner 2 </a>
                    </h3>
                    <p>Rule section: 12 CFR 1002.107(a)(19)</p>
                    <p></p>
                    <ul class="m-list m-list--links">
                        <li class="m-list__item">
                            <a href="#po_2_ethnicity"> Field 55: Ethnicity of principal owner 2 </a>
                        </li>
                        <li class="m-list__item">
                            <a href="#po_2_ethnicity_ff"> Field 56: Ethnicity of principal owner 2: free-form text field for other Hispanic or Latino ethnicity </a>
                        </li>
                        <li class="m-list__item">
                            <a href="#po_2_race"> Field 57: Race of principal owner 2 </a>
                        </li>
                        <li class="m-list__item">
                            <a href="#po_2_race_anai_ff"> Field 58: Race of principal owner 2: free-form text field for American Indian or Alaska Native Enrolled or Principal Tribe </a>
                        </li>
                        <li class="m-list__item">
                            <a href="#po_2_race_asian_ff"> Field 59: Race of principal owner 2: free-form text field for other Asian race </a>
                        </li>
                        <li class="m-list__item">
                            <a href="#po_2_race_baa_ff"> Field 60: Race of principal owner 2: free-form text field for other Black or African American race </a>
                        </li>
                        <li class="m-list__item">
                            <a href="#po_2_race_pi_ff"> Field 61: Race of principal owner 2: free-form text field for other Pacific Islander race </a>
                        </li>
                        <li class="m-list__item">
                            <a href="#po_2_gender_flag"> Field 62: Sex/gender of principal owner 2: NP flag </a>
                        </li>
                        <li class="m-list__item">
                            <a href="#po_2_gender_ff"> Field 63: Sex/gender of principal owner 2: free-form text field for self-identified sex/gender </a>
                        </li>
                    </ul>
                </div>
                <div class="o-fig__section--sub-sub" data-search-section="" data-scrollspy="rse-of-principal-owner-2">
                    <h4 class="report-header o-fig__heading">
                        <a id="po_2_ethnicity" href="#po_2_ethnicity"> Field 55: Ethnicity of principal owner 2 </a>
                    </h4>
                    <h5>Column name</h5>
                    po_2_ethnicity
                    <h5>Instructions</h5>
                    <ul>
                        <li>Field type: Multiple response</li>
                        <li>Conditionally required if there are at least two principal owners. Report not applicable by leaving blank if there are fewer than two principal owners.</li>
                    </ul>
                    <p>
                        <a href="#po_1_ethnicity">For details, see ethnicity of principal owner 1 (Field 46)</a>
                    </p>
                    <p></p>
                </div>
                <div class="o-fig__section--sub-sub" data-search-section="" data-scrollspy="rse-of-principal-owner-2">
                    <h4 class="report-header o-fig__heading">
                        <a id="po_2_ethnicity_ff" href="#po_2_ethnicity_ff"> Field 56: Ethnicity of principal owner 2: free-form text field for other Hispanic or Latino ethnicity </a>
                    </h4>
                    <h5>Column name</h5>
                    po_2_ethnicity_ff
                    <h5>Instructions</h5>
                    <ul>
                        <li>Field type: Text (width up to 300 characters)</li>
                        <li>Conditionally required if 'ethnicity of principal owner 2' contains code 977. Leave blank if code 977 is not entered.</li>
                    </ul>
                    <p>
                        <a href="#po_1_ethnicity_ff">For details, see ethnicity of principal owner 1: free-form text field for other Hispanic or Latino ethnicity (Field 47)</a>
                    </p>
                    <p></p>
                </div>
                <div class="o-fig__section--sub-sub" data-search-section="" data-scrollspy="rse-of-principal-owner-2">
                    <h4 class="report-header o-fig__heading">
                        <a id="po_2_race" href="#po_2_race"> Field 57: Race of principal owner 2 </a>
                    </h4>
                    <h5>Column name</h5>
                    po_2_race
                    <h5>Instructions</h5>
                    <ul>
                        <li>Field type: Multiple response</li>
                        <li>Conditionally required if there are at least two principal owners. Report not applicable by leaving blank if there are fewer than two principal owners.</li>
                    </ul>
                    <p>
                        <a href="#po_1_race">For details, see race of principal owner 1 (Field 48)</a>
                    </p>
                    <p></p>
                </div>
                <div class="o-fig__section--sub-sub" data-search-section="" data-scrollspy="rse-of-principal-owner-2">
                    <h4 class="report-header o-fig__heading">
                        <a id="po_2_race_anai_ff" href="#po_2_race_anai_ff"> Field 58: Race of principal owner 2: free-form text field for American Indian or Alaska Native Enrolled or Principal Tribe </a>
                    </h4>
                    <h5>Column name</h5>
                    po_2_race_anai_ff
                    <h5>Instructions</h5>
                    <ul>
                        <li>Field type: Text (width up to 300 characters)</li>
                        <li>Conditionally required if 'race of principal owner 2' contains code 971. Leave blank if code 971 is not entered.</li>
                    </ul>
                    <p>
                        <a href="#po_1_race_anai_ff">For details, see race of principal owner 1: free-form text field for American Indian or Alaska Native Enrolled or Principal Tribe (Field 49)</a>
                    </p>
                    <p></p>
                </div>
                <div class="o-fig__section--sub-sub" data-search-section="" data-scrollspy="rse-of-principal-owner-2">
                    <h4 class="report-header o-fig__heading">
                        <a id="po_2_race_asian_ff" href="#po_2_race_asian_ff"> Field 59: Race of principal owner 2: free-form text field for other Asian race </a>
                    </h4>
                    <h5>Column name</h5>
                    po_2_race_asian_ff
                    <h5>Instructions</h5>
                    <ul>
                        <li>Field type: Text (width up to 300 characters)</li>
                        <li>Conditionally required if 'race of principal owner 2' contains code 972. Leave blank if code 972 is not entered.</li>
                    </ul>
                    <p>
                        <a href="#po_1_race_asian_ff">For details, see race of principal owner 1: free-form text field for other Asian race (Field 50)</a>
                    </p>
                    <p></p>
                </div>
                <div class="o-fig__section--sub-sub" data-search-section="" data-scrollspy="rse-of-principal-owner-2">
                    <h4 class="report-header o-fig__heading">
                        <a id="po_2_race_baa_ff" href="#po_2_race_baa_ff"> Field 60: Race of principal owner 2: free-form text field for other Black or African American race </a>
                    </h4>
                    <h5>Column name</h5>
                    po_2_race_baa_ff
                    <h5>Instructions</h5>
                    <ul>
                        <li>Field type: Text (width up to 300 characters)</li>
                        <li>Conditionally required if 'race of principal owner 2' contains code 973. Leave blank if code 973 is not entered.</li>
                    </ul>
                    <p>
                        <a href="#po_1_race_baa_ff">For details, see race of principal owner 1: free-form text field for other Black or African American race (Field 51)</a>
                    </p>
                    <p></p>
                </div>
                <div class="o-fig__section--sub-sub" data-search-section="" data-scrollspy="rse-of-principal-owner-2">
                    <h4 class="report-header o-fig__heading">
                        <a id="po_2_race_pi_ff" href="#po_2_race_pi_ff"> Field 61: Race of principal owner 2: free-form text field for other Pacific Islander race </a>
                    </h4>
                    <h5>Column name</h5>
                    po_2_race_pi_ff
                    <h5>Instructions</h5>
                    <ul>
                        <li>Field type: Text (width up to 300 characters)</li>
                        <li>Conditionally required if 'race of principal owner 2' contains code 974. Leave blank if code 974 is not entered.</li>
                    </ul>
                    <p>
                        <a href="#po_1_race_pi_ff">For details, see race of principal owner 1: free-form text field for other Pacific Islander race (Field 52)</a>
                    </p>
                    <p></p>
                </div>
                <div class="o-fig__section--sub-sub" data-search-section="" data-scrollspy="rse-of-principal-owner-2">
                    <h4 class="report-header o-fig__heading">
                        <a id="po_2_gender_flag" href="#po_2_gender_flag"> Field 62: Sex/gender of principal owner 2: NP flag </a>
                    </h4>
                    <h5>Column name</h5>
                    po_2_gender_flag
                    <h5>Instructions</h5>
                    <ul>
                        <li>Field type: Single response</li>
                        <li>Conditionally required if there are at least two principal owners. Report not applicable by leaving blank if there are fewer than two principal owners.</li>
                    </ul>
                    <p>
                        <a href="#po_1_gender_flag">For details, see sex/gender of principal owner 1: NP flag (Field 53)</a>
                    </p>
                    <p></p>
                </div>
                <div class="o-fig__section--sub-sub" data-search-section="" data-scrollspy="rse-of-principal-owner-2">
                    <h4 class="report-header o-fig__heading">
                        <a id="po_2_gender_ff" href="#po_2_gender_ff"> Field 63: Sex/gender of principal owner 2: free-form text field for self-identified sex/gender </a>
                    </h4>
                    <h5>Column name</h5>
                    po_2_gender_ff
                    <h5>Instructions</h5>
                    <ul>
                        <li>Field type: Text (width up to 300 characters)</li>
                        <li>Conditionally required if 'sex/gender of principal owner 2' is code 1. Leave blank if code 1 is not entered.</li>
                    </ul>
                    <p>
                        <a href="#po_1_gender_ff">For details, see sex/gender of principal owner 1: free-form text field for self-identified sex/gender (Field 54)</a>
                    </p>
                    <p></p>
                </div>
                <div class="o-fig__section--sub" data-search-section="" data-scrollspy="rse-of-principal-owner-3">
                    <h3 class="report-header o-fig__heading">
                        <a id="rse-of-principal-owner-3" href="#rse-of-principal-owner-3"> 3.22 Demographic information of principal owner 3 </a>
                    </h3>
                    <p>Rule section: 12 CFR 1002.107(a)(19)</p>
                    <p></p>
                    <ul class="m-list m-list--links">
                        <li class="m-list__item">
                            <a href="#po_3_ethnicity"> Field 64: Ethnicity of principal owner 3 </a>
                        </li>
                        <li class="m-list__item">
                            <a href="#po_3_ethnicity_ff"> Field 65: Ethnicity of principal owner 3: free-form text field for other Hispanic or Latino ethnicity </a>
                        </li>
                        <li class="m-list__item">
                            <a href="#po_3_race"> Field 66: Race of principal owner 3 </a>
                        </li>
                        <li class="m-list__item">
                            <a href="#po_3_race_anai_ff"> Field 67: Race of principal owner 3: free-form text field for American Indian or Alaska Native Enrolled or Principal Tribe </a>
                        </li>
                        <li class="m-list__item">
                            <a href="#po_3_race_asian_ff"> Field 68: Race of principal owner 3: free-form text field for other Asian race </a>
                        </li>
                        <li class="m-list__item">
                            <a href="#po_3_race_baa_ff"> Field 69: Race of principal owner 3: free-form text field for other Black or African American race </a>
                        </li>
                        <li class="m-list__item">
                            <a href="#po_3_race_pi_ff"> Field 70: Race of principal owner 3: free-form text field for other Pacific Islander race </a>
                        </li>
                        <li class="m-list__item">
                            <a href="#po_3_gender_flag"> Field 71: Sex/gender of principal owner 3: NP flag </a>
                        </li>
                        <li class="m-list__item">
                            <a href="#po_3_gender_ff"> Field 72: Sex/gender of principal owner 3: free-form text field for self-identified sex/gender </a>
                        </li>
                    </ul>
                </div>
                <div class="o-fig__section--sub-sub" data-search-section="" data-scrollspy="rse-of-principal-owner-3">
                    <h4 class="report-header o-fig__heading">
                        <a id="po_3_ethnicity" href="#po_3_ethnicity"> Field 64: Ethnicity of principal owner 3 </a>
                    </h4>
                    <h5>Column name</h5>
                    po_3_ethnicity
                    <h5>Instructions</h5>
                    <ul>
                        <li>Field type: Multiple response</li>
                        <li>Conditionally required if there are at least three principal owners. Report not applicable by leaving blank if there are fewer than three principal owners.</li>
                    </ul>
                    <p>
                        <a href="#po_1_ethnicity">For details, see ethnicity of principal owner 1 (Field 46)</a>
                    </p>
                    <p></p>
                </div>
                <div class="o-fig__section--sub-sub" data-search-section="" data-scrollspy="rse-of-principal-owner-3">
                    <h4 class="report-header o-fig__heading">
                        <a id="po_3_ethnicity_ff" href="#po_3_ethnicity_ff"> Field 65: Ethnicity of principal owner 3: free-form text field for other Hispanic or Latino ethnicity </a>
                    </h4>
                    <h5>Column name</h5>
                    po_3_ethnicity_ff
                    <h5>Instructions</h5>
                    <ul>
                        <li>Field type: Text (width up to 300 characters)</li>
                        <li>Conditionally required if 'ethnicity of principal owner 3' contains code 977. Leave blank if code 977 is not entered.</li>
                    </ul>
                    <p>
                        <a href="#po_1_ethnicity_ff">For details, see ethnicity of principal owner 1: free-form text field for other Hispanic or Latino ethnicity (Field 47)</a>
                    </p>
                    <p></p>
                </div>
                <div class="o-fig__section--sub-sub" data-search-section="" data-scrollspy="rse-of-principal-owner-3">
                    <h4 class="report-header o-fig__heading">
                        <a id="po_3_race" href="#po_3_race"> Field 66: Race of principal owner 3 </a>
                    </h4>
                    <h5>Column name</h5>
                    po_3_race
                    <h5>Instructions</h5>
                    <ul>
                        <li>Field type: Multiple response</li>
                        <li>Conditionally required if there are at least three principal owners. Report not applicable by leaving blank if there are fewer than three principal owners.</li>
                    </ul>
                    <p>
                        <a href="#po_1_race">For details, see race of principal owner 1 (Field 48)</a>
                    </p>
                    <p></p>
                </div>
                <div class="o-fig__section--sub-sub" data-search-section="" data-scrollspy="rse-of-principal-owner-3">
                    <h4 class="report-header o-fig__heading">
                        <a id="po_3_race_anai_ff" href="#po_3_race_anai_ff"> Field 67: Race of principal owner 3: free-form text field for American Indian or Alaska Native Enrolled or Principal Tribe </a>
                    </h4>
                    <h5>Column name</h5>
                    po_3_race_anai_ff
                    <h5>Instructions</h5>
                    <ul>
                        <li>Field type: Text (width up to 300 characters)</li>
                        <li>Conditionally required if 'race of principal owner 3' contains code 971. Leave blank if code 971 is not entered.</li>
                    </ul>
                    <p>
                        <a href="#po_1_race_anai_ff">For details, see race of principal owner 1: free-form text field for American Indian or Alaska Native Enrolled or Principal Tribe (Field 49)</a>
                    </p>
                    <p></p>
                </div>
                <div class="o-fig__section--sub-sub" data-search-section="" data-scrollspy="rse-of-principal-owner-3">
                    <h4 class="report-header o-fig__heading">
                        <a id="po_3_race_asian_ff" href="#po_3_race_asian_ff"> Field 68: Race of principal owner 3: free-form text field for other Asian race </a>
                    </h4>
                    <h5>Column name</h5>
                    po_3_race_asian_ff
                    <h5>Instructions</h5>
                    <ul>
                        <li>Field type: Text (width up to 300 characters)</li>
                        <li>Conditionally required if 'race of principal owner 3' contains code 972. Leave blank if code 972 is not entered.</li>
                    </ul>
                    <p>
                        <a href="#po_1_race_asian_ff">For details, see race of principal owner 1: free-form text field for other Asian race (Field 50)</a>
                    </p>
                    <p></p>
                </div>
                <div class="o-fig__section--sub-sub" data-search-section="" data-scrollspy="rse-of-principal-owner-3">
                    <h4 class="report-header o-fig__heading">
                        <a id="po_3_race_baa_ff" href="#po_3_race_baa_ff"> Field 69: Race of principal owner 3: free-form text field for other Black or African American race </a>
                    </h4>
                    <h5>Column name</h5>
                    po_3_race_baa_ff
                    <h5>Instructions</h5>
                    <ul>
                        <li>Field type: Text (width up to 300 characters)</li>
                        <li>Conditionally required if 'race of principal owner 3' contains code 973. Leave blank if code 973 is not entered.</li>
                    </ul>
                    <p>
                        <a href="#po_1_race_baa_ff">For details, see race of principal owner 1: free-form text field for other Black or African American race (Field 51)</a>
                    </p>
                    <p></p>
                </div>
                <div class="o-fig__section--sub-sub" data-search-section="" data-scrollspy="rse-of-principal-owner-3">
                    <h4 class="report-header o-fig__heading">
                        <a id="po_3_race_pi_ff" href="#po_3_race_pi_ff"> Field 70: Race of principal owner 3: free-form text field for other Pacific Islander race </a>
                    </h4>
                    <h5>Column name</h5>
                    po_3_race_pi_ff
                    <h5>Instructions</h5>
                    <ul>
                        <li>Field type: Text (width up to 300 characters)</li>
                        <li>Conditionally required if 'race of principal owner 3' contains code 974. Leave blank if code 974 is not entered.</li>
                    </ul>
                    <p>
                        <a href="#po_1_race_pi_ff">For details, see race of principal owner 1: free-form text field for other Pacific Islander race (Field 52)</a>
                    </p>
                    <p></p>
                </div>
                <div class="o-fig__section--sub-sub" data-search-section="" data-scrollspy="rse-of-principal-owner-3">
                    <h4 class="report-header o-fig__heading">
                        <a id="po_3_gender_flag" href="#po_3_gender_flag"> Field 71: Sex/gender of principal owner 3: NP flag </a>
                    </h4>
                    <h5>Column name</h5>
                    po_3_gender_flag
                    <h5>Instructions</h5>
                    <ul>
                        <li>Field type: Single response</li>
                        <li>Conditionally required if there are at least three principal owners. Report not applicable by leaving blank if there are fewer than three principal owners.</li>
                    </ul>
                    <p>
                        <a href="#po_1_gender_flag">For details, see sex/gender of principal owner 1: NP flag (Field 53)</a>
                    </p>
                    <p></p>
                </div>
                <div class="o-fig__section--sub-sub" data-search-section="" data-scrollspy="rse-of-principal-owner-3">
                    <h4 class="report-header o-fig__heading">
                        <a id="po_3_gender_ff" href="#po_3_gender_ff"> Field 72: Sex/gender of principal owner 3: free-form text field for self-identified sex/gender </a>
                    </h4>
                    <h5>Column name</h5>
                    po_3_gender_ff
                    <h5>Instructions</h5>
                    <ul>
                        <li>Field type: Text (width up to 300 characters)</li>
                        <li>Conditionally required if 'sex/gender of principal owner 3' is code 1. Leave blank if code 1 is not entered.</li>
                    </ul>
                    <p>
                        <a href="#po_1_gender_ff">For details, see sex/gender of principal owner 1: free-form text field for self-identified sex/gender (Field 54)</a>
                    </p>
                    <p></p>
                </div>
                <div class="o-fig__section--sub" data-search-section="" data-scrollspy="rse-of-principal-owner-4">
                    <h3 class="report-header o-fig__heading">
                        <a id="rse-of-principal-owner-4" href="#rse-of-principal-owner-4"> 3.23 Demographic information of principal owner 4 </a>
                    </h3>
                    <p>Rule section: 12 CFR 1002.107(a)(19)</p>
                    <p></p>
                    <ul class="m-list m-list--links">
                        <li class="m-list__item">
                            <a href="#po_4_ethnicity"> Field 73: Ethnicity of principal owner 4 </a>
                        </li>
                        <li class="m-list__item">
                            <a href="#po_4_ethnicity_ff"> Field 74: Ethnicity of principal owner 4: free-form text field for other Hispanic or Latino ethnicity </a>
                        </li>
                        <li class="m-list__item">
                            <a href="#po_4_race"> Field 75: Race of principal owner 4 </a>
                        </li>
                        <li class="m-list__item">
                            <a href="#po_4_race_anai_ff"> Field 76: Race of principal owner 4: free-form text field for American Indian or Alaska Native Enrolled or Principal Tribe </a>
                        </li>
                        <li class="m-list__item">
                            <a href="#po_4_race_asian_ff"> Field 77: Race of principal owner 4: free-form text field for other Asian race </a>
                        </li>
                        <li class="m-list__item">
                            <a href="#po_4_race_baa_ff"> Field 78: Race of principal owner 4: free-form text field for other Black or African American race </a>
                        </li>
                        <li class="m-list__item">
                            <a href="#po_4_race_pi_ff"> Field 79: Race of principal owner 4: free-form text field for other Pacific Islander race </a>
                        </li>
                        <li class="m-list__item">
                            <a href="#po_4_gender_flag"> Field 80: Sex/gender of principal owner 4: NP flag </a>
                        </li>
                        <li class="m-list__item">
                            <a href="#po_4_gender_ff"> Field 81: Sex/gender of principal owner 4: free-form text field for self-identified sex/gender </a>
                        </li>
                    </ul>
                </div>
                <div class="o-fig__section--sub-sub" data-search-section="" data-scrollspy="rse-of-principal-owner-4">
                    <h4 class="report-header o-fig__heading">
                        <a id="po_4_ethnicity" href="#po_4_ethnicity"> Field 73: Ethnicity of principal owner 4 </a>
                    </h4>
                    <h5>Column name</h5>
                    po_4_ethnicity
                    <h5>Instructions</h5>
                    <ul>
                        <li>Field type: Multiple response</li>
                        <li>Conditionally required if there are four principal owners. Report not applicable by leaving blank if there are fewer than four principal owners.</li>
                    </ul>
                    <p>
                        <a href="#po_1_ethnicity">For details, see ethnicity of principal owner 1 (Field 46)</a>
                    </p>
                    <p></p>
                </div>
                <div class="o-fig__section--sub-sub" data-search-section="" data-scrollspy="rse-of-principal-owner-4">
                    <h4 class="report-header o-fig__heading">
                        <a id="po_4_ethnicity_ff" href="#po_4_ethnicity_ff"> Field 74: Ethnicity of principal owner 4: free-form text field for other Hispanic or Latino ethnicity </a>
                    </h4>
                    <h5>Column name</h5>
                    po_4_ethnicity_ff
                    <h5>Instructions</h5>
                    <ul>
                        <li>Field type: Text (width up to 300 characters)</li>
                        <li>Conditionally required if 'ethnicity of principal owner 4' contains code 977. Leave blank if code 977 is not entered.</li>
                    </ul>
                    <p>
                        <a href="#po_1_ethnicity_ff">For details, see ethnicity of principal owner 1: free-form text field for other Hispanic or Latino ethnicity (Field 47)</a>
                    </p>
                    <p></p>
                </div>
                <div class="o-fig__section--sub-sub" data-search-section="" data-scrollspy="rse-of-principal-owner-4">
                    <h4 class="report-header o-fig__heading">
                        <a id="po_4_race" href="#po_4_race"> Field 75: Race of principal owner 4 </a>
                    </h4>
                    <h5>Column name</h5>
                    po_4_race
                    <h5>Instructions</h5>
                    <ul>
                        <li>Field type: Multiple response</li>
                        <li>Conditionally required if there are four principal owners. Report not applicable by leaving blank if there are fewer than four principal owners.</li>
                    </ul>
                    <p>
                        <a href="#po_1_race">For details, see race of principal owner 1 (Field 48)</a>
                    </p>
                    <p></p>
                </div>
                <div class="o-fig__section--sub-sub" data-search-section="" data-scrollspy="rse-of-principal-owner-4">
                    <h4 class="report-header o-fig__heading">
                        <a id="po_4_race_anai_ff" href="#po_4_race_anai_ff"> Field 76: Race of principal owner 4: free-form text field for American Indian or Alaska Native Enrolled or Principal Tribe </a>
                    </h4>
                    <h5>Column name</h5>
                    po_4_race_anai_ff
                    <h5>Instructions</h5>
                    <ul>
                        <li>Field type: Text (width up to 300 characters)</li>
                        <li>Conditionally required if 'race of principal owner 4' contains code 971. Leave blank if code 971 is not entered.</li>
                    </ul>
                    <p>
                        <a href="#po_1_race_anai_ff">For details, see race of principal owner 1: free-form text field for American Indian or Alaska Native Enrolled or Principal Tribe (Field 49)</a>
                    </p>
                    <p></p>
                </div>
                <div class="o-fig__section--sub-sub" data-search-section="" data-scrollspy="rse-of-principal-owner-4">
                    <h4 class="report-header o-fig__heading">
                        <a id="po_4_race_asian_ff" href="#po_4_race_asian_ff"> Field 77: Race of principal owner 4: free-form text field for other Asian race </a>
                    </h4>
                    <h5>Column name</h5>
                    po_4_race_asian_ff
                    <h5>Instructions</h5>
                    <ul>
                        <li>Field type: Text (width up to 300 characters)</li>
                        <li>Conditionally required if 'race of principal owner 4' contains code 972. Leave blank if code 972 is not entered.</li>
                    </ul>
                    <p>
                        <a href="#po_1_race_asian_ff">For details, see race of principal owner 1: free-form text field for other Asian race (Field 50)</a>
                    </p>
                    <p></p>
                </div>
                <div class="o-fig__section--sub-sub" data-search-section="" data-scrollspy="rse-of-principal-owner-4">
                    <h4 class="report-header o-fig__heading">
                        <a id="po_4_race_baa_ff" href="#po_4_race_baa_ff"> Field 78: Race of principal owner 4: free-form text field for other Black or African American race </a>
                    </h4>
                    <h5>Column name</h5>
                    po_4_race_baa_ff
                    <h5>Instructions</h5>
                    <ul>
                        <li>Field type: Text (width up to 300 characters)</li>
                        <li>Conditionally required if 'race of principal owner 4' contains code 973. Leave blank if code 973 is not entered.</li>
                    </ul>
                    <p>
                        <a href="#po_1_race_baa_ff">For details, see race of principal owner 1: free-form text field for other Black or African American race (Field 51)</a>
                    </p>
                    <p></p>
                </div>
                <div class="o-fig__section--sub-sub" data-search-section="" data-scrollspy="rse-of-principal-owner-4">
                    <h4 class="report-header o-fig__heading">
                        <a id="po_4_race_pi_ff" href="#po_4_race_pi_ff"> Field 79: Race of principal owner 4: free-form text field for other Pacific Islander race </a>
                    </h4>
                    <h5>Column name</h5>
                    po_4_race_pi_ff
                    <h5>Instructions</h5>
                    <ul>
                        <li>Field type: Text (width up to 300 characters)</li>
                        <li>Conditionally required if 'race of principal owner 4' contains code 974. Leave blank if code 974 is not entered.</li>
                    </ul>
                    <p>
                        <a href="#po_1_race_pi_ff">For details, see race of principal owner 1: free-form text field for other Pacific Islander race (Field 52)</a>
                    </p>
                    <p></p>
                </div>
                <div class="o-fig__section--sub-sub" data-search-section="" data-scrollspy="rse-of-principal-owner-4">
                    <h4 class="report-header o-fig__heading">
                        <a id="po_4_gender_flag" href="#po_4_gender_flag"> Field 80: Sex/gender of principal owner 4: NP flag </a>
                    </h4>
                    <h5>Column name</h5>
                    po_4_gender_flag
                    <h5>Instructions</h5>
                    <ul>
                        <li>Field type: Single response</li>
                        <li>Conditionally required if there are four principal owners. Report not applicable by leaving blank if there are fewer than four principal owners.</li>
                    </ul>
                    <p>
                        <a href="#po_1_gender_flag">For details, see sex/gender of principal owner 1: NP flag (Field 53)</a>
                    </p>
                    <p></p>
                </div>
                <div class="o-fig__section--sub-sub" data-search-section="" data-scrollspy="rse-of-principal-owner-4">
                    <h4 class="report-header o-fig__heading">
                        <a id="po_4_gender_ff" href="#po_4_gender_ff"> Field 81: Sex/gender of principal owner 4: free-form text field for self-identified sex/gender </a>
                    </h4>
                    <h5>Column name</h5>
                    po_4_gender_ff
                    <h5>Instructions</h5>
                    <ul>
                        <li>Field type: Text (width up to 300 characters)</li>
                        <li>Conditionally required if 'sex/gender of principal owner 4' is code 1. Leave blank if code 1 is not entered.</li>
                    </ul>
                    <p>
                        <a href="#po_1_gender_ff">For details, see sex/gender of principal owner 1: free-form text field for self-identified sex/gender (Field 54)</a>
                    </p>
                    <p></p>
                </div>
            </div>
            <div class="o-fig__section" data-search-section="" data-scrollspy="4">
                <h2 class="o-fig__heading">
                    <a id="4" href="#4"> 4. Data validation </a>
                </h2>
                <p data-block-key="nwusr">
                    Data validations are a series of checks that run on a small business lending application register to ensure that the data entries are correct and ready to submit, meaning the data are both internally consistent and
                    consistent with the syntax and logic specified by this guide. When data are uploaded to the small business lending data submission platform, before the register can be certified and submitted, the platform will review
                    the submission to determine if the data pass the validations described in this section. What follows is a description of the types of validations that will be performed on a register prior to its certification and
                    acceptance.
                </p>
                <p data-block-key="d9036">First, validations vary by type:</p>
                <ul>
                    <li data-block-key="7c0to">
                        An <b>error validation</b> checks that each data field contains valid data and that each value submitted matches the expected type. Each record must pass all of these validations in order for the register to be
                        certified and submitted.
                    </li>
                    <li data-block-key="enbha">
                        A <b>warning validation</b> checks for values that could indicate a mistake in the register. These are quality checks to assist filers in checking that their register has been compiled correctly and alerting them to
                        possible problems. The filer may confirm the accuracy of all values flagged by warning validations as part of the filing process in order to certify and submit their data.
                    </li>
                </ul>
                <p data-block-key="6u6f">Validations also vary by scope:</p>
                <ul>
                    <li data-block-key="1enar">
                        Each <b>single-field validation</b> pertains to only one specific field in each record. These validations check that the data held in an individual field match the values that are expected. A single-field validation
                        may be an error validation or a warning validation.
                    </li>
                    <li data-block-key="ap6up">
                        <b>Multi-field validations</b> check that the values of certain fields make sense in combination with other values in the same record. These validations have a list of “affected data fields,” which are the individual
                        fields within the record whose values will be compared to identify whether the record passes the validation checks. For example, many multi-field validations check for the presence of conditionally required data,
                        meaning that such checks ensure that fields that should be blank are blank, and fields that should be populated are populated. A multi-field validation may be an error validation or a warning validation.
                    </li>
                    <li data-block-key="6r61d">There is also one <b>register-level validation</b>. This validation checks that the register does not contain duplicate IDs.</li>
                </ul>
                <p data-block-key="etvuf">
                    Most validations related to principal owners are the same for each set of principal owner fields. In the validation descriptions and pseudocode, the "X" in "Principal owner X" is a placeholder for the relevant specific
                    principal owner number (1-4).
                </p>
                <p data-block-key="a1ul6">
                    Below is a comprehensive list of validations that will be applied to each register before submission. For multi-field validations, we provide a pseudocode interpretation of each validation. This pseudocode is an
                    illustration of the logic of the validation, exclusively for the purpose of ensuring that the validation logic is clear and unambiguous. It is not code which can be compiled and run. For a tabular view of the validation
                    specification in CSV file format, see the following link:
                </p>
                <p data-block-key="abnhl">
                    <a class="a-link a-link--jump"
                       href="https://raw.githubusercontent.com/cfpb/sbl-content/2024-v1/fig-files/validation-spec/2024-validations.csv">
                        <span class="a-link__text">Validation spec (CSV)</span>
                        <svg class="cf-icon-svg cf-icon-svg--external-link" viewBox="0 0 14 19" xmlns="http://www.w3.org/2000/svg">
                            <path
                                d="M13.017 3.622v4.6a.554.554 0 0 1-1.108 0V4.96L9.747 7.122a1.65 1.65 0 0 1 .13.646v5.57A1.664 1.664 0 0 1 8.215 15h-5.57a1.664 1.664 0 0 1-1.662-1.663v-5.57a1.664 1.664 0 0 1 1.662-1.662h5.57A1.654 1.654 0 0 1 9 6.302l2.126-2.126H7.863a.554.554 0 1 1 0-1.108h4.6a.554.554 0 0 1 .554.554zM8.77 8.1l-2.844 2.844a.554.554 0 0 1-.784-.783l2.947-2.948H2.645a.555.555 0 0 0-.554.555v5.57a.555.555 0 0 0 .554.553h5.57a.555.555 0 0 0 .554-.554z"
                            ></path>
                        </svg>
                    </a>
                </p>
            </div>
            <div class="o-fig__section--sub" data-search-section="" data-scrollspy="4.1">
                <h3 class="o-fig__heading">
                    <a id="4.1" href="#4.1"> 4.1. Single-field errors </a>
                </h3>
            </div>
            <div class="o-fig__section--sub-sub" data-search-section="" data-scrollspy="4.1">
                <h4 class="o-fig__heading">
                    <a id="4.1.1" href="#4.1.1"> Validation ID: uid.invalid_text_length </a>
                </h4>
                <h5 data-block-key="1y2r1">Affected data field</h5>
                <ul>
                    <li data-block-key="9t2aj">uid</li>
                </ul>
                <h5 data-block-key="8huq7">Description</h5>
                <ul>
                    <li data-block-key="ffasd">‘Unique identifier’ must be at least 21 characters in length and at most 45 characters in length.</li>
                </ul>
            </div>
            <div class="o-fig__section--sub-sub" data-search-section="" data-scrollspy="4.1">
                <h4 class="o-fig__heading">
                    <a id="4.1.2" href="#4.1.2"> Validation ID: uid.invalid_text_pattern </a>
                </h4>
                <h5 data-block-key="1y2r1">Affected data field</h5>
                <ul>
                    <li data-block-key="9t2aj">uid</li>
                </ul>
                <h5 data-block-key="8huq7">Description</h5>
                <ul>
                    <li data-block-key="ffasd">‘Unique identifier’ may contain any combination of numbers and/or uppercase letters (i.e., 0-9 and A-Z), and must <b>not</b> contain any other characters.</li>
                </ul>
            </div>
            <div class="o-fig__section--sub-sub" data-search-section="" data-scrollspy="4.1">
                <h4 class="o-fig__heading">
                    <a id="4.1.3" href="#4.1.3"> Validation ID: app_date.invalid_date_format </a>
                </h4>
                <h5 data-block-key="1y2r1">Affected data field</h5>
                <ul>
                    <li data-block-key="9t2aj">app_date</li>
                </ul>
                <h5 data-block-key="8huq7">Description</h5>
                <ul>
                    <li data-block-key="ffasd">‘Application date’ must be a real calendar date using YYYYMMDD format.</li>
                </ul>
            </div>
            <div class="o-fig__section--sub-sub" data-search-section="" data-scrollspy="4.1">
                <h4 class="o-fig__heading">
                    <a id="4.1.4" href="#4.1.4"> Validation ID: app_method.invalid_enum_value </a>
                </h4>
                <h5 data-block-key="1y2r1">Affected data field</h5>
                <ul>
                    <li data-block-key="9t2aj">app_method</li>
                </ul>
                <h5 data-block-key="8huq7">Description</h5>
                <ul>
                    <li data-block-key="ffasd">‘Application method’ must equal 1, 2, 3, or 4.</li>
                </ul>
            </div>
            <div class="o-fig__section--sub-sub" data-search-section="" data-scrollspy="4.1">
                <h4 class="o-fig__heading">
                    <a id="4.1.5" href="#4.1.5"> Validation ID: app_recipient.invalid_enum_value </a>
                </h4>
                <h5 data-block-key="1y2r1">Affected data field</h5>
                <ul>
                    <li data-block-key="9t2aj">app_recipient</li>
                </ul>
                <h5 data-block-key="8huq7">Description</h5>
                <ul>
                    <li data-block-key="ffasd">‘Application recipient’ must equal 1 or 2.</li>
                </ul>
            </div>
            <div class="o-fig__section--sub-sub" data-search-section="" data-scrollspy="4.1">
                <h4 class="o-fig__heading">
                    <a id="4.1.6" href="#4.1.6"> Validation ID: ct_credit_product.invalid_enum_value </a>
                </h4>
                <h5 data-block-key="1y2r1">Affected data field</h5>
                <ul>
                    <li data-block-key="9t2aj">ct_credit_product</li>
                </ul>
                <h5 data-block-key="8huq7">Description</h5>
                <ul>
                    <li data-block-key="ffasd">‘Credit product’ must equal 1, 2, 3, 4, 5, 6, 7, 8, 977, or 988.</li>
                </ul>
            </div>
            <div class="o-fig__section--sub-sub" data-search-section="" data-scrollspy="4.1">
                <h4 class="o-fig__heading">
                    <a id="4.1.7" href="#4.1.7"> Validation ID: ct_credit_product_ff.invalid_text_length </a>
                </h4>
                <h5 data-block-key="1y2r1">Affected data field</h5>
                <ul>
                    <li data-block-key="9t2aj">ct_credit_product_ff</li>
                </ul>
                <h5 data-block-key="8huq7">Description</h5>
                <ul>
                    <li data-block-key="ffasd">‘Free-form text field for other credit products’ must <b>not</b> exceed 300 characters in length.</li>
                </ul>
            </div>
            <div class="o-fig__section--sub-sub" data-search-section="" data-scrollspy="4.1">
                <h4 class="o-fig__heading">
                    <a id="4.1.8" href="#4.1.8"> Validation ID: ct_guarantee.invalid_enum_value </a>
                </h4>
                <h5 data-block-key="1y2r1">Affected data field</h5>
                <ul>
                    <li data-block-key="9t2aj">ct_guarantee</li>
                </ul>
                <h5 data-block-key="8huq7">Description</h5>
                <ul>
                    <li data-block-key="ffasd">Each value in ‘type of guarantee’ (separated by semicolons) must equal 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 977, or 999.</li>
                </ul>
            </div>
            <div class="o-fig__section--sub-sub" data-search-section="" data-scrollspy="4.1">
                <h4 class="o-fig__heading">
                    <a id="4.1.9" href="#4.1.9"> Validation ID: ct_guarantee.invalid_number_of_values </a>
                </h4>
                <h5 data-block-key="1y2r1">Affected data field</h5>
                <ul>
                    <li data-block-key="9t2aj">ct_guarantee</li>
                </ul>
                <h5 data-block-key="8huq7">Description</h5>
                <ul>
                    <li data-block-key="ffasd">‘Type of guarantee’ must contain at least one and at most five values, separated by semicolons.</li>
                </ul>
            </div>
            <div class="o-fig__section--sub-sub" data-search-section="" data-scrollspy="4.1">
                <h4 class="o-fig__heading">
                    <a id="4.1.10" href="#4.1.10"> Validation ID: ct_guarantee_ff.invalid_text_length </a>
                </h4>
                <h5 data-block-key="1y2r1">Affected data field</h5>
                <ul>
                    <li data-block-key="9t2aj">ct_guarantee_ff</li>
                </ul>
                <h5 data-block-key="8huq7">Description</h5>
                <ul>
                    <li data-block-key="ffasd">‘Free-form text field for other guarantee’ must <b>not</b> exceed 300 characters in length.</li>
                </ul>
            </div>
            <div class="o-fig__section--sub-sub" data-search-section="" data-scrollspy="4.1">
                <h4 class="o-fig__heading">
                    <a id="4.1.11" href="#4.1.11"> Validation ID: ct_loan_term_flag.invalid_enum_value </a>
                </h4>
                <h5 data-block-key="1y2r1">Affected data field</h5>
                <ul>
                    <li data-block-key="9t2aj">ct_loan_term_flag</li>
                </ul>
                <h5 data-block-key="8huq7">Description</h5>
                <ul>
                    <li data-block-key="ffasd">‘Loan term: NA/NP flag’ must equal 900, 988, or 999.</li>
                </ul>
            </div>
            <div class="o-fig__section--sub-sub" data-search-section="" data-scrollspy="4.1">
                <h4 class="o-fig__heading">
                    <a id="4.1.12" href="#4.1.12"> Validation ID: ct_loan_term.invalid_numeric_format </a>
                </h4>
                <h5 data-block-key="1y2r1">Affected data field</h5>
                <ul>
                    <li data-block-key="9t2aj">ct_loan_term</li>
                </ul>
                <h5 data-block-key="8huq7">Description</h5>
                <ul>
                    <li data-block-key="ffasd">When present, ‘loan term’ must be a whole number.</li>
                </ul>
            </div>
            <div class="o-fig__section--sub-sub" data-search-section="" data-scrollspy="4.1">
                <h4 class="o-fig__heading">
                    <a id="4.1.13" href="#4.1.13"> Validation ID: ct_loan_term.invalid_numeric_value </a>
                </h4>
                <h5 data-block-key="1y2r1">Affected data field</h5>
                <ul>
                    <li data-block-key="9t2aj">ct_loan_term</li>
                </ul>
                <h5 data-block-key="8huq7">Description</h5>
                <ul>
                    <li data-block-key="ffasd">When present, ‘loan term’ must be greater than or equal to 1.</li>
                </ul>
            </div>
            <div class="o-fig__section--sub-sub" data-search-section="" data-scrollspy="4.1">
                <h4 class="o-fig__heading">
                    <a id="4.1.14" href="#4.1.14"> Validation ID: credit_purpose.invalid_enum_value </a>
                </h4>
                <h5 data-block-key="1y2r1">Affected data field</h5>
                <ul>
                    <li data-block-key="9t2aj">credit_purpose</li>
                </ul>
                <h5 data-block-key="8huq7">Description</h5>
                <ul>
                    <li data-block-key="ffasd">Each value in ‘credit purpose’ (separated by semicolons) must equal 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 977, 988, or 999.</li>
                </ul>
            </div>
            <div class="o-fig__section--sub-sub" data-search-section="" data-scrollspy="4.1">
                <h4 class="o-fig__heading">
                    <a id="4.1.15" href="#4.1.15"> Validation ID: credit_purpose.invalid_number_of_values </a>
                </h4>
                <h5 data-block-key="1y2r1">Affected data field</h5>
                <ul>
                    <li data-block-key="9t2aj">credit_purpose</li>
                </ul>
                <h5 data-block-key="8huq7">Description</h5>
                <ul>
                    <li data-block-key="ffasd">‘Credit purpose’ must contain at least one and at most three values, separated by semicolons.</li>
                </ul>
            </div>
            <div class="o-fig__section--sub-sub" data-search-section="" data-scrollspy="4.1">
                <h4 class="o-fig__heading">
                    <a id="4.1.16" href="#4.1.16"> Validation ID: credit_purpose_ff.invalid_text_length </a>
                </h4>
                <h5 data-block-key="1y2r1">Affected data field</h5>
                <ul>
                    <li data-block-key="9t2aj">credit_purpose_ff</li>
                </ul>
                <h5 data-block-key="8huq7">Description</h5>
                <ul>
                    <li data-block-key="ffasd">‘Free-form text field for other credit purpose’ must <b>not</b> exceed 300 characters in length.</li>
                </ul>
            </div>
            <div class="o-fig__section--sub-sub" data-search-section="" data-scrollspy="4.1">
                <h4 class="o-fig__heading">
                    <a id="4.1.17" href="#4.1.17"> Validation ID: amount_applied_for_flag.invalid_enum_value </a>
                </h4>
                <h5 data-block-key="1y2r1">Affected data field</h5>
                <ul>
                    <li data-block-key="9t2aj">amount_applied_for_flag</li>
                </ul>
                <h5 data-block-key="8huq7">Description</h5>
                <ul>
                    <li data-block-key="ffasd">‘Amount applied For: NA/NP flag’ must equal 900, 988, or 999.</li>
                </ul>
            </div>
            <div class="o-fig__section--sub-sub" data-search-section="" data-scrollspy="4.1">
                <h4 class="o-fig__heading">
                    <a id="4.1.18" href="#4.1.18"> Validation ID: amount_applied_for.invalid_numeric_format </a>
                </h4>
                <h5 data-block-key="1y2r1">Affected data field</h5>
                <ul>
                    <li data-block-key="9t2aj">amount_applied_for</li>
                </ul>
                <h5 data-block-key="8huq7">Description</h5>
                <ul>
                    <li data-block-key="ffasd">When present, ‘amount applied for’ must be a numeric value.</li>
                </ul>
            </div>
            <div class="o-fig__section--sub-sub" data-search-section="" data-scrollspy="4.1">
                <h4 class="o-fig__heading">
                    <a id="4.1.19" href="#4.1.19"> Validation ID: amount_applied_for.invalid_numeric_value </a>
                </h4>
                <h5 data-block-key="1y2r1">Affected data field</h5>
                <ul>
                    <li data-block-key="9t2aj">amount_applied_for</li>
                </ul>
                <h5 data-block-key="8huq7">Description</h5>
                <ul>
                    <li data-block-key="ffasd">When present, ‘amount applied for’ must be greater than 0.</li>
                </ul>
            </div>
            <div class="o-fig__section--sub-sub" data-search-section="" data-scrollspy="4.1">
                <h4 class="o-fig__heading">
                    <a id="4.1.20" href="#4.1.20"> Validation ID: amount_approved.invalid_numeric_format </a>
                </h4>
                <h5 data-block-key="1y2r1">Affected data field</h5>
                <ul>
                    <li data-block-key="9t2aj">amount_approved</li>
                </ul>
                <h5 data-block-key="8huq7">Description</h5>
                <ul>
                    <li data-block-key="ffasd">When present, ‘amount approved or originated’ must be a numeric value.</li>
                </ul>
            </div>
            <div class="o-fig__section--sub-sub" data-search-section="" data-scrollspy="4.1">
                <h4 class="o-fig__heading">
                    <a id="4.1.21" href="#4.1.21"> Validation ID: amount_approved.invalid_numeric_value </a>
                </h4>
                <h5 data-block-key="pi3yh">Affected data field</h5>
                <ul>
                    <li data-block-key="1n764">amount_approved</li>
                </ul>
                <h5 data-block-key="7aqkf">Description</h5>
                <ul>
                    <li data-block-key="kk0f">When present, ‘amount approved or originated’ must be greater than 0.</li>
                </ul>
            </div>
            <div class="o-fig__section--sub-sub" data-search-section="" data-scrollspy="4.1">
                <h4 class="o-fig__heading">
                    <a id="4.1.22" href="#4.1.22"> Validation ID: action_taken.invalid_enum_value </a>
                </h4>
                <h5 data-block-key="pi3yh">Affected data field</h5>
                <ul>
                    <li data-block-key="akbqo">action_taken</li>
                </ul>
                <h5 data-block-key="a6rtl">Description</h5>
                <ul>
                    <li data-block-key="1ua5e">‘Action taken’ must equal 1, 2, 3, 4, or 5.</li>
                </ul>
            </div>
            <div class="o-fig__section--sub-sub" data-search-section="" data-scrollspy="4.1">
                <h4 class="o-fig__heading">
                    <a id="4.1.23" href="#4.1.23"> Validation ID: action_taken_date.invalid_date_format </a>
                </h4>
                <h5 data-block-key="pi3yh">Affected data field</h5>
                <ul>
                    <li data-block-key="dvt2p">action_taken_date</li>
                </ul>
                <h5 data-block-key="4g6l6">Description</h5>
                <ul>
                    <li data-block-key="ep396">‘Action taken date’ must be a real calendar date using YYYYMMDD format.</li>
                </ul>
            </div>
            <div class="o-fig__section--sub-sub" data-search-section="" data-scrollspy="4.1">
                <h4 class="o-fig__heading">
                    <a id="4.1.24" href="#4.1.24"> Validation ID: action_taken_date.invalid_date_value </a>
                </h4>
                <h5 data-block-key="pi3yh">Affected data field</h5>
                <ul>
                    <li data-block-key="64nki">action_taken_date</li>
                </ul>
                <h5 data-block-key="66d2v">Description</h5>
                <ul>
                    <li data-block-key="72pnm">The date indicated by 'action taken date' must occur within the current reporting period: October 1, 2024 to December 31, 2024.</li>
                </ul>
            </div>
            <div class="o-fig__section--sub-sub" data-search-section="" data-scrollspy="4.1">
                <h4 class="o-fig__heading">
                    <a id="4.1.25" href="#4.1.25"> Validation ID: denial_reasons.invalid_enum_value </a>
                </h4>
                <h5 data-block-key="pi3yh">Affected data field</h5>
                <ul>
                    <li data-block-key="b0vdq">denial_reasons</li>
                </ul>
                <h5 data-block-key="ars6m">Description</h5>
                <ul>
                    <li data-block-key="28ou6">Each value in ‘denial reason(s)’ (separated by semicolons) must equal 1, 2, 3, 4, 5, 6, 7, 8, 9, 977, or 999.</li>
                </ul>
            </div>
            <div class="o-fig__section--sub-sub" data-search-section="" data-scrollspy="4.1">
                <h4 class="o-fig__heading">
                    <a id="4.1.26" href="#4.1.26"> Validation ID: denial_reasons.invalid_number_of_values </a>
                </h4>
                <h5 data-block-key="pi3yh">Affected data field</h5>
                <ul>
                    <li data-block-key="2dr74">denial_reasons</li>
                </ul>
                <h5 data-block-key="2rb1b">Description</h5>
                <ul>
                    <li data-block-key="2c950">‘Denial reason(s)’ must contain at least one and at most four values, separated by semicolons.</li>
                </ul>
            </div>
            <div class="o-fig__section--sub-sub" data-search-section="" data-scrollspy="4.1">
                <h4 class="o-fig__heading">
                    <a id="4.1.27" href="#4.1.27"> Validation ID: denial_reasons_ff.invalid_text_length </a>
                </h4>
                <h5 data-block-key="pi3yh">Affected data field</h5>
                <ul>
                    <li data-block-key="9g6lh">denial_reasons_ff</li>
                </ul>
                <h5 data-block-key="7lsp5">Description</h5>
                <ul>
                    <li data-block-key="4vmq3">‘Free-form text field for other denial reason(s)’ must <b>not</b> exceed 300 characters in length.</li>
                </ul>
            </div>
            <div class="o-fig__section--sub-sub" data-search-section="" data-scrollspy="4.1">
                <h4 class="o-fig__heading">
                    <a id="4.1.28" href="#4.1.28"> Validation ID: pricing_interest_rate_type.invalid_enum_value </a>
                </h4>
                <h5 data-block-key="akymd">Affected data field</h5>
                <ul>
                    <li data-block-key="7rlt6">pricing_interest_rate_type</li>
                </ul>
                <h5 data-block-key="28bkc">Description</h5>
                <ul>
                    <li data-block-key="3vhr0">'Interest rate type' must equal 1, 2, 3, 4, 5, 6, or 999.</li>
                </ul>
            </div>
            <div class="o-fig__section--sub-sub" data-search-section="" data-scrollspy="4.1">
                <h4 class="o-fig__heading">
                    <a id="4.1.29" href="#4.1.29"> Validation ID: pricing_init_rate_period.invalid_numeric_format </a>
                </h4>
                <h5 data-block-key="pi3yh">Affected data field</h5>
                <ul>
                    <li data-block-key="323dc">pricing_init_rate_period</li>
                </ul>
                <h5 data-block-key="5p0s8">Description</h5>
                <ul>
                    <li data-block-key="da099">When present, 'variable rate transaction: initial rate period' must be a whole number.</li>
                </ul>
            </div>
            <div class="o-fig__section--sub-sub" data-search-section="" data-scrollspy="4.1">
                <h4 class="o-fig__heading">
                    <a id="4.1.30" href="#4.1.30"> Validation ID: pricing_init_rate_period.invalid_numeric_value </a>
                </h4>
                <h5 data-block-key="bdfqs">Affected data field</h5>
                <ul>
                    <li data-block-key="7qdj1">pricing_init_rate_period</li>
                </ul>
                <h5 data-block-key="b63sv">Description</h5>
                <ul>
                    <li data-block-key="8lnig">When present, ‘variable rate transaction: initial rate period’ must be greater than 0.</li>
                </ul>
            </div>
            <div class="o-fig__section--sub-sub" data-search-section="" data-scrollspy="4.1">
                <h4 class="o-fig__heading">
                    <a id="4.1.31" href="#4.1.31"> Validation ID: pricing_fixed_rate.invalid_numeric_format </a>
                </h4>
                <h5 data-block-key="pi3yh">Affected data field</h5>
                <ul>
                    <li data-block-key="cjtbn">pricing_fixed_rate</li>
                </ul>
                <h5 data-block-key="9mb7i">Description</h5>
                <ul>
                    <li data-block-key="952q7">When present, ‘fixed rate: interest rate’ must be a numeric value.</li>
                </ul>
            </div>
            <div class="o-fig__section--sub-sub" data-search-section="" data-scrollspy="4.1">
                <h4 class="o-fig__heading">
                    <a id="4.1.32" href="#4.1.32"> Validation ID: pricing_var_margin.invalid_numeric_format </a>
                </h4>
                <h5 data-block-key="pi3yh">Affected data field</h5>
                <ul>
                    <li data-block-key="24k8j">pricing_var_margin</li>
                </ul>
                <h5 data-block-key="1r7td">Description</h5>
                <ul>
                    <li data-block-key="f2tad">When present, ‘variable rate transaction: margin’ must be a numeric value.</li>
                </ul>
            </div>
            <div class="o-fig__section--sub-sub" data-search-section="" data-scrollspy="4.1">
                <h4 class="o-fig__heading">
                    <a id="4.1.33" href="#4.1.33"> Validation ID: pricing_var_index_name.invalid_enum_value </a>
                </h4>
                <h5 data-block-key="bdfqs">Affected data field</h5>
                <ul>
                    <li data-block-key="29ln2">pricing_var_index_name</li>
                </ul>
                <h5 data-block-key="a333k">Description</h5>
                <ul>
                    <li data-block-key="2ev9n">‘Variable rate transaction: index name’ must equal 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 977, or 999.</li>
                </ul>
            </div>
            <div class="o-fig__section--sub-sub" data-search-section="" data-scrollspy="4.1">
                <h4 class="o-fig__heading">
                    <a id="4.1.34" href="#4.1.34"> Validation ID: pricing_var_index_name_ff.invalid_text_length </a>
                </h4>
                <h5 data-block-key="bdfqs">Affected data field</h5>
                <ul>
                    <li data-block-key="1lml8">pricing_var_index_name_ff</li>
                </ul>
                <h5 data-block-key="a7p4a">Description</h5>
                <ul>
                    <li data-block-key="e7f70">‘Variable rate transaction: index name: other’ must <b>not</b> exceed 300 characters in length.</li>
                </ul>
            </div>
            <div class="o-fig__section--sub-sub" data-search-section="" data-scrollspy="4.1">
                <h4 class="o-fig__heading">
                    <a id="4.1.35" href="#4.1.35"> Validation ID: pricing_var_index_value.invalid_numeric_format </a>
                </h4>
                <h5 data-block-key="bdfqs">Affected data field</h5>
                <ul>
                    <li data-block-key="42tkq">pricing_var_index_value</li>
                </ul>
                <h5 data-block-key="9p7n8">Description</h5>
                <ul>
                    <li data-block-key="bkios">When present, ‘variable rate transaction: index value’ must be a numeric value.</li>
                </ul>
            </div>
            <div class="o-fig__section--sub-sub" data-search-section="" data-scrollspy="4.1">
                <h4 class="o-fig__heading">
                    <a id="4.1.36" href="#4.1.36"> Validation ID: pricing_origination_charges.invalid_numeric_format </a>
                </h4>
                <h5 data-block-key="bdfqs">Affected data field</h5>
                <ul>
                    <li data-block-key="7qs6g">pricing_origination_charges</li>
                </ul>
                <h5 data-block-key="fm750">Description</h5>
                <ul>
                    <li data-block-key="4i8mp">When present, ‘total origination charges’ must be a numeric value.</li>
                </ul>
            </div>
            <div class="o-fig__section--sub-sub" data-search-section="" data-scrollspy="4.1">
                <h4 class="o-fig__heading">
                    <a id="4.1.37" href="#4.1.37"> Validation ID: pricing_broker_fees.invalid_numeric_format </a>
                </h4>
                <h5 data-block-key="bdfqs">Affected data field</h5>
                <ul>
                    <li data-block-key="8n62d">pricing_broker_fees</li>
                </ul>
                <h5 data-block-key="dckes">Description</h5>
                <ul>
                    <li data-block-key="fc9ch">When present, ‘amount of total broker fees’ must be a numeric value.</li>
                </ul>
            </div>
            <div class="o-fig__section--sub-sub" data-search-section="" data-scrollspy="4.1">
                <h4 class="o-fig__heading">
                    <a id="4.1.38" href="#4.1.38"> Validation ID: pricing_initial_charges.invalid_numeric_format </a>
                </h4>
                <h5 data-block-key="bdfqs">Affected data field</h5>
                <ul>
                    <li data-block-key="f52bh">pricing_initial_charges</li>
                </ul>
                <h5 data-block-key="jbid">Description</h5>
                <ul>
                    <li data-block-key="edg5s">When present, ‘initial annual charges’ must be a numeric value.</li>
                </ul>
            </div>
            <div class="o-fig__section--sub-sub" data-search-section="" data-scrollspy="4.1">
                <h4 class="o-fig__heading">
                    <a id="4.1.39" href="#4.1.39"> Validation ID: pricing_mca_addcost_flag.invalid_enum_value </a>
                </h4>
                <h5 data-block-key="bdfqs">Affected data field</h5>
                <ul>
                    <li data-block-key="c3j84">pricing_mca_addcost_flag</li>
                </ul>
                <h5 data-block-key="6ep5r">Description</h5>
                <ul>
                    <li data-block-key="dv38k">‘MCA/sales-based: additional cost for merchant cash advances or other sales-based financing: NA flag’ must equal 900 or 999.</li>
                </ul>
            </div>
            <div class="o-fig__section--sub-sub" data-search-section="" data-scrollspy="4.1">
                <h4 class="o-fig__heading">
                    <a id="4.1.40" href="#4.1.40"> Validation ID: pricing_mca_addcost.invalid_numeric_format </a>
                </h4>
                <h5 data-block-key="bdfqs">Affected data field</h5>
                <ul>
                    <li data-block-key="h6qq">pricing_mca_addcost</li>
                </ul>
                <h5 data-block-key="bkg61">Description</h5>
                <ul>
                    <li data-block-key="eb2k2">When present, ‘MCA/sales-based: additional cost for merchant cash advances or other sales-based financing’ must be a numeric value.</li>
                </ul>
            </div>
            <div class="o-fig__section--sub-sub" data-search-section="" data-scrollspy="4.1">
                <h4 class="o-fig__heading">
                    <a id="4.1.41" href="#4.1.41"> Validation ID: pricing_prepenalty_allowed.invalid_enum_value </a>
                </h4>
                <h5 data-block-key="bdfqs">Affected data field</h5>
                <ul>
                    <li data-block-key="e0am2">pricing_prepenalty_allowed</li>
                </ul>
                <h5 data-block-key="c6q1e">Description</h5>
                <ul>
                    <li data-block-key="6i31e">‘Prepayment penalty could be imposed’ must equal 1, 2, or 999.</li>
                </ul>
            </div>
            <div class="o-fig__section--sub-sub" data-search-section="" data-scrollspy="4.1">
                <h4 class="o-fig__heading">
                    <a id="4.1.42" href="#4.1.42"> Validation ID: pricing_prepenalty_exists.invalid_enum_value </a>
                </h4>
                <h5 data-block-key="bdfqs">Affected data field</h5>
                <ul>
                    <li data-block-key="2vs4j">pricing_prepenalty_exists</li>
                </ul>
                <h5 data-block-key="ct4a2">Description</h5>
                <ul>
                    <li data-block-key="7j6e1">‘Prepayment penalty exists’ must equal 1, 2, or 999.</li>
                </ul>
            </div>
            <div class="o-fig__section--sub-sub" data-search-section="" data-scrollspy="4.1">
                <h4 class="o-fig__heading">
                    <a id="4.1.43" href="#4.1.43"> Validation ID: census_tract_adr_type.invalid_enum_value </a>
                </h4>
                <h5 data-block-key="bdfqs">Affected data field</h5>
                <ul>
                    <li data-block-key="7f9sg">census_tract_adr_type</li>
                </ul>
                <h5 data-block-key="b685i">Description</h5>
                <ul>
                    <li data-block-key="619lp">‘Census tract: type of address’ must equal 1, 2, 3, or 988.</li>
                </ul>
            </div>
            <div class="o-fig__section--sub-sub" data-search-section="" data-scrollspy="4.1">
                <h4 class="o-fig__heading">
                    <a id="4.1.44" href="#4.1.44"> Validation ID: census_tract_number.invalid_text_length </a>
                </h4>
                <h5 data-block-key="bdfqs">Affected data field</h5>
                <ul>
                    <li data-block-key="8tnfb">census_tract_number</li>
                </ul>
                <h5 data-block-key="d2voa">Description</h5>
                <ul>
                    <li data-block-key="170v0">When present, ‘census tract: tract number’ must be a GEOID with exactly 11 digits.</li>
                </ul>
            </div>
            <div class="o-fig__section--sub-sub" data-search-section="" data-scrollspy="4.1">
                <h4 class="o-fig__heading">
                    <a id="4.1.45" href="#4.1.45"> Validation ID: gross_annual_revenue_flag.invalid_enum_value </a>
                </h4>
                <h5 data-block-key="bdfqs">Affected data field</h5>
                <ul>
                    <li data-block-key="c2g6p">gross_annual_revenue_flag</li>
                </ul>
                <h5 data-block-key="ehmj1">Description</h5>
                <ul>
                    <li data-block-key="1t1gg">‘Gross annual revenue: NP flag’ must equal 900 or 988.</li>
                </ul>
            </div>
            <div class="o-fig__section--sub-sub" data-search-section="" data-scrollspy="4.1">
                <h4 class="o-fig__heading">
                    <a id="4.1.46" href="#4.1.46"> Validation ID: gross_annual_revenue.invalid_numeric_format </a>
                </h4>
                <h5 data-block-key="bdfqs">Affected data field</h5>
                <ul>
                    <li data-block-key="4o618">gross_annual_revenue</li>
                </ul>
                <h5 data-block-key="clfm5">Description</h5>
                <ul>
                    <li data-block-key="2omd7">When present, ‘gross annual revenue’ must be a numeric value.</li>
                </ul>
            </div>
            <div class="o-fig__section--sub-sub" data-search-section="" data-scrollspy="4.1">
                <h4 class="o-fig__heading">
                    <a id="4.1.47" href="#4.1.47"> Validation ID: naics_code_flag.invalid_enum_value </a>
                </h4>
                <h5 data-block-key="bdfqs">Affected data field</h5>
                <ul>
                    <li data-block-key="4o3tm">naics_code_flag</li>
                </ul>
                <h5 data-block-key="1vci9">Description</h5>
                <ul>
                    <li data-block-key="far4">‘North American Industry Classification System (NAICS) code: NP flag’ must equal 900 or 988.</li>
                </ul>
            </div>
            <div class="o-fig__section--sub-sub" data-search-section="" data-scrollspy="4.1">
                <h4 class="o-fig__heading">
                    <a id="4.1.48" href="#4.1.48"> Validation ID: naics_code.invalid_text_length </a>
                </h4>
                <h5 data-block-key="bdfqs">Affected data field</h5>
                <ul>
                    <li data-block-key="4o3tm">naics_code</li>
                </ul>
                <h5 data-block-key="1vci9">Description</h5>
                <ul>
                    <li data-block-key="far4">When present, ‘North American Industry Classification System (NAICS) code’ must be three digits in length.</li>
                </ul>
            </div>
            <div class="o-fig__section--sub-sub" data-search-section="" data-scrollspy="4.1">
                <h4 class="o-fig__heading">
                    <a id="4.1.49" href="#4.1.49"> Validation ID: naics_code.invalid_naics_format </a>
                </h4>
                <h5 data-block-key="bdfqs">Affected data field</h5>
                <ul>
                    <li data-block-key="eren8">naics_code</li>
                </ul>
                <h5 data-block-key="a53ki">Description</h5>
                <ul>
                    <li data-block-key="2dskn">'North American Industry Classification System (NAICS) code' may only contain numeric characters.</li>
                </ul>
            </div>
            <div class="o-fig__section--sub-sub" data-search-section="" data-scrollspy="4.1">
                <h4 class="o-fig__heading">
                    <a id="4.1.50" href="#4.1.50"> Validation ID: number_of_workers.invalid_enum_value </a>
                </h4>
                <h5 data-block-key="bdfqs">Affected data field</h5>
                <ul>
                    <li data-block-key="6cm08">number_of_workers</li>
                </ul>
                <h5 data-block-key="fm5of">Description</h5>
                <ul>
                    <li data-block-key="b8vba">‘Number of workers’ must equal 1, 2, 3, 4, 5, 6, 7, 8, 9, or 988.</li>
                </ul>
            </div>
            <div class="o-fig__section--sub-sub" data-search-section="" data-scrollspy="4.1">
                <h4 class="o-fig__heading">
                    <a id="4.1.51" href="#4.1.51"> Validation ID: time_in_business_type.invalid_enum_value </a>
                </h4>
                <h5 data-block-key="bdfqs">Affected data field</h5>
                <ul>
                    <li data-block-key="a66di">time_in_business_type</li>
                </ul>
                <h5 data-block-key="ap3fj">Description</h5>
                <ul>
                    <li data-block-key="5ppe0">‘Time in business: type of response’ must equal 1, 2, 3, or 988.</li>
                </ul>
            </div>
            <div class="o-fig__section--sub-sub" data-search-section="" data-scrollspy="4.1">
                <h4 class="o-fig__heading">
                    <a id="4.1.52" href="#4.1.52"> Validation ID: time_in_business.invalid_numeric_format </a>
                </h4>
                <h5 data-block-key="bdfqs">Affected data field</h5>
                <ul>
                    <li data-block-key="16avp">time_in_business</li>
                </ul>
                <h5 data-block-key="9ov4d">Description</h5>
                <ul>
                    <li data-block-key="3si04">When present, ‘time in business’ must be a whole number.</li>
                </ul>
            </div>
            <div class="o-fig__section--sub-sub" data-search-section="" data-scrollspy="4.1">
                <h4 class="o-fig__heading">
                    <a id="4.1.53" href="#4.1.53"> Validation ID: time_in_business.invalid_numeric_value </a>
                </h4>
                <h5 data-block-key="bdfqs">Affected data field</h5>
                <ul>
                    <li data-block-key="5ucal">time_in_business</li>
                </ul>
                <h5 data-block-key="75hd9">Description</h5>
                <ul>
                    <li data-block-key="f2obd">When present, ‘time in business’ must be greater than or equal to 0.</li>
                </ul>
            </div>
            <div class="o-fig__section--sub-sub" data-search-section="" data-scrollspy="4.1">
                <h4 class="o-fig__heading">
                    <a id="4.1.54" href="#4.1.54"> Validation ID: business_ownership_status.invalid_enum_value </a>
                </h4>
                <h5 data-block-key="bdfqs">Affected data field</h5>
                <ul>
                    <li data-block-key="dbk8r">business_ownership_status</li>
                </ul>
                <h5 data-block-key="1175p">Description</h5>
                <ul>
                    <li data-block-key="5pgj">Each value in 'business ownership status' (separated by semicolons) must equal 1, 2, 3, 955, 966, or 988.</li>
                </ul>
            </div>
            <div class="o-fig__section--sub-sub" data-search-section="" data-scrollspy="4.1">
                <h4 class="o-fig__heading">
                    <a id="4.1.55" href="#4.1.55"> Validation ID: business_ownership_status.invalid_number_of_values </a>
                </h4>
                <h5 data-block-key="bdfqs">Affected data field</h5>
                <ul>
                    <li data-block-key="7mv4n">business_ownership_status</li>
                </ul>
                <h5 data-block-key="8qf0j">Description</h5>
                <ul>
                    <li data-block-key="4ciov">'Business ownership status' must contain at least one value.</li>
                </ul>
            </div>
            <div class="o-fig__section--sub-sub" data-search-section="" data-scrollspy="4.1">
                <h4 class="o-fig__heading">
                    <a id="4.1.56" href="#4.1.56"> Validation ID: num_principal_owners_flag.invalid_enum_value </a>
                </h4>
                <h5 data-block-key="bdfqs">Affected data field</h5>
                <ul>
                    <li data-block-key="451ub">num_principal_owners_flag</li>
                </ul>
                <h5 data-block-key="i4ke">Description</h5>
                <ul>
                    <li data-block-key="42r2a">‘Number of principal owners: NP flag’ must equal 900 or 988.</li>
                </ul>
            </div>
            <div class="o-fig__section--sub-sub" data-search-section="" data-scrollspy="4.1">
                <h4 class="o-fig__heading">
                    <a id="4.1.57" href="#4.1.57"> Validation ID: num_principal_owners.invalid_enum_value </a>
                </h4>
                <h5 data-block-key="bdfqs">Affected data field</h5>
                <ul>
                    <li data-block-key="d6h75">num_principal_owners</li>
                </ul>
                <h5 data-block-key="245r9">Description</h5>
                <ul>
                    <li data-block-key="b3eqa">When present, ‘number of principal owners’ must equal 0, 1, 2, 3, or 4.</li>
                </ul>
            </div>
            <div class="o-fig__section--sub-sub" data-search-section="" data-scrollspy="4.1">
                <h4 class="o-fig__heading">
                    <a id="4.1.58" href="#4.1.58"> Validation ID: po_X_ethnicity.invalid_enum_value </a>
                </h4>
                <h5 data-block-key="bdfqs">Affected data field</h5>
                <ul>
                    <li data-block-key="6jt1l">po_X_ethnicity</li>
                </ul>
                <h5 data-block-key="7nsr8">Description</h5>
                <ul>
                    <li data-block-key="cuv5t">When present, each value in ‘ethnicity of principal owner X’ (separated by semicolons) must equal 1, 11, 12, 13, 14, 2, 966, 977, or 988.</li>
                </ul>
            </div>
            <div class="o-fig__section--sub-sub" data-search-section="" data-scrollspy="4.1">
                <h4 class="o-fig__heading">
                    <a id="4.1.59" href="#4.1.59"> Validation ID: po_X_ethnicity_ff.invalid_text_length </a>
                </h4>
                <h5 data-block-key="bdfqs">Affected data field</h5>
                <ul>
                    <li data-block-key="59a90">po_X_ethnicity_ff</li>
                </ul>
                <h5 data-block-key="a4tpm">Description</h5>
                <ul>
                    <li data-block-key="36osn">‘Ethnicity of principal owner X: free-form text field for other Hispanic or Latino’ must <b>not</b> exceed 300 characters in length.</li>
                </ul>
            </div>
            <div class="o-fig__section--sub-sub" data-search-section="" data-scrollspy="4.1">
                <h4 class="o-fig__heading">
                    <a id="4.1.60" href="#4.1.60"> Validation ID: po_X_race.invalid_enum_value </a>
                </h4>
                <h5 data-block-key="bdfqs">Affected data field</h5>
                <ul>
                    <li data-block-key="f37vj">po_X_race</li>
                </ul>
                <h5 data-block-key="75od9">Description</h5>
                <ul>
                    <li data-block-key="e3gpk">
                        When present, each value in ‘race of principal owner X’ (separated by semicolons) must equal 1, 2, 21, 22, 23, 24, 25, 26, 27, 3, 31, 32, 33, 34, 35, 36, 37, 4, 41, 42, 43, 44, 5, 966, 971, 972, 973, 974, or 988.
                    </li>
                </ul>
            </div>
            <div class="o-fig__section--sub-sub" data-search-section="" data-scrollspy="4.1">
                <h4 class="o-fig__heading">
                    <a id="4.1.61" href="#4.1.61"> Validation ID: po_X_race_anai_ff.invalid_text_length </a>
                </h4>
                <h5 data-block-key="bdfqs">Affected data field</h5>
                <ul>
                    <li data-block-key="44qtf">po_X_race_anai_ff</li>
                </ul>
                <h5 data-block-key="av522">Description</h5>
                <ul>
                    <li data-block-key="3uue9">‘Race of principal owner X: free-form text field for American Indian or Alaska Native Enrolled or Principal Tribe’ must <b>not</b> exceed 300 characters in length.</li>
                </ul>
            </div>
            <div class="o-fig__section--sub-sub" data-search-section="" data-scrollspy="4.1">
                <h4 class="o-fig__heading">
                    <a id="4.1.62" href="#4.1.62"> Validation ID: po_X_race_asian_ff.invalid_text_length </a>
                </h4>
                <h5 data-block-key="bdfqs">Affected data field</h5>
                <ul>
                    <li data-block-key="chddd">po_X_race_asian_ff</li>
                </ul>
                <h5 data-block-key="14ehj">Description</h5>
                <ul>
                    <li data-block-key="9o2sc">‘Race of principal owner X: free-form text field for other Asian’ must <b>not</b> exceed 300 characters in length.</li>
                </ul>
            </div>
            <div class="o-fig__section--sub-sub" data-search-section="" data-scrollspy="4.1">
                <h4 class="o-fig__heading">
                    <a id="4.1.63" href="#4.1.63"> Validation ID: po_X_race_baa_ff.invalid_text_length </a>
                </h4>
                <h5 data-block-key="sahsd">Affected data field</h5>
                <ul>
                    <li data-block-key="fi1tl">po_X_race_baa_ff</li>
                </ul>
                <h5 data-block-key="cs8ml">Description</h5>
                <ul>
                    <li data-block-key="66q58">‘Race of principal owner X: free-form text field for other Black or African American’ must <b>not</b> exceed 300 characters in length.</li>
                </ul>
            </div>
            <div class="o-fig__section--sub-sub" data-search-section="" data-scrollspy="4.1">
                <h4 class="o-fig__heading">
                    <a id="4.1.64" href="#4.1.64"> Validation ID: po_X_race_pi_ff.invalid_text_length </a>
                </h4>
                <h5 data-block-key="sahsd">Affected data field</h5>
                <ul>
                    <li data-block-key="8tv68">po_X_race_pi_ff</li>
                </ul>
                <h5 data-block-key="8tou8">Description</h5>
                <ul>
                    <li data-block-key="ctgoj">‘Race of principal owner X: free-form text field for other Pacific Islander race’ must <b>not</b> exceed 300 characters in length.</li>
                </ul>
            </div>
            <div class="o-fig__section--sub-sub" data-search-section="" data-scrollspy="4.1">
                <h4 class="o-fig__heading">
                    <a id="4.1.65" href="#4.1.65"> Validation ID: po_X_gender_flag.invalid_enum_value </a>
                </h4>
                <h5 data-block-key="sahsd">Affected data field</h5>
                <ul>
                    <li data-block-key="d4br3">po_X_gender_flag</li>
                </ul>
                <h5 data-block-key="3v5t5">Description</h5>
                <ul>
                    <li data-block-key="6cg7f">When present, ‘sex/gender of principal owner X: NP flag’ must equal 1, 966, or 988.</li>
                </ul>
            </div>
            <div class="o-fig__section--sub-sub" data-search-section="" data-scrollspy="4.1">
                <h4 class="o-fig__heading">
                    <a id="4.1.66" href="#4.1.66"> Validation ID: po_X_gender_ff.invalid_text_length </a>
                </h4>
                <h5 data-block-key="sahsd">Affected data field</h5>
                <ul>
                    <li data-block-key="ddi62">po_X_gender_ff</li>
                </ul>
                <h5 data-block-key="42aqq">Description</h5>
                <ul>
                    <li data-block-key="2nihr">‘Sex/gender of principal owner X: free-form text field for self-identified sex/gender’ must <b>not</b> exceed 300 characters in length.</li>
                </ul>
            </div>
            <div class="o-fig__section--sub" data-search-section="" data-scrollspy="4.2">
                <h3 class="o-fig__heading">
                    <a id="4.2" href="#4.2"> 4.2. Multi-field errors </a>
                </h3>
            </div>
            <div class="o-fig__section--sub-sub" data-search-section="" data-scrollspy="4.2">
                <h4 class="o-fig__heading">
                    <a id="4.2.1" href="#4.2.1"> Validation ID: ct_credit_product_ff.conditional_field_conflict </a>
                </h4>
                <h5 data-block-key="ede7q">Affected data fields</h5>
                <ul>
                    <li data-block-key="d9o8q">ct_credit_product</li>
                    <li data-block-key="8bj5m">ct_credit_product_ff</li>
                </ul>
                <h5 data-block-key="8h181">Description</h5>
                <ul>
                    <li data-block-key="96bvf">When ‘credit product’ does <b>not</b> equal 977 (other), ‘free-form text field for other credit products’ must be blank.</li>
                    <li data-block-key="fr4mu">When ‘credit product’ equals 977, ‘free-form text field for other credit products’ must <b>not</b> be blank.</li>
                </ul>
                <pre>
IF ct_credit_product is not equal to 977 THEN
    IF ct_credit_ff is not blank THEN
        Error
    ENDIF
ELSEIF ct_credit_product is equal to 977 THEN
    IF ct_credit_ff is blank THEN
        Error
    ENDIF
ENDIF

                </pre>
            </div>
            <div class="o-fig__section--sub-sub" data-search-section="" data-scrollspy="4.2">
                <h4 class="o-fig__heading">
                    <a id="4.2.2" href="#4.2.2"> Validation ID: ct_guarantee_ff.conditional_field_conflict </a>
                </h4>
                <h5 data-block-key="ede7q">Affected data fields</h5>
                <ul>
                    <li data-block-key="d9o8q">ct_guarantee</li>
                    <li data-block-key="7ngtp">ct_guarantee_ff</li>
                </ul>
                <h5 data-block-key="8h181">Description</h5>
                <ul>
                    <li data-block-key="96bvf">When ‘type of guarantee’ does <b>not</b> contain 977 (other), ‘free-form text field for other guarantee’ must be blank.</li>
                    <li data-block-key="6u1pd">When ‘type of guarantee’ contains 977, ‘free-form text field for other guarantee’ must <b>not</b> be blank.</li>
                </ul>
                <pre>
IF ct_guarantee does not contain 977 THEN
    IF ct_guarantee_ff is not blank THEN
        Error
    ENDIF
ELSEIF ct_guarantee contains 977 THEN
    IF ct_guarantee_ff is blank THEN
        Error
    ENDIF
ENDIF

                </pre>
            </div>
            <div class="o-fig__section--sub-sub" data-search-section="" data-scrollspy="4.2">
                <h4 class="o-fig__heading">
                    <a id="4.2.3" href="#4.2.3"> Validation ID: ct_loan_term_flag.enum_value_conflict </a>
                </h4>
                <h5 data-block-key="ede7q">Affected data fields</h5>
                <ul>
                    <li data-block-key="d9o8q">ct_credit_product</li>
                    <li data-block-key="2ekt3">ct_loan_term_flag</li>
                </ul>
                <h5 data-block-key="8h181">Description</h5>
                <ul>
                    <li data-block-key="96bvf">When ‘credit product’ equals 1 (term loan - unsecured) or 2 (term loan - secured), ‘loan term: NA/NP flag’ must <b>not</b> equal 999 (not applicable).</li>
                    <li data-block-key="cmtbq">When ‘credit product’ equals 988 (not provided by applicant and otherwise undetermined), ‘loan term: NA/NP flag’ must equal 999.</li>
                </ul>
                <pre>
IF ct_credit_product is equal to 1 OR 2 THEN
    IF ct_loan_term_flag is equal to 999 THEN
        Error
    ENDIF
ELSEIF ct_credit_product is equal to 988 THEN
    IF ct_loan_term_flag is not equal to 999 THEN
        Error
    ENDIF
ENDIF

                </pre>
            </div>
            <div class="o-fig__section--sub-sub" data-search-section="" data-scrollspy="4.2">
                <h4 class="o-fig__heading">
                    <a id="4.2.4" href="#4.2.4"> Validation ID: ct_loan_term.conditional_field_conflict </a>
                </h4>
                <h5 data-block-key="ede7q">Affected data fields</h5>
                <ul>
                    <li data-block-key="d9o8q">ct_loan_term_flag</li>
                    <li data-block-key="1tg8c">ct_loan_term</li>
                </ul>
                <h5 data-block-key="8h181">Description</h5>
                <ul>
                    <li data-block-key="96bvf">When ‘loan term: NA/NP flag’ does <b>not</b> equal 900 (applicable and reported), ‘loan term’ must be blank.</li>
                    <li data-block-key="6fabh">When ‘loan term: NA/NP flag’ equals 900, ‘loan term’ must <b>not</b> be blank.</li>
                </ul>
                <pre>
IF ct_loan_term_flag is not equal to 900 THEN
    IF ct_loan_term is not blank THEN
        Error
    ENDIF
ELSEIF  ct_loan_term_flag is equal to 900 THEN
    IF ct_loan_term is blank THEN
        Error
    ENDIF
ENDIF

                </pre>
            </div>
            <div class="o-fig__section--sub-sub" data-search-section="" data-scrollspy="4.2">
                <h4 class="o-fig__heading">
                    <a id="4.2.5" href="#4.2.5"> Validation ID: credit_purpose_ff.conditional_field_conflict </a>
                </h4>
                <h5 data-block-key="ede7q">Affected data fields</h5>
                <ul>
                    <li data-block-key="d9o8q">credit_purpose</li>
                    <li data-block-key="diden">credit_purpose_ff</li>
                </ul>
                <h5 data-block-key="8h181">Description</h5>
                <ul>
                    <li data-block-key="96bvf">When ‘credit purpose’ does <b>not</b> contain 977 (other), ‘free-form text field for other credit purpose’ must be blank.</li>
                    <li data-block-key="3n1im">When ‘credit purpose’ contains 977, ‘free-form text field for other credit purpose’ must <b>not</b> be blank.</li>
                </ul>
                <pre>
IF credit_purpose does not contain 977 THEN
    IF credit_purpose_ff is not blank THEN
        Error
    ENDIF
ELSEIF credit_purpose contains 977 THEN
    IF credit_purpose_ff is blank THEN
        Error
    ENDIF
ENDIF

                </pre>
            </div>
            <div class="o-fig__section--sub-sub" data-search-section="" data-scrollspy="4.2">
                <h4 class="o-fig__heading">
                    <a id="4.2.6" href="#4.2.6"> Validation ID: amount_applied_for.conditional_field_conflict </a>
                </h4>
                <h5 data-block-key="ede7q">Affected data fields</h5>
                <ul>
                    <li data-block-key="d9o8q">amount_applied_for_flag</li>
                    <li data-block-key="bbo3f">amount_applied_for</li>
                </ul>
                <h5 data-block-key="8h181">Description</h5>
                <ul>
                    <li data-block-key="96bvf">When ‘amount applied for: NA/NP flag’ does <b>not</b> equal 900 (applicable and reported), ‘amount applied for’ must be blank.</li>
                    <li data-block-key="6fv5j">When ‘amount applied for: NA/NP flag’ equals 900, ‘amount applied for’ must <b>not</b> be blank.</li>
                </ul>
                <pre>
IF amount_applied_for_flag is not equal to 900 THEN
    IF amount_applied_for is not blank THEN
        Error
    ENDIF
ELSEIF amount_applied_for_flag is equal to 900 THEN
    IF amount_applied_for is blank THEN
        Error
    ENDIF
ENDIF

                </pre>
            </div>
            <div class="o-fig__section--sub-sub" data-search-section="" data-scrollspy="4.2">
                <h4 class="o-fig__heading">
                    <a id="4.2.7" href="#4.2.7"> Validation ID: amount_approved.conditional_field_conflict </a>
                </h4>
                <h5 data-block-key="ede7q">Affected data fields</h5>
                <ul>
                    <li data-block-key="d9o8q">action_taken</li>
                    <li data-block-key="823ag">amount_approved</li>
                </ul>
                <h5 data-block-key="8h181">Description</h5>
                <ul>
                    <li data-block-key="96bvf">When ‘action taken’ does <b>not</b> equal 1 (originated) or 2 (approved but not accepted), ‘amount approved or originated’ must be blank.</li>
                    <li data-block-key="77dlk">When ‘action taken’ equals 1 or 2, ‘amount approved or originated’ must <b>not</b> be blank.</li>
                </ul>
                <pre>
IF action_taken is not equal to 1 OR 2 THEN
    IF amount_approved is not blank THEN
        Error
    ENDIF
ELSEIF action_taken is equal to 1 OR 2 THEN
    IF amount_approved is blank THEN
        Error
    ENDIF
ENDIF

                </pre>
            </div>
            <div class="o-fig__section--sub-sub" data-search-section="" data-scrollspy="4.2">
                <h4 class="o-fig__heading">
                    <a id="4.2.8" href="#4.2.8"> Validation ID: action_taken_date.date_value_conflict </a>
                </h4>
                <h5 data-block-key="ede7q">Affected data fields</h5>
                <ul>
                    <li data-block-key="d9o8q">action_taken_date</li>
                    <li data-block-key="7itbh">app_date</li>
                </ul>
                <h5 data-block-key="8h181">Description</h5>
                <ul>
                    <li data-block-key="96bvf">The date indicated by ‘action taken date’ must occur on or after ‘application date’.</li>
                </ul>
                <pre>
IF action_taken_date is less than app_date THEN
    Error
ENDIF

                </pre>
            </div>
            <div class="o-fig__section--sub-sub" data-search-section="" data-scrollspy="4.2">
                <h4 class="o-fig__heading">
                    <a id="4.2.9" href="#4.2.9"> Validation ID: denial_reasons.enum_value_conflict </a>
                </h4>
                <h5 data-block-key="ede7q">Affected data fields</h5>
                <ul>
                    <li data-block-key="d9o8q">action_taken</li>
                    <li data-block-key="d3o6q">denial_reasons</li>
                </ul>
                <h5 data-block-key="8h181">Description</h5>
                <ul>
                    <li data-block-key="96bvf">When 'action taken' equals 3 (denied), 'denial reason(s)' must <b>not</b> contain 999 (not applicable).</li>
                    <li data-block-key="2iom9">When ‘action taken’ does <b>not</b> equal 3, ‘denial reason(s)’ must equal 999.</li>
                </ul>
                <pre>
If action_taken is equal to 3 THEN
    IF denial_reasons contains 999 THEN
        Error
    ENDIF
ELSEIF action_taken is not equal to 3 THEN
    IF denial_reasons is not equal to 999 THEN
        Error
    ENDIF
ENDIF

                </pre>
            </div>
            <div class="o-fig__section--sub-sub" data-search-section="" data-scrollspy="4.2">
                <h4 class="o-fig__heading">
                    <a id="4.2.10" href="#4.2.10"> Validation ID: denial_reasons_ff.conditional_field_conflict </a>
                </h4>
                <h5 data-block-key="ede7q">Affected data fields</h5>
                <ul>
                    <li data-block-key="d9o8q">denial_reasons</li>
                    <li data-block-key="f2sgi">denial_reasons_ff</li>
                </ul>
                <h5 data-block-key="8h181">Description</h5>
                <ul>
                    <li data-block-key="96bvf">When ‘denial reason(s)’ does <b>not</b> contain 977 (other), field ‘free-form text field for other denial reason(s)’ must be blank.</li>
                    <li data-block-key="vsi1">When ‘denial reason(s)’ contains 977, ‘free-form text field for other denial reason(s)’ must <b>not</b> be blank.</li>
                </ul>
                <pre>
IF denial_reasons does not contain 977 THEN
    IF denial_reasons_ff is not blank THEN
        Error
    ENDIF
ELSEIF denial_reasons contains 977 THEN
    IF denial_reasons_ff is blank THEN
        Error
    ENDIF
ENDIF

                </pre>
            </div>
            <div class="o-fig__section--sub-sub" data-search-section="" data-scrollspy="4.2">
                <h4 class="o-fig__heading">
                    <a id="4.2.11" href="#4.2.11"> Validation ID: pricing_all.conditional_fieldset_conflict </a>
                </h4>
                <h5 data-block-key="ede7q">Affected data fields</h5>
                <ul>
                    <li data-block-key="d9o8q">action_taken</li>
                    <li data-block-key="453dq">pricing_interest_rate_type</li>
                    <li data-block-key="9g4vm">pricing_mca_addcost_flag</li>
                    <li data-block-key="7rdsd">pricing_prepenalty_allowed</li>
                    <li data-block-key="8fe2b">pricing_prepenalty_exists</li>
                    <li data-block-key="12ffk">pricing_origination_charge</li>
                    <li data-block-key="admb9">pricing_broker_fees</li>
                    <li data-block-key="9e25k">pricing_initial_charges</li>
                </ul>
                <h5 data-block-key="e65g7">Description</h5>
                <p data-block-key="96bvf">When 'action taken' equals 3 (denied), 4 (withdrawn by applicant), or 5 (incomplete), the following fields must all equal 999 (not applicable):</p>
                <ul>
                    <li data-block-key="2naq4">'Interest rate type'</li>
                    <li data-block-key="3bllc">'MCA/sales-based: additional cost for merchant cash advances or other sales-based financing: NA flag'</li>
                    <li data-block-key="11vrb">'Prepayment penalty could be imposed'</li>
                    <li data-block-key="bl5au">'Prepayment penalty exists'</li>
                </ul>
                <p data-block-key="3qid6">And the following fields must all be blank:</p>
                <ul>
                    <li data-block-key="a8b13">'Total origination charges'</li>
                    <li data-block-key="bpatc">'Amount of total broker fees'</li>
                    <li data-block-key="ea7v9">'Initial annual charges'</li>
                </ul>
                <pre>
IF action_taken is equal to 3, 4, or 5 THEN
    IF (pricing_interest_rate_type is not equal to 999 OR
        pricing_mca_addcost_flag is not equal to 999 OR
        pricing_prepenalty_allowed is not equal to 999 OR
        pricing_prepenalty_exists is not equal to 999 OR
        pricing_origination_charges is not blank OR
        pricing_broker_fees is not blank OR
        pricing_initial_charges is not blank) THEN
            Error
    ENDIF
ENDIF

                </pre>
            </div>
            <div class="o-fig__section--sub-sub" data-search-section="" data-scrollspy="4.2">
                <h4 class="o-fig__heading">
                    <a id="4.2.12" href="#4.2.12"> Validation ID: pricing_charges.conditional_fieldset_conflict </a>
                </h4>
                <h5 data-block-key="nsktb">Affected data fields</h5>
                <ul>
                    <li data-block-key="c7g08">action_taken</li>
                    <li data-block-key="ceb6c">pricing_origination_charges</li>
                    <li data-block-key="3tr1c">pricing_broker_fees</li>
                    <li data-block-key="co26t">pricing_initial_charges</li>
                    <li data-block-key="fgsbc">pricing_prepenalty_allowed</li>
                    <li data-block-key="7vk8n">pricing_prepenalty_exists</li>
                </ul>
                <h5 data-block-key="2tt09">Description</h5>
                <p data-block-key="e48i5">When 'action taken' equals 1 (originated) or 2 (approved but not accepted), the following fields all must <b>not</b> be blank:</p>
                <ul>
                    <li data-block-key="b91qp">'Total origination charges'</li>
                    <li data-block-key="3re3f">'Amount of total broker fees'</li>
                    <li data-block-key="5n9qb">'Initial annual charges'</li>
                </ul>
                <p data-block-key="f4apk">And the following fields must <b>not</b> equal 999 (not applicable):</p>
                <ul>
                    <li data-block-key="ejqkf">'Prepayment penalty could be imposed'</li>
                    <li data-block-key="5a9bs">'Prepayment penalty exists'</li>
                </ul>
                <pre>
IF action_taken is equal to 1 or 2 THEN
    IF (pricing_origination_charges is blank OR
        pricing_broker_fees is blank OR
        pricing_initial_charges is blank OR
        pricing_prepenalty_allowed is equal to 999 OR
        pricing_prepenalty_exists is equal to 999) THEN
            Error
    ENDIF
ENDIF

                </pre>
            </div>
            <div class="o-fig__section--sub-sub" data-search-section="" data-scrollspy="4.2">
                <h4 class="o-fig__heading">
                    <a id="4.2.13" href="#4.2.13"> Validation ID: pricing_init_rate_period.conditional_field_conflict </a>
                </h4>
                <h5 data-block-key="txmgs">Affected data fields</h5>
                <ul>
                    <li data-block-key="adlaj">pricing_interest_rate_type</li>
                    <li data-block-key="3jv9f">pricing_init_rate_period</li>
                </ul>
                <h5 data-block-key="da9ir">Description</h5>
                <ul>
                    <li data-block-key="frodl">
                        When 'interest rate type' does <b>not</b> equal 3 (initial rate period &gt; 12 months, variable interest), 4 (initial rate period &gt; 12 months, fixed interest), 5 (initial rate period &lt;= 12 months, variable
                        interest), or 6 (initial rate period &lt;= 12 months, fixed interest), 'initial rate period' must be blank.
                    </li>
                    <li data-block-key="dpuhb">When 'interest rate type' equals 3, 4, 5, or 6, 'initial rate period' must <b>not</b> be blank</li>
                </ul>
                <pre>
IF pricing_interest_rate_type is not equal to 3, 4, 5, or 6 THEN
    IF pricing_init_rate_period is not blank THEN
        Error
    ENDIF
ELSEIF pricing_interest_rate_type is equal to 3, 4, 5, or 6 THEN
    IF pricing_init_rate_period is blank THEN
        Error
    ENDIF
ENDIF

                </pre>
            </div>
            <div class="o-fig__section--sub-sub" data-search-section="" data-scrollspy="4.2">
                <h4 class="o-fig__heading">
                    <a id="4.2.14" href="#4.2.14"> Validation ID: pricing_fixed_rate.conditional_field_conflict </a>
                </h4>
                <h5 data-block-key="txmgs">Affected data fields</h5>
                <ul>
                    <li data-block-key="2ft0t">pricing_interest_rate_type</li>
                    <li data-block-key="83tgs">pricing_fixed_rate</li>
                </ul>
                <h5 data-block-key="b7i2e">Description</h5>
                <ul>
                    <li data-block-key="38scp">
                        When 'interest rate type' does <b>not</b> equal 2 (fixed interest rate, no initial rate period), 4 (initial rate period &gt; 12 months, fixed interest rate), or 6 (initial rate period &lt;= 12 months, fixed interest
                        rate), 'fixed rate: interest rate' must be blank.
                    </li>
                    <li data-block-key="cra81">When 'interest rate type' equals 2, 4, or 6, 'fixed rate: interest rate' must <b>not</b> be blank.</li>
                </ul>
                <pre>
            IF pricing_interest_rate_type is not equal to 2, 4, or 6 THEN
                IF pricing_fixed_rate is not blank THEN
                    Error
                ENDIF
            ELSEIF pricing_interest_rate_type is equal to 2, 4, or 6 THEN
                IF pricing_fixed_rate is blank THEN
                    Error
                ENDIF
            ENDIF

                </pre>
            </div>
            <div class="o-fig__section--sub-sub" data-search-section="" data-scrollspy="4.2">
                <h4 class="o-fig__heading">
                    <a id="4.2.15" href="#4.2.15"> Validation ID: pricing_var_margin.conditional_field_conflict </a>
                </h4>
                <h5 data-block-key="txmgs">Affected data fields</h5>
                <ul>
                    <li data-block-key="85kob">pricing_interest_rate_type</li>
                    <li data-block-key="2odir">pricing_var_margin</li>
                </ul>
                <h5 data-block-key="95doi">Description</h5>
                <ul>
                    <li data-block-key="abji3">
                        When 'interest rate type' does <b>not</b> equal 1 (variable interest rate, no initial rate period), 3 (initial rate period &gt; 12 months, variable interest rate), or 5 (initial rate period &lt;= 12 months, variable
                        interest rate), 'variable rate transaction: margin' must be blank.
                    </li>
                    <li data-block-key="9njhn">When 'interest rate type' equals 1, 3, or 5, 'variable rate transaction: margin' must <b>not</b> be blank.</li>
                </ul>
                <pre>
            IF pricing_interest_rate_type is not equal to 1, 3, or 5 THEN
                IF pricing_var_margin is not blank THEN
                    Error
                ENDIF
            ELSEIF pricing_interest_rate_type is equal to 1, 3, or 5 THEN
                IF pricing_var_margin is blank THEN
                    Error
                ENDIF
            ENDIF

                </pre>
            </div>
            <div class="o-fig__section--sub-sub" data-search-section="" data-scrollspy="4.2">
                <h4 class="o-fig__heading">
                    <a id="4.2.16" href="#4.2.16"> Validation ID: pricing_var_index_name.enum_value_conflict </a>
                </h4>
                <h5 data-block-key="5tbwp">Affected data fields</h5>
                <ul>
                    <li data-block-key="f4u7l">pricing_interest_rate_type</li>
                    <li data-block-key="7ubfv">pricing_var_index_name</li>
                </ul>
                <h5 data-block-key="foqm4">Description</h5>
                <ul>
                    <li data-block-key="bn1rd">
                        When 'interest rate type' does <b>not</b> equal 1 (variable interest rate, no initial rate period), 3 (initial rate period &gt; 12 months, variable interest rate), or 5 (initial rate period &lt;= 12 months, variable
                        interest rate), 'variable rate transaction: index name' must equal 999.
                    </li>
                    <li data-block-key="5nsh0">When 'interest rate type' equals 1, 3, or 5, 'variable rate transaction: index name' must <b>not</b> equal 999.</li>
                </ul>
                <pre>
            IF pricing_interest_rate_type is not equal to 1, 3, or 5 THEN
                IF pricing_var_index_name is not equal to 999 THEN
                    Error
                ENDIF
            ELSEIF pricing_interest_rate_type is equal to 1, 3, or 5 THEN
                IF pricing_var_index_name is equal to 999 THEN
                    Error
                ENDIF
            ENDIF

                </pre>
            </div>
            <div class="o-fig__section--sub-sub" data-search-section="" data-scrollspy="4.2">
                <h4 class="o-fig__heading">
                    <a id="4.2.17" href="#4.2.17"> Validation ID: pricing_var_index_name_ff.conditional_field_conflict </a>
                </h4>
                <h5 data-block-key="5tbwp">Affected data fields</h5>
                <ul>
                    <li data-block-key="fl230">pricing_var_index_name;</li>
                    <li data-block-key="77op0">pricing_var_index_name_ff</li>
                </ul>
                <h5 data-block-key="1jcnt">Description</h5>
                <ul>
                    <li data-block-key="7p24a">When 'variable rate transaction: index name' does <b>not</b> equal 977 (other), 'variable rate transaction: index name: other' must be blank</li>
                    <li data-block-key="6lvlc">When 'variable rate transaction: index name' equals 977, 'variable rate transaction: index name: other' must <b>not</b> be blank.</li>
                </ul>
                <pre>
            IF pricing_var_index_name is not equal to 977 THEN
                IF pricing_var_index_name_ff is not blank THEN
                    Error
                ENDIF
            ELSEIF pricing_var_index_name is equal to 977 THEN
                IF pricing_var_index_name_ff is blank THEN
                    Error
                ENDIF
            ENDIF

                </pre>
            </div>
            <div class="o-fig__section--sub-sub" data-search-section="" data-scrollspy="4.2">
                <h4 class="o-fig__heading">
                    <a id="4.2.18" href="#4.2.18"> Validation ID: pricing_var_index_value.conditional_field_conflict </a>
                </h4>
                <h5 data-block-key="txmgs">Affected data fields</h5>
                <ul>
                    <li data-block-key="9kve7">pricing_interest_rate_type</li>
                    <li data-block-key="dgmrl">pricing_var_index_value</li>
                </ul>
                <h5 data-block-key="ac9s3">Description</h5>
                <ul>
                    <li data-block-key="92rnp">
                        When 'interest rate type' does <b>not</b> equal 1 (variable interest rate, no initial rate period), or 3 (initial rate period &gt; 12 months, variable interest rate), 'variable rate transaction: index value' must be
                        blank.
                    </li>
                    <li data-block-key="24i4b">When 'interest rate type' equals 1 or 3, 'variable rate transaction: index value' must <b>not</b> be blank.</li>
                </ul>
                <pre>
            IF pricing_interest_rate_type is not equal to 1 or 3 THEN
                IF pricing_var_index_value is not blank THEN
                    Error
                ENDIF
            ELSEIF pricing_interest_rate_type is equal to 1 or 3 THEN
                IF pricing_var_index_value is blank THEN
                    Error
                ENDIF
            ENDIF

                </pre>
            </div>
            <div class="o-fig__section--sub-sub" data-search-section="" data-scrollspy="4.2">
                <h4 class="o-fig__heading">
                    <a id="4.2.19" href="#4.2.19"> Validation ID: pricing_mca_addcost_flag.enum_value_conflict </a>
                </h4>
                <h5 data-block-key="txmgs">Affected data fields</h5>
                <ul>
                    <li data-block-key="fb8mf">ct_credit_product</li>
                    <li data-block-key="fljcs">pricing_mca_addcost_flag</li>
                </ul>
                <h5 data-block-key="5h4nb">Description</h5>
                <ul>
                    <li data-block-key="efmnk">
                        When 'credit product' does <b>not</b> equal 7 (merchant cash advance), 8 (other sales-based financing transaction) or 977 (other), ‘MCA/sales-based: additional cost for merchant cash advances or other sales-based
                        financing: NA flag’ must be 999 (not applicable).
                    </li>
                </ul>
                <pre>
            IF ct_credit_product is not equal to 7, 8, OR 977 THEN
                IF pricing_mca_addcost_flag is not equal to 999 THEN
                    Error
                ENDIF
            ENDIF

                </pre>
            </div>
            <div class="o-fig__section--sub-sub" data-search-section="" data-scrollspy="4.2">
                <h4 class="o-fig__heading">
                    <a id="4.2.20" href="#4.2.20"> Validation ID: pricing_mca_addcost.conditional_field_conflict </a>
                </h4>
                <h5 data-block-key="txmgs">Affected data fields</h5>
                <ul>
                    <li data-block-key="7adin">pricing_mca_addcost_flag</li>
                    <li data-block-key="4k6k7">pricing_mca_addcost</li>
                </ul>
                <h5 data-block-key="fkn0">Description</h5>
                <ul>
                    <li data-block-key="5tlii">
                        When ‘MCA/sales-based: additional cost for merchant cash advances or other sales-based financing: NA flag’ does <b>not</b> equal 900 (applicable), ‘MCA/sales-based: additional cost for merchant cash advances or other
                        sales-based financing’ must be blank.
                    </li>
                    <li data-block-key="24j0c">
                        When ‘MCA/sales-based: additional cost for merchant cash advances or other sales-based financing: NA flag’ equals 900, ‘MCA/sales-based: additional cost for merchant cash advances or other sales-based financing’ must
                        <b>not</b> be blank.
                    </li>
                </ul>
                <pre>
            IF pricing_mca_addcost_flag is not equal to 900 THEN
                IF pricing_mca_addcost is not blank THEN
                    Error
                ENDIF
            ELSEIF IF pricing_mca_addcost_flag is equal to 900 THEN
                IF pricing_mca_addcost is blank THEN
                    Error
                ENDIF
            ENDIF

                </pre>
            </div>
            <div class="o-fig__section--sub-sub" data-search-section="" data-scrollspy="4.2">
                <h4 class="o-fig__heading">
                    <a id="4.2.21" href="#4.2.21"> Validation ID: census_tract_number.conditional_field_conflict </a>
                </h4>
                <h5 data-block-key="2r7yt">Affected data fields</h5>
                <ul>
                    <li data-block-key="b8vk6">census_tract_adr_type</li>
                    <li data-block-key="8eejk">census_tract_number</li>
                </ul>
                <h5 data-block-key="q6v4">Description</h5>
                <ul>
                    <li data-block-key="146sc">When ‘census tract: type of address’ equals 988 (not provided by applicant and otherwise undetermined), ‘census tract: tract number’ must be blank.</li>
                    <li data-block-key="fhqqq">
                        When ‘census tract: type of address’ equals 1 (address or location where the loan proceeds will principally be applied), 2 (address or location of borrower’s main office or headquarters), or 3 (another address or
                        location associated with the applicant), ‘census tract: tract number’ must <b>not</b> be blank.
                    </li>
                </ul>
                <pre>
            IF census_tract_adr_type is equal to 988 THEN
                IF census_tract_number is not blank THEN
                    Error
                ENDIF
            ELSEIF census_tract_adr_type is equal to 1, 2, OR 3 THEN
                IF census_tract_number is blank THEN
                    Error
                ENDIF
            ENDIF

                </pre>
            </div>
            <div class="o-fig__section--sub-sub" data-search-section="" data-scrollspy="4.2">
                <h4 class="o-fig__heading">
                    <a id="4.2.22" href="#4.2.22"> Validation ID: gross_annual_revenue.conditional_field_conflict </a>
                </h4>
                <h5 data-block-key="2r7yt">Affected data fields</h5>
                <ul>
                    <li data-block-key="92h7">gross_annual_revenue_flag</li>
                    <li data-block-key="fkcjm">gross_annual_revenue</li>
                </ul>
                <h5 data-block-key="4sdmi">Description</h5>
                <ul>
                    <li data-block-key="89k8r">When ‘gross annual revenue: NP flag’ does <b>not</b> equal 900 (reported), ‘gross annual revenue’ must be blank.</li>
                    <li data-block-key="kk4h">When ‘gross annual revenue: NP flag’ equals 900, ‘gross annual revenue’ must <b>not</b> be blank.</li>
                </ul>
                <pre>
            IF gross_annual_revenue_flag is not equal to 900 THEN
                IF gross_annual_revenue is not blank THEN
                    Error
                ENDIF
            ELSEIF gross_annual_revenue_flag is equal to 900 THEN
                IF gross_annual_revenue is blank THEN
                    Error
                ENDIF
            ENDIF

                </pre>
            </div>
            <div class="o-fig__section--sub-sub" data-search-section="" data-scrollspy="4.2">
                <h4 class="o-fig__heading">
                    <a id="4.2.23" href="#4.2.23"> Validation ID: naics_code.conditional_field_conflict </a>
                </h4>
                <h5 data-block-key="2r7yt">Affected data fields</h5>
                <ul>
                    <li data-block-key="92h7">naics_code_flag</li>
                    <li data-block-key="fkcjm">naics_code</li>
                </ul>
                <h5 data-block-key="4sdmi">Description</h5>
                <ul>
                    <li data-block-key="89k8r">When ‘North American Industry Classification System (NAICS) code: NP flag’ does <b>not</b> equal 900 (reported), ‘North American Industry Classification System (NAICS) code’ must be blank.</li>
                    <li data-block-key="kk4h">When ‘North American Industry Classification System (NAICS) code: NP flag’ equals 900, ‘North American Industry Classification System (NAICS) code’ must <b>not</b> be blank.</li>
                </ul>
                <pre>
            IF naics_code_flag is not equal to 900 THEN
                IF naics_code is not blank THEN
                    Error
                ENDIF
            ELSEIF naics_code_flag is equal to 900 THEN
                IF naics_code is blank THEN
                    Error
                ENDIF
            ENDIF

                </pre>
            </div>
            <div class="o-fig__section--sub-sub" data-search-section="" data-scrollspy="4.2">
                <h4 class="o-fig__heading">
                    <a id="4.2.24" href="#4.2.24"> Validation ID: time_in_business.conditional_field_conflict </a>
                </h4>
                <h5 data-block-key="2r7yt">Affected data fields</h5>
                <ul>
                    <li data-block-key="5evn2">time_in_business_type</li>
                    <li data-block-key="18i9l">time_in_business</li>
                </ul>
                <h5 data-block-key="esrms">Description</h5>
                <ul>
                    <li data-block-key="3o11j">
                        When ‘time in business: type of response’ does <b>not</b> equal 1 (the number of years an applicant has been in business is collected or obtained by the financial institution), ‘time in business’ must be blank.
                    </li>
                    <li data-block-key="2g58a">When ‘time in business: type of response’ equals 1, ‘time in business’ must <b>not</b> be blank.</li>
                </ul>
                <pre>
            IF time_in_business_type is not equal to 1 THEN
                IF time_in_business is not blank THEN
                    Error
                ENDIF
            ELSEIF time_in_business_type is equal to 1 THEN
                IF time_in_business is blank THEN
                    Error
                ENDIF
            ENDIF

                </pre>
            </div>
            <div class="o-fig__section--sub-sub" data-search-section="" data-scrollspy="4.2">
                <h4 class="o-fig__heading">
                    <a id="4.2.25" href="#4.2.25"> Validation ID: num_principal_owners.conditional_field_conflict </a>
                </h4>
                <h5 data-block-key="2r7yt">Affected data fields</h5>
                <ul>
                    <li data-block-key="flbdu">num_principal_owners_flag</li>
                    <li data-block-key="j1iq">num_principal_owners</li>
                </ul>
                <h5 data-block-key="3b5hm">Description</h5>
                <ul>
                    <li data-block-key="5u621">When ‘number of principal owners: NP flag’ does <b>not</b> equal 900 (reported), ‘number of principal owners’ must be blank.</li>
                    <li data-block-key="d8mbp">When ‘number of principal owners: NP flag’ equals 900, ‘number of principal owners’ must <b>not</b> be blank.</li>
                </ul>
                <pre>
            IF num_principal_owners_flag is not equal to 900 THEN
                IF num_principal_owners is not blank THEN
                    Error
                ENDIF
            ELSEIF num_principal_owners_flag is equal to 900 THEN
                IF num_principal_owners is blank THEN
                    Error
                ENDIF
            ENDIF

                </pre>
            </div>
            <div class="o-fig__section--sub-sub" data-search-section="" data-scrollspy="4.2">
                <h4 class="o-fig__heading">
                    <a id="4.2.26" href="#4.2.26"> Validation ID: po_X_ethnicity_ff.conditional_field_conflict </a>
                </h4>
                <h5 data-block-key="2r7yt">Affected data fields</h5>
                <ul>
                    <li data-block-key="2j7hr">po_X_ethnicity</li>
                    <li data-block-key="81ul">po_X_ethnicity_ff</li>
                </ul>
                <h5 data-block-key="4furu">Description</h5>
                <ul>
                    <li data-block-key="4vuac">
                        When ‘ethnicity of principal owner X’ does <b>not</b> contain 977 (the applicant responded in the free-form text field), ‘ethnicity of principal owner X: free-form text field for other Hispanic or Latino' must be
                        blank.
                    </li>
                    <li data-block-key="8ijot">When ‘ethnicity of principal owner X’ contains 977, ‘ethnicity of principal owner X: free-form text field for other Hispanic or Latino’ must <b>not</b> be blank.</li>
                </ul>
                <pre>
            IF po_X_ethnicity does not contain 977 THEN
                IF po_X_ethnicity_ff is not blank THEN
                    Error
                ENDIF
            ELSEIF po_X_ethnicity contains 977 THEN
                IF po_X_ethnicity_ff is blank THEN
                    Error
                ENDIF
            ENDIF

                </pre>
            </div>
            <div class="o-fig__section--sub-sub" data-search-section="" data-scrollspy="4.2">
                <h4 class="o-fig__heading">
                    <a id="4.2.27" href="#4.2.27"> Validation ID: po_X_race_anai_ff.conditional_field_conflict </a>
                </h4>
                <h5 data-block-key="2r7yt">Affected data fields</h5>
                <ul>
                    <li data-block-key="7372e">po_X_race</li>
                    <li data-block-key="10iac">po_X_race_anai_ff</li>
                </ul>
                <h5 data-block-key="5ft7t">Description</h5>
                <ul>
                    <li data-block-key="7bors">
                        When ‘race of principal owner X’ does <b>not</b> contain 971 (the applicant responded in the free-form text field for American Indian or Alaska Native Enrolled or Principal Tribe), ‘race of principal owner X:
                        free-form text field for American Indian or Alaska Native Enrolled or Principal Tribe’ must be blank.
                    </li>
                    <li data-block-key="5puh">When ‘race of principal owner X’ contains 971, ‘race of principal owner X: free-form text field for American Indian or Alaska Native Enrolled or Principal Tribe’ must <b>not</b> be blank.</li>
                </ul>
                <pre>
            IF po_X_race does not contain 971 THEN
                IF po_X_race_anai_ff is not blank THEN
                    Error
                ENDIF
            ELSEIF po_X_race contains 971 THEN
                IF po_X_race_anai_ff is blank THEN
                    Error
                ENDIF
            ENDIF

                </pre>
            </div>
            <div class="o-fig__section--sub-sub" data-search-section="" data-scrollspy="4.2">
                <h4 class="o-fig__heading">
                    <a id="4.2.28" href="#4.2.28"> Validation ID: po_X_race_asian_ff.conditional_field_conflict </a>
                </h4>
                <h5 data-block-key="2r7yt">Affected data fields</h5>
                <ul>
                    <li data-block-key="ca152">po_X_race</li>
                    <li data-block-key="e8n5m">po_X_race_asian_ff</li>
                </ul>
                <h5 data-block-key="8df9a">Description</h5>
                <ul>
                    <li data-block-key="9me4l">
                        When ‘race of principal owner X’ does <b>not</b> contain 972 (the applicant responded in the free-form text field for other Asian race), ‘race of principal owner X: free-form text field for other Asian’ must be
                        blank.
                    </li>
                    <li data-block-key="ck3at">When ‘race of principal owner X’ contains 972, ‘race of principal owner X: free-form text field for other Asian’ must <b>not</b> be blank.</li>
                </ul>
                <pre>
            IF po_X_race does not contain 972 THEN
                IF po_X_race_asian_ff is not blank THEN
                    Error
                ENDIF
            ELSEIF po_X_race contains 972 THEN
                IF po_X_race_asian_ff is blank THEN
                    Error
                ENDIF
            ENDIF

                </pre>
            </div>
            <div class="o-fig__section--sub-sub" data-search-section="" data-scrollspy="4.2">
                <h4 class="o-fig__heading">
                    <a id="4.2.29" href="#4.2.29"> Validation ID: po_X_race_baa_ff.conditional_field_conflict </a>
                </h4>
                <h5 data-block-key="2r7yt">Affected data fields</h5>
                <ul>
                    <li data-block-key="2f3kk">po_X_race</li>
                    <li data-block-key="87meg">po_X_race_baa_ff</li>
                </ul>
                <h5 data-block-key="9tt41">Description</h5>
                <ul>
                    <li data-block-key="amfq">
                        When ‘race of principal owner X’ does <b>not</b> contain 973 (the applicant responded in the free-form text field for other Black or African race), ‘race of principal owner X: free-form text field for other Black or
                        African American’ must be blank.
                    </li>
                    <li data-block-key="9h089">When ‘race of principal owner X’ contains 973, ‘race of principal owner X: free-form text field for other Black or African American’ must <b>not</b> be blank.</li>
                </ul>
                <pre>
            IF po_X_race does not contain 973 THEN
                IF po_X_race_baa_ff is not blank THEN
                    Error
                ENDIF
            ELSEIF po_X_race contains 973 THEN
                IF po_X_race_baa_ff is blank THEN
                    Error
                ENDIF
            ENDIF

                </pre>
            </div>
            <div class="o-fig__section--sub-sub" data-search-section="" data-scrollspy="4.2">
                <h4 class="o-fig__heading">
                    <a id="4.2.30" href="#4.2.30"> Validation ID: po_X_race_pi_ff.conditional_field_conflict </a>
                </h4>
                <h5 data-block-key="2r7yt">Affected data fields</h5>
                <ul>
                    <li data-block-key="e8reo">po_X_race</li>
                    <li data-block-key="cotj1">po_X_race_pi_ff</li>
                </ul>
                <h5 data-block-key="4ij0g">Description</h5>
                <ul>
                    <li data-block-key="rgu9">
                        When ‘race of principal owner X’ does <b>not</b> contain 974 (the applicant responded in the free-form text field for other Pacific Islander race), ‘race of principal owner X: free-form text field for other Pacific
                        Islander race’ must be blank.
                    </li>
                    <li data-block-key="ef482">When ‘race of principal owner X’ contains 974, ‘race of principal owner X: free-form text field for other Pacific Islander race’ must <b>not</b> be blank.</li>
                </ul>
                <pre>
            IF po_X_race does not contain 974 THEN
                IF po_X_race_pi_ff is not blank THEN
                    Error
                ENDIF
            ELSEIF po_X_race contains 974 THEN
                IF po_X_race_pi_ff is blank THEN
                    Error
                ENDIF
            ENDIF

                </pre>
            </div>
            <div class="o-fig__section--sub-sub" data-search-section="" data-scrollspy="4.2">
                <h4 class="o-fig__heading">
                    <a id="4.2.31" href="#4.2.31"> Validation ID: po_X_gender_ff.conditional_field_conflict </a>
                </h4>
                <h5 data-block-key="2r7yt">Affected data fields</h5>
                <ul>
                    <li data-block-key="55rcg">po_X_gender_flag</li>
                    <li data-block-key="e8n3i">po_X_gender_ff</li>
                </ul>
                <h5 data-block-key="9er58">Description</h5>
                <ul>
                    <li data-block-key="9r97c">
                        When ‘sex/gender of principal owner X: NP flag’ does <b>not</b> equal 1 (the applicant responded in the free-form text field), ‘sex/gender of principal owner X: free-form text field for self-identified sex/gender’
                        must be blank.
                    </li>
                    <li data-block-key="5fdfe">When ‘sex/gender of principal owner X: NP flag’ equals 1, ‘sex/gender of principal owner X: free-form text field for self-identified sex/gender’ must <b>not</b> be blank.</li>
                </ul>
                <pre>
            IF po_X_gender_flag does not contain 1 THEN
                IF po_X_gender_ff is not blank THEN
                    Error
                ENDIF
            ELSEIF po_X_gender_flag contains 1 THEN
                IF po_X_gender_ff is blank THEN
                    Error
                ENDIF
            ENDIF

                </pre>
            </div>
            <div class="o-fig__section--sub" data-search-section="" data-scrollspy="4.3">
                <h3 class="o-fig__heading">
                    <a id="4.3" href="#4.3"> 4.3. Register-level errors </a>
                </h3>
            </div>
            <div class="o-fig__section--sub-sub" data-search-section="" data-scrollspy="4.3">
                <h4 class="o-fig__heading">
                    <a id="4.3.1" href="#4.3.1"> Validation ID: uid.duplicates_in_dataset </a>
                </h4>
                <h5 data-block-key="wuz9u">Affected data fields</h5>
                <ul>
                    <li data-block-key="7m789">uid</li>
                </ul>
                <h5 data-block-key="450mr">Description</h5>
                <ul>
                    <li data-block-key="dn2kn">Any ‘unique identifier’ may <b>not</b> be used in more than one record within a small business lending application register.</li>
                </ul>
                <pre>
            IF uid is duplicated within this filing THEN
                Error
            ENDIF

                </pre>
            </div>
            <div class="o-fig__section--sub" data-search-section="" data-scrollspy="4.4">
                <h3 class="o-fig__heading">
                    <a id="4.4" href="#4.4"> 4.4. Single-field warnings </a>
                </h3>
            </div>
            <div class="o-fig__section--sub-sub" data-search-section="" data-scrollspy="4.4">
                <h4 class="o-fig__heading">
                    <a id="4.4.1" href="#4.4.1"> Validation ID: uid.invalid_uid_lei </a>
                </h4>
                <h5 data-block-key="cqb8n">Affected data field</h5>
                <ul>
                    <li data-block-key="98h98">uid</li>
                </ul>
                <h5 data-block-key="e1ksj">Description</h5>
                <ul>
                    <li data-block-key="d8fnd">The first 20 characters of the ‘unique identifier’ should match the Legal Entity Identifier (LEI) for the financial institution.</li>
                </ul>
            </div>
            <div class="o-fig__section--sub-sub" data-search-section="" data-scrollspy="4.4">
                <h4 class="o-fig__heading">
                    <a id="4.4.2" href="#4.4.2"> Validation ID: ct_guarantee.multi_value_field_restriction </a>
                </h4>
                <h5 data-block-key="wuz9u">Affected data field</h5>
                <ul>
                    <li data-block-key="botk1">ct_guarantee</li>
                </ul>
                <h5 data-block-key="bb35j">Description</h5>
                <ul>
                    <li data-block-key="2ek0k">When ‘type of guarantee’ contains 999 (no guarantee), ‘type of guarantee’ should <b>not</b> contain more than one value.</li>
                </ul>
            </div>
            <div class="o-fig__section--sub-sub" data-search-section="" data-scrollspy="4.4">
                <h4 class="o-fig__heading">
                    <a id="4.4.3" href="#4.4.3"> Validation ID: ct_guarantee.duplicates_in_field </a>
                </h4>
                <h5 data-block-key="wuz9u">Affected data field</h5>
                <ul>
                    <li data-block-key="botk1">ct_guarantee</li>
                </ul>
                <h5 data-block-key="bb35j">Description</h5>
                <ul>
                    <li data-block-key="2ek0k">‘Type of guarantee’ should <b>not</b> contain duplicated values.</li>
                </ul>
            </div>
            <div class="o-fig__section--sub-sub" data-search-section="" data-scrollspy="4.4">
                <h4 class="o-fig__heading">
                    <a id="4.4.4" href="#4.4.4"> Validation ID: ct_loan_term.unreasonable_numeric_value </a>
                </h4>
                <h5 data-block-key="wuz9u">Affected data field</h5>
                <ul>
                    <li data-block-key="botk1">ct_loan_term</li>
                </ul>
                <h5 data-block-key="bb35j">Description</h5>
                <ul>
                    <li data-block-key="2ek0k">When present, ‘loan term’ should be less than 1200 (100 years).</li>
                </ul>
            </div>
            <div class="o-fig__section--sub-sub" data-search-section="" data-scrollspy="4.4">
                <h4 class="o-fig__heading">
                    <a id="4.4.5" href="#4.4.5"> Validation ID: credit_purpose.multi_value_field_restriction </a>
                </h4>
                <h5 data-block-key="wuz9u">Affected data field</h5>
                <ul>
                    <li data-block-key="botk1">credit_purpose</li>
                </ul>
                <h5 data-block-key="bb35j">Description</h5>
                <ul>
                    <li data-block-key="2ek0k">When ‘credit purpose’ contains 988 (not provided by applicant and otherwise undetermined) or 999 (not applicable), ‘credit purpose’ should <b>not</b> contain more than one value.</li>
                </ul>
            </div>
            <div class="o-fig__section--sub-sub" data-search-section="" data-scrollspy="4.4">
                <h4 class="o-fig__heading">
                    <a id="4.4.6" href="#4.4.6"> Validation ID: credit_purpose.duplicates_in_field </a>
                </h4>
                <h5 data-block-key="wuz9u">Affected data field</h5>
                <ul>
                    <li data-block-key="botk1">credit_purpose</li>
                </ul>
                <h5 data-block-key="bb35j">Description</h5>
                <ul>
                    <li data-block-key="2ek0k">‘Credit purpose’ should <b>not</b> contain duplicated values.</li>
                </ul>
            </div>
            <div class="o-fig__section--sub-sub" data-search-section="" data-scrollspy="4.4">
                <h4 class="o-fig__heading">
                    <a id="4.4.7" href="#4.4.7"> Validation ID: denial_reasons.multi_value_field_restriction </a>
                </h4>
                <h5 data-block-key="wuz9u">Affected data field</h5>
                <ul>
                    <li data-block-key="botk1">denial_reasons</li>
                </ul>
                <h5 data-block-key="bb35j">Description</h5>
                <ul>
                    <li data-block-key="2ek0k">When ‘denial reason(s)’ contains 999 (not applicable), ‘denial reason(s)’ should <b>not</b> contain more than one value.</li>
                </ul>
            </div>
            <div class="o-fig__section--sub-sub" data-search-section="" data-scrollspy="4.4">
                <h4 class="o-fig__heading">
                    <a id="4.4.8" href="#4.4.8"> Validation ID: denial_reasons.duplicates_in_field </a>
                </h4>
                <h5 data-block-key="wuz9u">Affected data field</h5>
                <ul>
                    <li data-block-key="botk1">denial_reasons</li>
                </ul>
                <h5 data-block-key="bb35j">Description</h5>
                <ul>
                    <li data-block-key="2ek0k">‘Denial reason(s)’ should <b>not</b> contain duplicated values.</li>
                </ul>
            </div>
            <div class="o-fig__section--sub-sub" data-search-section="" data-scrollspy="4.4">
                <h4 class="o-fig__heading">
                    <a id="4.4.9" href="#4.4.9"> Validation ID: pricing_fixed_rate.unreasonable_numeric_value </a>
                </h4>
                <h5 data-block-key="wuz9u">Affected data field</h5>
                <ul>
                    <li data-block-key="botk1">pricing_fixed_rate</li>
                </ul>
                <h5 data-block-key="bb35j">Description</h5>
                <ul>
                    <li data-block-key="248b8">When present, ‘fixed rate: interest rate’ should generally be greater than 0.1.</li>
                </ul>
            </div>
            <div class="o-fig__section--sub-sub" data-search-section="" data-scrollspy="4.4">
                <h4 class="o-fig__heading">
                    <a id="4.4.10" href="#4.4.10"> Validation ID: pricing_var_margin.unreasonable_numeric_value </a>
                </h4>
                <h5 data-block-key="wuz9u">Affected data field</h5>
                <ul>
                    <li data-block-key="botk1">pricing_var_margin</li>
                </ul>
                <h5 data-block-key="bb35j">Description</h5>
                <ul>
                    <li data-block-key="8jhbc">When present, ‘variable rate transaction: margin’ should generally be greater than 0.1.</li>
                </ul>
            </div>
            <div class="o-fig__section--sub-sub" data-search-section="" data-scrollspy="4.4">
                <h4 class="o-fig__heading">
                    <a id="4.4.11" href="#4.4.11"> Validation ID: census_tract_number.invalid_geoid </a>
                </h4>
                <h5 data-block-key="wuz9u">Affected data field</h5>
                <ul>
                    <li data-block-key="botk1">census_tract_number</li>
                </ul>
                <h5 data-block-key="bb35j">Description</h5>
                <ul>
                    <li data-block-key="2ek0k">When present, ‘census tract: tract number’ should be a valid census tract GEOID as defined by the U.S. Census Bureau.</li>
                </ul>
            </div>
            <div class="o-fig__section--sub-sub" data-search-section="" data-scrollspy="4.4">
                <h4 class="o-fig__heading">
                    <a id="4.4.12" href="#4.4.12"> Validation ID: naics_code.invalid_naics_value </a>
                </h4>
                <h5 data-block-key="wuz9u">Affected data field</h5>
                <ul>
                    <li data-block-key="botk1">naics_code</li>
                </ul>
                <h5 data-block-key="bb35j">Description</h5>
                <ul>
                    <li data-block-key="2ek0k">When present, ‘North American Industry Classification System (NAICS) code’ should be a valid NAICS code.</li>
                </ul>
            </div>
            <div class="o-fig__section--sub-sub" data-search-section="" data-scrollspy="4.4">
                <h4 class="o-fig__heading">
                    <a id="4.4.13" href="#4.4.13"> Validation ID: business_ownership_status.duplicates_in_field </a>
                </h4>
                <h5 data-block-key="nsktb">Affected data field</h5>
                <ul>
                    <li data-block-key="an0ql">business_ownership_status</li>
                </ul>
                <h5 data-block-key="aabmi">Description</h5>
                <ul>
                    <li data-block-key="39c2m">‘Business ownership status’ should <b>not</b> contain duplicated values.</li>
                </ul>
            </div>
            <div class="o-fig__section--sub-sub" data-search-section="" data-scrollspy="4.4">
                <h4 class="o-fig__heading">
                    <a id="4.4.14" href="#4.4.14"> Validation ID: business_ownership_status.multi_value_field_restriction </a>
                </h4>
                <h5 data-block-key="wuz9u">Affected data field</h5>
                <ul>
                    <li data-block-key="botk1">business_ownership_status</li>
                </ul>
                <h5 data-block-key="bb35j">Description</h5>
                <ul>
                    <li data-block-key="2ek0k">
                        When ‘business ownership status’ contains 966 (the applicant responded that they did not wish to provide this information) or 988 (not provided by applicant), ‘business ownership status’ should <b>not</b> contain
                        more than one value.
                    </li>
                </ul>
            </div>
            <div class="o-fig__section--sub-sub" data-search-section="" data-scrollspy="4.4">
                <h4 class="o-fig__heading">
                    <a id="4.4.15" href="#4.4.15"> Validation ID: po_X_ethnicity.duplicates_in_field </a>
                </h4>
                <h5 data-block-key="47oha">Affected data field</h5>
                <ul>
                    <li data-block-key="e571o">po_X_ethnicity</li>
                </ul>
                <h5 data-block-key="9lplg">Description</h5>
                <ul>
                    <li data-block-key="6v8ve">‘Ethnicity of principal owner X’ should <b>not</b> contain duplicated values.</li>
                </ul>
            </div>
            <div class="o-fig__section--sub-sub" data-search-section="" data-scrollspy="4.4">
                <h4 class="o-fig__heading">
                    <a id="4.4.16" href="#4.4.16"> Validation ID: po_X_ethnicity.multi_value_field_restriction </a>
                </h4>
                <h5 data-block-key="47oha">Affected data field</h5>
                <ul>
                    <li data-block-key="7ukg6">po_X_ethnicity</li>
                </ul>
                <h5 data-block-key="4q5sp">Description</h5>
                <ul>
                    <li data-block-key="br4jp">
                        When ‘ethnicity of principal owner X’ contains 966 (the applicant responded that they did not wish to provide this information) or 988 (not provided by applicant), ‘ethnicity of principal owner X’ should
                        <b>not</b> contain more than one value.
                    </li>
                </ul>
            </div>
            <div class="o-fig__section--sub-sub" data-search-section="" data-scrollspy="4.4">
                <h4 class="o-fig__heading">
                    <a id="4.4.17" href="#4.4.17"> Validation ID: po_X_race.duplicates_in_field </a>
                </h4>
                <h5 data-block-key="47oha">Affected data field</h5>
                <ul>
                    <li data-block-key="34csm">po_X_race</li>
                </ul>
                <h5 data-block-key="8jkkn">Description</h5>
                <ul>
                    <li data-block-key="2rec5">‘Race of principal owner X’ should <b>not</b> contain duplicated values.</li>
                </ul>
            </div>
            <div class="o-fig__section--sub-sub" data-search-section="" data-scrollspy="4.4">
                <h4 class="o-fig__heading">
                    <a id="4.4.18" href="#4.4.18"> Validation ID: po_X_race.multi_value_field_restriction </a>
                </h4>
                <h5 data-block-key="47oha">Affected data field</h5>
                <ul>
                    <li data-block-key="fbp21">po_X_race</li>
                </ul>
                <h5 data-block-key="729ir">Description</h5>
                <ul>
                    <li data-block-key="dgigg">
                        When ‘race of principal owner X’ contains 966 (the applicant responded that they did not wish to provide this information) or 988 (not provided by applicant), ‘race of principal owner X’ should <b>not</b> contain
                        more than one value.
                    </li>
                </ul>
            </div>
            <div class="o-fig__section--sub" data-search-section="" data-scrollspy="4.5">
                <h3 class="o-fig__heading">
                    <a id="4.5" href="#4.5"> 4.5. Multi-field warnings </a>
                </h3>
            </div>
            <div class="o-fig__section--sub-sub" data-search-section="" data-scrollspy="4.5">
                <h4 class="o-fig__heading">
                    <a id="4.5.1" href="#4.5.1"> Validation ID: ct_guarantee_ff.multi_invalid_number_of_values </a>
                </h4>
                <h5 data-block-key="4ygwa">Affected data fields</h5>
                <ul>
                    <li data-block-key="5i8hg">ct_guarantee</li>
                    <li data-block-key="2o5m7">ct_guarantee_ff</li>
                </ul>
                <h5 data-block-key="7052s">Description</h5>
                <ul>
                    <li data-block-key="5guh2">
                        ‘Type of guarantee’ and ‘free-form text field for other guarantee‘ combined should <b>not</b> contain more than five values. Code 977 (other), within 'type of guarantee', does <b>not</b> count toward the maximum
                        number of values for the purpose of this validation check.
                    </li>
                </ul>
                <pre>
            WHERE ct_guarantee_length = number of entries in ct_guarantee excluding 977 AND
                ct_guarantee_ff_length = number of entries in ct_guarantee_ff
                IF ct_guarantee_length + ct_guarantee_ff_length is greater than 5 THEN
                    Warning
                ENDIF
            ENDWHERE

                </pre>
            </div>
            <div class="o-fig__section--sub-sub" data-search-section="" data-scrollspy="4.5">
                <h4 class="o-fig__heading">
                    <a id="4.5.2" href="#4.5.2"> Validation ID: credit_purpose_ff.multi_invalid_number_of_values </a>
                </h4>
                <h5 data-block-key="4ygwa">Affected data fields</h5>
                <ul>
                    <li data-block-key="5i8hg">credit_purpose</li>
                    <li data-block-key="2o5m7">credit_purpose_ff</li>
                </ul>
                <h5 data-block-key="7052s">Description</h5>
                <ul>
                    <li data-block-key="5guh2">
                        ‘Credit purpose’ and ‘free-form text field for other credit purpose‘ combined should <b>not</b> contain more than three values. Code 977 (other), within 'credit purpose', does <b>not</b> count toward the maximum
                        number of values for the purpose of this validation check.
                    </li>
                </ul>
                <pre>
            WHERE credit_purpose_length = number of entries in credit_purpose excluding 977 AND
                credit_purpose_ff_length = number of entries in credit_purpose_ff
                IF credit_purpose_length + credit_purpose_ff_length is greater than 3 THEN
                    Warning
                ENDIF
            ENDWHERE

                </pre>
            </div>
            <div class="o-fig__section--sub-sub" data-search-section="" data-scrollspy="4.5">
                <h4 class="o-fig__heading">
                    <a id="4.5.3" href="#4.5.3"> Validation ID: action_taken_date.unreasonable_date_value </a>
                </h4>
                <h5 data-block-key="rauke">Affected data fields</h5>
                <ul>
                    <li data-block-key="dtos4">action_taken_date</li>
                    <li data-block-key="80aul">app_date</li>
                </ul>
                <h5 data-block-key="4n4ov">Description</h5>
                <ul>
                    <li data-block-key="rpcp">The date indicated by ‘application date’ should generally be less than two years (730 days) before ‘action taken date’.</li>
                </ul>
                <pre>
            IF action_taken_date is greater than (app_date plus 730 days) THEN
                Warning
            ENDIF

                </pre>
            </div>
            <div class="o-fig__section--sub-sub" data-search-section="" data-scrollspy="4.5">
                <h4 class="o-fig__heading">
                    <a id="4.5.4" href="#4.5.4"> Validation ID: denial_reasons_ff.multi_invalid_number_of_values </a>
                </h4>
                <h5 data-block-key="4ygwa">Affected data fields</h5>
                <ul>
                    <li data-block-key="5i8hg">denial_reasons</li>
                    <li data-block-key="2o5m7">denial_reasons_ff</li>
                </ul>
                <h5 data-block-key="7052s">Description</h5>
                <ul>
                    <li data-block-key="5guh2">
                        ‘Denial reason(s)’ and ‘free-form text field for other denial reason(s)‘ combined should <b>not</b> contain more than four values. Code 977 (other), within 'Denial reason(s)', does <b>not</b> count toward the maximum
                        number of values for the purpose of this validation check.
                    </li>
                </ul>
                <pre>
            WHERE denial_reasons_length = number of entries in denial_reasons excluding 977 AND
                denial_reasons_ff_length = number of entries in denial_reasons_ff
                IF denial_reasons_length + denial_reasons_ff_length is greater than 4 THEN
                    Warning
                ENDIF
            ENDWHERE

                </pre>
            </div>
            <div class="o-fig__section--sub-sub" data-search-section="" data-scrollspy="4.5">
                <h4 class="o-fig__heading">
                    <a id="4.5.5" href="#4.5.5"> Validation ID: po_demographics_0.conditional_fieldset_conflict </a>
                </h4>
                <h5 data-block-key="rauke">Affected data fields</h5>
                <ul>
                    <li data-block-key="dtos4">num_principal_owners</li>
                    <li data-block-key="frs6c">po_1_ethnicity</li>
                    <li data-block-key="3hosi">po_1_race</li>
                    <li data-block-key="dm0or">po_1_gender_flag</li>
                    <li data-block-key="fgfdb">po_2_ethnicity</li>
                    <li data-block-key="dc8l1">po_2_race</li>
                    <li data-block-key="fk5i">po_2_gender_flag</li>
                    <li data-block-key="4oh05">po_3_ethnicity</li>
                    <li data-block-key="aarqv">po_3_race</li>
                    <li data-block-key="frjj0">po_3_gender_flag</li>
                    <li data-block-key="47qjq">po_4_ethnicity</li>
                    <li data-block-key="coola">po_4_race</li>
                    <li data-block-key="30jmd">po_4_gender_flag</li>
                </ul>
                <h5 data-block-key="4n4ov">Description</h5>
                <ul>
                    <li data-block-key="rpcp">When ‘number of principal owners’ equals 0 or is blank, demographic fields for principal owners 1, 2, 3, and 4 should be blank.</li>
                </ul>
                <pre>
                IF num_principal_owners is equal to 0 OR is blank THEN
                    IF (po_1_ethnicity, po_1_race, po_1_gender_flag,
                        po_2_ethnicity, po_2_race, po_2_gender_flag,
                        po_3_ethnicity, po_3_race, po_3_gender_flag,
                        po_4_ethnicity, po_4_race, OR po_4_gender_flag) is not blank THEN
                            Warning
                    ENDIF
                ENDIF

                </pre>
            </div>
            <div class="o-fig__section--sub-sub" data-search-section="" data-scrollspy="4.5">
                <h4 class="o-fig__heading">
                    <a id="4.5.6" href="#4.5.6"> Validation ID: po_demographics_1.conditional_fieldset_conflict </a>
                </h4>
                <h5 data-block-key="rauke">Affected data fields</h5>
                <ul>
                    <li data-block-key="dtos4">num_principal_owners</li>
                    <li data-block-key="bqn56">po_1_ethnicity</li>
                    <li data-block-key="1hrt7">po_1_race</li>
                    <li data-block-key="b2ec9">po_1_gender_flag</li>
                    <li data-block-key="6t3h">po_2_ethnicity</li>
                    <li data-block-key="ftp6c">po_2_race</li>
                    <li data-block-key="ddghe">po_2_gender_flag</li>
                    <li data-block-key="2s753">po_3_ethnicity</li>
                    <li data-block-key="3qqsr">po_3_race</li>
                    <li data-block-key="3o9t3">po_3_gender_flag</li>
                    <li data-block-key="1bg76">po_4_ethnicity</li>
                    <li data-block-key="6mpee">po_4_race</li>
                    <li data-block-key="6rpcm">po_4_gender_flag</li>
                </ul>
                <h5 data-block-key="4n4ov">Description</h5>
                <ul>
                    <li data-block-key="rpcp">When ‘number of principal owners’ equals 1, ‘ethnicity of principal owner 1’, ‘race of principal owner 1’, and ‘sex/gender of principal owner 1: NP flag’ should <b>not</b> be blank.</li>
                    <li data-block-key="21i90">Demographic fields for principal owners 2, 3, and 4 should be blank.</li>
                </ul>
                <pre>
                IF num_principal_owners is equal to 1 THEN
                    IF (po_1_ethnicity, po_1_race, OR po_1_gender_flag) is blank THEN
                            Warning
                    ENDIF
                    IF (po_2_ethnicity, po_2_race, po_2_gender_flag,
                        po_3_ethnicity, po_3_race, po_3_gender_flag,
                        po_4_ethnicity, po_4_race, OR po_4_gender_flag) is not blank THEN
                            Warning
                    ENDIF
                ENDIF

                </pre>
            </div>
            <div class="o-fig__section--sub-sub" data-search-section="" data-scrollspy="4.5">
                <h4 class="o-fig__heading">
                    <a id="4.5.7" href="#4.5.7"> Validation ID: po_demographics_2.conditional_fieldset_conflict </a>
                </h4>
                <h5 data-block-key="rauke">Affected data fields</h5>
                <ul>
                    <li data-block-key="dtos4">num_principal_owners</li>
                    <li data-block-key="eefns">po_1_ethnicity</li>
                    <li data-block-key="cjpht">po_1_race</li>
                    <li data-block-key="a0kcn">po_1_gender_flag</li>
                    <li data-block-key="2hpc2">po_2_ethnicity</li>
                    <li data-block-key="ct0f">po_2_race</li>
                    <li data-block-key="5d15c">po_2_gender_flag</li>
                    <li data-block-key="2obmm">po_3_ethnicity</li>
                    <li data-block-key="edof3">po_3_race</li>
                    <li data-block-key="dljni">po_3_gender_flag</li>
                    <li data-block-key="dtsgp">po_4_ethnicity</li>
                    <li data-block-key="d3rtd">po_4_race</li>
                    <li data-block-key="ebin1">po_4_gender_flag</li>
                </ul>
                <h5 data-block-key="4n4ov">Description</h5>
                <ul>
                    <li data-block-key="rpcp">
                        When ‘number of principal owners’ equals 2, ‘ethnicity of principal owner 1 and 2’, ‘race of principal owner 1 and 2’, and ‘sex/gender of principal owner 1 and 2: NP flag’ should <b>not</b> be blank.
                    </li>
                    <li data-block-key="bairl">Demographic fields for principal owners 3 and 4 should be blank.</li>
                </ul>
                <pre>
                IF num_principal_owners is equal to 2 THEN
                    IF (po_1_ethnicity, po_1_race, po_1_gender_flag,
                        po_2_ethnicity, po_2_race, OR po_2_gender_flag) is blank THEN
                            Warning
                    ENDIF
                    IF (po_3_ethnicity, po_3_race, po_3_gender_flag,
                        po_4_ethnicity, po_4_race, OR po_4_gender_flag) is not blank THEN
                            Warning
                    ENDIF
                ENDIF

                </pre>
            </div>
            <div class="o-fig__section--sub-sub" data-search-section="" data-scrollspy="4.5">
                <h4 class="o-fig__heading">
                    <a id="4.5.8" href="#4.5.8"> Validation ID: po_demographics_3.conditional_fieldset_conflict </a>
                </h4>
                <h5 data-block-key="47oha">Affected data fields</h5>
                <ul>
                    <li data-block-key="8hfqa">num_principal_owners</li>
                    <li data-block-key="c26dj">po_1_ethnicity</li>
                    <li data-block-key="fb80c">po_1_race</li>
                    <li data-block-key="73lr8">po_1_gender_flag</li>
                    <li data-block-key="dvu70">po_2_ethnicity</li>
                    <li data-block-key="3ifcf">po_2_race</li>
                    <li data-block-key="dnb06">po_2_gender_flag</li>
                    <li data-block-key="944to">po_3_ethnicity</li>
                    <li data-block-key="ccqtf">po_3_race</li>
                    <li data-block-key="e6o61">po_3_gender_flag</li>
                    <li data-block-key="3mu0u">po_4_ethnicity</li>
                    <li data-block-key="aur7q">po_4_race</li>
                    <li data-block-key="98ad6">po_4_gender_flag</li>
                </ul>
                <h5 data-block-key="dkke6">Description</h5>
                <ul>
                    <li data-block-key="6oak8">
                        When ‘number of principal owners’ equals 3, ‘ethnicity of principal owner 1, 2, and 3’, ‘race of principal owner 1, 2, and 3’, and ‘sex/gender of principal owner 1, 2, and 3: NP flag’ should <b>not</b> be blank.
                    </li>
                    <li data-block-key="9cnt5">Demographic fields for principal owner 4 should be blank.</li>
                </ul>
                <pre>
                IF num_principal_owners is equal to 3 THEN
                    IF (po_1_ethnicity, po_1_race, po_1_gender_flag,
                        po_2_ethnicity, po_2_race, po_2_gender_flag
                        po_3_ethnicity, po_3_race, OR po_3_gender_flag) is blank THEN
                            Warning
                    ENDIF
                    IF (po_4_ethnicity, po_4_race, OR po_4_gender_flag) is not blank THEN
                            Warning
                    ENDIF
                ENDIF

                </pre>
            </div>
            <div class="o-fig__section--sub-sub" data-search-section="" data-scrollspy="4.5">
                <h4 class="o-fig__heading">
                    <a id="4.5.9" href="#4.5.9"> Validation ID: po_demographics_4.conditional_fieldset_conflict </a>
                </h4>
                <h5 data-block-key="47oha">Affected data fields</h5>
                <ul>
                    <li data-block-key="foapi">num_principal_owners</li>
                    <li data-block-key="bscp5">po_1_ethnicity</li>
                    <li data-block-key="c9oep">po_1_race</li>
                    <li data-block-key="5aa1c">po_1_gender_flag</li>
                    <li data-block-key="160ab">po_2_ethnicity</li>
                    <li data-block-key="b5d4">po_2_race</li>
                    <li data-block-key="dlk">po_2_gender_flag</li>
                    <li data-block-key="1itta">po_3_ethnicity</li>
                    <li data-block-key="fffn3">po_3_race</li>
                    <li data-block-key="bv824">po_3_gender_flag</li>
                    <li data-block-key="eaven">po_4_ethnicity</li>
                    <li data-block-key="8erq1">po_4_race</li>
                    <li data-block-key="3116m">po_4_gender_flag</li>
                </ul>
                <h5 data-block-key="48kp6">Description</h5>
                <ul>
                    <li data-block-key="bum5">
                        When ‘number of principal owners’ equals 4, ‘ethnicity of principal owner 1, 2, 3, and 4’, ‘race of principal owner 1, 2, 3, and 4’, and ‘sex/gender of principal owner 1, 2, 3, and 4: NP flag’ should <b>not</b> be
                        blank.
                    </li>
                </ul>
                <pre>
                    IF num_principal_owners is equal to 4 THEN
                        IF (po_1_ethnicity, po_1_race, po_1_gender_flag,
                            po_2_ethnicity, po_2_race, po_2_gender_flag,
                            po_3_ethnicity, po_3_race, po_3_gender_flag,
                            po_4_ethnicity, po_4_race, OR po_4_gender_flag) is blank THEN
                            Warning
                        ENDIF
                    ENDIF
                </pre>
            </div>
            <div class="o-fig__section" data-search-section="" data-scrollspy="5">
                <h2 class="o-fig__heading">
                    <a id="5" href="#5"> 5. Where to get help </a>
                </h2>
                <p data-block-key="nwusr">
                    Resources to help industry understand and comply with the small business lending rule are available on the CFPB’s website.
                    <a href="/compliance/compliance-resources/small-business-lending-resources/small-business-lending-collection-and-reporting-requirements/">Learn about complying with the small business lending rule.</a>
                </p>
                <p data-block-key="79unu">
                    You may also <a href="/compliance/compliance-resources/signup/#small-business-lending">sign up for an email distribution list</a> that the CFPB will use to announce future updates and additional resources as they become
                    available. If you have a specific regulatory interpretation question about the small business lending rule after reviewing these resources, you can
                    <a href="https://reginquiries.consumerfinance.gov">submit the question to the CFPB</a> on its website.
                </p>
            </div>
            <div class="o-fig__section" data-search-section="" data-scrollspy="6">
                <h2 class="o-fig__heading">
                    <a id="6" href="#6"> 6. Paperwork Reduction Act </a>
                </h2>
                <p data-block-key="nwusr">
                    According to the Paperwork Reduction Act of 1995, an agency may not conduct or sponsor, and, notwithstanding any other provision of law, a person is not required to respond to a collection of information unless it
                    displays a valid OMB control number. The OMB control number for this collection is 3170-0013. It expires on November 30, 2025. The obligation to respond to this collection of information is mandatory under section 704B
                    of the Equal Credit Opportunity Act, 15 U.S.C. 1691c-2, as implemented by Consumer Financial Protection Bureau’s Regulation B, 12 CFR part 1002. Comments regarding this collection of information, including the estimated
                    response time, suggestions for improving the usefulness of the information, or suggestions for reducing the burden to respond to this collection should be submitted to the Bureau of Consumer Financial Protection
                    (Attention: PRA Office), 1700 G Street NW, Washington, DC 20552, or by email to <a href="mailto:PRA@cfpb.gov">PRA@cfpb.gov</a>.
                </p>
                <p data-block-key="7vtit"></p>
                <p data-block-key="52r18">
                    <br />
                </p>
            </div>
        </div>
    </div>
</main>
`;
