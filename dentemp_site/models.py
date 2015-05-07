from django.db import models
from django.contrib.auth.models import User
from django.utils.dateformat import format


class UserProfile(models.Model):
    user = models.OneToOneField(User, primary_key=True)
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)
    phone_number = models.CharField(max_length=128)
    license = models.CharField(max_length=128, blank=True, null=True)
    picture = models.ImageField(upload_to='profile_images', blank=True, null=True)
    email = models.CharField(max_length=128)
    website = models.URLField(blank=True, null=True)
    street_address = models.CharField(max_length=128)
    city = models.CharField(max_length=128)
    state = models.CharField(max_length=128)
    zip = models.CharField(max_length=128)
    times_hired = models.IntegerField(default=0)
    employee_type = models.CharField(max_length=128)
    employee_rate = models.FloatField(default=0)
    times_worked = models.IntegerField(default=0)
    employee_rating = models.IntegerField(default=0)
    about_me_comments = models.CharField(max_length=255)
    anesthesia = models.CharField(max_length=255, blank=True, null=True)
    nitrous = models.CharField(max_length=255, blank=True, null=True)
    restorative = models.CharField(max_length=255, blank=True, null=True)

    def __unicode__(self):
        return self.email


class OfficeProfile(models.Model):
    user = models.OneToOneField(User, primary_key=True, related_name="office")
    office_name = models.CharField(max_length=128)
    phone_number = models.CharField(max_length=128)
    website = models.URLField(blank=True)
    logo = models.ImageField(upload_to='profile_images', blank=True)
    email = models.CharField(max_length=128)
    street_address = models.CharField(max_length=128)
    city = models.CharField(max_length=128)
    state = models.CharField(max_length=128)
    zip = models.CharField(max_length=128)
    has_hired = models.IntegerField(default=0, blank=True, null=True)
    employees_hired = models.CharField(max_length=10000, blank=True, null=True)
    # dates_needed = models.DateField()
    # employee_type_needed = models.CharField(max_length=128)
    # compensation_rate = models.FloatField(default=0)
    about_me_comments = models.CharField(max_length=255, blank=True, null=True)

    def __unicode__(self):
        return self.office_name


class EventProfile(models.Model):
    fulfilled_by = models.ForeignKey(User, blank=True, null=True)
    office_created = models.ForeignKey(User, related_name="events")
    date = models.DateField(default=0)
    employee_type_needed = models.CharField(max_length=128)
    compensation_rate = models.FloatField(default=0)
    is_taken = models.CharField(max_length=255)
    special_instructions = models.TextField(max_length=1000)

    # def __unicode__(self):
    #     return self.email


class DateAvailable(models.Model):
    employee_available = models.ForeignKey(User)
    is_available = models.BooleanField(default=True)
    date = models.DateField(default=0)
    # Todo Should I add a is_hygienist or is_assistant here?

    def __unicode__(self):
        return format(self.date, 'U')