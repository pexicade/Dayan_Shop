from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, JsonResponse


import traceback

def view_cart(request: HttpRequest) -> HttpResponse:
    return render(request, 'orders/cart.html')

def checkout_add_info(request: HttpRequest) -> HttpResponse:
    return render(request, 'orders/checkout_add_info.html')

#AJAX
def get_info(request: HttpRequest) -> HttpResponse:
    try:
        if request.method != 'POST':
            return JsonResponse({'status': 'fail', 'error': 'method not allowed'})
        user = request.user
        if not user.is_authenticated:
            return JsonResponse({'status':'fail','error': 'user not authenticated'})
        addresses = user.address.all()
        if not addresses:
            return JsonResponse({'status':'fail','error': 'no addresses found'})
        return JsonResponse({
            'status':'ok',
            'addresses': [address.to_json() for address in addresses],
            'fname': user.first_name,
            'lname': user.last_name,
            'email': user.email,
            'phone': user.phonenumber
            })
    except Exception as e:
        print(traceback.format_exc())
        return JsonResponse({'status':'fail','error': str(e)})