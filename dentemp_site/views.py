from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from models import UserProfile, DateAvailable
from django.contrib.auth import logout, login, authenticate
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
import json


def index(request):
    return render(request,
                  "index.html")


def log_in(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(username=email, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/user_dash/')
            else:
                return render(request, 'account_disabled.html')
        else:
            return render(request, 'incorrect_login.html')
    else:
        return render(request, 'log_in.html', {})


def new_user(request, id):
    user = User.objects.get(id=id)

    if request.POST:
        user.first_name = request.POST["first_name"]
        user.last_name = request.POST["last_name"]
        user.license = request.POST["license"]
        user.email = request.POST["email"]
        user.phone_number = request.POST["phone_number"]
        user.street_address = request.POST["street_address"]
        user.city = request.POST["city"]
        user.state = request.POST["state"]
        user.zip = request.POST["zip"]
        user.website = request.POST["website"]
        user.anesthesia = request.POST.get("anesthesia", False)
        user.nitrous = request.POST.get("nitrous", False)
        user.restorative = request.POST.get("anesthesia", False)
        user.save()
        user.backend = 'django.contrib.auth.backends.ModelBackend'
        login(request, user)
        return HttpResponseRedirect('/user_dash/')

    return render(request,
                  "new_user.html", {"user": user})


@login_required
def user_dash(request):
    days_selected = DateAvailable.objects.filter(employee_available=request.user)
    date_list = []
    for d in days_selected:
        date_list.append(str(d) + "000")
    output = "[" + ", ".join(date_list) + "]"
    return render(request,
                  "user_dash.html", {"days_selected": output})


def new_office(request, id):
    user = User.objects.get(id=id)

    if request.POST:
        user.first_name = request.POST["first_name"]
        user.last_name = request.POST["last_name"]
        user.license = request.POST["license"]
        user.email = request.POST["email"]
        user.phone_number = request.POST["phone_number"]
        user.street_address = request.POST["street_address"]
        user.city = request.POST["city"]
        user.state = request.POST["state"]
        user.zip = request.POST["zip"]
        user.website = request.POST["website"]
        user.anesthesia = request.POST["anesthesia"]
        user.nitrous = request.POST["nitrous"]
        user.restorative = request.POST["anesthesia"]
        user.password = request.POST["password"]
        user.save()
        user.backend = 'django.contrib.auth.backends.ModelBackend'
        login(request, user)

        return redirect("/office_dash/")

    return render(request,
                  "new_office.html", {"user": user})


def create_user(request):
    if request.POST:
        print request.POST
        email = request.POST["email"]
        password = request.POST["password"]
        user = User.objects.create_user(username=email, email=email, password=password)
        user.save()
        profile = UserProfile()
        profile.user = user
        profile.employee_type = request.POST["type"]
        profile.save()
        return redirect("/new_user/" + str(user.id) + "/")

    return render(request,
                  "create_user.html")


def create_office(request):
    if request.POST:
        email = request.POST["email"]
        password = request.POST["password"]
        user = User.objects.create_user(email, password)
        user.save()
        return redirect("new_office.html" + str(user.id) + "/")

    return render(request,
                  "new_office.html")


def elements(request):
    return render(request,
                  "elements.html")


@login_required
def log_out(request):
    logout(request)
    return render(request,
                  "log_out.html")


def generic(request):
    return render(request,
                  "generic.html")


def office_dash(request):
    return render(request,
                  "office_dash.html")


def account_disabled(request):
    return render(request,
                  "account_disabled.html")


def incorrect_login(request):
    return render(request,
                  "incorrect_login.html")


def profile(request):
    return render(request,
                  "profile.html")


def contact(request):
    return render(request,
                  "contact.html")
