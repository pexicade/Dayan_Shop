from nturl2path import url2pathname
from django.shortcuts import render
from django.http import HttpResponse, HttpRequest, JsonResponse
from django.db.models import QuerySet
from django.views.generic import ListView
from django.db.models import Model

from .models import Dress, classes

class index(ListView):
    model = classes['Dress']
    template_name = 'shop/index.html'
    context_object_name = 'dresses'
    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        for dress in Dress.objects.all():
            print(dress.name, dress.pk)
        return super().get(request, *args, **kwargs)

def itemView(request: HttpRequest, item_type: str, item_id: int) -> HttpResponse:
    return render(request, 'shop/item.html', {'item_type': item_type, 'item_id': item_id})

# def index(request: HttpRequest):
#     # image = ItemImage.objects.get(pk=15).image
#     dress = Dress.objects.get(pk=1)
#     # print
#     # cat = dress.sizes
#     # for c in cat.all():
#     #     print(type(c))
#     # fields = dress._meta.fields
#     # for field in fields:
#     #     print(dir(field))
#     # print([x for x in dir(dress) if not x.startswith('_') ])
    
#     return HttpResponse('Hello world')

#AJAX: html files send ajex request to recieve the data
def get_item(request: HttpRequest) -> HttpResponse:
    try:
        if request.method != 'POST':
            return JsonResponse({'status':'fail', 'error':'method not allowed'})
        data = request.POST
        item_type = data.get('item_type', None)
        item_id = data.get('item_id', None)
        if not item_type or not item_id:
            return JsonResponse({'status':'fail', 'error':'no item_type or item_id'})
        item = classes[item_type].objects.get(pk=item_id)
        item = item.to_json()
        return JsonResponse({'status':'ok','item': item})
    except Dress.DoesNotExist:
        return JsonResponse({'status':'fail','error': 'Dress does not exist'})
    except KeyError:
        return JsonResponse({'status':'fail','error': 'Item type does not exist'})
    except Exception as e:
        print(e)
        return JsonResponse({'status':'fail','error': 'Unknown error'})

def add_to_cart(request: HttpRequest) -> HttpResponse:
    try:
        if request.method != 'POST':
            return JsonResponse({'status':'fail', 'error':'method not allowed'})
        data = request.POST
        cart = request.session.get('cart', None)
        if not cart:
            cart = []
        item_type = data.get('item_type', None)
        item_id = data.get('item_id', None)
        if not item_type or not item_id:
            return JsonResponse({'status':'fail', 'error':'no item_type or item_id'})
        item_id = int(item_id)
        item1 = classes[item_type].objects.get(pk=item_id)# to make sure that the item_id is valid, because if it isnt it will throw an exception
        for c,item in enumerate(cart):
            if item[0] == item_type and item[1] == item_id:
                cart[c] = (item_type, item_id, item[2] + 1)
                break
        else:
            cart.append((item_type, item1.pk, 1))
        request.session['cart'] = cart
        return JsonResponse({'status':'ok', 'cart_item_count': len(cart)})
    except KeyError:
        return JsonResponse({'status':'fail','error': 'Item type does not exist'})
    except Dress.DoesNotExist:
        return JsonResponse({'status':'fail','error': 'Item does not exist'})
    except Exception as e:
        print(e)
        return JsonResponse({'status':'fail','error': 'Unknown error'})

def remove_from_cart(request: HttpRequest) -> HttpResponse:
    try:
        if request.method != 'POST':
            return JsonResponse({'status':'fail', 'error':'method not allowed'})
        data = request.POST
        cart = request.session.get('cart', None)
        if not cart:
            return JsonResponse({'status':'fail', 'error':'no item in cart'})
        item_type = data.get('item_type', None)
        item_id = data.get('item_id', None)
        if not item_type or not item_id:
            return JsonResponse({'status':'fail', 'error':'no item_type or item_id'})
        item_id = int(item_id)
        for item in cart:
            if item[0] == item_type and item[1] == item_id:
                cart.remove(item)
                break
        else:
            return JsonResponse({'status':'fail', 'error':'item not in cart'})
        request.session['cart'] = cart
        return JsonResponse({'status':'ok', 'cart_item_count': len(cart)})
    except Exception as e:
        print(e)
        return JsonResponse({'status':'fail','error': 'Unknown error'})

def decrease_item_count_from_cart(request: HttpRequest) -> HttpResponse:
    try:
        if request.method != 'POST':
            return JsonResponse({'status':'fail', 'error':'method not allowed'})
        data = request.POST
        cart = request.session.get('cart', None)
        if not cart:
            return JsonResponse({'status':'fail', 'error':'no item in cart'})
        item_type = data.get('item_type', None)
        item_id = data.get('item_id', None)
        if not item_type or not item_id:
            return JsonResponse({'status':'fail', 'error':'no item_type or item_id'})
        for c, item in enumerate(cart):
            if item[0] == item_type and item[1] == item_id:
                if item[2] > 0:
                    cart[c] = (item_type, item_id, item[2] - 1)
                else:
                    cart.remove(item)
                break
        else:
            return JsonResponse({'status':'fail', 'error':'item not in cart'})
        request.session['cart'] = cart
        return JsonResponse({'status':'ok', 'cart_item_count': len(cart)})
    except Exception as e:
        print(e)
        return JsonResponse({'status':'fail','error': 'Unknown error'})

def clear_cart(request: HttpRequest) -> HttpResponse:
    try:
        if request.method != 'POST':
            return JsonResponse({'status':'fail', 'error':'method not allowed'})
        cart = request.session.get('cart', None)
        if cart:
            request.session['cart'] = []
        return JsonResponse({'status':'ok',})
    except Exception as e:
        print(e)
        return JsonResponse({'status':'fail','error': 'Unknown error'})

def get_cart(request: HttpRequest) -> HttpResponse:
    try:
        if request.method != 'POST':
            return JsonResponse({'status':'fail', 'error':'method not allowed'})
        cart = request.session.get('cart', None)
        if not cart:
            return JsonResponse({'status':'fail', 'error':'no item in cart'})
        return JsonResponse({'status':'ok', 'cart': item_preview(cart), 'total_price': get_total_price(cart), 'item_count':len(cart), 'total_count': sum([item[2] for item in cart])})
    except Exception as e:
        print(e)
        return JsonResponse({'status':'fail','error': 'Unknown error'})

def item_preview(cart: list[tuple]) -> list[dict]:
    res = []
    for i in cart:
        item = classes[i[0]].objects.get(pk=i[1])
        image = item.images.all()[0]
        res.append({
            'item_type': i[0],
            'item_id': i[1],
            'item_name': item.name,
            'item_price': item.price,
            'item_count': i[2],
            'image': image.image.url,
            'image_alt': image.image_alt,
            'color': item.color.name,
            'size': item.sizes.all()[0].name,
        })
    return res

def get_total_price(cart: list[tuple]) -> int:
    total_price = 0
    for i in cart:
        item = classes[i[0]].objects.get(pk=i[1])
        total_price += item.price * i[2]
    return total_price