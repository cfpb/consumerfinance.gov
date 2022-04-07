from datetime import date


atlanta_ga = {"name": "Atlanta", "state_id": "GA"}
boston_ma = {"name": "Boston", "state_id": "MA"}
chicago_il = {"name": "Chicago", "state_id": "IL"}
los_angeles_ca = {"name": "Los Angeles", "state_id": "CA"}
new_york_ny = {"name": "New York", "state_id": "NY"}
phoenix_az = {"name": "Phoenix", "state_id": "AZ"}
st_louis_mo = {"name": "St. Louis", "state_id": "MO"}
washington_dc = {"name": "Washington", "state_id": "DC"}


northeast = {
    "name": "Northeast region",
    "states": ["CT", "DE", "MA", "NY"],
    "major_cities": [boston_ma, new_york_ny],
}


southeast = {
    "name": "Southeast region",
    "states": ["DC", "FL", "GA", "MD"],
    "major_cities": [washington_dc, atlanta_ga],
}


midwest = {
    "name": "Midwest region",
    "states": ["IA", "IL", "IN", "MO"],
    "major_cities": [chicago_il, st_louis_mo],
}


west = {
    "name": "West region",
    "states": ["AK", "AZ", "CA", "CO"],
    "major_cities": [phoenix_az, los_angeles_ca],
}


job_listing_details_defaults = {
    "title": "Director, Example Division",
    "url": "/jobs/example/",
    "offices": [washington_dc],
    "regions": [],
    "close_date": date(2099, 1, 1),
    "division": "Operations",
    "grades": [30],
    "salary_min": 50000,
    "salary_max": 100000,
    "applicant_types": [
        "Open to All US Citizens (Competitive service - Permanent)",
    ],
}


job_listing_details_test_cases = {
    "Job in single office": {},
    "Job in single office, remote allowed": {"remote_allowed": True},
    "Job with two offices": {"offices": [washington_dc, new_york_ny]},
    "Job with two offices, remote allowed": {
        "offices": [washington_dc, new_york_ny],
        "remote_allowed": True,
    },
    "Job with three offices": {
        "offices": [washington_dc, atlanta_ga, new_york_ny],
    },
    "Job with three offices, remote allowed": {
        "offices": [washington_dc, atlanta_ga, new_york_ny],
        "remote_allowed": True,
    },
    "Job for a single region": {"offices": [], "regions": [northeast]},
    "Job for two regions": {"offices": [], "regions": [northeast, southeast]},
    "Job for four regions": {
        "offices": [],
        "regions": [northeast, southeast, midwest, west],
    },
    "Job with no location": {"offices": [], "regions": []},
    "Job with single grade": {},
    "Job with multiple grades": {"grades": [52, 53, 60]},
    "Job with no grades": {"grades": []},
    "Job with fixed salary": {"salary_min": 10000, "salary_max": 10000},
    "Job with decimal salary": {"salary_min": 1234.56, "salary_max": 2345.0},
    "Job with hourly salary": {
        "salary_min": 15.00,
        "salary_max": 15.00,
        "salary_is_hourly": True,
    },
    "Job with hourly salary range": {
        "salary_min": 15.00,
        "salary_max": 22.50,
        "salary_is_hourly": True,
    },
    "Job with month that should not get abbreviated": {
        "close_date": date(2099, 6, 1),
    },
    "Job with single applicant type": {},
    "Job with multiple applicant types": {
        "applicant_types": [
            "Open to All US Citizens (Competitive service - Permanent)",
            "Open to status candidates (Competitive service - Permanent)",
        ],
    },
    "Job with no applicant types": {"applicant_types": []},
}


for job in job_listing_details_test_cases.values():
    for k, v in job_listing_details_defaults.items():
        job.setdefault(k, v)


job_listing_list_defaults = {
    "more_jobs_url": "/about-us/careers/current-openings/",
}


job_listing_list_test_cases = {
    "No open jobs": {},
    "Single open job": {
        "jobs": [
            {
                "title": "Director, Example Division",
                "url": "/jobs/example/",
                "close_date": date(2099, 1, 1),
            },
        ],
    },
    "Multiple open jobs": {
        "jobs": [
            {
                "title": f"Open job {i}",
                "url": f"/jobs/{i}",
                "close_date": date(2099, i, 1),
            }
            for i in range(5, 0, -1)
        ],
    },
}


for job_list in job_listing_list_test_cases.values():
    for k, v in job_listing_list_defaults.items():
        job_list.setdefault(k, v)


job_listing_table_test_cases = {
    "No open jobs": {},
    "Single open job": {
        "jobs": [
            {
                "title": "Example job",
                "url": "/jobs/example/",
                "grades": [30],
                "close_date": date(2099, 1, 1),
                "regions": [],
                "offices": washington_dc,
            },
        ],
    },
    "Multiple open jobs": {
        "jobs": [
            dict(job, title=title)
            for title, job in job_listing_details_test_cases.items()
        ],
    },
}
