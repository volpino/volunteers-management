from django import forms
from volnet.models import *
from django.db.models import Q
from datetime import datetime

class VolunteerInfoForm(forms.Form):
    first_name = forms.RegexField(regex=r'^[a-zA-Z]+$',
                                  max_length=100,
                                  widget=forms.TextInput(),
                                  label="First Name",
                                  required = True,
                                  error_messages={'invalid': "This value must contain only letters"})
    last_name = forms.RegexField(regex=r'^[a-zA-Z]+$',
                                 max_length=100,
                                 widget=forms.TextInput(),
                                 label="Last Name",
                                 required = True,
                                 error_messages={'invalid': "This value must contain only letters"})
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )

    SKILLS_CHOICES = (
        (0, 0),
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5)
    )
    gender = forms.ChoiceField(choices=GENDER_CHOICES,
                               label="Gender",
                               required=True)

    tel = forms.RegexField(regex=r'^[0-9-/]+$',
                       max_length=30,
                       widget=forms.TextInput(),
                       label="Telephone number",
                       required = True,
                       error_messages={'invalid': "This value must contain only numbers and - or /"})
    manual = forms.ChoiceField(choices=SKILLS_CHOICES,
                               label="Manual skills",
                               required=True)
    medical = forms.ChoiceField(choices=SKILLS_CHOICES,
                               label="Medical skills",
                               required=True)
    social = forms.ChoiceField(choices=SKILLS_CHOICES,
                               label="Social skills",
                               required=True)
    location = forms.CharField(label="Location place (*)")
    lat = forms.FloatField(label="Location latitude", required=True)
    lon = forms.FloatField(label="Location longitude", required=True)

    def save_volunteer(self, user):
        u = user
        u.first_name = self.cleaned_data["first_name"]
        u.last_name = self.cleaned_data["last_name"]
        u.save()
        v = Volunteer(user=user,
                      tel=self.cleaned_data["tel"],
                      gender=self.cleaned_data["gender"],
                      city_lat=self.cleaned_data["lat"],
                      city_lon=self.cleaned_data["lon"],
                      manual_skill=self.cleaned_data["manual"],
                      medical_skill=self.cleaned_data["medical"],
                      social_skill=self.cleaned_data["social"],
                      available=True)
        v.save()


class NewEmergencyForm(forms.Form):
    name = forms.CharField(label="Emergency Name",
                           max_length=100,
                           required = True)
    description = forms.CharField(label="Emergency Description",
                                  widget=forms.Textarea(),
                                  required=True)
    needed_people = forms.IntegerField(label="Estimated needed people",
                                       required=True)
    end_date = forms.DateField(label="Estimated deadline",
                               required=False)
    location = forms.CharField(label="Emergency place (*)")
    lat = forms.FloatField(label="Emergency latitude", required=True)
    lon = forms.FloatField(label="Emergency longitude", required=True)

    def save_emergency(self, user):
        #Quando checko che user sia in effetti un'organization
        qset = (Q(user__exact=user))
        organization = Organization.objects.filter(qset)
        if organization:
            em = Emergency(organization=organization[0],
                           name=self.cleaned_data["name"],
                           description=self.cleaned_data["description"],
                           needed_people=self.cleaned_data["needed_people"],
                           end_date=self.cleaned_data["end_date"],
                           lat=self.cleaned_data["lat"],
                           lon=self.cleaned_data["lon"],
                           active=True,
                           #notified_volunteers_set=set(),
                           #volunteers=set(),
                           start_date="2011-01-01"
                           )
            em.save()
