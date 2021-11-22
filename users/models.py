from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _

from .managers import CustomUserManager

GENDER_TPYE = (("male", "male"), ("female", "female"))
PLAY_TPYE = (
    ("passing", "passing"),
    ("dribbler", "dribbler"),
    ("pysical", "pysical"),
    ("balance", "balance"),
)


class User(AbstractUser):
    username = models.CharField(max_length=100)
    email = models.EmailField(_("email address"), unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    gender = models.CharField(max_length=20, choices=GENDER_TPYE, null=True, blank=True)
    phon_number = models.CharField(max_length=30, null=True, blank=True)
    bank_name = models.CharField(max_length=50, null=True, blank=True)
    bank_account = models.CharField(max_length=50, null=True, blank=True)
    bank_account_holder = models.CharField(max_length=50, null=True, blank=True)
    fairplay_point = models.IntegerField(null=True, blank=True)
    style = models.CharField(max_length=20, choices=PLAY_TPYE, null=True, blank=True)
    strength = models.CharField(max_length=50, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_newbie = models.BooleanField(default=True)
    is_vaccinated = models.BooleanField(default=True)

    def __str__(self):
        return self.email

    class Meta:
        db_table = "users"
        app_label = "users"


class Applier(AbstractUser):
    username = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_newbie = models.BooleanField(default=True)

    def __str__(self):
        return self.email

    class Meta:
        db_table = "users"
        app_label = "users"


class Level(AbstractUser):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey("User", models.DO_NOTHING, null=True, blank=True)
    match = models.ForeignKey("matches.Match", models.DO_NOTHING, null=True, blank=True)
    manager = models.ForeignKey("Manager", models.DO_NOTHING, null=True, blank=True)
    level = models.DecimalField(max_digits=8, decimal_places=1, null=True, blank=True)
    style = models.CharField(max_length=20, choices=PLAY_TPYE, null=True, blank=True)
    strength = models.CharField(max_length=50, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.email

    class Meta:
        db_table = "users"
        app_label = "users"
