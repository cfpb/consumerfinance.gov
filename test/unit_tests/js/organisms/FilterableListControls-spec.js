import FilterableListControls from '../../../../cfgov/unprocessed/js/organisms/FilterableListControls.js';

const BASE_CLASS = 'o-filterable-list-controls';
const HTML_SNIPPET = `
<div class="o-filterable-list-controls" id="o-filterable-list-controls">

<div class="o-expandable
            o-expandable--background
            o-expandable--border">
    <button class="o-expandable__header" type="button">
        <span class="o-expandable__label">
            Filter posts
        </span>
        <span class="o-expandable__cues">
            <span class="o-expandable__cue-open" role="img" aria-label="Show">
                Show
                filters
            </span>
            <span class="o-expandable__cue-close" role="img" aria-label="Hide">
                Hide
                filters
            </span>
        </span>
    </button>

    <div class="o-expandable__content">

    <form method="get" action=".">

        <div class="content-l">

        <div class="content-l__col
                    content-l__col-1">
            <div class="o-form__group">
                <div class="m-form-field">
                    <label class="a-label a-label--heading" for="title">
                        Item name
                    </label>
                    <input type="text"
                            name="title"
                            maxlength="250"
                            placeholder="Search for a specific word in item title"
                            class="a-text-input a-text-input--full"
                            id="title">
                </div>
            </div>
        </div>

        <div class="content-l__col
                    content-l__col-1-3">
            <div class="o-form__group">
                <fieldset class="o-form__fieldset">
                    <legend class="h4">
                        Category
                    </legend>
                    <ul class="m-list m-list--unstyled">

                        <li class="m-form-field m-form-field--checkbox">
                            <input class="a-checkbox" type="checkbox" value="at-the-cfpb" id="filter_categories_at-the-cfpb" name="categories">
                            <label class="a-label" for="filter_categories_at-the-cfpb">
                                At the CFPB
                            </label>
                        </li>

                        <li class="m-form-field m-form-field--checkbox">
                            <input class="a-checkbox" type="checkbox" value="directors-notebook" id="filter_categories_directors-notebook" name="categories">
                            <label class="a-label" for="filter_categories_directors-notebook">
                                Director's notebook
                            </label>
                        </li>

                        <li class="m-form-field m-form-field--checkbox">
                            <input class="a-checkbox" type="checkbox" value="policy-compliance" id="filter_categories_policy-compliance" name="categories">
                            <label class="a-label" for="filter_categories_policy-compliance">
                                Policy and compliance
                            </label>
                        </li>

                        <li class="m-form-field m-form-field--checkbox">
                            <input class="a-checkbox" type="checkbox" value="data-research-reports" id="filter_categories_data-research-reports" name="categories">
                            <label class="a-label" for="filter_categories_data-research-reports">
                                Data, research, and reports
                            </label>
                        </li>

                        <li class="m-form-field m-form-field--checkbox">
                            <input class="a-checkbox" type="checkbox" value="info-for-consumers" id="filter_categories_info-for-consumers" name="categories">
                            <label class="a-label" for="filter_categories_info-for-consumers">
                                Info for consumers
                            </label>
                        </li>

                    </ul>
                </fieldset>
            </div>
        </div>

        <div class="content-l__col
                    content-l__col-2-3">
            <div class="content-l">

                    <div class="content-l__col
                                content-l__col-1-2">
                        <div class="o-form__group">
                            <div class="m-form-field">
                                <label class="a-label a-label--heading" for="topics">
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

                    <div class="content-l__col
                                content-l__col-1">
                        <div class="o-form__group">
                            <fieldset class="o-form__fieldset">
                                <legend class="h4">
                                    Date range
                                </legend>
                                <div class="content-l">
                                    <div class="content-l__col
                                                content-l__col-1-2">
                                        <div class="m-form-field">
                                            <label class="a-label a-label--heading" for="from_date">
                                                From:
                                            </label>
                                            <input type="text" name="from_date" data-type="date" placeholder="mm/dd/yyyy" class="a-text-input a-text-input--full" id="from_date">
                                        </div>
                                    </div>
                                    <div class="content-l__col
                                                content-l__col-1-2">
                                        <div class="m-form-field">
                                            <label class="a-label a-label--heading" for="to_date">
                                                To:
                                            </label>
                                            <input type="text" name="to_date" data-type="date" placeholder="mm/dd/yyyy" class="a-text-input a-text-input--full" id="to_date">
                                        </div>
                                    </div>
                                </div>
                            </fieldset>
                        </div>
                    </div>

            </div>
        </div>

            <div class="content-l__col
                        content-l__col-1">
                <div class="m-btn-group">
                    <input class="a-btn" type="submit" value="Apply filters">
                    <a class="a-btn a-btn--link a-btn--warning" href="/about-us/blog/">
                        Clear filters
                    </a>
                </div>
            </div>
        </div>
    </form>

    </div>

</div>

<div class="m-notification">
    <div class="m-notification__content">
        <div class="m-notification__message"></div></div>
    </div>

</div>
`;

describe('FilterableListControls', () => {
  let filterableListControlsDom;
  let filterableListControls;

  beforeEach(() => {
    document.body.innerHTML = HTML_SNIPPET;
    filterableListControlsDom = document.querySelector(`.${BASE_CLASS}`);
    filterableListControls = new FilterableListControls(
      filterableListControlsDom,
    );
  });

  describe('init()', () => {
    it('should return the FormSubmit instance when initialized', () => {
      expect(filterableListControlsDom.getAttribute('data-js-hook')).toBeNull();
      filterableListControls.init();
      expect(
        filterableListControlsDom.getAttribute('data-js-hook'),
      ).toStrictEqual('state_atomic_init');
    });
  });
});
