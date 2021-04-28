import {
  FilterableListControls
} from '../../../../cfgov/unprocessed/js/organisms/FilterableListControls';

const BASE_CLASS = 'o-filterable-list-controls';
const HTML_SNIPPET = `
<div class="o-filterable-list-controls" id="o-filterable-list-controls">

<div class="o-expandable
            o-expandable__padded
            o-expandable__background
            o-expandable__border">

    <button class="o-expandable_header o-expandable_target o-expandable_target__collapsed" type="button">
        <span class="h4 o-expandable_header-left o-expandable_label">
            Filter posts
        </span>
        <span class="o-expandable_header-right o-expandable_link">
            <span class="o-expandable_cue o-expandable_cue-open">
                <span class="u-visually-hidden-on-mobile">
                    Show
                    filters
                </span>
            </span>
            <span class="o-expandable_cue o-expandable_cue-close">
                <span class="u-visually-hidden-on-mobile">
                    Hide
                    filters
                </span>
            </span>
        </span>
    </button>

    <div class="o-expandable_content
                o-expandable_content__transition
                o-expandable_content__collapsed">

    <form method="get" action=".">

        <div class="content-l">

        <div class="content-l_col
                    content-l_col-1">
            <div class="o-form_group">
                <div class="m-form-field">
                    <label class="a-label a-label__heading" for="title">
                        Item name
                    </label>
                    <input type="text"
                           name="title"
                           maxlength="250"
                           placeholder="Search for a specific word in item title"
                           class="a-text-input a-text-input__full"
                           id="title">
                </div>
            </div>
        </div>

        <div class="content-l_col
                    content-l_col-1-3">
            <div class="o-form_group">
                <fieldset class="o-form_fieldset">
                    <legend class="a-legend">
                        Category
                    </legend>
                    <ul class="m-list m-list__unstyled">

                        <li class="m-form-field m-form-field__checkbox">
                            <input class="a-checkbox" type="checkbox" value="at-the-cfpb" id="filter_categories_at-the-cfpb" name="categories">
                            <label class="a-label" for="filter_categories_at-the-cfpb">
                                At the CFPB
                            </label>
                        </li>

                        <li class="m-form-field m-form-field__checkbox">
                            <input class="a-checkbox" type="checkbox" value="directors-notebook" id="filter_categories_directors-notebook" name="categories">
                            <label class="a-label" for="filter_categories_directors-notebook">
                                Director's notebook
                            </label>
                        </li>

                        <li class="m-form-field m-form-field__checkbox">
                            <input class="a-checkbox" type="checkbox" value="policy_compliance" id="filter_categories_policy_compliance" name="categories">
                            <label class="a-label" for="filter_categories_policy_compliance">
                                Policy and compliance
                            </label>
                        </li>

                        <li class="m-form-field m-form-field__checkbox">
                            <input class="a-checkbox" type="checkbox" value="data-research-reports" id="filter_categories_data-research-reports" name="categories">
                            <label class="a-label" for="filter_categories_data-research-reports">
                                Data, research, and reports
                            </label>
                        </li>

                        <li class="m-form-field m-form-field__checkbox">
                            <input class="a-checkbox" type="checkbox" value="info-for-consumers" id="filter_categories_info-for-consumers" name="categories">
                            <label class="a-label" for="filter_categories_info-for-consumers">
                                Info for consumers
                            </label>
                        </li>

                    </ul>
                </fieldset>
            </div>
        </div>

        <div class="content-l_col
                    content-l_col-2-3">
            <div class="content-l">

                    <div class="content-l_col
                                content-l_col-1-2">
                        <div class="o-form_group">
                            <div class="m-form-field">
                                <label class="a-label a-label__heading" for="topics">
                                    Topic
                                </label>
                                <select multiple>
                                  <option>Financial education</option>
                                  <option>Mortgages</option>
                                  <option>Student loans</option>
                                </select>
                            </div>
                        </div>
                    </div>

                    <div class="content-l_col
                                content-l_col-1">
                        <div class="o-form_group">
                            <fieldset class="o-form_fieldset">
                                <legend class="a-legend">
                                    Date range
                                </legend>
                                <div class="content-l">
                                    <div class="content-l_col
                                                content-l_col-1-2">
                                        <div class="m-form-field">
                                            <label class="a-label a-label__heading" for="from_date">
                                                From:
                                            </label>
                                            <input type="text" name="from_date" data-type="date" placeholder="mm/dd/yyyy" class="a-text-input a-text-input__full" id="from_date">
                                        </div>
                                    </div>
                                    <div class="content-l_col
                                                content-l_col-1-2">
                                        <div class="m-form-field">
                                            <label class="a-label a-label__heading" for="to_date">
                                                To:
                                            </label>
                                            <input type="text" name="to_date" data-type="date" placeholder="mm/dd/yyyy" class="a-text-input a-text-input__full" id="to_date">
                                        </div>
                                    </div>
                                </div>
                            </fieldset>
                        </div>
                    </div>

            </div>
        </div>

            <div class="content-l_col
                        content-l_col-1
                        m-btn-group">
                <input class="a-btn" type="submit" value="Apply filters">
                <a class="a-btn a-btn__link a-btn__warning" href="/about-us/blog/">
                    Clear filters
                </a>
            </div>
        </div>
    </form>

    </div>

</div>

<div class="m-notification">
    <div class="m-notification_content">
        <div class="h4 m-notification_message"></div></div>
</div>


</div>
`;

describe( 'FilterableListControls', () => {
  let filterableListControlsDom;
  let filterableListControls;

  beforeEach( () => {
    document.body.innerHTML = HTML_SNIPPET;
    filterableListControlsDom = document.querySelector( `.${ BASE_CLASS }` );
    filterableListControls = new FilterableListControls(
      filterableListControlsDom
    );
  } );

  describe( 'init()', () => {
    it( 'should return the FormSubmit instance when initialized', () => {
      expect( filterableListControlsDom.getAttribute( 'data-js-hook' ) ).toBeNull();
      filterableListControls.init();
      expect( filterableListControlsDom.getAttribute( 'data-js-hook' ) ).toStrictEqual( 'state_atomic_init' );
    } );
  } );

  describe( 'error handling', () => {
    it( 'should highlight text input fields with errors', done => {
      const FIELD_ERROR_CLASS = 'a-text-input__error';
      const form = document.querySelector( 'form' );
      const field = document.querySelector( '#from_date' );

      filterableListControls.init();

      expect( field.classList.contains( FIELD_ERROR_CLASS ) ).toBeFalsy();

      filterableListControls.addEventListener( 'fieldInvalid', () => {
        expect( field.classList.contains( FIELD_ERROR_CLASS ) ).toBeTruthy();
        done();
      } );

      field.value = 'text that is not a valid date';
      form.dispatchEvent( new Event( 'submit' ) );
    } );
  } );
} );
