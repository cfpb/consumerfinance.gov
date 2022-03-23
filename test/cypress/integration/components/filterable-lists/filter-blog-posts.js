/* The tests assume some blog posts already exist, and will need some test post data if they're run locally.
The posts should be in five different categories, and tagged with at least five different topic tags.
The posts should also have at least three different languages with some blog titles specific to those languages. */
import { Filter } from './filter-helpers';
import { FilterableListControl } from './filterable-list-control-helpers';
import { Pagination } from '../pagination/pagination-helpers';


const blog = new FilterableListControl();
const filter = new Filter();
const page = new Pagination();

describe( 'Filter Blog Posts based on content', () => {
  beforeEach( () => {
    cy.visit( '/about-us/blog/' );
  } );
  it( 'Item name search', () => {
    // get the title of any blog post
    blog.resultTitle().then( title => {
      // When I enter the title in the item name input field
      blog.filterItemName( title.get( 0 ).innerText );
      // And I click "Apply filters" button
      blog.applyFilters();
      // Then I should see only results with the title in the post title
      blog.resultsContent().should(
        'contain', title.get( 0 ).innerText
      );
      // And the page url should contain "title=" followed by the title
      cy.url().should(
        'include', 'title=' + encodeURIComponent(title.get( 0 ).innerText.split( ' ' ).join( '+' ))
      );
    } );
  } );
  it( 'Select a single category', () => {
    // retrieve the category
    filter.getCategory().then( category => {
      // When I select the first option in the Category multiselect
      filter.clickCategory( category.get( 0 ).getAttribute( 'value' ) );
      // And I click "Apply filters" button
      blog.applyFilters();
      // Then I should see only results in that category
      blog.notification().should( 'be.visible' );
      // And the page url should contain "categories=" category
      cy.url().should(
        'include',
        'categories=' + category.get( 0 ).getAttribute( 'value' )
      );
    } );
  } );
  it( 'Select multiple categories', () => {
    // retrieve the categories
    filter.getCategory().then( categories => {
      // When I select all options checkboxes in the Category multiselect
      filter.clickCategory( categories.get( 0 ).getAttribute( 'value' ) );
      filter.clickCategory( categories.get( 1 ).getAttribute( 'value' ) );
      filter.clickCategory( categories.get( 2 ).getAttribute( 'value' ) );
      filter.clickCategory( categories.get( 3 ).getAttribute( 'value' ) );
      filter.clickCategory( categories.get( 4 ).getAttribute( 'value' ) );
      // And I click "Apply filters" button
      blog.applyFilters();
      // Then I should see only results that are in at least one of the selected categories
      blog.notification().should( 'be.visible' );
      // And the page url should contain "categories=at-the-cfpb"
      cy.url().should(
        'include',
        'categories=' + categories.get( 0 ).getAttribute( 'value' )
      );
      // And the page url should contain "categories=directors-notebook"
      cy.url().should(
        'include',
        'categories=' + categories.get( 1 ).getAttribute( 'value' )
      );
      // And the page url should contain "categories=policy_compliance"
      cy.url().should(
        'include',
        'categories=' + categories.get( 2 ).getAttribute( 'value' )
      );
      // And the page url should contain "categories=data-research-reports"
      cy.url().should(
        'include',
        'categories=' + categories.get( 3 ).getAttribute( 'value' )
      );
      // And the page url should contain "categories=info-for-consumers"
      cy.url().should(
        'include',
        'categories=' + categories.get( 4 ).getAttribute( 'value' )
      );
    } );
  } );
  it( 'Date range to present', () => {
    // get the date from a result
    blog.resultDate().then( date => {
      // When I enter the date in the From date entry field
      blog.filterFromDate(
        date.get( 0 ).getAttribute( 'datetime' ).split( 'T' )[0]
      );
      // And I click "Apply filters" button
      blog.applyFilters();
      // Then the page url should contain "from_date=" date
      cy.url().should(
        'include',
        'from_date=' + date.get( 0 ).getAttribute( 'datetime' ).split( 'T' )[
          0
        ] );
      // Then I should see only results dated that year or later
      blog.lastResultHeader().should(
        'contain', date.get( 0 ).getAttribute( 'datetime' ).split( '-' )[0]
      );
    } );
  } );
  it( 'Date range in past', () => {
    // get the date from a result
    blog.resultDate().then( date => {
      // When I enter the date in the From date entry field
      blog.filterFromDate(
        date.get( 0 ).getAttribute( 'datetime' ).split( 'T' )[0]
      );
      // And I enter the date in the To date entry field
      blog.filterToDate(
        date.get( 0 ).getAttribute( 'datetime' ).split( 'T' )[0]
      );
      // And I click "Apply filters" button
      blog.applyFilters();
      // Then I should see only results from the year belonging to that date
      blog.notification().should( 'be.visible' );
      blog.resultsHeaderRight().should(
        'contain', date.get( 0 ).getAttribute( 'datetime' ).split( '-' )[0]
      );
      // And the page url should contain "from_date=" date
      cy.url().should(
        'include',
        'from_date=' + date.get( 0 ).getAttribute( 'datetime' ).split( 'T' )[
          0
        ]
      );
      // And the page url should contain "to_date=" date
      cy.url().should(
        'include',
        'to_date=' + date.get( 0 ).getAttribute( 'datetime' ).split( 'T' )[
          0
        ]
      );
    } );
  } );
  it( 'Select a single topic', () => {
    // get a topic
    filter.getTopic().then( topic => {
      // When I click the first checkbox in the Topic list
      filter.clickTopic( topic.get( 0 ).getAttribute( 'value' ) );
      // And I click "Apply filters" button
      blog.applyFilters();
      // Then I should see only results tagged with the selected topic
      blog.notification().should( 'be.visible' );
      filter.getTopicLabel(
        topic.get( 0 ).getAttribute( 'value' )
      ).then( label => {
        blog.resultsContent().should( 'contain', label.get( 0 ).innerText );
      } );
      // And the page url should contain "topics=" topic
      cy.url().should(
        'include',
        'topics=' + topic.get( 0 ).getAttribute( 'value' )
      );
    } );
  } );
  it( 'Select multiple topics', () => {
    // get topics
    filter.getTopic().then( topics => {
      // When I select five checkboxes in the Topic list
      filter.clickTopic( topics.get( 0 ).getAttribute( 'value' ) );
      filter.clickTopic( topics.get( 1 ).getAttribute( 'value' ) );
      filter.clickTopic( topics.get( 2 ).getAttribute( 'value' ) );
      filter.clickTopic( topics.get( 3 ).getAttribute( 'value' ) );
      filter.clickTopic( topics.get( 4 ).getAttribute( 'value' ) );
      // And I click "Apply filters" button
      blog.applyFilters();
      // Then I should see results tagged with at least one of the topics
      blog.notification().should( 'be.visible' );
      filter.getTopicLabel(
        topics.get( 0 ).getAttribute( 'value' )
      ).then( label => {
        blog.resultsContent().should( 'contain', label.get( 0 ).innerText );
      } );
      // And the page url should contain "topics=" first topic
      cy.url().should(
        'include',
        'topics=' + topics.get( 0 ).getAttribute( 'value' )
      );
      // And the page url should contain "topics=" second topic
      cy.url().should(
        'include',
        'topics=' + topics.get( 1 ).getAttribute( 'value' )
      );
      // And the page url should contain "topics=" third topic
      cy.url().should(
        'include',
        'topics=' + topics.get( 2 ).getAttribute( 'value' )
      );
      // And the page url should contain "topics=" fourth topic
      cy.url().should(
        'include',
        'topics=' + topics.get( 3 ).getAttribute( 'value' )
      );
      // And the page url should contain "topics=" fifth topic
      cy.url().should(
        'include',
        'topics=' + topics.get( 4 ).getAttribute( 'value' )
      );
    } );
  } );
  it( 'Type-ahead topics', () => {
    // get topics
    filter.getTopic().then( topics => {
      // When I type a topic in the topic input box
      filter.typeAheadTopic(
        topics.get( 0 ).getAttribute( 'value' ).split( '-' ).join( ' ' )
      );
      // And when I select a topic in the list
      filter.clickTopic( topics.get( 0 ).getAttribute( 'value' ) );
      // And when I type a different topic in the topic input box
      filter.typeAheadTopic(
        topics.get( 1 ).getAttribute( 'value' ).split( '-' ).join( ' ' )
      );
      // And when I select a topic in the list
      filter.clickTopic( topics.get( 1 ).getAttribute( 'value' ) );
      // And I click "Apply filters" button
      blog.applyFilters();
      // Then I should see only results tagged with the selected topic
      blog.notification().should( 'be.visible' );
      filter.getTopicLabel(
        topics.get( 0 ).getAttribute( 'value' )
      ).then( label => {
        blog.resultsContent().should( 'contain', label.get( 0 ).innerText );
      } );
      filter.getTopicLabel(
        topics.get( 1 ).getAttribute( 'value' )
      ).then( label => {
        blog.resultsContent().should( 'contain', label.get( 0 ).innerText );
      } );
      // And the page url should contain "topics=reverse-mortgages"
      cy.url().should(
        'include',
        'topics=' + topics.get( 0 ).getAttribute( 'value' )
      );
      // And the page url should contain "topics=servicemembers"
      cy.url().should(
        'include',
        'topics=' + topics.get( 1 ).getAttribute( 'value' )
      );
    } );
  } );
  it( 'Select category and topic', () => {
    // check results for blog post with category and topic
    blog.getResultCategoryHasTags().then( category => {
      blog.getResultTagHasCategories().then( topic => {
        // When I select a checkbox in the Category list
        filter.clickCategory(
          category.get( 0 ).innerText.split( '\n' ).pop().trim()
        );
        // When I select a checkbox in the Topic list
        filter.clickTopic(
          topic.get( 0 ).innerText.split( '\n' ).pop().trim()
        );
        // And I click "Apply filters" button
        filter.apply();
        // Then I should see only results that are both in the selected category and tagged with the selected topic
        blog.notification().should( 'be.visible' );
        blog.resultsHeaderContent().should(
          'contain', category.get( 0 ).innerText.split( '\n' ).pop().trim()
        );
        filter.getTopicLabel(
          topic.get( 0 ).innerText.split(
            '\n'
          ).pop().trim().split( ' ' ).join(
            '-'
          ).toLowerCase() ).then( label => {
          blog.resultsContent().should( 'contain', label.get( 0 ).innerText );
        } );
        // And the page url should contain "categories=policy_compliance"
        cy.url().should(
          'include',
          'categories=' + encodeURIComponent(category.get( 0 ).innerText.split(
            '\n'
          ).pop().trim().split( ' ' ).join( '-' ).toLowerCase())
        );
        // And the page url should contain "topics=students"
        cy.url().should(
          'include',
          'topics=' + topic.get( 0 ).innerText.split(
            '\n'
          ).pop().trim().split( ' ' ).join( '-' ).toLowerCase().replace(/[.,\/#!$%\^&\*;:{}=\-_`'~()]/g,"")
        );
      } );
    } );
  } );
  it( 'Clear filters', () => {
    // check results for blog post with category and topic
    blog.getResultCategoryHasTags().then( category => {
      blog.getResultTagHasCategories().then( topic => {
        // When I select a checkbox in the Category list
        filter.clickCategory(
          category.get( 0 ).innerText.split( '\n' ).pop().trim()
        );
        // When I select a checkbox in the Topic list
        filter.clickTopic(
          topic.get( 0 ).innerText.split( '\n' ).pop().trim()
        );
        // And I click "Apply filters" button
        filter.apply();
        // Then I should see only results that are both in the selected category and tagged with the selected topic
        blog.notification().should( 'be.visible' );
        blog.resultsHeaderContent().should(
          'contain', category.get( 0 ).innerText.split( '\n' ).pop().trim()
        );
        filter.getTopicLabel(
          topic.get( 0 ).innerText.split(
            '\n'
          ).pop().trim().split( ' ' ).join(
            '-'
          ).toLowerCase() ).then( label => {
          blog.resultsContent().should( 'contain', label.get( 0 ).innerText );
        } );
        // And the page url should contain "categories=policy_compliance"
        cy.url().should(
          'include',
          'categories=' + encodeURIComponent(category.get( 0 ).innerText.split(
            '\n'
          ).pop().trim().split( ' ' ).join( '-' ).toLowerCase())
        );
        // And the page url should contain "topics=students"
        cy.url().should(
          'include',
          'topics=' + topic.get( 0 ).innerText.split(
            '\n'
          ).pop().trim().split( ' ' ).join( '-' ).toLowerCase().replace(/[.,\/#!$%\^&\*;:{}=\-_`'~()]/g,"")
        );
        // And when I click "Show filters"
        filter.show();
        // And when I click "Clear filters"
        filter.clear();
        // Then the page url should not contain "categories=info-for-consumers"
        cy.url().should(
          'not.include',
          'categories=' + encodeURIComponent(category.get( 0 ).innerText.split(
            '\n'
          ).pop().trim().split( ' ' ).join( '-' ).toLowerCase())
        );
        // And the page url should not contain "topics=consumer-complaints"
        cy.url().should(
          'not.include',
          'topics=' + topic.get( 0 ).innerText.split(
            '\n'
          ).pop().trim().split( ' ' ).join( '-' ).toLowerCase().replace(/[.,\/#!$%\^&\*;:{}=\-_`'~()]/g,"")
        );
        // Then there is no visible notification
        blog.notification().should( 'not.be.visible' );
      } );
    } );
  } );
  it( 'Hide filters', () => {
    // When I click "Hide filters"
    filter.hide();
    // Then there is no visible notification
    blog.notification().should( 'not.be.visible' );
  } );
  it( 'Select a single language', () => {
    // When I select a checkbox in the Language list
    filter.clickLanguage( 'es' );
    // And I click "Apply filters" button
    blog.applyFilters();
    // Then I should see only results posted by the selected language
    blog.notification().should( 'be.visible' );
    blog.resultsContent().should( 'contain', 'Estafas con beneficios' );
    // And the page url should contain "language=es"
    cy.url().should( 'include', 'language=es' );
    // And the page url should not contain "language=en"
    cy.url().should( 'not.include', 'language=en' );
  } );
  it( 'Select multiple languages', () => {
    // When I select two checkboxes in the Language list
    filter.clickLanguage( 'es' );
    filter.clickLanguage( 'tl' );
    // And I click "Apply filters" button
    blog.applyFilters();
    // Then I should see only results posted by at least one of the two selected languages
    blog.notification().should( 'be.visible' );
    blog.resultsContent().should( 'contain', 'Estafas con beneficios' );
    blog.resultsContent().should( 'contain', 'Paano tutulungan' );
    // And the page url should contain "language=es"
    cy.url().should( 'include', 'language=es' );
    // And the page url should contain "language=ar"
    cy.url().should( 'include', 'language=tl' );
  } );
  it( 'Type-ahead languages', () => {
    // When I type "Spanish" in the Language input box
    filter.typeAheadLanguage( 'Spanish' );
    // And when I select the first checkbox in the Language list
    filter.clickLanguage( 'es' );
    // And I click "Apply filters" button
    blog.applyFilters();
    // Then I should see only results posted by the selected language
    blog.notification().should( 'be.visible' );
    blog.resultsContent().should( 'contain', 'Estafas con beneficios' );
    // And the page url should contain "language=es"
    cy.url().should( 'include', 'language=es' );
    // And the page url should not contain "language=en"
    cy.url().should( 'not.include', 'language=en' );
  } );
  it( 'Item name search plus category', () => {
    // get the title of any blog post
    blog.getResultCategory().then( category => {
      // get category for that blog post
      blog.getResultTitleHasCategory().then( title => {
        // When I type title in the item name input box
        blog.filterItemName( title.get( 0 ).innerText );
        // And I select a checkbox in the category list
        filter.clickCategory(
          category.get( 0 ).innerText.split( '\n' ).pop().trim()
        );
        // And I click "Apply filters" button
        blog.applyFilters();
        // Then I should see only results tagged with the selected category with title in the post title
        blog.notification().should( 'be.visible' );
        blog.resultsContent().should( 'contain', title.get( 0 ).innerText );
        blog.resultsHeaderContent().should(
          'contain', category.get( 0 ).innerText.split( '\n' ).pop().trim()
        );
        // And the page url should contain "title=" title
        cy.url().should( 'include', 'title=' + encodeURIComponent(title.get( 0 ).innerText.split( ' ' ).join( '+' )));
        // And the page url should contain "categories=" category
        cy.url().should(
          'include',
          'categories=' + encodeURIComponent(category.get( 0 ).innerText.split(
            '\n'
          ).pop().trim().split( ' ' ).join( '-' ).toLowerCase())
        );
      } );
    } );
  } );
  it( 'Item name search plus topic', () => {
    // get the title of any blog post
    blog.getResultTag().then( topic => {
      // get topic for that blog post
      blog.getResultTitleHasTag().then( title => {
        // When I type title in the item name input box
        blog.filterItemName( title.get( 0 ).innerText );
        // And I select a checkbox in the Topic list
        filter.clickTopic(
          topic.get( 0 ).innerText.split( '\n' ).pop().trim()
        );
        // And I click "Apply filters" button
        blog.applyFilters();
        // Then I should see only results tagged with the selected topic with title in the post title
        blog.notification().should( 'be.visible' );
        blog.resultsContent().should( 'contain', title.get( 0 ).innerText );
        filter.getTopicLabel(
          topic.get( 0 ).innerText.split(
            '\n'
          ).pop().trim().split( ' ' ).join(
            '-'
          ).toLowerCase() ).then( label => {
          blog.resultsContent().should( 'contain', label.get( 0 ).innerText );
        } );
        // And the page url should contain "title=" title
        cy.url().should( 'include', 'title=' + encodeURIComponent(title.get( 0 ).innerText.split( ' ' ).join( '+' )) );
        // And the page url should contain "topics=" topic
        cy.url().should(
          'include',
          'topics=' + topic.get( 0 ).innerText.split(
            '\n'
          ).pop().trim().split( ' ' ).join( '-' ).toLowerCase()
        );
      } );
    } );
  } );
  it( 'Item name search plus date range', () => {
    // get the date from a result
    blog.resultDate().then( date => {
      // get the title of any blog post
      blog.resultTitle().then( title => {
        // When I type "loans" in the item name input box
        blog.filterItemName( title.get( 0 ).innerText );
        // And I type "01/01/2020" in the From date entry field
        blog.filterFromDate(
          date.get( 0 ).getAttribute( 'datetime' ).split( 'T' )[0]
        );
        // And I type "01/01/2021" in the To date entry field to bound the date range
        blog.filterToDate(
          date.get( 0 ).getAttribute( 'datetime' ).split( 'T' )[0]
        );
        // And I click "Apply filters" button
        blog.applyFilters();
        // Then I should see only results dated "01/01/2020" or later with "loans" in the post title
        blog.notification().should( 'be.visible' );
        blog.lastResultHeader().should(
          'contain',
          date.get( 0 ).getAttribute( 'datetime' ).split( '-' )[0]
        );
        blog.resultsContent().should( 'contain', title.get( 0 ).innerText );
        // And the page url should contain "title=loans"
        cy.url().should( 'include', 'title=' + encodeURIComponent(title.get( 0 ).innerText.split( ' ' ).join( '+' )) );
        // And the page url should contain "from_date=2020-01-01"
        cy.url().should(
          'include',
          'from_date=' + date.get( 0 ).getAttribute(
            'datetime'
          ).split( 'T' )[0]
        );
      } );
    } );
  } );
  it( 'Item name search plus language', () => {
    // When I type "loans" in the item name input box
    blog.filterItemName( 'loans' );
    // And I select a checkbox in the Languages list
    filter.clickLanguage( 'es' );
    // And I click "Apply filters" button
    blog.applyFilters();
    // Then I should see only results posted by the select language with "loans" in the post title
    blog.notification().should( 'be.visible' );
    blog.resultsContent().should( 'contain', 'Qué necesita saber sobre' );
    blog.resultsContent().should( 'contain', 'loans' );
    // And the page url should contain "title=loans"
    cy.url().should( 'include', 'title=loans' );
    // And the page url should contain "language=es"
    cy.url().should( 'include', 'language=es' );
  } );
} );
