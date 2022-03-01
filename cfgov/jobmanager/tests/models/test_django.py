from unittest import TestCase

from jobmanager.models import (
    ApplicantType,
    Grade,
    JobCategory,
    JobLength,
    MajorCity,
    Office,
    Region,
    ServiceType,
    State,
)


class ApplicantTypeTests(TestCase):
    def test_str(self):
        self.assertEqual(str(ApplicantType(applicant_type="foo")), "foo")

    def test_str_display_title_takes_precedence(self):
        self.assertEqual(
            str(ApplicantType(applicant_type="foo", display_title="bar")),
            "bar",
        )

    def test_compare_lt(self):
        self.assertLess(
            ApplicantType(applicant_type="a"),
            ApplicantType(applicant_type="b"),
        )

    def test_compare_gt(self):
        self.assertGreater(
            ApplicantType(applicant_type="b"),
            ApplicantType(applicant_type="a"),
        )


class GradeTests(TestCase):
    def test_str(self):
        self.assertEqual(
            str(Grade(grade="53", salary_min=1, salary_max=100)), "53"
        )

    def test_compare_lt(self):
        self.assertLess(
            Grade(grade="53", salary_min=1, salary_max=100),
            Grade(grade="60", salary_min=1, salary_max=100),
        )

    def test_compare_gt(self):
        self.assertGreater(
            Grade(grade="60", salary_min=1, salary_max=100),
            Grade(grade="53", salary_min=1, salary_max=100),
        )


class JobCategoryTests(TestCase):
    def test_str(self):
        self.assertEqual(str(JobCategory(job_category="foo")), "foo")


class ServiceTypeTests(TestCase):
    def test_str(self):
        self.assertEqual(str(ServiceType(service_type="foo")), "foo")


class JobLengthTests(TestCase):
    def test_str(self):
        self.assertEqual(str(JobLength(job_length="foo")), "foo")


class RegionTests(TestCase):
    def test_str(self):
        self.assertEqual(str(Region(name="foo", abbreviation="fo")), "foo")


class StateTests(TestCase):
    def test_str(self):
        self.assertEqual(
            str(State(name="foo", abbreviation="fo", region_id="ba")), "foo"
        )

    def test_compare_lt(self):
        self.assertLess(
            State(name="bar", abbreviation="ba", region_id="bz"),
            State(name="foo", abbreviation="fo", region_id="ba"),
        )

    def test_compare_gt(self):
        self.assertGreater(
            State(name="foo", abbreviation="fo", region_id="ba"),
            State(name="bar", abbreviation="ba", region_id="bz"),
        )


class OfficeTests(TestCase):
    def test_str(self):
        self.assertEqual(
            str(Office(name="foo", state_id="ba", abbreviation="fo")),
            "foo, ba",
        )


class MajorCityTests(TestCase):
    def test_str(self):
        self.assertEqual(
            str(MajorCity(name="foo", state_id="ba", region_id="bu")),
            "foo, ba",
        )
