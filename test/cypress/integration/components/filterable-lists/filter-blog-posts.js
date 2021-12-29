/* The tests assume some blog posts already exist, and will need some test post data if they're run locally.
This includes at least one post that contains the word "loan" in the title, one post without the word "loan" in the title,
posts published both before and after the date 12/31/2020. The posts should be in several different categories,
and tagged with several different topic tags, including at least one with the tag "mortgages" and at least one without the "mortgages" tag.
The posts should also have several different languages, including at least one in Spanish and one in Tagalog. */
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
    // When I enter "loan" in the item name input field
    blog.filterItemName( 'loan' );
    // And I click "Apply filters" button
    blog.applyFilters();
    // Then I should see only results with the word "loan" in the post title
    blog.resultsContent().should( 'contain', 'loan' );
    // And the page url should contain "title=loan"
    cy.url().should( 'include', 'title=loan' );
  } );
  it( 'Select a single category', () => {
    // When I select the first option in the Category multiselect
    filter.clickCategory( 'At the CFPB' );
    // And I click "Apply filters" button
    blog.applyFilters();
    // Then I should see only results in that category
    blog.notification().should( 'be.visible' );
    // And the page url should contain "categories=at-the-cfpb"
    cy.url().should( 'include', 'categories=at-the-cfpb' );
  } );
  it( 'Select multiple categories', () => {
    // When I select all options checkboxes in the Category multiselect
    filter.clickCategory( 'at-the-cfpb' );
    filter.clickCategory( 'directors-notebook' );
    filter.clickCategory( 'policy_compliance' );
    filter.clickCategory( 'data-research-reports' );
    filter.clickCategory( 'info-for-consumers' );
    // And I click "Apply filters" button
    blog.applyFilters();
    // Then I should see only results that are in at least one of the selected categories
    blog.notification().should( 'be.visible' );
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
    // When I enter "01/01/2020" in the From date entry field
    blog.filterFromDate( '2020-01-01' );
    // And I click "Apply filters" button
    blog.applyFilters();
    // Then the page url should contain "from_date=2020-01-01"
    cy.url().should( 'include', 'from_date=2020-01-01' );
    // When I paginate to the last page of results
    page.lastResults();
    // Then I should see only results dated 01/01/2020 or later
    blog.lastResultHeader().should( 'contain', '2020' );
  } );
  it( 'Date range in past', () => {
    // When I enter "01/01/2020" in the From date entry field
    blog.filterFromDate( '2020-01-01' );
    // And I enter "12/31/2020" in the To date entry field
    blog.filterToDate( '2020-12-31' );
    // And I click "Apply filters" button
    blog.applyFilters();
    // Then I should see only results between 01/01/2020 and 12/31/2020, inclusive
    blog.notification().should( 'be.visible' );
    blog.resultsHeaderRight().should( 'not.contain', '2019' );
    blog.resultsHeaderRight().should( 'not.contain', '2021' );
    blog.resultsHeaderRight().should( 'contain', '2020' );
    // And the page url should contain "from_date=2020-01-01"
    cy.url().should( 'include', 'from_date=2020-01-01' );
    // And the page url should contain "to_date=2020-12-31"
    cy.url().should( 'include', 'to_date=2020-12-31' );
  } );
  it( 'Select a single topic', () => {
    // When I click the first checkbox in the Topic list
    filter.clickTopic( 'Financial Education' );
    // And I click "Apply filters" button
    blog.applyFilters();
    // Then I should see only results tagged with the selected topic
    blog.notification().should( 'be.visible' );
    blog.resultsContent().should( 'contain', 'education' );
    // And the page url should contain "topics=financial-education"
    cy.url().should( 'include', 'topics=financial-education' );
  } );
  it( 'Select multiple topics', () => {
    // When I select five checkboxes in the Topic list
    filter.clickTopic( 'Student loans' );
    filter.clickTopic( 'Financial education' );
    filter.clickTopic( 'Mortgages' );
    filter.clickTopic( 'Consumer complaints' );
    filter.clickTopic( 'Financial well-being' );
    // And I click "Apply filters" button
    blog.applyFilters();
    // Then I should see only results tagged with at least one of the two selected topics
    blog.notification().should( 'be.visible' );
    blog.resultsContent().should( 'contain', 'financial' );
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
    filter.typeAheadTopic( 'Mortgages' );
    // And when I select a topic in the list
    filter.clickTopic( 'Reverse mortgages' );
    // And when I type "Dervicemembers" in the topic input box
    filter.typeAheadTopic( 'Servicemembers' );
    // And when I select a topic in the list
    filter.clickTopic( 'Servicemembers' );
    // And I click "Apply filters" button
    blog.applyFilters();
    // Then I should see only results tagged with the selected topic
    blog.notification().should( 'be.visible' );
    blog.resultsContent().should( 'contain', 'Reverse mortgages' );
    blog.resultsContent().should( 'contain', 'Servicemembers' );
    // And the page url should contain "topics=reverse-mortgages"
    cy.url().should( 'include', 'topics=reverse-mortgages' );
    // And the page url should contain "topics=servicemembers"
    cy.url().should( 'include', 'topics=servicemembers' );
  } );
  it( 'Select category and topic', () => {
    // When I select a checkbox in the Category list
    filter.clickCategory( 'policy_compliance' );
    // When I select a checkbox in the Topic list
    filter.clickTopic( 'Students' );
    // And I click "Apply filters" button
    blog.applyFilters();
    // Then I should see only results that are both in the selected category and tagged with the selected topic
    blog.notification().should( 'be.visible' );
    blog.resultsContent().should( 'contain', 'student' );
    blog.resultsContent().should( 'contain', 'policy' );
    // And the page url should contain "categories=policy_compliance"
    cy.url().should( 'include', 'categories=policy_compliance' );
    // And the page url should contain "topics=students"
    cy.url().should( 'include', 'topics=students' );
  } );
  it( 'Clear filters', () => {
    // When I select the last option in the Category multiselect
    filter.clickCategory( 'Info for consumers' );
    // When I select a checkbox in the Topic list
    filter.clickTopic( 'Consumer complaints' );
    // And I click "Apply filters" button
    filter.apply();
    // Then the page url should contain "categories=info-for-consumers"
    cy.url().should( 'include', 'categories=info-for-consumers' );
    // And the page url should contain "topics=consumer-complaints"
    cy.url().should( 'include', 'topics=consumer-complaints' );
    // Then I should see only results that are both in the selected category and tagged with the selected topic
    blog.resultsContent().should( 'contain', 'consumer' );
    // And when I click "Show filters"
    filter.show();
    // And when I click "Clear filters"
    filter.clear();
    // Then the page url should not contain "categories=info-for-consumers"
    cy.url().should( 'not.include', 'categories=info-for-consumers' );
    // And the page url should not contain "topics=consumer-complaints"
    cy.url().should( 'not.include', 'topics=consumer-complaints' );
    // Then there is no visible notification
    blog.notification().should( 'not.be.visible' );
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
    blog.resultsContent().should( 'not.contain', 'Summary of the 2021' );
    // And the page url should contain "language=es"
    cy.url().should( 'include', 'language=es' );
    // And the page url should not contain "language=en"
    cy.url().should( 'not.include', 'language=en' );
  } );
  it( 'Item name search plus category', () => {
    // When I type "loans" in the item name input box
    blog.filterItemName( 'loans' );
    // And I select the last option in the Category multiselect
    filter.clickCategory( 'Info for consumers' );
    // And I click "Apply filters" button
    blog.applyFilters();
    // Then I should see only results in the selected category with "loans" in the post title
    blog.notification().should( 'be.visible' );
    blog.resultsContent().should( 'contain', 'consumers' );
    blog.resultsContent().should( 'contain', 'loans' );
    // And the page url should contain "title=loans"
    cy.url().should( 'include', 'title=loans' );
    // And the page url should contain "categories=info-for-consumers"
    cy.url().should( 'include', 'categories=info-for-consumers' );
  } );
  it( 'Item name search plus topic', () => {
    // When I type "loans" in the item name input box
    blog.filterItemName( 'loans' );
    // And I select a checkbox in the Topic list
    filter.clickTopic( 'Student loans' );
    // And I click "Apply filters" button
    blog.applyFilters();
    // Then I should see only results tagged with the selected topic with "loans" in the post title
    blog.notification().should( 'be.visible' );
    blog.resultsContent().should( 'contain', 'loans' );
    // And the page url should contain "title=loans"
    cy.url().should( 'include', 'title=loans' );
    // And the page url should contain "topics=student-loans"
    cy.url().should( 'include', 'topics=student-loans' );
  } );
  it( 'Item name search plus date range', () => {
    // When I type "loans" in the item name input box
    blog.filterItemName( 'loans' );
    // And I type "01/01/2020" in the From date entry field
    blog.filterFromDate( '2020-01-01' );
    // And I type "01/01/2021" in the To date entry field to bound the date range
    blog.filterToDate( '2021-01-01' );
    // And I click "Apply filters" button
    blog.applyFilters();
    // Then I should see only results dated "01/01/2020" or later with "loans" in the post title
    blog.notification().should( 'be.visible' );
    blog.lastResultHeader().should( 'contain', '2020' );
    blog.resultsHeaderRight().should( 'not.contain', '2019' );
    blog.resultsContent().should( 'contain', 'loans' );
    // And the page url should contain "title=loans"
    cy.url().should( 'include', 'title=loans' );
    // And the page url should contain "from_date=2020-01-01"
    cy.url().should( 'include', 'from_date=2020-01-01' );
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
