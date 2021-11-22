from django.db import models

# Create your models here.
class Region(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30, blank=True, null=True)

    class Meta:
        db_table = "regions"
        app_label = "matches"


class District(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30, blank=True, null=True)

    class Meta:
        db_table = "districts"
        app_label = "matches"


class Match(models.Model):
    id = models.AutoField(primary_key=True)
    city = models.ForeignKey("City", models.DO_NOTHING, null=True, blank=True)
    date = models.DateTimeField()
    schedule = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "matches"
        app_label = "matches"
