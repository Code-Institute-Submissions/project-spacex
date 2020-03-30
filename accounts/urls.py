from django.urls import path, include
from .views import (
    logout_page,
    login_page,
    signup_page,
    profile_page,
    contact_details_page)


urlpatterns = [
    path('logout/', logout_page, name='logout'),
    path('login/', login_page, name='login'),
    path('signup/', signup_page, name='signup'),
    path('profile/', profile_page, name='profile'),
    path('contact-details/', contact_details_page, name='contact_details'),
    path('password-reset/', include('accounts.urls_reset'))
]
