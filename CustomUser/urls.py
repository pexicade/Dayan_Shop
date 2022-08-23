from django.urls import path
from .views import (load_provinces, load_cities, load_cities2, load_province_and_city, signupView, loginView, logoutView, profile, accountOverview,
    edit_profile, edit_fit, update_password, add_address, edit_address, delete_address)

urlpatterns = [
    path('ajax/load_provinces/', load_provinces, name='load_provinces'),
    path('ajax/load_cities/', load_cities, name='load_cities'),
    path('ajax/load_cities2/', load_cities2, name='load_cities2'),
    path('ajax/load_cities/', load_cities, name='load_cities'),
    path('ajax/load_province_and_city/', load_province_and_city, name="load_province_and_city"),
    path('signup/', signupView, name="signup"),
    path('login/', loginView, name="login"),
    path('logout/', logoutView, name="logout"),
    path('profile/', profile, name="profile"),
    path('', accountOverview, name="account_overview"),
    path('profile/edit/',edit_profile, name="edit_profile"),
    path('profile/fit/',edit_fit, name="edit_fit"),
    path('profile/password/',update_password, name="update_password"),
    path('profile/add_address/',add_address, name="add_address"),
    path('profile/edit_address/<int:adrs_id>',edit_address, name="edit_address"),
    path('profile/delete_address/',delete_address, name="delete_address"),

]