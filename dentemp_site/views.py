from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from models import UserProfile
from django.contrib.auth import logout, login, authenticate
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required


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

def contact(request):
    return render(request,
                  "contact.html")


def log_in(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            print "if user hit"
            if user.is_active:
                print("user is active")
                login(request, user)
                return HttpResponseRedirect('/user_dash/')
            else:
                return render(request, 'account_disabled.html')
        else:
            return render(request, 'incorrect_login.html')
    else:
        return render(request, 'log_in.html', {})



def create_user(request):
    if request.POST:
        print request.POST
        username = request.POST["username"]
        password = request.POST["password"]
        user = User.objects.create_user(username=username, password=password)
        user.save()
        profile = UserProfile()
        profile.user = user
        profile.employee_type = request.POST["type"]
        profile.save()
        return redirect("/new_user/")

    return render(request,
                  "create_user.html")


def create_office(request):
    if request.POST:
        username = request.POST.get["username"]
        password = request.POST.get["password"]
        user = User.objects.create_user(username, password)
        user.save()
        return redirect("new_office.html")

    return render(request,
                  "create_office.html")


def elements(request):
    return render(request,
                  "elements.html")

@login_required
def log_out(request):
    logout(request)
    return render(request,
                  "log_out.html")
# # Use the login_required() decorator to ensure only those logged in can access the view.
# def user_logout(request):
#     # Since we know the user is logged in, we can now just log them out.
#     logout(request)
#
#     # Take the user back to the homepage.
#     return HttpResponseRedirect('/rango/')


def generic(request):
    return render(request,
                  "generic.html")


def user_dash(request):
    return render(request,
                  "user_dash.html")


def office_dash(request):
    return render(request,
                  "office_dash.html")


def account_disabled(request):
    return render(request,
                  "account_disabled.html")


def incorrect_login(request):
    return render(request,
                  "incorrect_login.html")


def new_user(request):

    # if request.method == 'POST':

    return render(request, "new_user.html")


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