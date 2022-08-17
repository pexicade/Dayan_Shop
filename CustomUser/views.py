from django.shortcuts import redirect, render
from django.http import HttpRequest, JsonResponse, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .models import City, Address, User
from .forms import UserSignUpForm
from .fit_choices import BODYTYPE_CHOICES, HEIGHT_CHOICES, BUST_CHOICES, WAIST_CHOICES, HIP_CHOICES

import json

@login_required(login_url='login')
def accountOverview(request: HttpRequest) -> HttpResponse:
    return render(request, 'CustomUser/account_overview.html', {})

@login_required(login_url='login')
def profile(request: HttpRequest):
    user = request.user
    context = {'name': user.get_full_name(), 'email': user.email, 'fit': fit_converter(user.get_fit()), 'msg': request.session.get('msg')}
    if request.session.get('msg'):
        del request.session['msg']
    return render(request, 'CustomUser/profile.html', context)

def fit_converter(fit: dict[str]) -> dict:
    res = {}
    for key, value in fit.items():
        if key =='weight':
            res['weight'] = value
        elif value != None and value != 'None':
            res[key] = globals()[f'{key.upper()}_CHOICES'][int(value)][1]
        else:
            res[key] = '-'
    return res

@login_required(login_url='login')
def edit_profile(request: HttpRequest) -> HttpResponse:
    user = request.user
    if request.method == 'POST':
        user.first_name = request.POST['first_name'] or user.first_name
        user.last_name = request.POST['last_name'] or user.last_name
        user.email = request.POST['email'] or user.email
        user.phonenumber = request.POST['phonenumber'] or user.phonenumber
        day = request.POST['birth_day']
        month = request.POST.get('birth_month', None)
        year = request.POST['birth_year']
        print(day, month, year)
        if day and month and year:
            user.birthdate = f'{year}-{month}-{day}'
        user.save()
        request.session['msg'] = 'Profile Successfully updated'
        return redirect('profile')
    context = {'fname': user.first_name, 'lname': user.last_name, 'email': user.email, 'phone': user.phonenumber,
    'birthdate': user.birthdate}
    for k,v in context.items():
        if v is None or v=='None':
            context[k] = ''
    return render(request, 'CustomUser/edit_profile.html', context)

@login_required(login_url='login')
def edit_fit(request: HttpRequest) -> HttpResponse:
    user = request.user
    if request.method == 'POST':
        user.bodytype = request.POST['bodytype'] or user.bodytype
        user.height = request.POST['height'] or user.height
        user.weight = request.POST['weight'] or user.weight
        user.waist = request.POST['waist'] or user.waist
        user.hip = request.POST['hip'] or user.hip
        user.bust = request.POST['bust'] or user.bust
        user.save()
        request.session['msg'] = 'Fit deatils Successfully updated'
        return redirect('profile')
    context = {'fit': user.get_fit(), 'choices': json.dumps({"bodytype": BODYTYPE_CHOICES, "height": [(x,y.replace('"','')) for x,y in HEIGHT_CHOICES], "waist": [(x,y.replace('"','')) for x,y in WAIST_CHOICES], "hip": [(x,y.replace('"','')) for x,y in HIP_CHOICES], "bust": BUST_CHOICES})}
    for k,v in context.items():
        if v is None or v=='None':
            context[k] = ''
    return render(request, 'CustomUser/edit_fit.html', context)

@login_required(login_url='login')
def update_password(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        user = request.user
        current_pass = request.POST['current_password']
        new_pass = request.POST['new_password']
        if user.check_password(current_pass):
            user.set_password(new_pass)
            user.save()
            request.session['msg'] = 'Password Successfully updated'
            return redirect('profile')
        return render(request, 'CustomUser/update_password.html', {'error': 'Current password is incorrect!'})    
    return render(request, 'CustomUser/update_password.html', {})

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
    
#TODO
# def password_reset_request(request: HttpRequest) -> HttpResponse:
#     code = request.GET.get('code')

# def resetPassword(request: HttpRequest) -> HttpResponse:
#     if request.method == 'POST':
#         email = request.POST['email']
#         user = User.objects.get(email=email)
#         if user:
#             user.set_password('password')
#             user.save()
#             return render(request, 'CustomUser/reset_password.html', {'msg': 'Password reset successfully'})
#         return render(request, 'CustomUser/reset_password.html', {'error': 'Email not found'})
#     return render(request, 'CustomUser/reset_password.html', {})

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