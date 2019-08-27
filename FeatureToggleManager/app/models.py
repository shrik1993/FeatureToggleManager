"""
Definition of models.
"""

from djongo import models
from django_pandas.managers import DataFrameManager

class TeamData(models.Model):
    columns = models.ListField()
    data = models.ListField()
    team_name = models.CharField(max_length=200, primary_key=True)
