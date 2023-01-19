from django.shortcuts import render
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import FlowersBunch, CategoryPrice, Reason


def index_page(request):
    context = {}
    return render(request, 'index.html', context)


@csrf_exempt
def send_bunch(request) -> JsonResponse:
    """
    Отправка букета по выбранным параметрам в телеграмбота
    """
    if request.method == 'POST':
        category = CategoryPrice.objects.get(name=request.POST.get('category'))
        reason = Reason.objects.get(name=request.POST.get('reason'))

        bunches = FlowersBunch.objects.filter(
            category=category,
            reason=reason,
        )

        print(bunches)

        response = {
            'status': 'true',
            'bunch': [
                {
                    'name': bunch.name,
                    'price': bunch.price,
                    'image': request.build_absolute_uri(bunch.image.url),
                    'description': bunch.description,
                    'composition': bunch.composition,
                }
                for bunch in bunches]
        }
        return JsonResponse(response, status=200)

    response = {
        'status': 'false',
        'message': 'Not supported method'
    }
    return JsonResponse(response, status=501)