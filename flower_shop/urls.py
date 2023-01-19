from django.urls import path

from .views import index_page, send_bunch, send_categories, send_reasons

app_name = "flower_shop"

urlpatterns = [
    path('', index_page, name="index_page"),
    path('bunch/send/', send_bunch),
    path('categories/send/', send_categories),
    path('reasons/send/', send_reasons),
]
