from django.conf.urls import url

from data_research.views import (
    MapData, MetaData, TimeSeriesData, TimeSeriesNational
)


urlpatterns = [

    url(r'^time-series/(?P<days_late>[3890-]*)/(?P<fips>[0-9non-]*)/?$',
        TimeSeriesData.as_view(),
        name='data_research_api_mortgage_timeseries'),
    url(r'^time-series/(?P<days_late>[3890-]*)/national/?$',
        TimeSeriesNational.as_view(),
        name='data_research_api_mortgage_timeseries_national'),
    url(r'^map-data/(?P<days_late>[3890-]*)/(?P<geo>[a-z]*)/(?P<year_month>\d{4}-\d{2})/?$',  # noqa: E501
        MapData.as_view(),
        name='data_research_api_mortgage_mapdata'),
    url(r'^metadata/(?P<meta_name>[a-z_]*)/?$',
        MetaData.as_view(),
        name='data_research_api_metadata'),
]
