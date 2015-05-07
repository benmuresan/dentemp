from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from models import UserProfile, DateAvailable, EventProfile, OfficeProfile
from django.contrib.auth import logout, login, authenticate
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
import json
import time
from datetime import date
# import dateutil.parser



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
                offices = OfficeProfile.objects.filter(user=user)
                if len(offices) > 0:
                    return HttpResponseRedirect("/office_dash/")
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


def new_office(request, id):
    user = User.objects.get(id=id)

    if request.POST:
        profile = OfficeProfile.objects.get(user=user)
        profile.office_name = request.POST["office_name"]
        user.email = request.POST["email"]
        profile.phone_number = request.POST["phone_number"]
        profile.street_address = request.POST["street_address"]
        profile.city = request.POST["city"]
        profile.state = request.POST["state"]
        profile.zip = request.POST["zip"]
        profile.website = request.POST["website"]
        user.save()
        profile.save()
        user.backend = 'django.contrib.auth.backends.ModelBackend'
        login(request, user)

        return HttpResponseRedirect("/office_dash/")

    return render(request,
                  "new_office.html", {"user": user})


@login_required
def user_dash(request):
    days_selected = DateAvailable.objects.filter(employee_available=request.user)
    date_list = []
    cal_date_list = []
    for d in days_selected:
        date_list.append({"id": d.id, "timestamp": str(d) + "000"})
        cal_date_list.append(str(d) + "000")
    cal_output = "[" + ", ".join(cal_date_list) + "]"
    output = json.dumps(date_list)
    days_available = len(days_selected)
    accepted_position = EventProfile.objects.filter(fulfilled_by=request.user)
    event_list = []
    for event in accepted_position:
        print event.office_created
        profile = OfficeProfile.objects.get(user=event.office_created)
        # event_list.append({"office_name": event.office_created, "date": event.date})
        event_list.append({"office_name": profile.office_name, "date": str(event.date)})
    event_output = json.dumps(event_list)
    # print event_output

    number_of_events = EventProfile.objects.filter(fulfilled_by=request.user)
    num_events = len(number_of_events)
    first_name = UserProfile.objects.filter(first_name=request.user)
    last_name = UserProfile.objects.filter(last_name=request.user)

    return render(request,
                  "user_dash.html",
                  {"days_selected": output,
                   "event_output": event_output,
                   "cal_days_selected": cal_output,
                   "days_available": days_available,
                   "number_of_events": num_events,
                   "first_name": first_name,
                   "last_name": last_name})


@login_required
def office_dash(request):
    number_of_events = EventProfile.objects.filter(office_created=request.user)
    num_events = len(number_of_events)
    office_name = OfficeProfile.objects.get(user=request.user)

    return render(request,
                  "office_dash.html",
                  {"number_of_events": num_events,
                   "office_name": office_name})


def create_user(request):
    if request.POST:
        print request.POST
        email = request.POST["email"]
        password1 = request.POST["password1"]
        password2 = request.POST["password2"]
        if password1 == password2:
            password = password1
        else:
            return redirect("/password_no_match/")

        user = User.objects.create_user(username=email, email=email, password=password)
        user.save()
        profile = UserProfile()
        profile.user = user
        profile.employee_type = request.POST["type"]
        print profile
        profile.save()
        return redirect("/new_user/" + str(user.id) + "/")

    return render(request,
                  "create_user.html")


def create_office(request):
    if request.POST:
        email = request.POST["email"]
        password1 = request.POST["password1"]
        password2 = request.POST["password2"]
        if password1 == password2:
            password = password1
        else:
            return redirect("/password_no_match/")
        # password = request.POST["password"]
        user = User.objects.create_user(username=email, email=email, password=password)
        user.save()
        profile = OfficeProfile()
        profile.user = user
        profile.save()
        return redirect("/new_office/" + str(user.id) + "/")

    return render(request,
                  "create_office.html")


    # if request.POST:
    # email = request.POST["email"]
    # password = request.POST["password"]
    #     user = User.objects.create_user(username=email, email=email, password=password)
    #     user.save()
    #     return redirect("/new_office/" + str(user.id) + "/")
    #
    # return render(request,
    #               "create_office.html")


def elements(request):
    return render(request,
                  "elements.html")


@csrf_exempt
def add_date(request):
    if request.POST:
        d = request.POST["date_available"]
        print d
        # da = date.fromtimestamp(int(d) / 1000)
        da = date.fromtimestamp(int(d) / 1000)
        date_available, created = DateAvailable.objects.get_or_create(employee_available=request.user, date=da)
        print da
        date_available.date = da
        date_available.employee_available = request.user
        date_available.save()
    return HttpResponse("Success")


@csrf_exempt
def add_office_event(request):
    context_dict = {}
    if request.POST:
        d = request.POST["date_available"]
        print d
        da = date.fromtimestamp(int(d) / 1000)
        employees_available = DateAvailable.objects.filter(date=da, is_available=True)
        print employees_available[0]
        context_dict = {"employees": employees_available}
    return render(request,
                  "add_office_event.html",
                  context_dict)


@csrf_exempt
def remove_date(request):
    if request.POST:
        d = request.POST["date_available"]
        da = date.fromtimestamp(int(d) / 1000)
        date_available = DateAvailable.objects.filter(employee_available=request.user, date=da)
        if len(date_available) < 1:
            return HttpResponse("Not found.")
        date_available[0].delete()
    return HttpResponse("Success")


@csrf_exempt
def remove_date_by_id(request):
    if request.POST:
        id = request.POST["id"]
        date_available = DateAvailable.objects.filter(id=id)
        if len(date_available) < 1:
            return HttpResponse("Not found.")
        date_available[0].delete()
    return HttpResponse("Success")


def pick_user(request):
    r = time.strftime("%Y-%m-%d", time.localtime(int("1430092800")))
    employees = DateAvailable.objects.filter(date=r)
    for x in employees:
        print x.employee_available.last_name, x.date
    return render(request, "")


@login_required
def log_out(request):
    logout(request)
    return render(request,
                  "log_out.html")


def generic(request):
    return render(request,
                  "generic.html")


def password_no_match(request):
    return render(request,
                  "password_no_match.html")


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
