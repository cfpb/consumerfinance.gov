from django.db import models


"""
Contains a model used for tracking market data with the consumer credit trends (CCT)
portion of www.consumerfinance.gov
"""

# Used for tracking Market data for the CCT
class Market(models.Model):
    """ A basic Market object. """
    # Market key corresponds to data in Wagtail DB for lookup? Or name?
    market_key = models.CharField(max_length=20)
    num_originations = models.CharField(max_length=20)
    value_originations = models.CharField(max_length=20)
    year_over_year_change = models.CharField(max_length=20)

    # Market-specific descriptor text
    num_originations_text = models.CharField()     
    value_originations_text = models.CharField()   
    year_over_year_change_text = models.CharField()
    # latest data may be a generic cct_data_month value in db, not per-market
    # because they all get updated by the same job
    latest_data = models.CharField(max_length=15)   # monthname year
