from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from models import UserProfile, DateAvailable, EventProfile, OfficeProfile, LatLong
from django.contrib.auth import logout, login, authenticate
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
import json
import time
from datetime import date
from radius import filter_by_distance
# from math import sqrt

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
        profile = UserProfile.objects.get(user=user)

        location = LatLong()
        location.user = user
        location.lat = request.POST["lat"]
        location.long = request.POST["long"]

        profile.first_name = request.POST["first_name"]
        user.first_name = request.POST["first_name"]
        profile.last_name = request.POST["last_name"]
        user.last_name = request.POST["last_name"]
        profile.license = request.POST["license"]
        profile.email = request.POST["email"]
        profile.phone_number = request.POST["phone_number"]
        profile.street_address = request.POST["street_address"]
        profile.city = request.POST["city"]
        profile.state = request.POST["state"]
        profile.zip = request.POST["zip"]
        profile.website = request.POST["website"]
        profile.anesthesia = request.POST.get("anesthesia", False)
        profile.nitrous = request.POST.get("nitrous", False)
        profile.restorative = request.POST.get("anesthesia", False)
        location.save()
        profile.save()
        user.save()
        user.backend = 'django.contrib.auth.backends.ModelBackend'
        login(request, user)
        return HttpResponseRedirect('/user_dash/')

    return render(request,
                  "new_user.html", {"user": user})


def new_office(request, id):
    user = User.objects.get(id=id)

    if request.POST:
        location = LatLong()
        location.user = user
        location.lat = request.POST["lat"]
        location.long = request.POST["long"]

        profile = OfficeProfile.objects.get(user=user)
        profile.office_name = request.POST["office_name"]
        # user.email = request.POST["email"]
        profile.email = request.POST["email"]
        profile.phone_number = request.POST["phone_number"]
        profile.street_address = request.POST["street_address"]
        profile.city = request.POST["city"]
        profile.state = request.POST["state"]
        profile.zip = request.POST["zip"]
        profile.website = request.POST["website"]
        location.save()
        user.save()
        profile.save()
        user.backend = 'django.contrib.auth.backends.ModelBackend'
        login(request, user)

        return HttpResponseRedirect("/office_dash/")

    return render(request,
                  "new_office.html", {"user": user})


@login_required
def user_dash(request):
    # Creates a DateAvailable object with a timestamp and id attached.
    days_selected = DateAvailable.objects.filter(employee_available=request.user, is_available=True)
    days_available = len(days_selected)
    date_list = []
    cal_date_list = []
    for d in days_selected:
        print (str(d))
        date_list.append({"id": d.id, "timestamp": str(d) + "000"})
        cal_date_list.append(str(d) + "000")
    cal_output = "[" + ", ".join(cal_date_list) + "]"
    output = json.dumps(date_list)
    print output
    # -----------------------------------------------------------------------------------------

    # Creates event_output json which contains office name/date/id that selected the user.
    requested_user = EventProfile.objects.filter(requested_user=request.user)
    event_list = []
    for event in requested_user:
        print event.office_created
        print event.date
        profile = OfficeProfile.objects.get(user=event.office_created)
        # event_list.append({"office_name": event.office_created, "date": event.date})
        event_list.append({"office_name": profile.office_name, "id": event.id, "date": str(event.date)})
    event_output = json.dumps(event_list)
    # --------------------------------------------------------------------------------------------

    number_of_events = EventProfile.objects.filter(requested_user=request.user)
    num_events = len(number_of_events)
    x = UserProfile.objects.get(user=request.user)
    first_name = x.first_name
    last_name = x.last_name
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


def elements(request):
    return render(request,
                  "elements.html")


@csrf_exempt
def add_date(request):
    if request.POST:
        d = request.POST["date_available"]
        print d
        da = date.fromtimestamp(int(d) / 1000)
        date_available, created = DateAvailable.objects.get_or_create(employee_available=request.user, date=da)
        print da
        date_available.date = da
        date_available.employee_available = request.user
        date_available.save()
    return HttpResponse("Success")


@csrf_exempt
def add_office_event(request):
    users_available = []
    # users_available = {}
    # # This is where def filter_by_distance is used.
    # # Location information for each user is retrieved, and placed into an array to be used for sorting.
    # # ------------------------------------------------------------------------------------------------------
    #
    # lat_long_data = []
    # location_data = LatLong.objects.all()  # This object should contain Lat, Long, user.
    # for each in location_data:
    # # print each.user.id
    #     lat_long_data.append([float(each.lat), float(each.long), each.user.id])
    # # print lat_long_data
    #
    # # ------------------------------------------------------------------------------------------------------

    # context_dict = {}
    if request.POST:
        d = request.POST["date_needed"]
        # This is where the employee type comes in.
        type_user = request.POST["type_user"]
        # print type_user
        da = date.fromtimestamp(int(d) / 1000)
        # print da
        employee_available = DateAvailable.objects.filter(date=da, is_available=True,
                                                          employee_available__profile__employee_type=type_user)
        print employee_available

        employee_available_on_date = []
        for i in employee_available:
            profile = UserProfile.objects.get(user=i.employee_available)
            first_name = profile.first_name
            last_name = profile.last_name
            # print first_name
            # print last_name
            employee_available_on_date.append({"first_name": first_name, "last_name": last_name})
            users_available = json.dumps(employee_available_on_date)
            print users_available


            # context_dict = {"employees": users_available}
            # return redirect("/add_office_event/", {
            # "users_available": users_available,
            #     "lat_long_data": lat_long_data})

        return redirect('/add_office_event/', {
            "users_available": users_available})
        # "lat_long_data": lat_long_data})

    return render(request,
                  "add_office_event.html")


