from django.shortcuts import render_to_response
from django.http import HttpResponse

def home(request):
    user = request.user
    if user.is_authenticated():
        return HttpResponseRedirect("/accounts/profile/")
    return render_to_response("index.html")
