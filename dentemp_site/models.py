from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, primary_key=True)
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)
    license = models.CharField(max_length=128)
    picture = models.ImageField(upload_to='profile_images', blank=True)
    email = models.CharField(max_length=128)
    website = models.URLField(blank=True)
    address = models.CharField(max_length=128)
    times_hired = models.IntegerField(default=0)
    employee_type = models.CharField(max_length=128)
    employee_rate = models.FloatField(default=0)
    times_worked = models.IntegerField(default=0)
    employee_rating = models.IntegerField(default=0)
    about_me_comments = models.CharField(max_length=255)
    skills = models.CharField(max_length=255)

    # def __unicode__(self):
    # return self.email


class OfficeProfile(models.Model):
    user = models.OneToOneField(User, primary_key=True)
    office_name = models.CharField(max_length=128)
    website = models.URLField(blank=True)
    logo = models.ImageField(upload_to='profile_images', blank=True)
    email = models.CharField(max_length=128)
    address = models.CharField(max_length=128)
    has_hired = models.IntegerField(default=0)
    employees_hired = models.CharField(max_length=0)
    dates_needed = models.DateField(default=0)
    employee_type_needed = models.CharField(max_length=128)
    compensation_rate = models.FloatField(default=0)
    about_me_comments = models.CharField(max_length=255)

    def __unicode__(self):
        return self.email


class EventProfile(models.Model):
    fulfilled_by = models.ForeignKey(UserProfile, blank=True, null=True)
    office_created = models.ForeignKey(OfficeProfile)
    date = models.DateField(default=0)
    employee_type_needed = models.CharField(max_length=128)
    compensation_rate = models.FloatField(default=0)
    is_taken = models.CharField(max_length=255)
    special_instructions = models.TextField(max_length=1000)

    def __unicode__(self):
        return self.email


class DateAvailable(models.Model):
    employee_available = models.ForeignKey(UserProfile)
    date = models.DateField(default=0)