@csrf_exempt
def user_accept_event(request):
    if request.POST:
        date = request.POST["date"]
        id = request.POST["id"]
        print id
        print date
        ds = time.strptime(date, "%m/%d/%Y")
        print ds
        da = str(ds[0]) + '-' + str(ds[1]) + '-' + str(ds[2])
        # da = str(ds[1]) + '-' + str(ds[2]) + '-' + str(ds[0])
        print da
        # id_object = DateAvailable.objects.filter(id=id)
        # print id_object
        # date_accepted = request.POST["date_accepted"]
        a = DateAvailable.objects.get(employee_available=request.user, date=da)
        # a = DateAvailable.objects.get(id=id)
        print a
        a.is_available = False
        # Todo office would receive this user as confirmed on their dash for this day.
        a.save()
        print a.is_available
        # Todo user date would be removed from available.  And the office event would be removed/closed.
        # Todo This is where an email would be sent to the office that the date has been accepted.
    return HttpResponse("Success")


@csrf_exempt
def remove_date(request):
    if request.POST:
        d = request.POST["date_available"]
        da = date.fromtimestamp(int(d) / 1000)
        date_available = DateAvailable.objects.filter(employee_available=request.user, date=da)
        print date_available
        if len(date_available) < 1:
            return HttpResponse("Not found.")
        date_available[0].delete()
    return HttpResponse("Success")


@csrf_exempt
def remove_date_by_id(request):
    if request.POST:
        id = request.POST["id"]
        print id
        date_available = DateAvailable.objects.filter(id=id)
        if len(date_available) < 1:
            return HttpResponse("Not found.")
        date_available[0].delete()
    return HttpResponse("Success")


    # Sends the dates the user is available to the calendar.


def dates_clicked(request):
    # Creates a DateAvailable object with a timestamp and id attached.
    days_selected = DateAvailable.objects.filter(employee_available=request.user, is_available=True)
    days_available = len(days_selected)
    date_list = []
    cal_date_list = []
    for d in days_selected:
        date_list.append({"id": d.id, "timestamp": str(d) + "000"})
        cal_date_list.append(str(d) + "000")
    cal_output = "[" + ", ".join(cal_date_list) + "]"
    output = json.dumps(cal_output)
    print output
    return HttpResponse(output, content_type="application/json")


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


# def profile(request):
# return render(request,
# "profile.html")


@login_required
def profile(request):
    profile = UserProfile.objects.get(user=request.user)
    # profile = UserProfile.objects.get(user=user)
    print profile.first_name
    first_name = profile.first_name
    last_name = profile.last_name
    license = profile.license
    email = profile.email
    phone_number = profile.phone_number
    street_address = profile.street_address
    city = profile.city
    state = profile.state
    zip = profile.zip
    website = profile.website
    anesthesia = profile.anesthesia
    nitrous = profile.nitrous
    restorative = profile.restorative

    # first_name = profile.first_name
    # profile.first_name = request.POST["first_name"]
    # profile.last_name = request.POST["last_name"]
    # profile.last_name = request.POST["last_name"]
    # profile.license = request.POST["license"]
    # profile.email = request.POST["email"]
    # profile.phone_number = request.POST["phone_number"]
    # profile.street_address = request.POST["street_address"]
    # profile.city = request.POST["city"]
    # profile.state = request.POST["state"]
    # profile.zip = request.POST["zip"]
    # profile.website = request.POST["website"]
    # profile.anesthesia = request.POST.get("anesthesia", False)
    # profile.nitrous = request.POST.get("nitrous", False)
    # profile.restorative = request.POST.get("anesthesia", False)

    return render(request,
                  'profile.html',
                  {"first_name": first_name,
                   "last_name": last_name,
                   "email": email,
                   "phone_number": phone_number,
                   "street_address": street_address,
                   "city": city,
                   "state": state,
                   "zip": zip,
                   "website": website,
                   "anesthesia": anesthesia,
                   "nitrous": nitrous,
                   "restorative": restorative,
                   "license": license,
                  })


@login_required
def office_profile(request):
    profile = OfficeProfile.objects.get(user=request.user)
    # profile = UserProfile.objects.get(user=user)
    print profile.office_name
    office_name = profile.office_name
    email = profile.email
    phone_number = profile.phone_number
    street_address = profile.street_address
    city = profile.city
    state = profile.state
    zip = profile.zip
    website = profile.website

    # first_name = profile.first_name
    # profile.first_name = request.POST["first_name"]
    # profile.last_name = request.POST["last_name"]
    # profile.last_name = request.POST["last_name"]
    # profile.license = request.POST["license"]
    # profile.email = request.POST["email"]
    # profile.phone_number = request.POST["phone_number"]
    # profile.street_address = request.POST["street_address"]
    # profile.city = request.POST["city"]
    # profile.state = request.POST["state"]
    # profile.zip = request.POST["zip"]
    # profile.website = request.POST["website"]
    # profile.anesthesia = request.POST.get("anesthesia", False)
    # profile.nitrous = request.POST.get("nitrous", False)
    # profile.restorative = request.POST.get("anesthesia", False)

    return render(request,
                  'office_profile.html',
                  {"office_name": office_name,
                   "email": email,
                   "phone_number": phone_number,
                   "street_address": street_address,
                   "city": city,
                   "state": state,
                   "zip": zip,
                   "website": website,
                  })


def contact(request):
    return render(request,
                  "contact.html")
