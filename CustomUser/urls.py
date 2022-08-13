from django.urls import path
from .views import (load_cities, load_province_and_city, signupView, loginView, logoutView, profile)

urlpatterns = [
    path('ajax/load_cities/', load_cities, name='load_cities'),
    path('ajax/load_province_and_city/', load_province_and_city, name="load_province_and_city"),
    path('signup/', signupView, name="signup"),
    path('login/', loginView, name="login"),
    path('logout/', logoutView, name="logout"),
    path('profile/', profile, name="profile"),

]