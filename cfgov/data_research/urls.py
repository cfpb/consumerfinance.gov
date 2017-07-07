from django.conf.urls import url

from data_research.views import TimeSeriesData, MapData

urlpatterns = [

    url(r'^map-data/(?P<fips>\d+)/?$',
        MapData.as_view(),
        name='data_research_api_mapdata'),
    url(r'^time-series/(?P<fips>\d+)/?$',
        TimeSeriesData.as_view(),
        name='data_research_fips_timeseries'),
]
