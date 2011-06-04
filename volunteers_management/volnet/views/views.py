from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from volnet.models import *
from forms import *
from django.template import RequestContext


def home(request):
    user = request.user
    if user.is_authenticated():
        return HttpResponseRedirect("/accounts/profile/")
    return render_to_response("index.html")

def is_member(user):
    qset = (Q(user__exact=user))
    member = Member.objects.filter(qset)
    if member:
        return True
    else:
        return False

def is_organization(user):
    qset = (Q(user__exact=user))
    member = Organization.objects.filter(qset)
    if member:
        return True
    else:
        return False

def is_volunteer(user):
    qset = (Q(user__exact=user))
    member = Volunteer.objects.filter(qset)
    if member:
        return True
    else:
        return False

@login_required
def profile(request):
    user = request.user
    organization = is_organization(user)
    member = is_member(user)
    volunteer = is_volunteer(user)
    if organization or member or volunteer:
        render_to_response("home.html", locals())
    if request.method == "POST":
        form = VolunteerInfoForm(request.POST)
        if form.is_valid():
            form.save_volunteer(user)
    else:
        form = VolunteerInfoForm()

    return render_to_response("insert_volunteer_info.html", locals(),
                              context_instance=RequestContext(request))

