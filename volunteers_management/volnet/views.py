from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from volnet.models import *

def home(request):
    user = request.user
    if user.is_authenticated():
        return HttpResponseRedirect("/accounts/profile/")
    return render_to_response("index.html")

def is_member(user):
    qset = (Q(user__exact=user))
    member = Member.objects.filter(qset)
    return member != None

def is_organization(user):
    qset = (Q(user__exact=user))
    member = Organization.objects.filter(qset)
    return member != None

def is_volunteer(user):
    qset = (Q(user__exact=user))
    member = Volunteer.objects.filter(qset)
    return member != None

@login_required
def profile(request):
    user = request.user
    if is_organization(user):
        return render_to_response("home_organizations.html")
    elif is_member(user):
        return render_to_reponse("home_members.html")
    elif is_volunteer(user):
        return render_to_response("home_volunteers.html")


