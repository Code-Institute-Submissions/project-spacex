from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import ContactDetail
from .forms import UserLoginForm, UserSignupForm, UserContactDetailForm, UserUpdateForm


@login_required
def logout_page(request):
    auth.logout(request)
    messages.success(request, "You have successfully been logged out")
    return redirect(reverse('login'))


def login_page(request):

    if request.user.is_authenticated:
        return redirect(reverse('profile'))

    if request.method == "POST":
        login_form = UserLoginForm(request.POST)

        if login_form.is_valid():
            user = auth.authenticate(username=request.POST['username'],
                                     password=request.POST['password'])

            if user:
                auth.login(user=user, request=request)
                messages.success(request, "You have successfully logged in!")
                return redirect(reverse('profile'))
            else:
                login_form.add_error(
                    None, "Your username or password is incorrect")

    else:
        login_form = UserLoginForm()
    context = {
        "page_title": "Log In",
        "form": login_form
    }
    return render(request, "login.html", context)


def signup_page(request):

    if request.user.is_authenticated:
        return redirect(reverse('profile'))

    if request.method == "POST":
        signup_form = UserSignupForm(request.POST)

        if signup_form.is_valid():
            signup_form.save()

            user = auth.authenticate(username=request.POST['username'],
                                     password=request.POST['password1'])

            if user:
                auth.login(user=user, request=request)
                contact = ContactDetail(user=user)
                contact.save()
                messages.success(request, "Your account has been created")
                return redirect(reverse('profile'))
            else:
                messages.error(
                    request, "We were unable to register your account.")

    else:
        signup_form = UserSignupForm()

    context = {
        "page_title": "Sign Up",
        "form": signup_form
    }
    return render(request, 'signup.html', context)


@login_required
def profile_page(request):
    user = User.objects.get(email=request.user.email)
    contact = ContactDetail.objects.get(user=request.user)

    context = {
        "page_title": "Profile",
        "user": user,
        "contact": contact
    }
    return render(request, 'profile.html', context)


@login_required
def contact_details_page(request):

    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        c_form = UserContactDetailForm(
            request.POST,
            request.FILES,
            instance=request.user.contactdetail)
        if u_form.is_valid() and c_form.is_valid():
            u_form.save()
            c_form.save()
            messages.success(request, f'Your account details have been updated!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        c_form = UserContactDetailForm(instance=request.user.contactdetail)

    context = {
        "page_title": "Contact details",
        "u_form": u_form,
        "c_form": c_form
    }
    
    return render(request, 'contact_details.html', context)
