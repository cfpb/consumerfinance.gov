from django.conf.urls import url

from data_research.views import (
    TimeSeriesData, TimeSeriesNational, MapData, MetaData)

urlpatterns = [

    url(r'^time-series/(?P<fips>\d{2,5})/?$',
        TimeSeriesData.as_view(),
        name='data_research_api_mortgage_timeseries'),
    url(r'^time-series/national/?$',
        TimeSeriesNational.as_view(),
        name='data_research_api_mortgage_timeseries_national'),
    url(r'^map-data/(?P<geo>counties)/(?P<year_month>\d{4}-\d{2})/?$',
        MapData.as_view(),
        name='data_research_api_mortgage_county_mapdata'),
    url(r'^map-data/(?P<geo>metros)/(?P<year_month>\d{4}-\d{2})/?$',
        MapData.as_view(),
        name='data_research_api_mortgage_metro_mapdata'),
    url(r'^map-data/(?P<geo>states)/(?P<year_month>\d{4}-\d{2})/?$',
        MapData.as_view(),
        name='data_research_api_mortgage_state_mapdata'),
    url(r'^metadata/(?P<meta_name>[a-z_]*)/?$',
        MetaData.as_view(),
        name='data_research_api_metadata'),
]
