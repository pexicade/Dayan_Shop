from nturl2path import url2pathname
from django.shortcuts import render
from django.http import HttpResponse, HttpRequest, JsonResponse
from django.db.models import QuerySet
from django.views.generic import ListView
from django.contrib.contenttypes.models import ContentType

from .models import Dress, Kala, item_dct
from CustomUser.models import User
from orders.models import get_shipping_fee

import traceback

class index(ListView):
    model = item_dct['Dress']
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
        print(item_type, item_id)
        item = item_dct[item_type].objects.get(pk=item_id)
        print(item, type(item))
        item = item.to_json()
        print('x')
        item['is_favorite'] = False
        if request.user.is_authenticated:
            is_favorite = request.user.favorites.filter(item_id__in=[item_id]).exists()
            print(is_favorite)
            item['is_favorite'] = is_favorite
        return JsonResponse({'status':'ok','item': item})
    except Dress.DoesNotExist:
        return JsonResponse({'status':'fail','error': 'Dress does not exist'})
    except KeyError:
        return JsonResponse({'status':'fail','error': 'Item type does not exist'})
    # except Exception as e:
    #     print('HERE',e)
    #     return JsonResponse({'status':'fail','error': 'Unknown error'})
# CART
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
        item1 = item_dct[item_type].objects.get(pk=item_id)# to make sure that the item_id is valid, because if it isnt it will throw an exception
        for c,item in enumerate(cart):
            if item[0] == item_type and item[1] == item_id:
                if item1.quantity <= item[2]:
                    return JsonResponse({'status':'fail', 'error':'not enough quantity'})
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
        cart_items = item_preview(cart)
        return JsonResponse({
            'status':'ok',
            'cart': cart_items,
            'total_price': get_total_price(cart),
            'item_count':len(cart),
            'total_count': sum([item[2] for item in cart]),
            'shipping_fee': get_shipping_fee(sum(float(item['weight']) for item in cart_items))
            })
    except Exception as e:
        print(traceback.format_exc())
        print(e)
        return JsonResponse({'status':'fail','error': 'Unknown error'})

def item_preview(cart: list[tuple]) -> list[dict]:
    res = []
    for i in cart:
        item = item_dct[i[0]].objects.get(pk=i[1])
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
            'weight': item.weight,
            'available': item.quantity > i[2]
        })
    return res

def get_total_price(cart: list[tuple]) -> int:
    total_price = 0
    for i in cart:
        item = item_dct[i[0]].objects.get(pk=i[1])
        total_price += item.price * i[2]
    return total_price

# Favorite
def get_favorites(request: HttpRequest) -> HttpResponse:
    try:
        if request.method != 'POST':
            return JsonResponse({'status':'fail', 'error':'method not allowed'})
        if not request.user.is_authenticated():
            return JsonResponse({'status':'fail', 'error':'user not authenticated'})
        favorites = request.user.favorites()
        if not favorites:
            return JsonResponse({'status':'fail', 'error':'no favorites'})
        return JsonResponse({'status':'ok', 'favorites': favorites})
    except Exception as e:
        print(e)
        return JsonResponse({'status':'fail','error': 'Unknown error'})

def add_to_favorite(request: HttpRequest) -> HttpResponse:
    try:
        if request.method != 'POST':
            return JsonResponse({'status':'fail', 'error':'method not allowed'})
        data = request.POST
        item_type = data.get('item_type', None)
        item_id = data.get('item_id', None)
        if not item_type or not item_id:
            return JsonResponse({'status':'fail', 'error':'no item_type or item_id'})
        print(item_type, item_id)
        favorites = request.user.favorites
        for favorite in favorites.all():
            if str(favorite.item_content_type.model) == item_type.lower() and favorite.item_id == int(item_id):
                return JsonResponse({'status':'fail', 'error':'item already in favorites'})
        favorites.add(Kala.objects.get(item_content_type=ContentType.objects.get_for_model(item_dct[item_type]), item_id=item_id))
        return JsonResponse({'status':'ok',})
    except Kala.DoesNotExist:
        return JsonResponse({'status':'fail', 'error':'item not found'})
    except Exception as e:
        print(e)
        return JsonResponse({'status':'fail','error': 'Unknown error'})

def remove_from_favorite(request: HttpRequest) -> HttpResponse:
    try:
        if request.method != 'POST':
            return JsonResponse({'status':'fail', 'error':'method not allowed'})
        data = request.POST
        item_type = data.get('item_type', None)
        item_id = data.get('item_id', None)
        if not item_type or not item_id:
            return JsonResponse({'status':'fail', 'error':'no item_type or item_id'})
        print(item_type, item_id)
        favorites = request.user.favorites
        for favorite in favorites.all():
            # print(, favorite.item_id == int(item_id))
            if str(favorite.item_content_type.model) == item_type.lower() and favorite.item_id == int(item_id):
                favorites.remove(favorite)
                break
        else:
            return JsonResponse({'status':'fail', 'error':'item not in favorites'})
        return JsonResponse({'status':'ok',})
    except Exception as e:
        print(e)
        return JsonResponse({'status':'fail','error': 'Unknown error'})
