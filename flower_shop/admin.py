from django.contrib import admin
from django.utils.html import format_html
from django.utils.http import url_has_allowed_host_and_scheme
from django.http import HttpResponseRedirect

from .models import Reason, CategoryPrice, FlowersBunch, Order


@admin.register(Reason)
class ReasonAdmin(admin.ModelAdmin):
    pass


@admin.register(CategoryPrice)
class CategoryPriceAdmin(admin.ModelAdmin):
    pass

@admin.register(Order)
class OrderPriceAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'firstname',
        'phonenumber',
        'address',
        'order_status'
    ]
    ordering = ['id']
    def response_post_save_change(self, request, obj):
        res = super().response_post_save_change(request, obj)
        if "next" in request.GET:
            if url_has_allowed_host_and_scheme(request.GET['next'], None):
                return HttpResponseRedirect(request.GET['next'])
        else:
            return res


@admin.register(FlowersBunch)
class FlowersBunchAdmin(admin.ModelAdmin):
    model = FlowersBunch
    list_display = ['name', 'preview', 'price', 'reason', 'category']

    readonly_fields = ['preview']

    def preview(self, obj):
        if not obj.image:
            return 'нет картинки'
        return format_html('<img src="{url}" style="max-height: 100px;"/>',
                           url=obj.image.url)

    def reason(self, obj):
        return obj.reason.name

    def category(self, obj):
        return obj.category.name


