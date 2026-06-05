import re
from datetime import timedelta

from django.test import RequestFactory, TestCase
from django.utils import timezone

from wagtail.models import Page, Site

from core.testutils.test_cases import WagtailPageTreeTestCase
from v1.atomic_elements.organisms import RelatedPosts
from v1.models.base import CFGOVPage, CFGOVPageCategory
from v1.models.blog_page import BlogPage
from v1.models.learn_page import EventPage
from v1.models.newsroom_page import NewsroomPage


class RelatedPostsTestCase(WagtailPageTreeTestCase):
    @classmethod
    def get_page_tree(cls):
        now = timezone.now()
        yesterday = now - timedelta(days=1)
        two_days_ago = yesterday - timedelta(days=1)

        return [
            (
                Page(title="About us"),
                [
                    Page(title="Blog"),
                    [
                        BlogPage(
                            title="Blog 1", live=True, date_published=now
                        ),
                        BlogPage(
                            title="Blog 2", live=True, date_published=yesterday
                        ),
                    ],
                    Page(title="Newsroom"),
                    [
                        NewsroomPage(
                            title="Newsroom 1", live=True, date_published=now
                        ),
                        NewsroomPage(
                            title="Newsroom 2",
                            live=True,
                            date_published=yesterday,
                        ),
                        NewsroomPage(title="Newsroom 3", live=False),
                    ],
                    Page(title="Events"),
                    [
                        EventPage(
                            title="Event 1",
                            live=True,
                            date_published=now,
                            start_dt=now,
                        ),
                        EventPage(
                            title="Event 2",
                            live=True,
                            date_published=yesterday,
                            start_dt=now,
                        ),
                        Page(title="Archive past events"),
                        [
                            EventPage(
                                title="Event 3",
                                live=True,
                                date_published=two_days_ago,
                                start_dt=now,
                            )
                        ],
                    ],
                ],
                Page(title="Activity log"),
                BlogPage(title="BlogPage that lives in the wrong place"),
            ),
        ]

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()

        # Page tags and categories can't be set at creation time, so they need
        # to be added after the page tree has been created.
        blog1 = BlogPage.objects.get(slug="blog-1")
        blog1.tags.add("foo", "bar")
        blog1.save()

        blog2 = BlogPage.objects.get(slug="blog-2")
        blog2.tags.add("foo", "bar")
        blog2.save()

        newsroom1 = NewsroomPage.objects.get(slug="newsroom-1")
        newsroom1.tags.add("foo")
        newsroom1.categories.add(CFGOVPageCategory(name="speech"))
        newsroom1.save()

    def _related_posts_value(self, **kwargs):
        return dict(RelatedPosts().to_python(kwargs))

    def test_page_not_in_site_has_no_related_posts(self):
        self.assertEqual(
            RelatedPosts.related_posts(
                BlogPage(title="This was never added to a Site"),
                self._related_posts_value(),
            ),
            [],
        )

    def test_ignore_tags(self):
        related_posts = RelatedPosts.related_posts(
            BlogPage.objects.get(slug="blog-1"),
            self._related_posts_value(tag_filtering="ignore"),
        )

        # Blog has one related post besides the one to which we are relating.
        self.assertEqual(related_posts[0]["title"], "Blog")
        self.assertEqual(related_posts[0]["icon"], "speech-bubble")
        self.assertQuerySetEqual(
            related_posts[0]["posts"],
            BlogPage.objects.filter(slug__in=["blog-2"]),
        )

        # Newsroom has 2 related posts, excluding the non-live post.
        self.assertEqual(related_posts[1]["title"], "Newsroom")
        self.assertEqual(related_posts[1]["icon"], "newspaper")
        self.assertQuerySetEqual(
            related_posts[1]["posts"],
            NewsroomPage.objects.filter(slug__in=["newsroom-1", "newsroom-2"]),
        )

        # Events has 3 related posts, including the nested archived one.
        self.assertEqual(related_posts[2]["title"], "Events")
        self.assertEqual(related_posts[2]["icon"], "date")
        self.assertQuerySetEqual(
            related_posts[2]["posts"],
            EventPage.objects.filter(
                slug__in=["event-1", "event-2", "event-3"]
            ),
        )

    def test_limit(self):
        related_posts = RelatedPosts.related_posts(
            BlogPage.objects.get(slug="blog-1"),
            self._related_posts_value(tag_filtering="ignore", limit=1),
        )

        # The limit gets applied per-source.
        self.assertQuerySetEqual(
            related_posts[0]["posts"],
            BlogPage.objects.filter(slug__in=["blog-2"]),
        )
        self.assertQuerySetEqual(
            related_posts[1]["posts"],
            NewsroomPage.objects.filter(slug__in=["newsroom-1"]),
        )
        self.assertQuerySetEqual(
            related_posts[2]["posts"],
            EventPage.objects.filter(slug__in=["event-1"]),
        )

    def test_any_tags(self):
        related_posts = RelatedPosts.related_posts(
            BlogPage.objects.get(slug="blog-1"),
            self._related_posts_value(tag_filtering="any"),
        )

        # Blog has one related post with the same tags.
        self.assertEqual(related_posts[0]["title"], "Blog")
        self.assertQuerySetEqual(
            related_posts[0]["posts"],
            BlogPage.objects.filter(slug__in=["blog-2"]),
        )

        # Newsroom has only 1 related post with any of the same tags.
        self.assertEqual(related_posts[1]["title"], "Newsroom")
        self.assertQuerySetEqual(
            related_posts[1]["posts"],
            NewsroomPage.objects.filter(slug__in=["newsroom-1"]),
        )

        # Events has no related posts with any of the same tags, so it doesn't
        # show up in the related posts structure.
        self.assertEqual(len(related_posts), 2)

    def test_all_tags(self):
        related_posts = RelatedPosts.related_posts(
            BlogPage.objects.get(slug="blog-1"),
            self._related_posts_value(tag_filtering="all"),
        )

        # Blog has one related post with all the same tags.
        self.assertEqual(related_posts[0]["title"], "Blog")
        self.assertQuerySetEqual(
            related_posts[0]["posts"],
            BlogPage.objects.filter(slug__in=["blog-2"]),
        )

        # Neither Newsroom nor Events have any related posts with all of the
        # same tags, so they don't show up in the related posts structure.
        self.assertEqual(len(related_posts), 1)

    def test_categories(self):
        related_posts = RelatedPosts.related_posts(
            BlogPage.objects.get(slug="blog-1"),
            self._related_posts_value(
                tag_filtering="ignore", specific_categories=["Speech"]
            ),
        )

        # Blog doesn't have this category, so it isn't filtered.
        self.assertQuerySetEqual(
            related_posts[0]["posts"],
            BlogPage.objects.filter(slug__in=["blog-2"]),
        )

        # Newsroom has only one related post with the right category.
        self.assertEqual(related_posts[1]["title"], "Newsroom")
        self.assertQuerySetEqual(
            related_posts[1]["posts"],
            NewsroomPage.objects.filter(slug__in=["newsroom-1"]),
        )

        # Event also doesn't have this category, so it isn't filtered.
        self.assertQuerySetEqual(
            related_posts[2]["posts"],
            EventPage.objects.filter(
                slug__in=["event-1", "event-2", "event-3"]
            ),
        )

    def test_related_posts_rendering(self):
        html = RelatedPosts().render(
            self._related_posts_value(),
            context={
                "page": BlogPage.objects.get(slug="blog-1"),
                "request": RequestFactory().get("/"),
            },
        )

        self.assertEqual(len(re.findall("m-list__item", html)), 2)


class TestGenerateViewMoreUrl(TestCase):
    def setUp(self):
        self.request = RequestFactory().get("/")
        self.root = Site.objects.first().root_page

    def _create_activity_log_page(self):
        activity_log = CFGOVPage(title="Activity log", slug="activity-log")
        self.root.add_child(instance=activity_log)

    def test_no_activity_log_page_raises_does_not_exist(self):
        page = CFGOVPage(title="test")
        self.root.add_child(instance=page)

        with self.assertRaises(Page.DoesNotExist):
            RelatedPosts.view_more_url(page, self.request)

    def test_no_tags_url_has_no_query_string(self):
        self._create_activity_log_page()

        page = CFGOVPage(title="test")
        self.root.add_child(instance=page)

        self.assertEqual(
            RelatedPosts.view_more_url(page, self.request), "/activity-log/"
        )

    def test_tags_get_appended_as_query_string(self):
        self._create_activity_log_page()

        page = CFGOVPage(title="test")
        self.root.add_child(instance=page)
        page.tags.add("bar")
        page.tags.add("foo")

        self.assertEqual(
            RelatedPosts.view_more_url(page, self.request),
            "/activity-log/?topics=bar&topics=foo",
        )
