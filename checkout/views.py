from django.shortcuts import render, redirect, reverse
from django.contrib.auth.models import User
from accounts.models import ContactDetail
from accounts.forms import UserContactDetailForm
from django.contrib.auth.decorators import login_required
from django.contrib import auth, messages

# Create your views here.


@login_required
def checkout_confirm_page(request):
    """Render page to confirm checkcout and booker's contact details"""

    user = User.objects.get(email=request.user.email)

    # Check if user already provided contact details
    try:
        contact = ContactDetail.objects.get(user=request.user)
    except ContactDetail.DoesNotExist:
        contact = None

    # Load contact form with pre-filled fields
    if contact is not None:
        if request.method == 'POST':
            form = UserContactDetailForm(
                request.POST,
                request.FILES,
                instance=request.user.contactdetail)
            if form.is_valid():
                form.save()
                messages.success(
                    request, f'Your contact details have been saved!')
                return redirect('view_cart')
        else:
            form = UserContactDetailForm(instance=request.user.contactdetail)

    # Create new instance of ContactDetail model
    else:
        if request.method == 'POST':
            form = UserContactDetailForm(request.POST)
            if form.is_valid():
                contact_details = form.save(commit=False)
                contact_details.user = request.user
                contact_details.save()
                messages.success(
                    request, f'Your contact details have been saved!')
                return redirect('view_cart')
        else:
            form = UserContactDetailForm()

    context = {
        "page_title": "Booker details",
        "user": user,
        "form": form
    }

    return render(request, "checkout_confirm.html", context)
