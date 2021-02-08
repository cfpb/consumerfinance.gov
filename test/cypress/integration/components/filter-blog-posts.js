/* The tests assume some blog posts already exist, and will need some test post data if they're run locally.
This includes at least one post that contains the word "loan" in the title, one post without the word "loan" in the title,
posts published both before and after the date 01/01/2017. The posts should be in several different categories,
and tagged with several different topic tags, including at least one with the tag "mortgages" and at least one without the "mortgages" tag.
The posts should also have several different authors, including at least one with the author "CFPB Web Team". */
import { Filter } from '../../components/filter';
import { FilterableListControl } from '../../components/filterable-list-control';

const page = new FilterableListControl();
const filter = new Filter();

describe( 'Filter Blog Posts based on content', () => {
  beforeEach( () => {
    cy.visit( '/about-us/blog/' );
    // And I open the filterable list control
    page.openFilterableListControl();
    // The I click "Show filters" button
    page.showFilters();
  } );
  it( 'Item name search', () => {
    // When I enter "loan" in the item name input field
    page.filterItemName( 'loan' );
    // And I click "Apply filters" button
    page.applyFilters();
    // Then I should see only results with the word "loan" in the post title
    page.results().should( 'contain', 'loan' );
    // And the page url should contain "title=loan"
    cy.url().should( 'include', 'title=loan' );
  } );
  it( 'Select a single category', () => {
    // When I select the first checkbox in the Category list
    filter.checkCategoryName( 'At the CFPB' );
    // And I click "Apply filters" button
    page.applyFilters();
    // Then I should see only results in that category
    page.notification().should( 'be.visible' );
    // And the page url should contain "categories=at-the-cfpb"
    cy.url().should( 'include', 'categories=at-the-cfpb' );
  } );
  it( 'Select multiple categories', () => {
    // When I select all five checkboxes in the Category list
    filter.checkCategoryName( 'At the CFPB' );
    filter.checkCategoryId( 'directors-notebook' );
    filter.checkCategoryId( 'policy_compliance' );
    filter.checkCategoryId( 'data-research-reports' );
    filter.checkCategoryName( 'Info for consumers' );
    // And I click "Apply filters" button
    page.applyFilters();
    // Then I should see only results that are in at least one of the selected categories
    page.notification().should( 'be.visible' );
    // And the page url should contain "categories=at-the-cfpb"
    cy.url().should( 'include', 'categories=at-the-cfpb' );
    // And the page url should contain "categories=directors-notebook"
    cy.url().should( 'include', 'categories=directors-notebook' );
    // And the page url should contain "categories=policy_compliance"
    cy.url().should( 'include', 'categories=policy_compliance' );
    // And the page url should contain "categories=data-research-reports"
    cy.url().should( 'include', 'categories=data-research-reports' );
    // And the page url should contain "categories=info-for-consumers"
    cy.url().should( 'include', 'categories=info-for-consumers' );
  } );
  it( 'Date range to present', () => {
    // When I enter "01/01/2021" in the From date entry field
    page.filterFromDate( '2021-01-01' );
    // And I click "Apply filters" button
    page.applyFilters();
    // Then I should see only results dated 01/01/2021 or later
    page.notification().should( 'be.visible' );
    page.lastResult().should( 'contain', '2021' );
    page.results().should( 'not.contain', '2020' );
    // And the page url should contain "from_date=2021-01-01"
    cy.url().should( 'include', 'from_date=2021-01-01' );
  } );
  it( 'Date range in past', () => {
    // When I enter "01/01/2020" in the From date entry field
    page.filterFromDate( '2020-01-01' );
    // And I enter "12/31/2020" in the To date entry field
    page.filterToDate( '2020-12-31' );
    // And I click "Apply filters" button
    page.applyFilters();
    // Then I should see only results between 01/01/2020 and 01/01/2021, inclusive
    page.notification().should( 'be.visible' );
    page.results().should( 'not.contain', '2019' );
    page.firstResult().should( 'contain', '2020' );
    page.firstResult().should( 'not.contain', '2021' );
    // And the page url should contain "from_date=2020-01-01"
    cy.url().should( 'include', 'from_date=2020-01-01' );
    // And the page url should contain "to_date=2020-12-31"
    cy.url().should( 'include', 'to_date=2020-12-31' );
  } );
  it( 'Select a single topic', () => {
    // When I click the first checkbox in the Topic list
    filter.clickTopic( 'Financial Education' );
    // And I click "Apply filters" button
    page.applyFilters();
    // Then I should see only results tagged with the selected topic
    page.notification().should( 'be.visible' );
    page.results().should( 'contain', 'education' );
    // And the page url should contain "topics=financial-education"
    cy.url().should( 'include', 'topics=financial-education' );
  } );
  it( 'Select multiple topics', () => {
    // When I select five checkboxes in the Topic list
    filter.clickTopic( 'Student loans' );
    filter.clickTopic( 'Financial Education' );
    filter.clickTopic( 'Mortgages' );
    filter.clickTopic( 'Consumer complaints' );
    filter.clickTopic( 'Financial well-being' );
    // And I click "Apply filters" button
    page.applyFilters();
    // Then I should see only results tagged with at least one of the two selected topics
    page.notification().should( 'be.visible' );
    page.results().should( 'contain', 'financial' );
    // And the page url should contain "topics=student-loans"
    cy.url().should( 'include', 'topics=student-loans' );
    // And the page url should contain "topics=financial-education"
    cy.url().should( 'include', 'topics=financial-education' );
    // And the page url should contain "topics=mortgages"
    cy.url().should( 'include', 'topics=mortgages' );
    // And the page url should contain "topics=consumer-complaints"
    cy.url().should( 'include', 'topics=consumer-complaints' );
    // And the page url should contain "topics=financial-well-being"
    cy.url().should( 'include', 'topics=financial-well-being' );
  } );
  it( 'Type-ahead topics', () => {
    // When I type "mortgage" in the topic input box
    filter.clickTopic( 'Mortgages' );
    // Then the list of topics should show only tags that contain the word "mortgage"
    page.results().should( 'contain', 'mortgage' );
    // And when I select a topic in the list
    filter.clickTopic( 'Servicemembers' );
    // And I click "Apply filters" button
    page.applyFilters();
    // Then I should see only results tagged with the selected topic
    page.notification().should( 'be.visible' );
    page.results().should( 'contain', 'service' );
    // And the page url should contain "topics=mortgages"
    cy.url().should( 'include', 'topics=mortgages' );
    // And the page url should contain "topics=servicemembers"
    cy.url().should( 'include', 'topics=servicemembers' );
  } );
  it( 'Select category and topic', () => {
    // When I select a checkbox in the Category list
    filter.checkCategoryId( 'policy_compliance' );
    // When I select a checkbox in the Topic list
    filter.clickTopic( 'Students' );
    // And I click "Apply filters" button
    page.applyFilters();
    // Then I should see only results that are both in the selected category and tagged with the selected topic
    page.notification().should( 'be.visible' );
    page.results().should( 'contain', 'student' );
    page.results().should( 'contain', 'policy' );
    // And the page url should contain "categories=policy_compliance"
    cy.url().should( 'include', 'categories=policy_compliance' );
    // And the page url should contain "topics=students"
    cy.url().should( 'include', 'topics=students' );
  } );
  it( 'Clear and hide filters', () => {
    // When I select the last checkbox in the Category list
    filter.checkCategoryName( 'Info for consumers' );
    // When I select a checkbox in the Topic list
    filter.clickTopic( 'Consumer complaints' );
    // And I click "Apply filters" button
    page.applyFilters();
    // Then the page url should contain "categories=info-for-consumers"
    cy.url().should( 'include', 'categories=info-for-consumers' );
    // And the page url should contain "topics=consumer-complaints"
    cy.url().should( 'include', 'topics=consumer-complaints' );
    // Then I should see only results that are both in the selected category and tagged with the selected topic
    page.results().should( 'contain', 'consumer' );
    // And when I click "Show filters"
    page.showFilters();
    // And when I click "Clear filters"
    page.clearFilters();
    // And I click "Hide filters" button
    page.hideFilters();
    // Then the page url should not contain "categories=info-for-consumers"
    cy.url().should( 'not.include', 'categories=info-for-consumers' );
    // And the page url should not contain "topics=consumer-complaints"
    cy.url().should( 'not.include', 'topics=consumer-complaints' );
    // Then I should see the full list of results
    page.notification().should( 'be.visible' );
  } );
  it( 'Select a single author', () => {
    // When I select a checkbox in the Author list
    filter.clickAuthor( 'CFPB Web Team' );
    // And I click "Apply filters" button
    page.applyFilters();
    // Then I should see only results posted by the selected author
    page.notification().should( 'be.visible' );
    page.results().should( 'contain', 'CFPB Web Team' );
    // And the page url should contain "authors=cfpb-web-team"
    cy.url().should( 'include', 'authors=cfpb-web-team' );
    // And the page url should not contain "authors=cfpb-research-team"
    cy.url().should( 'not.include', 'authors=cfpb-research-team' );
  } );
  it( 'Select multiple authors', () => {
    // When I select five checkboxes in the Author list
    filter.clickAuthor( 'CFPB Web Team' );
    filter.clickAuthor( 'CFPB Research Team' );
    filter.clickAuthor( 'Owning a Home Team' );
    filter.clickAuthor( 'Office of Enforcement' );
    filter.clickAuthor( 'Adam Scott' );
    // And I click "Apply filters" button
    page.applyFilters();
    // Then I should see only results posted by at least one of the two selected authors
    page.notification().should( 'be.visible' );
    page.results().should( 'contain', 'CFPB' );
    // And the page url should contain "authors=cfpb-web-team"
    cy.url().should( 'include', 'authors=cfpb-web-team' );
    // And the page url should contain "authors=cfpb-research-team"
    cy.url().should( 'include', 'authors=cfpb-research-team' );
    // And the page url should contain "authors=owning-a-home-team"
    cy.url().should( 'include', 'authors=owning-a-home-team' );
    // And the page url should contain "authors=office-of-enforcement"
    cy.url().should( 'include', 'authors=office-of-enforcement' );
    // And the page url should contain "authors=adam-scott"
    cy.url().should( 'include', 'authors=adam-scott' );
  } );
  it( 'Type-ahead authors', () => {
    // When I type "CFPB" in the Author input box
    filter.clickAuthor( 'CFPB' );
    // Then the list of authors should show only items that contain "CFPB"
    page.results().should( 'contain', 'CFPB' );
    // And when I select the first checkbox in the Author list
    filter.clickAuthor( 'CFPB Research Team' );
    // And I click "Apply filters" button
    page.applyFilters();
    // Then I should see only results posted by the selected author
    page.notification().should( 'be.visible' );
    page.results().should( 'contain', 'CFPB Research Team' );
    page.results().should( 'not.contain', 'CFPB Web Team' );
    // And the page url should contain "authors=cfpb-research-team"
    cy.url().should( 'include', 'authors=cfpb-research-team' );
    // And the page url should not contain "authors=cfpb-web-team"
    cy.url().should( 'not.include', 'authors=cfpb-web-team' );
  } );
  it( 'Item name search plus category', () => {
    // When I type "loans" in the item name input box
    page.filterItemName( 'loans' );
    // And I select the last checkbox in the Category list
    filter.checkCategoryName( 'Info for consumers' );
    // And I click "Apply filters" button
    page.applyFilters();
    // Then I should see only results in the selected category with "loans" in the post title
    page.notification().should( 'be.visible' );
    page.results().should( 'contain', 'consumers' );
    page.results().should( 'contain', 'loans' );
    // And the page url should contain "title=loans"
    cy.url().should( 'include', 'title=loans' );
    // And the page url should contain "categories=info-for-consumers"
    cy.url().should( 'include', 'categories=info-for-consumers' );
  } );
  it( 'Item name search plus topic', () => {
    // When I type "loans" in the item name input box
    page.filterItemName( 'loans' );
    // And I select a checkbox in the Topic list
    filter.clickTopic( 'Student loans' );
    // And I click "Apply filters" button
    page.applyFilters();
    // Then I should see only results tagged with the selected topic with "loans" in the post title
    page.notification().should( 'be.visible' );
    page.results().should( 'contain', 'loans' );
    // And the page url should contain "title=loans"
    cy.url().should( 'include', 'title=loans' );
    // And the page url should contain "topics=student-loans"
    cy.url().should( 'include', 'topics=student-loans' );
  } );
  it( 'Item name search plus date range', () => {
    // When I type "loans" in the item name input box
    page.filterItemName( 'loans' );
    // And I type "01/01/2020" in the From date entry field
    page.filterFromDate( '2020-01-01' );
    // And I click "Apply filters" button
    page.applyFilters();
    // Then I should see only results dated "01/01/2020" or later with "loans" in the post title
    page.notification().should( 'be.visible' );
    page.lastResult().should( 'contain', '2020' );
    page.results().should( 'not.contain', '2019' );
    page.results().should( 'contain', 'loans' );
    // And the page url should contain "title=loans"
    cy.url().should( 'include', 'title=loans' );
    // And the page url should contain "from_date=2020-01-01"
    cy.url().should( 'include', 'from_date=2020-01-01' );
  } );
  it( 'Item name search plus author', () => {
    // When I type "loans" in the item name input box
    page.filterItemName( 'loans' );
    // And I select a checkbox in the Author list
    filter.clickAuthor( 'CFPB Web Team' );
    // And I click "Apply filters" button
    page.applyFilters();
    // Then I should see only results posted by the select author with "loans" in the post title
    page.notification().should( 'be.visible' );
    page.results().should( 'contain', 'CFPB Web Team' );
    page.results().should( 'contain', 'loans' );
    // And the page url should contain "title=loans"
    cy.url().should( 'include', 'title=loans' );
    // And the page url should contain "authors=cfpb-web-team"
    cy.url().should( 'include', 'authors=cfpb-web-team' );
  } );
} );
