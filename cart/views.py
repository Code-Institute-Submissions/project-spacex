from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from checkout.models import BookingReference


def view_cart(request):
    """Render the cart content page and empty session variable
    'booking_references' in case user interrupted checkout process"""

    # Check if user authenticated and if not set referrer to checkout
    if not request.user.is_authenticated:
        request.session['referrer'] = 'checkout'

    # Clear existing booking references
    if 'booking_references' in request.session:
        booking_references = request.session['booking_references']
        for key in booking_references:
            BookingReference.objects.filter(
                id=booking_references[key]).delete()
        del request.session['booking_references']

    return render(request, "cart.html")


def add_to_cart(request, id):
    """Add passenger(s) for a specified trip to the cart"""

    passenger = int(request.POST.get('passenger'))
    cart = request.session.get('cart', {})

    str_id = str(id)
    if str_id in cart:
        cart[str_id] = int(cart[str_id])+passenger
    else:
        cart[id] = cart.get(id, passenger)

    request.session['cart'] = cart

    messages.success(request, "This trip was added to your cart")
    return redirect(reverse('view_cart'))


def adjust_cart(request, id):
    """Ajust passenger number for a specified trip"""

    passenger = int(request.POST.get('passenger'))
    cart = request.session.get('cart', {})

    if passenger > 0:
        cart[id] = passenger
    else:
        str_id = str(id)
        cart.pop(str_id)

    request.session['cart'] = cart
    return redirect(reverse('view_cart'))


def remove_from_cart(request, id):
    """Remove a specified trip from the cart"""

    cart = request.session.get('cart', {})
    str_id = str(id)
    cart.pop(str_id)

    request.session['cart'] = cart

    messages.success(request, "This trip was removed from your cart")
    return redirect(reverse('view_cart'))
