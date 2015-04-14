from django.shortcuts import render, redirect
from .forms import NewUserForm, NewOfficeForm
from django.contrib.auth.models import User
from models import UserProfile

# def new_user(request):
# if request.method == 'POST':
# form = NewUserForm
# if form.is_valid():
#             form.save()
#     else:
#         form = NewUserForm
#     context_dict = {'form': form}
#     return render(request, 'new_user.html', context_dict)


def index(request):
    return render(request,
                  "index.html")


def profile(request):
    return render(request,
                  "profile.html")


def log_in(request):
    if request.POST:
        username = request.POST["username"]
        password = request.POST["password"]
        user = User.objects.create_user(username, password)
        user.save()
        profile = UserProfile()
        profile.user = user
        profile.employee_type = request.POST["type"]
        profile.save()
        return redirect("user_dash")

    return render(request,
                  "log_in.html")


def create_user(request):
    if request.POST:
        print request.POST
        username = request.POST["username"]
        password = request.POST["password"]
        user = User.objects.create_user(username, password)
        user.save()
        profile = UserProfile()
        profile.user = user
        profile.employee_type = request.POST["type"]
        profile.save()
        return redirect("new_user.html")

    return render(request,
                  "create_user.html")


def create_office(request):
    if request.POST:
        username = request.POST["username"]
        password = request.POST["password"]
        user = User.objects.create_user(username, password)
        user.save()
        return redirect("new_office.html")

    return render(request,
                  "create_office.html")


def elements(request):
    return render(request,
                  "elements.html")


def log_out(request):
    return render(request,
                  "log_out.html")


def generic(request):
    return render(request,
                  "generic.html")


def user_dash(request):
    return render(request,
                  "user_dash.html")


def office_dash(request):
    return render(request,
                  "office_dash.html")


def new_user(request):
    new_user_form = NewUserForm()



    # A boolean value for telling the template whether the registration was successful.
    # Set to False initially. Code changes value to True when registration succeeds.
    registered = False

    # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':
        # Attempt to grab information from the raw form information.
        # Note that we make use of both UserForm and UserProfileForm.
        new_user_form = NewUserForm(data=request.POST)
        # If the two forms are valid...
        if new_user_form.is_valid():
            # Save the user's form data to the database.
            user = new_user_form.save()
            registered = True
    else:
        new_user_form = NewUserForm()
        # profile_form = UserProfileForm()

    # Render the template depending on the context.
    return render(request,
                  'new_user.html',
                  {'new_user_form': new_user_form, 'registered': registered})


def new_office(request):
    new_office_form = NewOfficeForm()

    registered = False

    if request.method == 'POST':
        new_office_form = NewOfficeForm(data=request.POST)
        if new_office_form.is_valid():
            # Save the user's form data to the database.
            user = new_office_form.save()

            registered = True

    else:
        new_office_form = NewOfficeForm()
        # profile_form = UserProfileForm()

    # Render the template depending on the context.
    return render(request,
                  'new_office.html',
                  {'new_office_form': new_office_form, 'registered': registered})