import mock
from django import forms
from django.db.models import Q
from unittest import TestCase
from ....forms import FilterableListForm, EventArchiveFilterForm, \
    NewsroomFilterForm, ActivityLogFilterForm
from ....models import CFGOVPage
from ....models.handlers.filterable_list_handlers import \
    FilterableListHandler, EventArchiveHandler, NewsroomHandler, \
    ActivityLogHandler


class TestFilterableListHandler(TestCase):
    def setUp(self):
        self.page = mock.Mock()
        self.request = mock.Mock()
        self.context = {}
        self.handler = FilterableListHandler(self.page, self.request, self.context)

    @mock.patch('v1.models.handlers.filterable_list_handlers.FilterableListHandler._process_filters')
    @mock.patch('v1.models.handlers.filterable_list_handlers.FilterableListHandler._get_forms')
    def test_process_calls_get_forms(self, mock_get_forms, mock_process_filters):
        self.handler.process(mock.MagicMock())
        assert mock_get_forms.called

    @mock.patch('v1.models.handlers.filterable_list_handlers.FilterableListHandler._process_filters')
    @mock.patch('v1.models.handlers.filterable_list_handlers.FilterableListHandler._get_forms')
    def test_process_calls_process_filters(self, mock_get_forms, mock_process_filters):
        self.handler.process(mock.MagicMock())
        assert mock_process_filters.called

    @mock.patch('v1.models.handlers.filterable_list_handlers.FilterableListHandler._process_filters')
    @mock.patch('v1.models.handlers.filterable_list_handlers.FilterableListHandler._get_forms')
    def test_process_calls_get_forms(self, mock_get_forms, mock_process_filters):
        self.handler.process(mock.MagicMock())
        assert mock_get_forms.called

    @mock.patch('v1.models.handlers.filterable_list_handlers.FilterableListHandler._process_filters')
    @mock.patch('v1.models.handlers.filterable_list_handlers.FilterableListHandler._get_forms')
    def test_process_sets_context(self, mock_get_forms, mock_process_filters):
        self.handler.process(mock.MagicMock())
        for key in ['filters', 'get_secondary_nav_items', 'has_active_filters']:
            assert key in self.context.keys()

    @mock.patch('v1.models.handlers.filterable_list_handlers.FilterableListHandler._get_filter_form_class')
    @mock.patch('v1.models.handlers.filterable_list_handlers.FilterableListHandler._process_form_data')
    def test_get_forms_calls_get_filter_form_class_on_block_class(self, mock_process_form_data, mock_get_filter_form_class):
        block = mock.Mock()
        mock_form_class = mock.Mock()
        mock_get_filter_form_class.return_value = mock_form_class
        block_tuples = [(0, block)]
        self.handler._get_forms(block_tuples)
        assert mock_get_filter_form_class.called

    @mock.patch('v1.models.handlers.filterable_list_handlers.FilterableListHandler._get_filter_form_class')
    @mock.patch('v1.models.handlers.filterable_list_handlers.FilterableListHandler._process_form_data')
    def test_get_forms_calls_process_form_data_with_form_class_and_form_id(self, mock_process_form_data, mock_get_filter_form_class):
        block = mock.Mock()
        mock_form_class = mock.Mock()
        mock_get_filter_form_class.return_value = mock_form_class
        block_tuples = [(0, block)]
        mock_process_form_data.return_value = 'test'
        self.handler._get_forms(block_tuples)
        mock_process_form_data.assert_called_with(mock_form_class, 0)

    @mock.patch('v1.models.handlers.filterable_list_handlers.FilterableListHandler._get_filter_form_class')
    @mock.patch('v1.models.handlers.filterable_list_handlers.FilterableListHandler._process_form_data')
    def test_get_forms_instantiates_form(self, mock_process_form_data, mock_get_filter_form_class):
        block = mock.Mock()
        mock_form_class = mock.Mock()
        mock_get_filter_form_class.return_value = mock_form_class
        block_tuples = [(0, block)]
        mock_process_form_data.return_value = 'test'
        self.handler._get_forms(block_tuples)
        mock_form_class.assert_called_with('test', parent=self.page.parent(), hostname=self.request.site.hostname)

    def test_get_filter_form_class_returns_form_class(self):
        result = self.handler._get_filter_form_class()
        assert issubclass(result, forms.Form)

    def test_process_form_data_adds_declared_field_as_key(self):
        mock_form_class = mock.Mock()
        mock_form_class.declared_fields = ['topics']
        data = self.handler._process_form_data(mock_form_class, 0)
        assert 'topics' in data

    def test_process_form_data_adds_field_value_from_request(self):
        mock_form_class = mock.Mock()
        mock_form_class.declared_fields = ['topics', 'date']
        data = self.handler._process_form_data(mock_form_class, 0)
        self.request.GET.getlist.assert_called_with('filter0_topics', [])
        self.request.GET.get.assert_called_with('filter0_date', '')

    def test_process_filters_returns_filters_context(self):
        result = self.handler._process_filters([], [])
        assert 'forms' in result
        assert 'page_sets' in result

    @mock.patch('v1.models.handlers.filterable_list_handlers.FilterableListHandler._results_per_page')
    @mock.patch('v1.models.handlers.filterable_list_handlers.FilterableListHandler.get_page_set')
    def test_process_filters_calls_is_valid_for_each_form(self, mock_getpageset, mock_resultsperpage):
        forms = [mock.Mock(), mock.Mock()]
        block_tuples = [mock.MagicMock(), mock.MagicMock()]
        self.handler._process_filters(forms, block_tuples)
        for form in forms:
            assert form.is_valid.called

    @mock.patch('v1.models.handlers.filterable_list_handlers.FilterableListHandler._results_per_page')
    @mock.patch('v1.models.handlers.filterable_list_handlers.FilterableListHandler.get_page_set')
    def test_process_filters_calls_results_per_page(self, mock_getpageset, mock_resultsperpage):
        block_tuples = [mock.MagicMock()]
        self.handler._process_filters([mock.Mock()], block_tuples)
        mock_resultsperpage.assert_called_with(block_tuples[0][1])

    @mock.patch('v1.models.handlers.filterable_list_handlers.FilterableListHandler._results_per_page')
    @mock.patch('v1.models.handlers.filterable_list_handlers.FilterableListHandler.get_page_set')
    def test_process_filters_calls_get_page_set(self, mock_getpageset, mock_resultsperpage):
        form = mock.Mock()
        block_tuples = [mock.MagicMock()]
        self.handler._process_filters([form], block_tuples)
        assert mock_getpageset.called

    @mock.patch('v1.models.handlers.filterable_list_handlers.Paginator')
    @mock.patch('v1.models.handlers.filterable_list_handlers.FilterableListHandler._results_per_page')
    @mock.patch('v1.models.handlers.filterable_list_handlers.FilterableListHandler.get_page_set')
    def test_process_filters_instantiates_Paginator_with_page_set_and_limit(self, mock_getpageset, mock_resultsperpage, mock_paginator):
        mock_getpageset.return_value = 'page set'
        mock_resultsperpage.return_value = '1'
        form = mock.Mock()
        block_tuples = [mock.MagicMock()]
        self.handler._process_filters([form], block_tuples)
        mock_paginator.assert_called_with('page set', '1')

    @mock.patch('v1.models.handlers.filterable_list_handlers.Paginator')
    @mock.patch('v1.models.handlers.filterable_list_handlers.FilterableListHandler._results_per_page')
    @mock.patch('v1.models.handlers.filterable_list_handlers.FilterableListHandler.get_page_set')
    def test_process_filters_gets_page_number_from_request(self, mock_getpageset, mock_resultsperpage, mock_paginator):
        form = mock.Mock()
        block_tuples = [mock.MagicMock()]
        paginator = mock.Mock()
        mock_paginator.return_value = paginator
        self.handler._process_filters([form], block_tuples)
        self.request.GET.get.assert_called_with('page')

    @mock.patch('v1.models.handlers.filterable_list_handlers.Paginator')
    @mock.patch('v1.models.handlers.filterable_list_handlers.FilterableListHandler._results_per_page')
    @mock.patch('v1.models.handlers.filterable_list_handlers.FilterableListHandler.get_page_set')
    def test_process_filters_calls_paginators_page_fn(self, mock_getpageset, mock_resultsperpage, mock_paginator):
        form = mock.Mock()
        block_tuples = [mock.MagicMock()]
        paginator = mock.Mock()
        mock_paginator.return_value = paginator
        self.handler._process_filters([form], block_tuples)
        assert paginator.page.called

    @mock.patch('v1.models.handlers.filterable_list_handlers.ContentType')
    @mock.patch('v1.models.handlers.filterable_list_handlers.Paginator')
    @mock.patch('v1.models.handlers.filterable_list_handlers.FilterableListHandler._results_per_page')
    @mock.patch('v1.models.handlers.filterable_list_handlers.FilterableListHandler.get_page_set')
    def test_process_filters_calls_none_for_invalid_form(self, mock_getpageset, mock_resultsperpage, mock_paginator, mock_contenttype):
        form = mock.Mock()
        form.is_valid.return_value = False
        block_tuples = [mock.MagicMock()]
        paginator = mock.Mock()
        mock_paginator.return_value = paginator
        self.handler._process_filters([form], block_tuples)
        assert mock_contenttype.objects.none.called

    @mock.patch('v1.models.handlers.filterable_list_handlers.ContentType')
    @mock.patch('v1.models.handlers.filterable_list_handlers.Paginator')
    @mock.patch('v1.models.handlers.filterable_list_handlers.FilterableListHandler._results_per_page')
    @mock.patch('v1.models.handlers.filterable_list_handlers.FilterableListHandler.get_page_set')
    def test_process_filters_instantiates_Paginator_for_invalid_form(self, mock_getpageset, mock_resultsperpage, mock_paginator, mock_contenttype):
        form = mock.Mock()
        form.is_valid.return_value = False
        block_tuples = [mock.MagicMock()]
        paginator = mock.Mock()
        mock_paginator.return_value = paginator
        self.handler._process_filters([form], block_tuples)
        assert mock_paginator.called

    @mock.patch('v1.models.handlers.filterable_list_handlers.AbstractFilterPage')
    def test_get_page_set_calls_filtering_functions(self, mock_filterpage):
        mock_form = mock.Mock()
        mock_form._generate_query.return_value = Q()
        self.page.depth = 1
        self.handler.request.site.hostname = 'fakehostname'
        self.handler.get_page_set(mock_form)
        mock_filterpage.objects.child_of.assert_called_with(self.page)
        mock_filterpage.objects.child_of().filter.assert_called_with(mock_form._generate_query())
        mock_filterpage.objects.child_of().filter().live_shared.assert_called_with(self.handler.request.site.hostname)
        assert mock_filterpage.objects.child_of().filter().live_shared().distinct.called
        mock_filterpage.objects.child_of().filter().live_shared().distinct().order_by.assert_called_with('-date_published')

    def test_results_per_page(self):
        block = mock.MagicMock()
        result = self.handler._results_per_page(block)
        assert result == block.value['results_limit']

    def test_get_filter_form_class_returns_filterablelistform(self):
        form_class = self.handler._get_filter_form_class()
        self.assertEquals(form_class, FilterableListForm)


