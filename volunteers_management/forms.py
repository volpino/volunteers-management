from django import forms
from volnet.models import *

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
    lat = forms.FloatField("Home city latitude", required=True)
    lon = forms.FloatField("Home city longitude", required=True)

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
