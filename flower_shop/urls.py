from django.urls import path

from .views import index_page, send_bunch

app_name = "flower_shop"

urlpatterns = [
    path('', index_page, name="index_page"),
    path('bunch/send/', send_bunch),
]