class TestEventArchiveHandler(TestCase):
    def setUp(self):
        self.page = mock.Mock()
        self.request = mock.Mock()
        self.context = {}
        self.handler = EventArchiveHandler(self.page, self.request, self.context)

    @mock.patch('v1.models.handlers.filterable_list_handlers.EventPage')
    def test_get_page_set_returns_EventPage_queryset(self, mock_EventPage):
        result = self.handler.get_page_set(mock.Mock())
        assert result is mock_EventPage.objects.child_of().filter().live_shared().distinct().order_by()

    def test_get_filter_form_class_returns_eventarchiveform(self):
        form_class = self.handler._get_filter_form_class()
        self.assertEquals(form_class, EventArchiveFilterForm)


class TestNewsroomHandler(TestCase):
    def setUp(self):
        self.page = mock.Mock()
        self.request = mock.Mock()
        self.context = {}
        self.handler = NewsroomHandler(self.page, self.request, self.context)

    @mock.patch('v1.models.handlers.filterable_list_handlers.AbstractFilterPage')
    @mock.patch('v1.models.handlers.filterable_list_handlers.NewsroomHandler._get_page_queries')
    def test_get_page_set_calls_get_page_queries(self, mock_getpagequeries, mock_filterpage):
        form = mock.Mock()
        categories = mock.MagicMock()
        form.cleaned_data.get.return_value = categories
        self.handler.get_page_set(form)
        mock_getpagequeries.assert_called_with(form, categories)

    @mock.patch('v1.models.handlers.filterable_list_handlers.NewsroomHandler._get_blog_query')
    @mock.patch('v1.models.handlers.filterable_list_handlers.NewsroomHandler._get_newsroom_query')
    @mock.patch('v1.models.handlers.filterable_list_handlers.NewsroomHandler._if_and_only_blog')
    def test_get_page_queries_calls_methods(self, mock_if_and_only_blog, mock_get_newsroom_query, mock_get_blog_query):
        form = mock.Mock()
        categories = mock.MagicMock()
        mock_if_and_only_blog.return_value = (True, False)
        self.handler._get_page_queries(form, categories)
        assert mock_if_and_only_blog.called
        assert mock_get_newsroom_query.called
        assert mock_get_blog_query.called

    @mock.patch('v1.models.handlers.filterable_list_handlers.NewsroomHandler._get_blog_query')
    @mock.patch('v1.models.handlers.filterable_list_handlers.NewsroomHandler._get_newsroom_query')
    @mock.patch('v1.models.handlers.filterable_list_handlers.NewsroomHandler._if_and_only_blog')
    def test_get_page_queries_returns_Q(self, mock_if_and_only_blog, mock_get_newsroom_query, mock_get_blog_query):
        form = mock.Mock()
        categories = mock.MagicMock()
        mock_if_and_only_blog.return_value = (False, False)
        mock_get_newsroom_query.return_value = Q()
        mock_get_blog_query.return_value = Q()
        result = self.handler._get_page_queries(form, categories)
        self.assertIsInstance(result, Q)

    @mock.patch('v1.models.handlers.filterable_list_handlers.AbstractFilterPage')
    def test_get_newsroom_query_returns_Q(self, mock_filterpage):
        form = mock.Mock()
        form._generate_query.return_value = Q()
        mock_filterpage.objects.child_of_q.return_value = Q()
        result = self.handler._get_newsroom_query(form)
        self.assertIsInstance(result, Q)

    @mock.patch('v1.models.handlers.filterable_list_handlers.AbstractFilterPage')
    @mock.patch('v1.models.handlers.filterable_list_handlers.CFGOVPage')
    def test_get_blog_query_returns_Q(self, mock_cfgovpage, mock_filterpage):
        form = mock.MagicMock()
        form._generate_query.return_value = Q()
        form.cleaned_data['categories'] = []
        mock_filterpage.objects.child_of_q.return_value = Q()
        result = self.handler._get_blog_query(form)
        self.assertIsInstance(result, Q)

    @mock.patch('v1.models.handlers.filterable_list_handlers.AbstractFilterPage')
    @mock.patch('v1.models.handlers.filterable_list_handlers.CFGOVPage')
    def test_get_blog_query_returns_Q_if_blog_is_not_found(self, mock_cfgovpage, mock_filterpage):
        form = mock.MagicMock()
        form._generate_query.return_value = Q()
        form.cleaned_data['categories'] = []
        mock_cfgovpage.objects.get.side_effect = CFGOVPage.DoesNotExist()
        with self.assertRaises(CFGOVPage.DoesNotExist) as dne:
            result = self.handler._get_blog_query(form)
            self.assertIsInstance(result, Q)

    def test_get_filter_form_class_returns_newsroomform(self):
        form_class = self.handler._get_filter_form_class()
        self.assertEquals(form_class, NewsroomFilterForm)


