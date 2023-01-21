from django.urls import path

from .views import index_page, send_bunch, send_categories, send_reasons, \
    create_order, send_orders, send_random_bunch

app_name = "flower_shop"

urlpatterns = [
    path('', index_page, name="index_page"),
    path('bunch/send/', send_bunch),
    path('categories/send/', send_categories),
    path('reasons/send/', send_reasons),
    path('order/create/', create_order),
    path('courier/send/', send_orders),
    path('random_bunch/send/', send_random_bunch),
]
