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
    except:
        return JsonResponse({'status':'fail','error': 'Unknown error'})


#admin action view
def make_duplicate(request: HttpRequest, queryset: QuerySet) -> HttpResponse:
    return HttpResponse('Hello world')