class TestActivityLogHandler(TestCase):
    def setUp(self):
        self.page = mock.Mock()
        self.request = mock.Mock()
        self.context = {}
        self.handler = ActivityLogHandler(self.page, self.request, self.context)

    @mock.patch('v1.models.handlers.filterable_list_handlers.ActivityLogHandler._process_queries')
    @mock.patch('v1.models.handlers.filterable_list_handlers.ActivityLogHandler._set_blog_and_report_queries')
    @mock.patch('v1.models.handlers.filterable_list_handlers.ActivityLogHandler._set_newsroom_query')
    @mock.patch('v1.models.handlers.filterable_list_handlers.ActivityLogHandler._process_categories')
    def test_get_page_set_calls_methods(self, mock_process_categories, mock_set_newsroom_query, mock_set_blog_and_report_queries, mock_process_queries):
        form = mock.Mock()
        form.cleaned_data.get.return_value = []
        self.handler.get_page_set(form)
        assert mock_process_categories.called
        assert mock_set_newsroom_query.called
        assert mock_set_blog_and_report_queries.called
        assert mock_process_queries.called

    def test_process_categories_returns_flags_for_blog_and_reports(self):    
        result = self.handler._process_categories([])
        assert 'blog' in result.keys()
        assert 'research-reports' in result.keys()
        assert isinstance(result['blog'], bool)
        assert isinstance(result['research-reports'], bool)

    def test_process_categories_sets_flag_for_categories(self):
        result = self.handler._process_categories(['blog', 'research-reports'])
        self.assertEquals(result, {'blog': True, 'research-reports': True})

    def test_process_categories_deletes_selections_from_original_categories(self):
        categories = ['blog', 'research-reports']
        result = self.handler._process_categories(categories)
        self.assertEquals(categories, [])

    @mock.patch('v1.models.handlers.filterable_list_handlers.AbstractFilterPage')
    @mock.patch('v1.models.handlers.filterable_list_handlers.CFGOVPage')
    def test_set_newsroom_query_sets_queries_dict_with_Q(self, mock_cfgovpage, mock_filterpage):
        mock_filterpage.objects.child_of_q.return_value = Q()
        form = mock.Mock()
        form._generate_query.return_value = Q()
        queries = {}
        self.handler._set_newsroom_query(form, [], [], queries)
        assert 'newsroom' in queries
        self.assertIsInstance(queries['newsroom'], Q)

    @mock.patch('v1.models.handlers.filterable_list_handlers.CFGOVPage')
    def test_set_newsroom_query_doesnotset_queries_dict_after_exception(self, mock_cfgovpage):
        mock_cfgovpage.objects.get.side_effect = CFGOVPage.DoesNotExist()
        with self.assertRaises(CFGOVPage.DoesNotExist) as dne:
            queries = {}
            form = mock.Mock()
            self.handler._set_newsroom_query(form, [], [], queries)
            assert 'newsroom' not in queries

    @mock.patch('v1.models.handlers.filterable_list_handlers.AbstractFilterPage')
    @mock.patch('v1.models.handlers.filterable_list_handlers.CFGOVPage')
    def test_set_blog_and_report_queries_deletes_categories_from_cleaned_data(self, mock_cfgovpage, mock_filterpage):
        form = mock.MagicMock()
        form._generate_query.return_value = Q()
        mock_filterpage.objects.child_of_q.return_value = Q()
        form.cleaned_data['categories'] = ['cat1', 'cat2']
        self.handler._set_blog_and_report_queries(form, {}, {})
        assert 'categories' not in form.cleaned_data

    @mock.patch('v1.models.handlers.filterable_list_handlers.AbstractFilterPage')
    @mock.patch('v1.models.handlers.filterable_list_handlers.CFGOVPage')
    def test_set_blog_and_report_queries_generates_query_for_each_selection(self, mock_cfgovpage, mock_filterpage):
        form = mock.MagicMock()
        form._generate_query.return_value = Q()
        mock_filterpage.objects.child_of_q.return_value = Q()
        self.handler._set_blog_and_report_queries(form, {1: True, 2: True}, {})
        self.assertEquals(mock_cfgovpage.objects.get.call_count, 2)
        self.assertEquals(mock_filterpage.objects.child_of_q.call_count, 2)

    @mock.patch('v1.models.handlers.filterable_list_handlers.AbstractFilterPage')
    @mock.patch('v1.models.handlers.filterable_list_handlers.CFGOVPage')
    def test_set_blog_and_report_queries_sets_queries_for_selections(self, mock_cfgovpage, mock_filterpage):
        form = mock.MagicMock()
        form._generate_query.return_value = Q()
        mock_filterpage.objects.child_of_q.return_value = Q()
        queries = {}
        self.handler._set_blog_and_report_queries(form, {1: True, 2: False}, queries)
        assert 1 in queries
        assert 2 not in queries
        self.assertIsInstance(queries[1], Q)
        self.assertEquals(mock_cfgovpage.objects.get.call_count, 1)
        self.assertEquals(mock_filterpage.objects.child_of_q.call_count, 1)

    @mock.patch('__builtin__.reduce')
    @mock.patch('v1.models.handlers.filterable_list_handlers.AbstractFilterPage')
    def test_process_queries_reduces_queries_and_calls_filter_with_the_query(self, mock_filterpage, mock_reduce):
        queries = {1: Q(), 2: Q()}
        query = Q()
        mock_reduce.return_value = query
        self.handler._process_queries(queries)
        mock_filterpage.objects.filter.assert_called_with(query)

    @mock.patch('v1.models.handlers.filterable_list_handlers.AbstractFilterPage')
    def test_process_queries_reduces_queries_and_calls_filter_with_the_query(self, mock_filterpage):
        queries = {1: Q(), 2: Q()}
        mock_filterpage.objects.filter().live_shared().distinct().order_by.return_value = 'page_set'
        result = self.handler._process_queries(queries)
        assert mock_filterpage.objects.filter.called
        mock_filterpage.objects.filter().live_shared.assert_called_with(self.request.site.hostname)
        assert mock_filterpage.objects.filter().live_shared().distinct.called
        assert mock_filterpage.objects.filter().live_shared().distinct().order_by.called
        self.assertEquals(result, 'page_set')

    def test_get_filter_form_class_returns_activitylogform(self):
        form_class = self.handler._get_filter_form_class()
        self.assertEquals(form_class, ActivityLogFilterForm)
