from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
from django.db import models

from dashboard.models import Manufacturer, Company, Location, Supplier, Software, Hardware, Asset, DashUser

PRICE_TYPE = (
    ('Monthly', 'Monthly'),
    ('Annually', 'Annually'),
    ('Free', 'Free')
)


class Setting(models.Model):
    address = models.CharField(max_length=255, null=True, blank=True)
    contact_email = models.CharField(max_length=255, null=True, blank=True)
    phone_number = models.CharField(max_length=255, null=True, blank=True)
    social_facebook_link = models.CharField(max_length=255, null=True, blank=True)
    social_twitter_link = models.CharField(max_length=255, null=True, blank=True)
    footer = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return "SETTINGS"

class Feature(models.Model):
    icon = models.CharField(max_length=255, blank=True, null=True)
    title = models.CharField(max_length=255, blank=True, null=True)
    text = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title

class Demo(models.Model):
    image = models.ImageField(upload_to='demos', null=True)
    title = models.CharField(max_length=255, blank=True, null=True)
    text = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title

class About(models.Model):
    title = models.CharField(max_length=255, null=True, blank=True)
    text = models.TextField(blank=True, null=True)

    def __str__(self):
        return "ABOUT DETAILS"

class Contact(models.Model):
    title = models.CharField(max_length=255, null=True, blank=True)
    text = models.TextField(blank=True, null=True)
    phone = models.CharField(max_length=255, null=True, blank=True)
    address = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return "CONTACT DETAILS"

class Client(models.Model):
    name = models.CharField(max_length=64, null=True)
    logo = models.ImageField(upload_to="clients", null=True)
    url = models.CharField(max_length=64, null=True)

    def __str__(self):
        return self.name


class Account(models.Model):
    name = models.CharField(max_length=64, null=True)
    asset_limit = models.IntegerField(null=True, default=10, help_text="Give 0 for unlimited.")
    price = models.DecimalField(max_digits=64, decimal_places=2, null=True, default=0)
    price_detail = models.CharField(max_length=255, null=True)
    details = RichTextField(null=True, config_name='awesome_ckeditor')
    color_code = models.CharField(max_length=64, null=True)
    type = models.CharField(max_length=64, default="Monthly", choices=PRICE_TYPE)

    def __str__(self):
        return self.name


class Customer(models.Model):
    user = models.OneToOneField(User)
    company_name = models.CharField(max_length=64, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    address2 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=64, null=True, blank=True)
    state = models.CharField(max_length=64, null=True, blank=True)
    zip_or_postal = models.CharField(max_length=64, null=True, blank=True)
    country = models.CharField(max_length=64, null=True, blank=True)
    phone_number = models.CharField(max_length=255, null=True, blank=True)
    plan_name = models.CharField(max_length=64, null=True, blank=True)
    asset_limit = models.IntegerField(null=True, default=10, blank=True)
    price = models.DecimalField(max_digits=64, decimal_places=2, null=True, default=0, blank=True)
    details = RichTextField(null=True, config_name='awesome_ckeditor', blank=True)
    type = models.CharField(max_length=64, default="Monthly", choices=PRICE_TYPE, blank=True)
    manufacturers = models.ManyToManyField(Manufacturer, blank=True)
    companies = models.ManyToManyField(Company, blank=True)
    locations = models.ManyToManyField(Location, blank=True)
    suppliers = models.ManyToManyField(Supplier, blank=True)
    softwares = models.ManyToManyField(Software, blank=True)
    hardwares = models.ManyToManyField(Hardware, blank=True)
    assets = models.ManyToManyField(Asset, blank=True)
    dashusers = models.ManyToManyField(DashUser, blank=True)

    def assets_count(self):
        return self.assets.all().count()

    def fullname(self):
        return self.user.first_name + " " + self.user.last_name

    def __str__(self):
        return self.user.first_name + " " + self.user.last_name

class Header(models.Model):
    bg_image = models.ImageField(default="headers/default.jpg", upload_to="headers")
    text_area = models.TextField(blank=True, null=True)
    button_text = models.CharField(max_length=64, null=True)
    button_url = models.CharField(max_length=64, null=True)

    def __str__(self):
        return "HEADER DETAILS"