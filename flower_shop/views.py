from django.shortcuts import render
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import FlowersBunch, CategoryPrice, Reason, Order
from random import choice

def index_page(request):
    context = {}
    return render(request, 'index.html', context)


@csrf_exempt
def send_bunch(request) -> JsonResponse:
    """
    Отправка букета по выбранным параметрам в телеграмбота
    """
    if request.method == 'POST':
        name_category = request.POST.get('category')
        name_reason = request.POST.get('reason')
        if name_category == "Не важно":
            if name_reason == "Без повода":
                bunches = FlowersBunch.objects.all()
            else:
                reason = Reason.objects.get(name=name_reason)
                bunches = FlowersBunch.objects.filter(
                    reason=reason,
                )
        else:
            if name_reason == "Без повода":
                category = CategoryPrice.objects.get(name=name_category)
                bunches = FlowersBunch.objects.filter(
                    category=category,
                )
            else:
                category = CategoryPrice.objects.get(name=name_category)
                reason = Reason.objects.get(name=name_reason)
                bunches = FlowersBunch.objects.filter(
                    category=category,
                    reason=reason,
                )


        response = {
            'status': 'true',
            'bunch': [
                {
                    'name': bunch.name,
                    'price': bunch.price,
                    'image': request.build_absolute_uri(bunch.image.url),
                    'description': bunch.description,
                    'composition': bunch.composition,
                    'bunch_id': bunch.id
                }
                for bunch in bunches]
        }
        return JsonResponse(response, status=200)

    response = {
        'status': 'false',
        'message': 'Not supported method'
    }
    return JsonResponse(response, status=501)


def send_categories(request) -> JsonResponse:
    """
    Отправка категорий для формирования клавиатуры
    """
    categories = CategoryPrice.objects.all()
    response = {
        'categories': [category.name for category in categories]
    }
    return JsonResponse(response, status=200)


def send_reasons(request) -> JsonResponse:
    """
    Отправка повода для формирования клавиатуры
    """
    reasons = Reason.objects.all()
    response = {
        'reasons': [reason.name for reason in reasons]
    }
    return JsonResponse(response, status=200)


@csrf_exempt
def create_order(request) -> JsonResponse:
    """
    Создание объекта заказа
    """
    if request.method == 'POST':
        try:
            firstname = request.POST.get('firstname')
            address = request.POST.get('address')
            phonenumber = request.POST.get('phonenumber')
            delivered_at = request.POST.get('delivered_at')
            bunch = FlowersBunch.objects.get(id=request.POST.get('bunch_id'))

            order = Order.objects.create(
                firstname=firstname,
                address=address,
                phonenumber=phonenumber,
                delivered_at=delivered_at,
                bunch=bunch
            )

            response = {
                'status': 'true',
                'message': 'Спасибо за заказ, в ближайшее время курьер свяжется с вами',
                'name': order.bunch.name,
                'price': order.bunch.price,
                'image': request.build_absolute_uri(order.bunch.image.url),
                'description': order.bunch.description,
                'composition': order.bunch.composition,
                'bunch_id': order.bunch.id,
            }
            return JsonResponse(response, status=200)

        except:
            response = {
                'status': 'false',
                'message': 'Введены некорректные данные, проверьте формат ввода даты и номера телефона'
            }
            return JsonResponse(response, status=501)

    response = {
        'status': 'false',
        'message': 'Not supported method'
    }
    return JsonResponse(response, status=501)


@csrf_exempt
def send_orders(request) -> JsonResponse:
    """
    Отправляем заказы курьеру
    """

    orders = Order.objects.filter(delivered_at__contains=request.POST.get('delivered_at'),
                                  order_status='raw_order')
    if orders:
        response = {
            'orders': [
                {
                    'firstname': order.firstname,
                    'address': order.address,
                    'method_payment': order.method_payment,
                    'comment': order.comment,
                    'phonenumber': str(order.phonenumber),
                    'delivered_at': order.delivered_at,
                    'price': order.bunch.price,
                    'image': request.build_absolute_uri(order.bunch.image.url),
                    'bunch_id': order.bunch.id
                }
                for order in orders]
        }
    else:
        response = {
            'message': 'На выбранную дату нет заказов'}

    return JsonResponse(
        response,
        status=200,
        json_dumps_params={'ensure_ascii': False}
    )

def send_random_bunch(request) -> JsonResponse:
    """
    Отправка случайного букета
    """
    bunches = FlowersBunch.objects.all()
    list_id = []
    for bunch in bunches:
        list_id.append(bunch.id)
    bunch_id = choice(list_id)
    bunch = FlowersBunch.objects.get(id=bunch_id)
    response = {
        'bunch':
            {
                'name': bunch.name,
                'price': bunch.price,
                'image': request.build_absolute_uri(bunch.image.url),
                'description': bunch.description,
                'composition': bunch.composition,
                'bunch_id': bunch.id
            }
    }
    return JsonResponse(response, status=200)
