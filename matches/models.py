from django.db import models

# Create your models here.
class City(models.Model):
    idx = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30, blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "cities"
        app_label = "matches"


class Question(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey("user.User", models.DO_NOTHING, null=False)
    product_category = models.ForeignKey(
        "articles.ArticleProductCategory", models.DO_NOTHING, null=True, blank=True
    )
    value_category = models.ForeignKey(
        "articles.ArticleValueCategory", models.DO_NOTHING, null=True, blank=True
    )
    description = models.CharField(max_length=1500, blank=True, null=True)

    class Meta:
        db_table = "questions"
        app_label = "questions"
