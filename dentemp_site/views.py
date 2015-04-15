from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from models import UserProfile
from django.contrib.auth import logout


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
    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == 'POST':
        # Gather the username and password provided by the user.
        # This information is obtained from the login form.
                # We use request.POST.get('<variable>') as opposed to request.POST['<variable>'],
                # because the request.POST.get('<variable>') returns None, if the value does not exist,
                # while the request.POST['<variable>'] will raise key error exception
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Use Django's machinery to attempt to see if the username/password
        # combination is valid - a User object is returned if it is.
        user = authenticate(username=username, password=password)

        # If we have a User object, the details are correct.
        # If None (Python's way of representing the absence of a value), no user
        # with matching credentials was found.
        if user:
            # Is the account active? It could have been disabled.
            if user.is_active:
                # If the account is valid and active, we can log the user in.
                # We'll send the user back to the homepage.
                log_in(request, user)
                return render('/user_dash/')
            else:
                # An inactive account was used - no logging in!
                return render('account_disabled.html')
        else:
            return render('incorrect_login.html')


    # The request is not a HTTP POST, so display the login form.
    # This scenario would most likely be a HTTP GET.
    else:
        # No context variables to pass to the template system, hence the
        # blank dictionary object...
        return render(request, 'log_in.html', {})
    # if request.POST:
    #     username = request.POST["username"]
    #     password = request.POST["password"]
    #     user = User.objects.create_user(username, password)
    #     user.save()
    #     profile = UserProfile()
    #     profile.user = user
    #     profile.employee_type = request.POST["type"]
    #     profile.save()
    #     return redirect("user_dash")
    #
    # return render(request,
    #               "log_in.html")


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


def log_out(request):
    return render(request,
                  "log_out.html")
# # Use the login_required() decorator to ensure only those logged in can access the view.
# @login_required
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