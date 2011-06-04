from django.db import models
from django.contrib.auth.models import User
from fields import IntegerRangeField

GENDER_CHOICES = (
    ('M', 'Male'),
    ('F', 'Female'),
)

SKILLS_CHOICES = (
    ('M', 'Manual skills'),
    ('E', 'Medical skills'),
    ('S', 'Social skills')
)


class Volunteer(models.Model):
    user = models.OneToOneField(User, unique=True)
    tel = models.CharField("Telephone number", max_length=30)
    gender = models.CharField("Gender", max_length=1, choices=GENDER_CHOICES)
    city_lat = models.FloatField("City Latitude")
    city_lon = models.FloatField("City Longitude")
    manual_skill = IntegerRangeField("Manual skills", min_value=0, max_value=5)
    medical_skill = IntegerRangeField("Medical skills", min_value=0,
                                      max_value=5)
    social_skill = IntegerRangeField("Social skills", min_value=0, max_value=5)
    available = models.BooleanField("Availability")

    def __unicode__(self):
        return self.user.username

class VolunteerComment(models.Model):
    volunteer = models.ForeignKey(Volunteer)
    text = models.TextField("Text")
    feedback = models.NullBooleanField("Feedback")

class Organization(models.Model):
    user = models.OneToOneField(User, unique=True)
    name = models.CharField("Organization name", max_length=100)

    def __unicode__(self):
        return self.name

class Member(Volunteer):
    organization = models.ForeignKey(Organization)

class Emergency(models.Model):
    organization = models.ForeignKey(Organization)
    name = models.CharField("Emergency", max_length=100)
    description = models.TextField("Description")
    needed_people = models.IntegerField("Estimated needed people")
    notified_volunteers = models.ManyToManyField(Volunteer,
                          related_name="notified_emergency", blank=True)
    volunteers = models.ManyToManyField(Volunteer,
                 related_name="emergency_volunteers", blank=True)
    start_date = models.DateField("Start date")
    end_date = models.DateField("End date")
    lat = models.FloatField("Latitude")
    lon = models.FloatField("Longitude")
    active = models.BooleanField("Active")

    def __unicode__(self):
        return self.name

class Event(models.Model):
    member = models.ForeignKey(Member)
    emergency = models.ForeignKey(Emergency)
    volunteers = models.ManyToManyField(Volunteer,
                 related_name="event_volunteers", blank=True)
    name = models.CharField("Name", max_length=100)
    description = models.TextField("Description")
    skill_type = models.CharField("Skills type required", max_length=1,
                                  choices=SKILLS_CHOICES)
    min_skill = IntegerRangeField("Minimum skills required",
                                         max_value=5)
    priority = IntegerRangeField("Priority (1-5)", min_value=1, max_value=5)
    start_date = models.DateField("Start date")
    end_date = models.DateField("End date")
    lat = models.FloatField("Latitude")
    lon = models.FloatField("Longitude")
    active = models.BooleanField("Active")

class EventComment(models.Model):
    user = models.ForeignKey(User)
    event = models.ForeignKey(Event)
    text = models.TextField("Text")
