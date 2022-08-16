from django.shortcuts import redirect, render
from django.http import HttpRequest, JsonResponse, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .models import City, Address
from .forms import UserSignUpForm

@login_required(login_url='login')
def accountOverview(request: HttpRequest) -> HttpResponse:
    return render(request, 'CustomUser/account_overview.html', {})

@login_required(login_url='login')
def profile(request: HttpRequest):
    user = request.user
    context = {'name': user.get_full_name(), 'email': user.email, 'fit': user.get_fit()}
    return render(request, 'CustomUser/profile.html', context)

#LOGIN, LOGOUT SIGNIP Views
def signupView(request: HttpRequest) -> HttpResponse:
    if request.user.is_authenticated:
        return redirect('profile')
    context = {}
    if request.method == 'POST':
        form = UserSignUpForm(data=request.POST)
        if form.is_valid:
            print('Form is Valid')
            form.save()
            user = authenticate(request, email=request.POST['email'], password=request.POST['passowrd1'])
            print(f'{user = }')
            login(request, user)
            return redirect('profile')
        print(f'err: {form.errors}')
        context['form'] = form
        context['errors'] = form.errors
    context['form'] = UserSignUpForm()
    return render(request, 'CustomUser/signup.html',context=context)

def loginView(request: HttpRequest) -> HttpResponse:
    nextUrl = request.GET.get('next')
    if request.user.is_authenticated:
        print('already logged in')
        return redirect(nextUrl) if nextUrl else redirect('profile')
    if request.method == 'POST':
        user = authenticate(request,email=request.POST['email'],password=request.POST['password'])
        if user is not None:
            login(request, user)
            return redirect(nextUrl) if nextUrl else redirect('profile')
        print('user is not valid')
        return render(request, "CustomUser/login.html",{'error':'email or password is incorrect'})
    return render(request, "CustomUser/login.html", {})

def logoutView(request: HttpRequest) -> HttpResponse:
    if request.user.is_authenticated:
        logout(request)
        return redirect('login')
    return HttpResponse('Not logged in')

#AJAX
def load_cities(request: HttpRequest):
    province_id = request.GET.get('province_id')
    cities = City.objects.filter(province_id=province_id)
    return render(request, 'CustomUser/ajax/load_cities.html', {'cities': cities})

def load_province_and_city(request: HttpRequest):
    address_id = request.GET.get('address_id')
    address = Address.objects.get(pk=address_id)
    city = address.city
    province = city.province
    cities = City.objects.filter(province_id=province.id).values()
    for i,c in enumerate(cities):
        if c['name'] == city.name:
            city_id_in_respect_to_province = i
    return JsonResponse({
        'status': 'OK',
        'city_id': city.id,
        'city_name': city.name,
        'province_id': province.id,
        'province_name': province.name,
        'city_id_in_respect_to_province': city_id_in_respect_to_province+1,
    })