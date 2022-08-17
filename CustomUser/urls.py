from django.urls import path
from .views import (load_cities, load_province_and_city, signupView, loginView, logoutView, profile, accountOverview,
    edit_profile, edit_fit, update_password)

urlpatterns = [
    path('ajax/load_cities/', load_cities, name='load_cities'),
    path('ajax/load_province_and_city/', load_province_and_city, name="load_province_and_city"),
    path('signup/', signupView, name="signup"),
    path('login/', loginView, name="login"),
    path('logout/', logoutView, name="logout"),
    path('profile/', profile, name="profile"),
    path('', accountOverview, name="account_overview"),
    path('profile/edit',edit_profile, name="edit_profile"),
    path('profile/fit',edit_fit, name="edit_fit"),
    path('profile/password',update_password, name="update_password"),
]